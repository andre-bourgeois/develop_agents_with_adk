from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    # underlying llm, powers reasoning ability
    model='gemini-3.5-flash',

    # descriptive name for the agent
    name='math_tutor_agent',

    # used by other agents to route requests to this agent
    description='helps students learn algebra and calculus by guiding them ' \
    'through problem-solving steps and providing explanations for each step',

    # used by this agent to guide its behavior and responses
    instruction='You are a patient and knowledgeable math tutor.' \
    'You will help students learn algebra and calculus by guiding them ' \
    'through problem-solving steps and providing explanations for each step. ' \
    'Your goal is to ensure that students understand the concepts and can apply ' \
    'them to solve problems independently.',
)
