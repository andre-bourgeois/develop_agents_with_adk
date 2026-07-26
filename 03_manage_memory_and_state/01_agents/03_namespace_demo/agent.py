"""
Namespace Demo - Shows all four state namespaces
Demonstrates temp:, session, user:, and app: persistence scopes.

Reference: https://google.github.io/adk-docs/sessions/state.md

==============================================================================
REVISION SUMMARY (vs. original course-copied version)
==============================================================================
1. Instruction placeholders changed from "{key?default text}" style
   (e.g. {app:name?Namespace Demo}, {user:theme?not set}) to bare "{key?}".
   WHY: same parser limitation found in the previous lesson's agent -
   ADK 2.5.0's instructions_utils.py only implements {key} (strict) and
   {key?} (blank if missing). Any extra text after "?" fails validation
   and the whole placeholder is sent to the LLM unresolved. This applies
   identically to namespaced keys like {app:name} and {user:theme} - the
   "app:"/"user:"/"temp:" prefix itself is handled correctly by the
   parser, only the "?default text" suffix is the problem.

2. Default-value wording ("Namespace Demo" / "1.0" for app fields,
   "not set" for user/session/temp fields) moved out of the template
   syntax and into plain-English instruction text.

3. Model left as 'gemini-3.5-flash' rather than the course material's
   'gemini-2.5-flash', to stay consistent with the working setup from
   the previous exercise. Swap this if you'd rather match the course
   material exactly - both are valid model names.

NOTE ON temp: STATE (full explanation in test_namespaces.py's header):
temp:-prefixed keys can only be set by a tool while an invocation is
actively running - they cannot be pre-seeded by external code before a
run in this ADK version. This agent has no tools, so {temp:step} will
always resolve to blank/"not set" no matter what the test script tries
to set beforehand. Structural limitation of this ADK version, not a
mistake in this file.
==============================================================================
"""

from google.adk.agents import LlmAgent

# Create agent that uses all four namespaces
root_agent = LlmAgent(
    model='gemini-3.5-flash',
    name='namespace_demo',

    # UPDATED instruction block - see REVISION SUMMARY above for why the
    # placeholder syntax and default wording changed.
    instruction="""
        You are a demo assistant showing state namespaces.

        === App State (global for all users) ===
        App name: {app:name?}
        App version: {app:version?}

        === User State (persists across sessions) ===
        User preference: {user:theme?}

        === Session State (persists this conversation) ===
        Conversation topic: {topic?}

        === Temp State (current turn only) ===
        Current step: {temp:step?}

        If App name is blank, use "Namespace Demo". If App version is blank, use "1.0".
        For User preference, Conversation topic, or Current step, if any is blank, say "not set" for that one.

        Respond with a friendly message showing these namespace values.
        """,

    output_key="response",
)