import asyncio
from google.adk import runners
from google.genai import types
from agent import root_agent

USER_ID = "user"
APP_NAME = "academic_research_app"

async def run_prompt(user_id, runner, content, session_id):
    """A helper function to run a prompt and get the response."""
    response_generator = runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content,
    )
    message = ""
    async for event in response_generator:
        if event.is_final_response() and event.content and event.content.parts:
            message += (event.content.parts[0].text or "")
        elif hasattr(event, 'text'):
            message += event.text
    return "assistant", message


async def main():
    """Runs a single turn conversation with the agent."""
    runner = runners.InMemoryRunner(
        agent=root_agent,
        app_name=APP_NAME,
    )
    session = await runner.session_service.create_session(
        user_id=USER_ID,
        app_name=APP_NAME,
    )

    query = "Find papers about policy gradients and large language models and transformers and graph neural networks"
    author, message = await run_prompt(
        USER_ID,
        runner,
        types.Content(role="user", parts=[types.Part.from_text(text=query)]),
        session_id=session.id,
    )
    print(f"[{author}]: {message}")


if __name__ == "__main__":
    asyncio.run(main())