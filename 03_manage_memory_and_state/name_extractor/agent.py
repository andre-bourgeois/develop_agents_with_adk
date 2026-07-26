"""
Name Extractor - Demonstrates Session State Basics
Shows how to use output_key to save data and access it via session.state.

Reference: https://google.github.io/adk-docs/sessions/state.md
"""

from google.adk.agents.llm_agent import Agent

name_extractor = Agent(
    model='gemini-3-flash-preview',
    name='name_extractor',
    description='Extracts names from user input and saves them in session state.',
    instruction="Extract the person's name from the message. Return ONLY the name",
    output_key='extracted_name', # saves response to state["extracted_name"]
)

root_agent = name_extractor