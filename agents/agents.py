from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from prompts.prompts import for_agent_prompt, against_agent_prompt, judge_agent_prompt
from tools.tools import evaluate_phase, get_previous_arguments, get_topic

model = ChatOllama(
    model="llama3.2:1b",
    temperature=0.9,
    num_predict=250
)

for_agent = create_react_agent(
    model=model,
    tools=[get_topic, get_previous_arguments],
    state_modifier=for_agent_prompt
)

against_agent = create_react_agent(
    model=model,
    tools=[get_topic, get_previous_arguments],
    state_modifier=against_agent_prompt
)

judge_agent = create_react_agent(
    model=model,
    tools=[evaluate_phase],
    state_modifier=judge_agent_prompt
)