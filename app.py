from dotenv import load_dotenv, find_dotenv
from graph.graph import graph

load_dotenv(find_dotenv())

try:
    print(graph.get_graph().draw_mermaid())
except Exception:
    pass

events = graph.stream(
    {
        "messages": [
            (
                "user",
                "Should people pursue scientific progres over needs of everyone?"
            )
        ],
    },
    {"recursion_limit": 100},
)
for event in events:
    for value in event.values():
        print("Assistant:", value["messages"][-1].content)
        print("--------------")
