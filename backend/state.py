# state.py
# ---------------------------------------------------------
# TravelState is the shared "clipboard" object that flows through
# every node in the LangGraph. Every agent reads fields it needs
# and writes its own results before passing the whole thing on.
# ---------------------------------------------------------
from typing import TypedDict, Optional, Literal


class TravelState(TypedDict):
    # --- Inputs, set once before the graph starts running ---
    user_id: int
    origin: str
    destination: str
    start_date: str
    end_date: str
    budget_cap: float             # converted to USD — used for all internal math
    budget_cap_original: float    # exactly what the user typed, in their own currency — DISPLAY ONLY
    currency: str                  # "INR" or "USD" — pulled from the user's row in Postgres

    # --- Filled in as agents run ---
    flight_options: list
    hotel_options: list
    activity_options: list
    selected_flight: Optional[dict]
    selected_hotel: Optional[dict]
    total_cost: float

    # --- Budget negotiation loop state ---
    budget_status: Literal["pending", "within_budget", "over_budget", "best_effort"]
    retry_count: int
    max_retries: int

    # --- Final output ---
    final_itinerary: Optional[dict]
    trace: list        # the agentic AI trace — see trace.py
