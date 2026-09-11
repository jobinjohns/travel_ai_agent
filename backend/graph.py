# graph.py
# ---------------------------------------------------------
# Wires every agent node together into one LangGraph graph.
# This file defines the ORDER agents run in and the CONDITIONS
# under which the flow loops back or finishes — the actual
# "orchestration" logic of the whole system lives here.
# ---------------------------------------------------------
from langgraph.graph import StateGraph, END
from state import TravelState
from agents.travel_planner import travel_planner_node
from agents.flight_agent import flight_agent_node
from agents.hotel_agent import hotel_agent_node
from agents.activity_agent import activity_agent_node
from agents.budget_agent import budget_agent_node, should_retry
from agents.final_planner import final_planner_node


def build_graph():
    # Create a new graph, telling LangGraph the shape of the shared state
    graph = StateGraph(TravelState)

    # Register every function as a named node
    graph.add_node("travel_planner", travel_planner_node)
    graph.add_node("flight_agent", flight_agent_node)
    graph.add_node("hotel_agent", hotel_agent_node)
    graph.add_node("activity_agent", activity_agent_node)
    graph.add_node("budget_agent", budget_agent_node)
    graph.add_node("final_planner", final_planner_node)

    # Every run starts at travel_planner
    graph.set_entry_point("travel_planner")

    # Straight-line path through the search agents, one after another.
    # (Kept sequential rather than parallel — simpler to trace, log,
    # and debug for a first build; a natural upgrade later.)
    graph.add_edge("travel_planner", "flight_agent")
    graph.add_edge("flight_agent", "hotel_agent")
    graph.add_edge("hotel_agent", "activity_agent")
    graph.add_edge("activity_agent", "budget_agent")

    # THE key agentic behavior: after budget_agent runs, call
    # should_retry() to decide where to go next. If it returns "retry",
    # loop all the way back to flight_agent and search again with the
    # (now-updated) retry_count. If "finish", move on to final_planner.
    graph.add_conditional_edges(
        "budget_agent",
        should_retry,
        {
            "retry": "flight_agent",
            "finish": "final_planner",
        },
    )

    # After final_planner, the graph is done
    graph.add_edge("final_planner", END)

    # .compile() turns this definition into an actual runnable object
    return graph.compile()
