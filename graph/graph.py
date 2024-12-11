from langgraph.graph import StateGraph, START, END, MessagesState
from agents.agents import for_agent, against_agent, judge_agent


def verdict(state: MessagesState):
    messages = state["messages"]
    if len(messages) > 5:
        return END
    return "continue"

workflow = StateGraph(MessagesState)
workflow.add_node("for_agent", for_agent)
workflow.add_node("against_agent", against_agent)
workflow.add_node("judge", judge_agent)

workflow.add_edge(START, "for_agent")
workflow.add_edge("for_agent", "against_agent")
workflow.add_edge("against_agent", "judge")
workflow.add_conditional_edges(
    "judge",
    verdict,
    {"continue": "for_agent", END: END}
)

graph = workflow.compile()