# trace.py
# ---------------------------------------------------------
# The "agentic AI trace" — an ordered log of what every agent
# decided and why, for one run. This is what makes the system's
# reasoning visible instead of a black box, and it's what gets
# shown in the UI's trace panel.
# ---------------------------------------------------------
from datetime import datetime


def new_trace() -> list:
    """Creates a fresh, empty trace list for a new trip-planning run."""
    return []


def log_step(
    trace: list,
    node_name: str,
    decision: str,
    reasoning: str,
    link: str = None,
    options: list = None,
) -> None:
    """
    Called by every agent right before it hands control to the next
    node. Appends one structured entry describing what happened.

    `link` is an optional single fallback link (rarely used now).
    `options` is the itemized detail the three search agents pass —
    a list of {name, price_display, link} for EACH thing they found,
    so the UI can show actual costs and per-item links right at that
    step, instead of just a count and one generic search link.
    """
    entry = {
        "node": node_name,
        "decision": decision,
        "reasoning": reasoning,
        "timestamp": datetime.utcnow().isoformat(),
    }
    if link:
        entry["link"] = link
    if options:
        entry["options"] = options

    trace.append(entry)
    # Note: trace is a list passed by reference, so this mutates the
    # same list object that lives inside the shared state — every
    # agent sees every previous step's trace entries too.


def deduplicated_for_display(trace: list) -> list:
    """
    Returns a version of the trace with only the LAST occurrence of
    each node kept (in original order). Used so the UI never shows a
    stale decision — e.g. an early "over budget" result from
    budget_agent's first pass — once a later pass through the same
    node has superseded it.

    The full, un-deduplicated trace (every attempt) is still what
    gets saved to the database in routes/plan.py — this function only
    affects what's returned to the frontend for display.
    """
    last_index_for_node = {}
    for i, step in enumerate(trace):
        # As we scan forward, each node's LATEST index simply
        # overwrites its previous one in this dict
        last_index_for_node[step["node"]] = i

    keep_indices = set(last_index_for_node.values())
    return [step for i, step in enumerate(trace) if i in keep_indices]
