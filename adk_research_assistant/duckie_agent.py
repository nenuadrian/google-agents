import os
from typing import List, TypedDict

from google.adk.agents.llm_agent import Agent
from google.adk.tools.function_tool import FunctionTool
from ddgs import DDGS


GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


class DuckieSearchResult(TypedDict):
    title: str
    href: str
    body: str


def search_duckie_with_client(
    query: str,
    *,
    max_results: int = 10,
) -> List[DuckieSearchResult]:
    """Use the `ddgs` Python client to fetch recent papers.

    This is a low-level utility that the LLM agent can call via tool usage,
    or that you can call directly from Python.
    """
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=max_results))
        return [
            DuckieSearchResult(
                title=r.get("title", ""),
                href=r.get("href", ""),
                body=r.get("body", ""),
            )
            for r in results
        ]


search_duckie_with_client_tool = FunctionTool(func=search_duckie_with_client)

# --------

duckie_research_agent = Agent(
    model=GEMINI_MODEL,
    name="duckie_research_agent",
    description=(
        "Sub-agent that can call a custom DuckDuckGo search tool "
        "to find recent information for given research topics."
    ),
    instruction=(
        "Role: research assistant specialized in searching the web with DuckDuckGo.\n"
        "Capabilities: access to search_duckie_with_client(query, max_results) returning search results.\n"
        "Workflow:\n"
        "1. Normalize the supplied topics and decide whether to call the tool once or multiple times.\n"
        "2. Choose max_results (default 10, adjust when many topics), then call the tool.\n"
        "3. Merge the results and organize them by topic or theme.\n"
        "Output: Provide each result's title, url, and a 1–2 sentence summary. Conclude with key takeaways or gaps."
    ),
tools=[search_duckie_with_client_tool],
    output_key="duckie_research_result",
)
