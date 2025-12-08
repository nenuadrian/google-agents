import os

from datetime import datetime
from typing import Dict, List, Literal, TypedDict

import arxiv
from google.adk.agents.llm_agent import Agent
from google.adk.tools import FunctionTool

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


class ArxivPaper(TypedDict):
    title: str
    authors: List[str]
    year: int
    arxiv_id: str
    url: str
    summary: str
    topic: str


def _build_arxiv_query_string(topics: List[str]) -> str:
    """Build an arXiv API query string from a list of topics.

    We keep this simple and AND the topic phrases together.
    """

    cleaned = [t.strip() for t in topics if t.strip()]
    if not cleaned:
        raise ValueError("At least one topic is required")

    # Example: "(ti:\"graph neural networks\" OR abs:\"graph neural networks\")"
    parts = []
    for t in cleaned:
        phrase = t.replace('"', '"')
        parts.append(f'(ti:"{phrase}" OR abs:"{phrase}")')

    return " AND ".join(parts)


def search_arxiv_with_client(
    topics: List[str],
    *,
    max_results: int = 10,
    sort_by: Literal[
        "relevance",
        "lastUpdatedDate",
        "submittedDate",
    ] = "submittedDate",
) -> List[ArxivPaper]:
    """Use the `arxiv` Python client to fetch recent papers.

    This is a low-level utility that the LLM agent can call via tool usage,
    or that you can call directly from Python.
    """

    query = _build_arxiv_query_string(topics)

    sort_criterion_map: Dict[str, arxiv.SortCriterion] = {
        "relevance": arxiv.SortCriterion.Relevance,
        "lastUpdatedDate": arxiv.SortCriterion.LastUpdatedDate,
        "submittedDate": arxiv.SortCriterion.SubmittedDate,
    }

    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=sort_criterion_map[sort_by],
    )

    client = arxiv.Client()

    papers: List[ArxivPaper] = []
    for result in client.results(search):
        year = result.published.year if result.published else datetime.utcnow().year
        papers.append(
            ArxivPaper(
                title=result.title,
                authors=[a.name for a in result.authors],
                year=year,
                arxiv_id=result.get_short_id(),
                url=result.entry_id,
                summary=result.summary,
                topic=", ".join(topics),
            )
        )

    return papers


search_arxiv_with_client_tool = FunctionTool(func=search_arxiv_with_client)

arxiv_research_agent = Agent(
    model=GEMINI_MODEL,
    name="arxiv_research_agent",
    description=(
        "Sub-agent that can call a custom arXiv search tool "
        "to find recent papers for given research topics."
    ),
    instruction=(
        "You are an academic research assistant specialized in searching arXiv. "
        "You have access to a Python tool `search_arxiv_with_client(topics, "
        "max_results, sort_by)` that returns structured paper metadata. "
        "Given a list of topics, decide sensible values for max_results and "
        "sort_by (defaulting to recent submissions), call the tool, and then "
        "format the results as a concise list including: title, authors, year, "
        "arXiv ID, URL, and a 1–2 sentence summary for each paper. Group by "
        "topic where helpful. Get 50 papers."
    ),
    tools=[search_arxiv_with_client_tool],
    output_key="arxiv_research_result",
)
