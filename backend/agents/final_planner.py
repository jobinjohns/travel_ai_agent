# agents/final_planner.py
# ---------------------------------------------------------
# The last node. Assembles everything into one clean itinerary:
# converts every price into the user's currency, builds a
# route-specific search link for the flight, hotel, and each
# activity, and writes a clear plain-language message about whether
# the plan fits the budget — always phrased in the user's own currency.
# ---------------------------------------------------------
from urllib.parse import quote
from state import TravelState
from trace import log_step
from currency import convert_price, format_price


def final_planner_node(state: TravelState) -> TravelState:
    currency = state["currency"]
    origin = state["origin"]
    destination = state["destination"]

    # --- Flight ---
    flight = state["selected_flight"]
    flight_out = {
        **flight,
        "price_display": format_price(convert_price(flight["price"], currency), currency),
        # No real booking API in this build — link to a route-specific
        # search instead of pretending we can complete an actual booking
        "link": (
            "https://www.google.com/travel/flights?q="
            + quote(f"{flight['airline']} flights from {origin} to {destination}")
        ),
    }

    # --- Hotel ---
    hotel = state["selected_hotel"]
    hotel_out = {
        **hotel,
        "price_display": format_price(convert_price(hotel["price"], currency), currency),
        "link": f"https://www.booking.com/searchresults.html?ss={quote(hotel['name'] + ' ' + destination)}",
    }

    # --- Activities ---
    activities_out = []
    for activity in state["activity_options"]:
        activities_out.append({
            **activity,
            "price_display": format_price(convert_price(activity["price"], currency), currency),
            "link": f"https://www.google.com/search?q={quote(activity['name'] + ' ' + destination)}",
        })

    # --- Budget summary + message, all in the user's own currency ---
    cap_display = format_price(state["budget_cap_original"], currency)
    total_display = format_price(convert_price(state["total_cost"], currency), currency)

    over_by_display = None
    if state["budget_status"] == "best_effort":
        shortfall_usd = state["total_cost"] - state["budget_cap"]
        if shortfall_usd > 0:
            over_by_display = format_price(convert_price(shortfall_usd, currency), currency)

    if over_by_display:
        message = (
            f"This plan is {over_by_display} over your budget of {cap_display} — "
            f"here's the closest option we could find."
        )
    elif state["retry_count"] > 0:
        message = f"This plan fits within your budget of {cap_display} — optimized to get the most out of it."
    else:
        message = f"This plan fits within your budget of {cap_display}."

    state["final_itinerary"] = {
        "origin": origin,
        "destination": destination,
        "dates": f"{state['start_date']} to {state['end_date']}",
        "flight": flight_out,
        "hotel": hotel_out,
        "activities": activities_out,
        "budget_cap_display": cap_display,
        "total_display": total_display,
        "over_by_display": over_by_display,
        "budget_status": state["budget_status"],
        "message": message,
    }

    log_step(
        trace=state["trace"],
        node_name="final_planner",
        decision="itinerary_ready",
        reasoning=f"Assembled final itinerary, total {total_display}. {message}",
    )

    return state
