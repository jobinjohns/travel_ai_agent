# agents/budget_agent.py
# ---------------------------------------------------------
# The core "agentic" decision point, and where flight/hotel/activity
# SELECTION actually happens (the search agents only searched).
#
# Pass 1: try the full-value plan (cheapest flight + cheapest hotel +
# every activity). If that fits, done.
# Pass 2 (only if needed): run the exhaustive combo optimizer to find
# the combination that spends the most money without exceeding the
# cap — i.e. the closest possible plan to the budget.
# If even the cheapest possible plan is still over budget, stop
# looping (a second identical, exhaustive search can't change the
# answer) and report a clear best-effort plan with the exact shortfall.
#
# Every number shown to the user — here and in the final itinerary —
# is in THEIR currency, never a raw internal USD figure.
# ---------------------------------------------------------
from state import TravelState
from trace import log_step
from llm_client import ask_llm
from currency import convert_price, format_price
from agents.combo_optimizer import find_best_combo


def budget_agent_node(state: TravelState) -> TravelState:
    flights = state["flight_options"]
    hotels = state["hotel_options"]
    activities = state["activity_options"]
    cap = state["budget_cap"]                 # USD — used for all real math
    currency = state["currency"]
    # The exact number the user typed, in their own currency — for
    # display only, so we never show a rounded/converted figure where
    # the original is available
    cap_display = format_price(state["budget_cap_original"], currency)

    if state["retry_count"] == 0:
        # Pass 1: the "ideal" plan — cheapest flight, cheapest hotel,
        # every activity included
        flight = min(flights, key=lambda f: f["price"])
        hotel = min(hotels, key=lambda h: h["price"])
        chosen_activities = activities
        attempt_note = "full plan with every activity included"
    else:
        # Pass 2: search every flight / hotel / activity-subset
        # combination for the one that spends the most without
        # exceeding the cap — the best plan actually achievable
        combo = find_best_combo(flights, hotels, activities, cap)
        if combo is None:
            # Not even the cheapest flight + cheapest hotel alone fits
            flight = min(flights, key=lambda f: f["price"])
            hotel = min(hotels, key=lambda h: h["price"])
            chosen_activities = []
        else:
            flight = combo["flight"]
            hotel = combo["hotel"]
            chosen_activities = combo["activities"]
        attempt_note = "optimized plan, trimmed to fit as close to your budget as possible"

    state["selected_flight"] = flight
    state["selected_hotel"] = hotel
    state["activity_options"] = chosen_activities

    total = flight["price"] + hotel["price"] + sum(a["price"] for a in chosen_activities)
    state["total_cost"] = total
    total_display = format_price(convert_price(total, currency), currency)

    if total <= cap:
        state["budget_status"] = "within_budget"
        reasoning = f"Total {total_display} fits within your {cap_display} budget ({attempt_note})."

    elif state["retry_count"] < state["max_retries"]:
        # With static mock data, one optimization pass is exhaustive —
        # max_retries stays configurable for when real, variable APIs
        # are plugged in later (see the TODOs in the search agents),
        # where a repeated search could genuinely return something new.
        state["retry_count"] += 1
        state["budget_status"] = "over_budget"
        reasoning = (
            f"Total {total_display} exceeds your {cap_display} budget with the full plan. "
            f"Retrying with an optimized selection to fit closer to your budget."
        )

    else:
        state["budget_status"] = "best_effort"
        shortfall_display = format_price(convert_price(total - cap, currency), currency)
        reasoning = (
            f"Even the closest achievable plan ({total_display}) is {shortfall_display} "
            f"over your {cap_display} budget. Returning this as the best available option."
        )

    # Turn the raw numbers into a friendly one-line explanation for the
    # trace/UI. We explicitly tell the LLM to keep our numbers/symbols
    # as-is, so it can't accidentally re-introduce the wrong currency.
    friendly_note = ask_llm(
        system_prompt=(
            "You explain trip-budget decisions to travelers in one encouraging "
            "sentence. Keep any numbers and currency symbols exactly as given "
            "to you — do not change or convert them."
        ),
        user_prompt=reasoning,
    )

    log_step(
        trace=state["trace"],
        node_name="budget_agent",
        decision=state["budget_status"],
        reasoning=friendly_note,
    )

    return state


def should_retry(state: TravelState) -> str:
    """
    LangGraph conditional-edge function: decides whether to loop back
    to flight_agent (re-running search + selection) or move on to
    final_planner, based on what budget_agent_node just decided.
    """
    if state["budget_status"] == "over_budget":
        return "retry"
    return "finish"
