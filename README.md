# Develop Agents with Agent Development Kit (ADK)

A collection of agents built while working through the hands-on sections of Google's **Develop Agents with Agent Development Kit (ADK)** learning path. Each folder maps to a stage of that path and builds from basic agents through to agents that plan, hold state, call external tools, and be trusted to work independently through complex requests.

Following on from this, I'm in the process of working through the subsequent learning path that focuses on deploying production-ready agents in enterprise environments - work for this path will be available in its own repo once complete.

Where the code contained differs to the code provided in the curriculum, comments have been included to highlight where these changes have been made and why. Many of these were due to slight differences in the version of ADK and models used in the curriculum and those used by me throughout my study.

## Repository Structure

| Folder | Focus |
|---|---|
| `01_getting_started` | Building and running your first agent |
| `02_optimise_behaviour` | Instruction design, structured output, model configuration, planning |
| `03_manage_memory_and_state` | Session state, templating, persistence namespaces |
| `04_add_capabilities_with_tools` | Search grounding, code execution, MCP, custom tools |

Each agent folder contains several agents within their own subfolders. Each subfolder contains an `agent.py` (or `root_agent.yaml` for config-based agents) plus any supporting resources and test scripts.

## 01. Getting Started

Environment setup and the fundamentals of an ADK agent.

- Setting up a Python virtual environment and installing `google-adk`
- The four core parameters of every agent: `model`, `name`, `description`, `instruction`
- Running agents four ways: `adk web`, `adk run`, `adk api_server`, and programmatically via `Runner`
- Defining agents in Python vs. YAML (`adk create --type=config`)

Agents: `my_first_agent`, `my_config_agent`

## 02. Optimise Behaviour

Writing production-grade instructions and controlling model output.

- Five reusable instruction patterns: identity, mission, methodology, boundaries, few-shot examples
- Structured output with Pydantic `BaseModel` schemas and `output_key`
- Model selection and configuration: Gemini Pro vs. Flash, temperature, safety settings
- Planning for multi-step tasks with `BuiltInPlanner`, `PlanReActPlanner`, and `ThinkingConfig`

Agents: `customer_support_agent`, `product_extractor`, `model_comparison`, `problem_solver`

## 03. Manage Memory & State

Giving agents programmatic control over data across a conversation.

- Reading and writing exact values with `session.state`
- Auto-saving output with the `output_key` parameter
- Injecting state into instructions with `{variable}` templating
- Persistence scopes: `temp:`, session, `user:`, `app:`

Agents: `name_extractor`, `personalised_greeter`, `namespace_demo`

## 04. Add Capabilities with Tools

Turning agents from responders into agents that can act.

- Real-time information via Google Search grounding
- Precise calculation via code execution
- Connecting to external systems via MCP servers (filesystem, databases, APIs)
- Writing custom function tools and handling their errors
- Coordinating multiple tools and delegating to sub-agents (agent-as-tool)

Agents: `geography_assistant`, `math_assistant`, `research_assistant`, `file_reader_assistant`, `travel_agent`, `customer_support_agent`

## Course & Reference Material

This repo follows Google's public course and documentation for ADK:

- [Develop Agents with Agent Development Kit (ADK)](https://www.skills.google/paths/3545)

Official documentation referenced throughout:

- [ADK documentation](https://google.github.io/adk-docs/)

## Prerequisites

- Python 3.10+
- `pip install google-adk`
- A `GOOGLE_API_KEY` set in a local `.env` file per agent (not committed, see `.gitignore`)
