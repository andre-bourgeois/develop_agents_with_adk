"""
Test script to see state access directly.
Run with: python test_state.py

This test file diverges significantly from the original course file, which was written for 
an older ADK version. See changes below for details.

=== CHANGES FROM ORIGINAL COURSE FILE ===

1. Added `import asyncio` and wrapped the whole script in `async def main()`,
   run via `asyncio.run(main())` at the bottom.
   WHY: `session_service.create_session()` and `session_service.get_session()`
   are coroutines in this ADK version. The original script called
   `create_session()` at the top level without `await`, which silently
   returned an un-awaited coroutine object instead of a real Session
   (visible as a `RuntimeWarning: coroutine ... was never awaited`).

2. Added `await` before `session_service.create_session(...)`.
   WHY: same reason as above, this was the direct cause of the warning.

3. Changed `user_message=user_message` to `new_message=user_message` in the
   first `runner.run()` call.
   WHY: `Runner.run()` has no `user_message` parameter in this ADK version;
   the correct keyword is `new_message`. This was the exact `TypeError`
   in the original traceback. (Your second `runner.run()` call already
   used `new_message` correctly, so this just makes both calls consistent.)

4. Added `role="user"` to the `Content(...)` objects.
   WHY: not strictly required to fix an error, but matches ADK's documented
   pattern and avoids ambiguity about which party a message came from.

5. Added `session = await session_service.get_session(...)` after each
   `runner.run()` call, and read `session.state` from that re-fetched
   object instead of the original `session` variable from the top of
   the script.
   WHY: this is the key session-related fix. The `session` object returned
   by `create_session()` at the start is a snapshot from before the agent
   ran. The Runner updates its own internal copy of the session as it
   processes events; your original local `session` variable never sees
   those updates. Reading `session.state` from the original variable
   returns `{}` forever, regardless of what the agent actually stored.
   This matches ADK's own documented pattern of re-fetching via
   `get_session()` after a run to inspect updated state.

Reference: https://google.github.io/adk-docs/sessions/state.md
"""

import asyncio
from dotenv import load_dotenv
load_dotenv()  # NEW: loads .env file so GOOGLE_API_KEY is available (see change notes above the file if needed)

from agent import root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

APP_NAME = "name_extractor_app"
USER_ID = "test_user"
SESSION_ID = "test_session"


async def main():  # CHANGED: whole script now runs inside an async function
    session_service = InMemorySessionService()

    # CHANGED: added `await` — create_session() is a coroutine
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )

    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service
    )

    # Test: Extract name
    # CHANGED: added role="user"
    user_message = Content(role="user", parts=[Part(text="Hello, my name is André.")])

    print("=== Running Name Extraction Test ===")
    result = runner.run(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=user_message  # CHANGED: was user_message=user_message (invalid kwarg)
    )

    for event in result:
        if event.is_final_response():
            print(f"\nAgent Response: {event.content.parts[0].text}")

    # NEW: re-fetch session instead of reading the stale object from above
    session = await session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )

    print(f"\n=== State after execution ===")
    print(f"Full state: {session.state}")
    print(f"Extracted name: {session.state.get('extracted_name')}")

    if session.state.get('extracted_name'):
        print(f"Name successfully extracted and stored!")
    else:
        print("Name extraction failed.")

    # Test accessing in subsequent turns
    print("\n=== Running Subsequent Turn Test ===")
    result2 = runner.run(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=Content(role="user", parts=[Part(text="Can you tell me what name you extracted?")])
    )

    for event in result2:
        if event.is_final_response():
            print(f"\nAgent Response: {event.content.parts[0].text}")

    # NEW: re-fetch again, same reason as above
    session = await session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )

    print(f"\nState still contains extracted name: {session.state.get('extracted_name')}")
    print("State persists across turns!")


if __name__ == "__main__":
    asyncio.run(main())  # NEW: entry point that runs the whole async script