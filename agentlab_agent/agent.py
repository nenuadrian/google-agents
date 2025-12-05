import arxiv
from google.adk.agents.llm_agent import Agent

def search_papers(query: str) -> str:
    """
    Searches for papers on arXiv.

    Args:
        query: The search query.

    Returns:
        A formatted string with the top 5 papers.
    """
    search = arxiv.Search(
        query=query,
        max_results=5,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    results = ""
    for r in search.results():
        results += f"Title: {r.title}\n"
        results += f"Authors: {', '.join(a.name for a in r.authors)}\n"
        results += f"Summary: {r.summary}\n\n"
    return results

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
    tools=[search_papers],
)

if __name__ == '__main__':
    query = "Find papers about policy gradients and large language models and transformers and graph neural networks"
    response = root_agent.chat(query)
    print(response)