# agents/hotel_agent.py
# ---------------------------------------------------------
# Same pattern as flight_agent — search, then report each hotel's
# name, per-night cost, and a route-specific booking search link.
# ---------------------------------------------------------
from urllib.parse import quote
from state import TravelState
from trace import log_step
from currency import convert_price, format_price

MOCK_HOTELS = [
    {"name": "Ibis Budget", "price": 90, "rating": 3.9},
    {"name": "Hampton Inn", "price": 130, "rating": 4.3},
    {"name": "Generator Hostel", "price": 55, "rating": 4.0},
]


def hotel_agent_node(state: TravelState) -> TravelState:
    # TODO: replace with a real hotel search API, e.g. Amadeus Hotel
    # Search or Booking.com's affiliate API
    options = MOCK_HOTELS
    state["hotel_options"] = options

    destination = state["destination"]
    currency = state["currency"]

    options_detail = []
    for h in options:
        options_detail.append({
            "name": h["name"],
            "price_display": format_price(convert_price(h["price"], currency), currency) + "/night",
            "link": f"https://www.booking.com/searchresults.html?ss={quote(h['name'] + ' ' + destination)}",
        })

    log_step(
        trace=state["trace"],
        node_name="hotel_agent",
        decision="options_found",
        reasoning=f"Found {len(options)} hotel options in {destination}.",
        options=options_detail,
    )

    return state
