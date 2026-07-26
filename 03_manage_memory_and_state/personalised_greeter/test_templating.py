"""
Test state templating with different state values.

Run with: python test_templating.py

==============================================================================
REVISION SUMMARY (vs. original course-copied version)
==============================================================================
1. Added `import asyncio`, and wrapped `create_session()` in `asyncio.run()`.
   WHY: InMemorySessionService.create_session() is `async def` in this ADK
   version (2.5.0). Calling it without awaiting just creates an unexecuted coroutine
   object - "session1" was never actually created, which caused a
   SessionNotFoundError on the first runner.run() call.

2. Added `from dotenv import load_dotenv` + `load_dotenv()` at the top of
   the file, before importing the agent.
   WHY: ADK's own CLI tools (`adk run` / `adk web`) auto-load a .env file
   from the project directory, but a plain `python test_templating.py`
   invocation does not. Without this, GOOGLE_API_KEY never reached the
   process environment and model calls failed with "No API key was
   provided."

3. Added `Event` / `EventActions` imports and a new `set_state()` helper
   function. Replaced all direct `session.state["key"] = value` mutations
   with `asyncio.run(set_state({...}))` calls.
   WHY: in this ADK version (2.5.0), both create_session() and get_session() always
   return a COPY of the internally stored session (see
   google/adk/sessions/in_memory_session_service.py, _copy_session()).
   Mutating session.state directly on our local copy never touched the
   internal storage the Runner actually reads from, so none of our test
   state changes were ever visible to the agent. The only supported way to
   persist a state change is via session_service.append_event() with an
   EventActions(state_delta=...), which set_state() wraps.

4. Added a session refresh - `session = asyncio.run(session_service.get_session(...))`
   - after each test, before printing state.
   WHY: same reason as #3. Our local `session` variable is a snapshot, not
   a live view, so it has to be re-fetched to display what's actually
   stored after a set_state() call.

5. Reformatted the state-printing lines from two prints
   (`print("=== Test N State ===")` / `print(session.state)`) into one:
   `print(f"Test N State: {session.state}\n")`, plus a divider line
   between test blocks. Cosmetic only, no functional change.

6. Test 3's sample data changed from "Alex" / "Spanish" / "Hola de nuevo"
   to "André" / "French" / "Bonjour à nouveau". Personal preference, not a
   bug fix, kept here for the record.
==============================================================================
"""

import asyncio

# NEW: python-dotenv import + call - must run before `from agent import
# root_agent`, since the agent's model client reads the API key from the
# environment as soon as it's built.
from dotenv import load_dotenv
load_dotenv()

from agent import root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

# NEW: needed to commit state changes via append_event() instead of direct
# dict mutation (see REVISION SUMMARY #3).
from google.adk.events.event import Event
from google.adk.events.event_actions import EventActions


# Setup
session_service = InMemorySessionService()
# UPDATED: wrapped in asyncio.run() - create_session() is async in this ADK
# version (2.5.0); calling it unawaited silently no-ops (see REVISION SUMMARY #1).
session = asyncio.run(session_service.create_session(
    app_name="greeter_app",
    user_id="user1",
    session_id="session1"
))


runner = Runner(
    agent=root_agent,
    app_name="greeter_app",
    session_service=session_service
)


# NEW: replaces direct `session.state[key] = value` mutation, which this
# ADK version (2.5.0) silently discards (see REVISION SUMMARY #3).
async def set_state(delta: dict) -> None:
    await session_service.append_event(
        session,
        Event(author="user", actions=EventActions(state_delta=delta)),
    )


# Test 1: No state set (all defaults)
print("=== Test 1: No state (all defaults) ===")

result1 = runner.run(
    user_id="user1",
    session_id="session1",
    new_message=Content(parts=[Part(text="Hello")])
)

for event in result1:
    if event.is_final_response():
        print(f"Agent:{event.content.parts[0].text}\n")

# NEW: refresh our local session reference so the state we print reflects
# what's actually stored (see REVISION SUMMARY #4).
session = asyncio.run(session_service.get_session(
    app_name="greeter_app", user_id="user1", session_id="session1"
))

# UPDATED: combined onto one line, plus a divider (cosmetic, REVISION SUMMARY #5).
print(f"Test 1 State: {session.state}\n")
print("--------------------------------------------------\n\n")

# Test 2: Set user name only
print("=== Test 2: With user name ===")

# UPDATED: was `session.state["user_name"] = "Alex"` - replaced with a
# properly committed state change (see REVISION SUMMARY #3).
asyncio.run(set_state({"user_name": "André"}))

result2 = runner.run(
    user_id="user1",
    session_id="session1",
    new_message=Content(parts=[Part(text="Hello again")])
)

for event in result2:
    if event.is_final_response():
        print(f"Agent:{event.content.parts[0].text}\n")

session = asyncio.run(session_service.get_session(
    app_name="greeter_app", user_id="user1", session_id="session1"
))

print(f"Test 2 State: {session.state}\n")
print("--------------------------------------------------\n\n")

# Test 3: Set all state values
print("=== Test 3: With all state values ===")

# UPDATED: was three direct `session.state[...] = ...` assignments -
# replaced with a single committed state change (see REVISION SUMMARY #3).
# Sample values also changed from Alex/Spanish to André/French.
asyncio.run(set_state({
    "user_name": "André",
    "user_language": "French",
    "membership_tier": "premium",
}))

result3 = runner.run(
    user_id="user1",
    session_id="session1",
    new_message=Content(parts=[Part(text="Bonjour à nouveau")])
)

for event in result3:
    if event.is_final_response():
        print(f"Agent:{event.content.parts[0].text}\n")

session = asyncio.run(session_service.get_session(
    app_name="greeter_app", user_id="user1", session_id="session1"
))

print(f"Test 3 State: {session.state}\n")