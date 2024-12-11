from langchain_core.tools import tool
from langgraph.graph import MessagesState

@tool
def evaluate_phase(state: MessagesState):
    """
    Use this to get arguments provided by agant which is for the given topic
    and the one which is against during the pending phase of the debate.
    """
    messages = state["messages"]
    argument_for = 'Argument for:\n' + messages[-2][1]
    argument_against = '\nArgument against:\n' + messages[-1][1]
    whole_phase =  + argument_for + argument_against
    return whole_phase

@tool
def get_topic(state: MessagesState):
    """
    Use this tool to get the topic of ongoing debate.
    """
    topic = state["messages"][0][1]
    return topic

@tool
def get_previous_arguments(state: MessagesState):
    """
    Use this tool to analyze previously provided arguments by both sides: for and against.
    """
    messages = state["messages"]
    arguments_for = 'Arguments for:\n'
    arguments_against = 'Arguments against:\n'
    for message in messages:
        if message[0] == 'for_agent':
            arguments_for += message[1] + '\n'
        elif message[0] == 'against_agent':
            arguments_against += message[1] + '\n'
    return arguments_for + arguments_against
