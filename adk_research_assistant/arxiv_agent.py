import os
from datetime import datetime
from typing import Dict, List, Literal, TypedDict

from google.adk.agents.llm_agent import Agent
from google.adk.tools.function_tool import FunctionTool
import arxiv


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

    cleaned = list(dict.fromkeys(t.strip() for t in topics if t.strip()))
    if not cleaned:
        raise ValueError("At least one topic is required")

    # Example: "(ti:\"graph neural networks\" OR abs:\"graph neural networks\")"
    parts = []
    for t in cleaned:
        phrase = t.replace('"', '\\"')
        parts.append(f'(ti:"{phrase}" OR abs:"{phrase}")')

    return " AND ".join(parts)


def search_arxiv_with_client(
    topics: List[str],
    *,
    max_results: int = 50,
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

# --------

arxiv_research_agent = Agent(
    model=GEMINI_MODEL,
    name="arxiv_research_agent",
    description=(
        "Sub-agent that can call a custom arXiv search tool "
        "to find recent papers for given research topics."
    ),
    instruction=(
        "Role: academic research assistant specialized in arXiv.\n"
        "Capabilities: access to search_arxiv_with_client(topics, max_results, sort_by) returning structured paper metadata.\n"
        "Workflow:\n"
        "1. Normalize the supplied topics and decide whether to call the tool once or multiple times (e.g., one per topic cluster).\n"
        "2. Choose max_results (default 50, adjust when many topics) and an appropriate sort order (use submittedDate unless directed otherwise), then call the tool.\n"
        "3. Merge the results, de-duplicate by arXiv ID, and organize them by topic or theme.\n"
        "Output: Provide each paper's title, authors, year, arXiv ID, URL, and a 1–2 sentence summary. Conclude with key takeaways or gaps."
    ),
    tools=[search_arxiv_with_client_tool],
    output_key="arxiv_research_result",
)
