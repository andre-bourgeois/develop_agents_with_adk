"""
Test state namespaces to see persistence differences.

Run with: python test_namespaces.py

==============================================================================
REVISION SUMMARY (vs. original course-copied version)
==============================================================================
1. Added `import asyncio`, dotenv loading, and wrapped both
   `create_session()` calls in `asyncio.run()`.
   WHY: same issue as the previous exercise - create_session() is async
   in this ADK version, and GOOGLE_API_KEY needs to be loaded from .env
   manually when running a plain `python` script instead of `adk run`/
   `adk web`. See test_templating.py's header for the full explanation.

2. Added `Event` / `EventActions` imports and a `set_state()` helper.
   Replaced all five direct `session.state["key"] = value` assignments
   with a single `asyncio.run(set_state({...}))` call.
   WHY: create_session()/get_session() always return a COPY of the
   internally stored session in this ADK version, so direct mutation is
   silently discarded. The only way to persist a change is via
   session_service.append_event() with a state_delta. Same root cause as
   the previous exercise, just applied to five keys instead of one.

3. NEW FINDING - temp: state cannot be set from outside an invocation at
   all in this ADK version, even via append_event.
   WHY: google/adk/sessions/_session_util.py's extract_state_delta()
   explicitly filters out any key starting with "temp:" before it's
   routed into the app/user/session delta buckets:
       elif not key.startswith(State.TEMP_PREFIX):
           deltas["session"][key] = state[key]
   A temp:-prefixed delta matches neither the app, user, nor the "else"
   session branch, so it's silently dropped - not stored anywhere, not
   even transiently. Combined with Runner.run() always re-fetching the
   session fresh from the session_service (confirmed in runners.py's
   _get_or_create_session(), which never reads from any session object
   held by our script), there is no code path left by which external
   test code can make {temp:step} resolve to anything. In this ADK
   version, temp: state can only be written by a tool while an
   invocation is actively running (via tool_context.state). Since our
   agent has no tools, this script still sets "temp:step" below for
   parity with the course material and to prove the point, but expect
   it to print as None in every test, not just "after turn 1" as the
   original tutorial describes. Genuine capability gap vs. the course
   material, not a bug in this script.

4. Refreshed the local `session` (and `session2`) reference via
   `session_service.get_session()` after state-changing operations, for
   the same reason as #2 - to display what's actually stored rather than
   a stale local copy.
==============================================================================
"""

import asyncio

# NEW: must run before `from agent import root_agent` - the agent's model
# client reads the API key from the environment as soon as it's built.
from dotenv import load_dotenv
load_dotenv()

from agent import root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

# NEW: needed to commit state changes via append_event() instead of direct
# dict mutation (see REVISION SUMMARY #2).
from google.adk.events.event import Event
from google.adk.events.event_actions import EventActions


# Setup
session_service = InMemorySessionService()
# UPDATED: wrapped in asyncio.run() - create_session() is async in this ADK
# version (see REVISION SUMMARY #1).
session = asyncio.run(session_service.create_session(
    app_name="namespace_demo_app",
    user_id="user1",
    session_id="session1"
))

runner = Runner(
    agent=root_agent,
    app_name="namespace_demo_app",
    session_service=session_service
)


# NEW: replaces direct `session.state[key] = value` mutation, which this
# ADK version silently discards for app:/user:/session state, and always
# discards outright for temp: state (see REVISION SUMMARY #2 and #3).
async def set_state(delta: dict) -> None:
    await session_service.append_event(
        session,
        Event(author="user", actions=EventActions(state_delta=delta)),
    )


# Set all four namespace types
print("=== Setting state in all namespaces ===")

# UPDATED: was five separate `session.state["key"] = value` lines -
# replaced with one committed state change. NOTE: "temp:step" is included
# here for parity with the course material, but per REVISION SUMMARY #3 it
# will never actually be stored or become visible to the agent.
asyncio.run(set_state({
    "app:name": "Namespace Demo",
    "app:version": "2.0",
    "user:theme": "dark",
    "topic": "state management",
    "temp:step": "initialization",  # NOTE: silently dropped, see header
}))

session = asyncio.run(session_service.get_session(
    app_name="namespace_demo_app", user_id="user1", session_id="session1"
))

print(f"State before run: {session.state}\n")

# Run agent
print("=== Running agent (Turn 1) ===")

result = runner.run(
    user_id="user1",
    session_id="session1",
    new_message=Content(parts=[Part(text="Show me the namespace values")])
)

# Show response
for event in result:
    if event.is_final_response():
        print(f"Agent response:\n{event.content.parts[0].text}\n")

# NEW: refresh local session reference so the state we print reflects what's
# actually stored (see REVISION SUMMARY #4).
session = asyncio.run(session_service.get_session(
    app_name="namespace_demo_app", user_id="user1", session_id="session1"
))

# Check state after turn
print("=== State after Turn 1 ===")
print(f"Full state: {session.state}")
# UPDATED comment: temp:step was never set in the first place in this ADK
# version, not just "discarded after the turn" - see REVISION SUMMARY #3.
print(f"temp:step: {session.state.get('temp:step')}")  # Always None here, not just after this turn
print(f"topic: {session.state.get('topic')}")  # Should persist
print(f"user:theme: {session.state.get('user:theme')}")  # Should persist
print(f"app:version: {session.state.get('app:version')}")  # Should persist


print("\n=== Simulating Turn 2 (same session) ===")

result2 = runner.run(
    user_id="user1",
    session_id="session1",
    new_message=Content(parts=[Part(text="Check state again")])
)

for event in result2:
    if event.is_final_response():
        print(f"Agent response:\n{event.content.parts[0].text}\n")

# NEW: refresh again before printing (see REVISION SUMMARY #4).
session = asyncio.run(session_service.get_session(
    app_name="namespace_demo_app", user_id="user1", session_id="session1"
))

print("=== State after Turn 2 ===")
print(f"Full state: {session.state}")
print(f"temp:step: {session.state.get('temp:step')}")  # Still None
print(f"topic: {session.state.get('topic')}")  # Still here (session state)
print(f"user:theme: {session.state.get('user:theme')}")  # Still here (user state)


# Simulate new session
print("\n=== Simulating NEW Session (session2) ===")

# UPDATED: wrapped in asyncio.run() - same reason as the first
# create_session() call (see REVISION SUMMARY #1).
session2 = asyncio.run(session_service.create_session(
    app_name="namespace_demo_app",
    user_id="user1",  # Same user
    session_id="session2"  # Different session
))

print(f"New session state: {session2.state}")
print(f"topic: {session2.state.get('topic')}")  # Should be GONE (session-scoped)
print(f"user:theme: {session2.state.get('user:theme')}")  # Should PERSIST (user-scoped)
print(f"app:version: {session2.state.get('app:version')}")  # Should PERSIST (app-scoped)