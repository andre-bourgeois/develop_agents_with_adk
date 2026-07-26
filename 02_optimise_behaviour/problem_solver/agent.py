"""
Problem-solving agent with built-in planning capabilities.
Demonstrates ADK's BuiltInPlanner with ThinkingConfig
"""

from google.adk.agents.llm_agent import Agent
from google.adk.planners import BuiltInPlanner
from google.genai import types

root_agent = Agent(
    model='gemini-3.5-flash',
    name='strategic_problem_solver',
    description='Solves complex problems using multi-step reasoning and planning',
    instruction="""You are a strategic problem-solver.

    Your approach to complex problems.
    1. **Understand** - Break the problem down into components.
    2. **Analyse** - Consider multiple approaches and trade-offs.
    3. **Plan** - Develop a step-by-step solution strategy.
    4. **Execute** - Provide clear, actionable recommendations.

    For complex problems:
    - Think through implications and edge cases.
    - Consider short-term vs long-term consequences.
    - Identify potential risks and mitigation strategies.
    - Provide reasoning for your recommendations.

    Be thorough, analytic, and systematic in your approach.""",
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True, # Show reasoning process
            thinking_budget=2048   # Large budget for complex thinking
        )
    )
)
