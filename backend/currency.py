# currency.py
# ---------------------------------------------------------
# All the logic for deciding which currency to show a user, and
# converting/formatting prices for display.
# Rule: country == India -> INR, everything else -> USD.
# ---------------------------------------------------------

USD_TO_INR_RATE = 83.0


def get_currency_for_country(country: str) -> str:
    """Called once, at signup, to decide which currency a user sees."""
    normalized = country.strip().lower()
    if normalized == "india":
        return "INR"
    return "USD"


def convert_price(amount_usd: float, target_currency: str) -> float:
    """USD -> target currency. All our mock source data is priced in USD."""
    if target_currency == "INR":
        return round(amount_usd * USD_TO_INR_RATE, 2)
    return round(amount_usd, 2)


def to_usd(amount: float, source_currency: str) -> float:
    """
    The inverse of convert_price(): converts an amount FROM the
    user's currency INTO USD. Used once per trip request, to translate
    the budget cap the user typed (e.g. in INR) into the same currency
    all the internal agent math uses, so comparisons are correct.
    """
    if source_currency == "INR":
        return round(amount / USD_TO_INR_RATE, 2)
    return round(amount, 2)


def format_price(amount: float, currency: str) -> str:
    """(1500.5, 'INR') -> '₹1,500.50'   (1500.5, 'USD') -> '$1,500.50'"""
    symbol = "₹" if currency == "INR" else "$"
    return f"{symbol}{amount:,.2f}"
