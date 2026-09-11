# agents/combo_optimizer.py
# ---------------------------------------------------------
# A small brute-force search used by budget_agent when the "full
# value" plan doesn't fit the budget. Tries every flight, every
# hotel, and every possible subset of activities, and returns
# whichever full combination spends the MOST money without going
# OVER the budget cap — i.e., the plan that gets closest to (but
# never past) what the user can actually afford.
#
# Brute force is completely fine here: with just a handful of
# flights/hotels/activities, checking every possibility is fast and
# far easier to understand than a fancier algorithm would be.
# ---------------------------------------------------------
from itertools import combinations


def find_best_combo(flights, hotels, activities, budget_cap):
    """
    Returns {"flight": ..., "hotel": ..., "activities": [...], "total": ...}
    for the best-fitting combination, or None if not even the cheapest
    flight + cheapest hotel alone fits the budget.
    """
    best = None

    for flight in flights:
        for hotel in hotels:
            base_cost = flight["price"] + hotel["price"]

            if base_cost > budget_cap:
                # This flight+hotel pair alone is already too expensive.
                # No subset of activities (which only ADD cost) can ever
                # bring it back under budget, so skip it immediately.
                continue

            remaining = budget_cap - base_cost
            subset, subset_cost = _best_activity_subset(activities, remaining)
            total = base_cost + subset_cost

            # Keep this combination if it's the best (highest-spending,
            # still-under-budget) one found so far
            if best is None or total > best["total"]:
                best = {
                    "flight": flight,
                    "hotel": hotel,
                    "activities": subset,
                    "total": total,
                }

    return best


def _best_activity_subset(activities, remaining_budget):
    """
    Checks every possible subset of activities (there are only 2^n of
    them — fine for a handful of activities) and returns whichever
    subset spends the most money without exceeding remaining_budget.
    """
    best_subset = []
    best_total = 0

    for size in range(len(activities) + 1):
        for combo in combinations(activities, size):
            total = sum(a["price"] for a in combo)
            if total <= remaining_budget and total > best_total:
                best_subset = list(combo)
                best_total = total

    return best_subset, best_total
