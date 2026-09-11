# agents/activity_agent.py
# ---------------------------------------------------------
# Suggests activities, reporting each one's name, cost, and a
# specific search link — same itemized pattern as the other search
# agents.
# ---------------------------------------------------------
from urllib.parse import quote
from state import TravelState
from trace import log_step
from currency import convert_price, format_price

MOCK_ACTIVITIES = [
    {"name": "Canal cruise", "price": 20},
    {"name": "Museum pass", "price": 22},
    {"name": "Bike tour", "price": 30},
    {"name": "Walking tour", "price": 0},
]


def activity_agent_node(state: TravelState) -> TravelState:
    # TODO: replace with real Google Maps Places + OpenWeather calls
    options = MOCK_ACTIVITIES
    state["activity_options"] = options

    destination = state["destination"]
    currency = state["currency"]

    options_detail = []
    for a in options:
        options_detail.append({
            "name": a["name"],
            "price_display": format_price(convert_price(a["price"], currency), currency),
            "link": f"https://www.google.com/search?q={quote(a['name'] + ' ' + destination)}",
        })

    log_step(
        trace=state["trace"],
        node_name="activity_agent",
        decision="options_found",
        reasoning=f"Found {len(options)} possible activities in {destination}.",
        options=options_detail,
    )

    return state
