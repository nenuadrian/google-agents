import os
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.agents.parallel_agent import ParallelAgent
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools import google_search

from arxiv_agent import arxiv_research_agent
from email_agent import email_agent

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


google_agent = LlmAgent(
    name="GoogleSearchResearchAgent",
    model=GEMINI_MODEL,
    instruction="""You are an AI Research Assistant.
Use the Google Search tool provided.
Summarize your key findings concisely (1-2 sentences).
Output *only* the summary.
""",
    description="Researches using Google.",
    tools=[google_search],
    # Store result in state for the merger agent
    output_key="google_research_result",
)

parallel_research_agent = ParallelAgent(
    name="ParallelWebResearchAgent",
    sub_agents=[google_agent, arxiv_research_agent],
    description="Runs multiple research agents in parallel to gather information.",
)

merger_agent = LlmAgent(
    name="MergeSynthesisAgent",
    model=GEMINI_MODEL,
    instruction="""You are an AI Assistant responsible for combining research findings into a structured report.

 Your primary task is to synthesize the following research summaries, clearly attributing findings to their source areas. Structure your response using headings for each topic. Ensure the report is coherent and integrates the key points smoothly.

 **Crucially: Your entire response MUST be grounded *exclusively* on the information provided in the 'Input Summaries' below. Do NOT add any external knowledge, facts, or details not present in these specific summaries.**

 **Research:**

 *   **Google Search Results:**
     {google_research_result}

 *   **arXiv Papers:**
     {arxiv_research_result}

 **Output Format:**

 Output *only* the structured report following this format. Do not include introductory or concluding phrases outside this structure, and strictly adhere to using only the provided input summary content.
 
 Respond also with a suggested email subject line that encapsulates the report's content.
 """,
    description="Combines research findings from parallel agents into a structured, cited report, strictly grounded on provided inputs.",
)

sequential_pipeline_agent = SequentialAgent(
    name="ResearchAndSynthesisPipeline",
    sub_agents=[parallel_research_agent, merger_agent, email_agent],
    description="Coordinates parallel research and synthesizes the results.",
)


root_agent = sequential_pipeline_agent
