# agents/flight_agent.py
# ---------------------------------------------------------
# Searches for flight options between the user's origin and
# destination. Selection happens later in budget_agent — this
# agent's job is to search AND report back exactly what it found:
# each flight's airline, cost (in the user's currency), and a
# route-specific link — not just a count and one generic link.
# ---------------------------------------------------------
from urllib.parse import quote
from state import TravelState
from trace import log_step
from currency import convert_price, format_price

# All prices in USD — our internal "common currency" for all agent math.
# NOTE: these are static mock prices, not calculated from the actual
# origin/destination distance — see the TODO below for real search.
MOCK_FLIGHTS = [
    {"airline": "KLM", "price": 420, "duration_hrs": 9.5},
    {"airline": "Lufthansa", "price": 510, "duration_hrs": 11},
    {"airline": "Air India", "price": 380, "duration_hrs": 10},
]


def flight_agent_node(state: TravelState) -> TravelState:
    # TODO: replace with a real flight search API call using BOTH
    # origin and destination, e.g.:
    #   options = amadeus_client.search_flights(
    #       origin=state["origin"], destination=state["destination"],
    #       date=state["start_date"]
    #   )
    # Real APIs price by actual route distance; this mock data doesn't.
    options = MOCK_FLIGHTS
    state["flight_options"] = options

    origin = state["origin"]
    destination = state["destination"]
    currency = state["currency"]

    # Build the itemized detail the UI actually shows: every option
    # found, its cost in the user's own currency, and a link specific
    # to that airline + route (not a generic destination-only search)
    options_detail = []
    for f in options:
        options_detail.append({
            "name": f["airline"],
            "price_display": format_price(convert_price(f["price"], currency), currency),
            "link": (
                "https://www.google.com/travel/flights?q="
                + quote(f"{f['airline']} flights from {origin} to {destination}")
            ),
        })

    log_step(
        trace=state["trace"],
        node_name="flight_agent",
        decision="options_found",
        reasoning=f"Found {len(options)} flight options from {origin} to {destination}.",
        options=options_detail,
    )

    return state
