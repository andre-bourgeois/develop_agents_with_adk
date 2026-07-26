# Developing Agents with Google ADK

A hands-on collection of agents built while working through Google's **Engineer AI Agents with Agent Development Kit (ADK)** learning path. Each folder maps to a stage of that path, moving from a first "hello world" agent through to agents that plan, hold state, and call external tools.

## Repository structure

| Folder | Focus |
|---|---|
| `01_getting_started` | Building and running your first agent |
| `02_optimise_behaviour` | Instruction design, structured output, model configuration, planning |
| `03_manage_memory_and_state` | Session state, templating, persistence namespaces |
| `04_add_capabilities_with_tools` | Search grounding, code execution, MCP, custom tools |

Each agent folder contains an `agent.py` (or `root_agent.yaml` for config-based agents) plus any supporting test scripts.

## 01. Getting started

Environment setup and the fundamentals of an ADK agent.

- Setting up a Python virtual environment and installing `google-adk`
- The four core parameters of every agent: `model`, `name`, `description`, `instruction`
- Running agents four ways: `adk web`, `adk run`, `adk api_server`, and programmatically via `Runner`
- Defining agents in Python vs. YAML (`adk create --type=config`)

Agents: `my_first_agent`, `my_config_agent`

## 02. Optimise behaviour

Writing production-grade instructions and controlling model output.

- Five reusable instruction patterns: identity, mission, methodology, boundaries, few-shot examples
- Structured output with Pydantic `BaseModel` schemas and `output_key`
- Model selection and configuration: Gemini Pro vs. Flash, temperature, safety settings
- Planning for multi-step tasks with `BuiltInPlanner`, `PlanReActPlanner`, and `ThinkingConfig`

Agents: `customer_support_agent`, `product_extractor`, `model_comparison`, `problem_solver`

## 03. Manage memory and state

Giving agents programmatic control over data across a conversation.

- Reading and writing exact values with `session.state`
- Auto-saving output with the `output_key` parameter
- Injecting state into instructions with `{variable}` templating
- Persistence scopes: `temp:`, session, `user:`, `app:`

Agents: `name_extractor`, `personalised_greeter`, `namespace_demo`

## 04. Add capabilities with tools

Turning agents from responders into agents that can act.

- Real-time information via Google Search grounding
- Precise calculation via code execution
- Connecting to external systems via MCP servers (filesystem, databases, APIs)
- Writing custom function tools and handling their errors
- Coordinating multiple tools and delegating to sub-agents (agent-as-tool)

Agents: `geography_assistant`, `math_assistant`, `research_assistant`, `file_reader_assistant`, `travel_agent`, `customer_support_agent`

## Course and reference material

This repo follows Google's public course and documentation for ADK:

- [Engineer AI Agents with Agent Development Kit (ADK)](https://www.skills.google/course_templates/1382) — Google Cloud Skills Boost
- [Understand Google Cloud Agents](https://www.skills.google/course_templates/1504)
- [Build your first agent with Agent Development Kit (ADK)](https://www.skills.google/course_templates/1563)

Official documentation referenced throughout:

- [ADK documentation](https://google.github.io/adk-docs/)
- [Google Search tool for ADK](https://google.github.io/adk-docs/tools/gemini-api/google-search/)
- [Structuring data with ADK](https://google.github.io/adk-docs/agents/llm-agents/#structuring-data-input_schema-output_schema-output_key)
- [Sequential agents](https://google.github.io/adk-docs/agents/workflow-agents/sequential-agents/)

## Prerequisites

- Python 3.10+
- `pip install google-adk`
- A `GOOGLE_API_KEY` set in a local `.env` file per agent (not committed, see `.gitignore`)
