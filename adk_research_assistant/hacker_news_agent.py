import os
from typing import List, TypedDict

from google.adk.agents.llm_agent import Agent
from google.adk.tools.function_tool import FunctionTool
from haxor.haxor import Haxor


GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


class HackerNewsStory(TypedDict):
    title: str
    url: str
    score: int
    by: str
    time: int


def search_hacker_news(
    query: str,
    *,
    limit: int = 10,
) -> List[HackerNewsStory]:
    """Use the `haxor` Python client to fetch top stories from Hacker News.
    """
    hn = Haxor()
    stories = []
    # The haxor library doesn't support query-based search, so we'll get top stories and filter by query.
    top_stories = hn.get_top_stories()
    if top_stories:
        for story_id in top_stories[:limit*2]: # Get more to filter
            story = hn.get_item(story_id)
            if story and query.lower() in story.title.lower():
                stories.append(
                    HackerNewsStory(
                        title=story.title,
                        url=story.url,
                        score=story.score,
                        by=story.by,
                        time=story.time,
                    )
                )
            if len(stories) >= limit:
                break
    return stories


search_hacker_news_tool = FunctionTool(func=search_hacker_news)

# --------

hacker_news_research_agent = Agent(
    model=GEMINI_MODEL,
    name="hacker_news_research_agent",
    description=(
        "Sub-agent that can call a custom Hacker News search tool "
        "to find recent information for given research topics."
    ),
    instruction=(
        "Role: research assistant specialized in searching Hacker News.\n"
        "Capabilities: access to search_hacker_news(query, limit) returning search results.\n"
        "Workflow:\n"
        "1. Normalize the supplied topics and decide whether to call the tool once or multiple times.\n"
        "2. Choose limit (default 10, adjust when many topics), then call the tool.\n"
        "3. Merge the results and organize them by topic or theme.\n"
        "Output: Provide each result's title, url, and a 1–2 sentence summary. Conclude with key takeaways or gaps."
    ),
    tools=[search_hacker_news_tool],
    output_key="hacker_news_research_result",
)
