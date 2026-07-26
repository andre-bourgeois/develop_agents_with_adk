"""
Model configuration demonstration showing factual vs creative optimisation.
Demonstrates ADK's generate_content_config with different settings.
"""

from google.adk.agents.llm_agent import Agent
from google.genai import types

# Agent 1: Optimised for Factual Data Extraction
# Uses low temp for consistency, strict safety for accuracy

factual_agent = Agent(
    model='gemini-3-flash-preview',
    name='data_extractor',
    description='Extracts factual information with high consistency',
    instruction="""
        You are a precise data extractor.

        Extract facts exactly as stated. Do not:
        - add information not present in the input
        - make assumption or inferences
        - use creative language

        be accurate, concise, and deterministic.
    """,
    generate_content_config=types.GenerateContentConfig(
        temperature=0.1, # very low for consistency
        max_output_tokens=500,
        top_p=0.8,
        top_k=10,
        safety_settings=[
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE
            )
        ]
    )
)

# Agent 2: Optimised for creative brainstorming
# Uses high-temp for creativity, can use pro model for better ideas, but not used here in example

creative_agent = Agent(
    model='gemini-3-flash-preview',
    name='creative_agent',
    description='Generates creative ideas and explores possibilities',
    instruction="""
        You are a creative brainstorming partner.

        Generat innovative, diverse, and imaginative ideas. Feel free to:
        - think outside of the box
        - combine unexpected concepts
        - explore unconventional approaches

        be creative, caried, and thought provoking.
    """,
    generate_content_config=types.GenerateContentConfig(
        temperature=0.9, # high for creativity
        max_output_tokens=1000, # longer to allow for details
        top_p=0.95,
        top_k=40,
        safety_settings=[
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
            )
        ]
    )
)

#root_agent = factual_agent
root_agent = creative_agent
