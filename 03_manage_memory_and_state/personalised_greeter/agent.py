"""
Personalized Greeter - Demonstrates State Templating
Shows how {var} templating injects state values into instructions.

Reference: https://google.github.io/adk-docs/sessions/state.md

==============================================================================
REVISION SUMMARY (vs. original course-copied version)
==============================================================================
1. Instruction placeholders changed from "{key?default text}" style
   (e.g. {user_name?there}, {membership_tier?free}) to bare "{key?}".
   WHY: ADK 2.5.0's templating parser (google/adk/utils/instructions_utils.py)
   only implements two placeholder forms - {key} (strict, raises KeyError
   if missing) and {key?} (resolves to "" if missing). Any placeholder with
   extra text after the "?" fails an internal isidentifier() check and is
   sent to the LLM completely unresolved, braces and all. Confirmed by
   extracting and running the library's own matching logic against these
   exact placeholders.

2. Removed the invalid nested placeholder from the original course text:
   {membership_tier?Your membership level is: {membership_tier}}
   A placeholder can't legally contain another placeholder inside its
   conditional text, in any version of this syntax.

3. Default-value and conditional-mention behaviour (e.g. "say 'there' if
   no name is known", "only mention membership if it's set") moved out of
   the template syntax entirely and into plain-English instruction text,
   since the framework can no longer apply that logic for us.
==============================================================================
"""

from google.adk.agents import LlmAgent

# Agent with state templating
root_agent = LlmAgent(
    model='gemini-3.5-flash',
    name='personalized_greeter',
    # UPDATED instruction block - see REVISION SUMMARY above for why the
    # placeholder syntax and the default/conditional wording changed.
    instruction="""
You are a friendly assistant.

User information (may be blank if not provided):
- Name: {user_name?}
- Preferred language: {user_language?}
- Membership tier: {membership_tier?}

If Name is blank, do not address the user directly.
If Preferred language is blank, respond in English; otherwise respond in that language.
If Membership tier is blank, do not mention membership at all.
If Membership tier is set, briefly acknowledge it (e.g. "Your membership tier is: <tier>").

Greet the user warmly and offer assistance.
"""
)