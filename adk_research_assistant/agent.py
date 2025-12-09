import os
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.agents.parallel_agent import ParallelAgent
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.google_search_tool import google_search

from arxiv_agent import arxiv_research_agent
from email_agent import email_agent

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


google_agent = LlmAgent(
    name="GoogleSearchResearchAgent",
    model=GEMINI_MODEL,
    instruction="""You are an AI research assistant specializing in finding latest research using web search.
1. Invoke the Google Search tool with a focused query before drafting your answer.
2. Ground every statement in the retrieved results and synthesize them into one concise (1–2 sentence) summary.
3. Output only that summary; include citations and extra commentary.
""",
    description="Researches using Google.",
    tools=[google_search],
    # Store result in state for the merger agent
    output_key="google_research_result",
)

# --------

parallel_research_agent = ParallelAgent(
    name="ParallelWebResearchAgent",
    sub_agents=[google_agent, arxiv_research_agent],
    description="Runs multiple research agents in parallel to gather information.",
)

merger_agent = LlmAgent(
    name="MergeSynthesisAgent",
    model=GEMINI_MODEL,
    instruction="""You are an AI assistant merging research outputs into a structured report.

Follow this workflow:
1. Read the Google, arXiv, Duckie, and Hacker News summaries below; do not use external knowledge.
2. Identify the main topics or themes present and organize them into clear headings.
3. Under each heading, integrate the relevant findings, attributing them to their source (Google, arXiv, Duckie, or Hacker News) in-line.
4. Conclude with a brief overall insight section synthesizing cross-source takeaways.
5. Provide a suggested email subject line on the final line in the format: "Suggested Subject: ..."

Input Summaries:
- Google Search Results:
  {google_research_result}

- arXiv Papers:
  {arxiv_research_result}

Output Requirements:
- Use Markdown headings (##) for each topic.
- Write concise paragraphs or bullet points under each heading.
- Ensure all content is grounded exclusively in the input summaries.
- End with the required subject line and nothing else.
""",
    description="Combines research findings from parallel agents into a structured, cited report, strictly grounded on provided inputs.",
)

# --------

sequential_pipeline_agent = SequentialAgent(
    name="ResearchAndSynthesisPipeline",
    sub_agents=[parallel_research_agent, merger_agent, email_agent],
    description="Coordinates parallel research and synthesizes the results.",
)


root_agent = sequential_pipeline_agent
