# agents/travel_planner.py
# ---------------------------------------------------------
# The entry-point agent. Runs first. Summarizes the trip using the
# LLM — shown in the trace — using the budget exactly as the user
# typed it, in their OWN currency (not the internal USD figure the
# rest of the graph uses for math).
# ---------------------------------------------------------
from state import TravelState
from trace import log_step
from llm_client import ask_llm
from currency import format_price


def travel_planner_node(state: TravelState) -> TravelState:
    cap_display = format_price(state["budget_cap_original"], state["currency"])

    brief = ask_llm(
        system_prompt=(
            "You are a travel planning assistant. Summarize trip "
            "requests in one short, friendly sentence. Keep any "
            "numbers and currency symbols exactly as given."
        ),
        user_prompt=(
            f"Trip from {state['origin']} to {state['destination']}, "
            f"Dates: {state['start_date']} to {state['end_date']}, "
            f"Budget: {cap_display}"
        ),
    )

    log_step(
        trace=state["trace"],
        node_name="travel_planner",
        decision="request_understood",
        reasoning=brief,
    )

    return state
