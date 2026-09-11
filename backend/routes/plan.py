# routes/plan.py
# ---------------------------------------------------------
# The main endpoint. Identifies the user from their JWT token (not
# from the request body), fetches their currency from Postgres,
# converts their typed budget cap into USD (internal math currency)
# while keeping the original entered value for display, runs the
# LangGraph, saves the result, and returns the itinerary + a
# de-duplicated trace (see trace.py) for the UI.
# ---------------------------------------------------------
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User, TripPlan
from schemas import TripRequest
from graph import build_graph
from trace import new_trace, deduplicated_for_display
from currency import to_usd
from auth import get_current_user_id

router = APIRouter(prefix="/plan", tags=["plan"])

# Build the graph ONCE at startup, not on every request
travel_graph = build_graph()


@router.post("/")
def plan_trip(
    request: TripRequest,
    user_id: int = Depends(get_current_user_id),   # comes from the token, not the request body
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # The user typed their budget in THEIR currency (e.g. INR). Convert
    # it to USD once, here, so every agent downstream can compare plain
    # numbers without ever thinking about currency again.
    budget_cap_usd = to_usd(request.budget_cap, user.currency)

    initial_state = {
        "user_id": user.id,
        "origin": request.origin,
        "destination": request.destination,
        "start_date": request.start_date,
        "end_date": request.end_date,
        "budget_cap": budget_cap_usd,
        "budget_cap_original": request.budget_cap,
        "currency": user.currency,
        "flight_options": [],
        "hotel_options": [],
        "activity_options": [],
        "selected_flight": None,
        "selected_hotel": None,
        "total_cost": 0.0,
        "budget_status": "pending",
        "retry_count": 0,
        # With static mock data, one optimization retry is exhaustive —
        # further retries can't change a deterministic result. Raise
        # this once real APIs are plugged in (see the agent TODOs).
        "max_retries": 1,
        "final_itinerary": None,
        "trace": new_trace(),
    }

    final_state = travel_graph.invoke(initial_state)

    # Store the FULL trace (every attempt, including any superseded
    # ones) in the database — useful history even though the UI only
    # shows the latest decision per agent.
    trip_record = TripPlan(
        user_id=user.id,
        origin=request.origin,
        destination=request.destination,
        start_date=request.start_date,
        end_date=request.end_date,
        budget_cap=request.budget_cap,
        total_cost=final_state["total_cost"],
        currency=user.currency,
        itinerary=final_state["final_itinerary"],
        trace=final_state["trace"],
    )
    db.add(trip_record)
    db.commit()

    return {
        "itinerary": final_state["final_itinerary"],
        # De-duplicated for the UI: if budget_agent (or any node) ran
        # twice because of the retry loop, only its LAST decision is
        # shown — no stale "over budget" step left behind once a later
        # pass has superseded it.
        "trace": deduplicated_for_display(final_state["trace"]),
    }
