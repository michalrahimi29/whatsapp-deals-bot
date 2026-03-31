"""
WhatsApp message handler for the Israeli deals bot.

Processes incoming WhatsApp messages (via Twilio webhook) and returns
formatted responses showing available deals for a given store.
"""

import os

from database import get_or_create_user, find_stores, get_store_deals

WEB_URL = os.environ.get("WEB_BASE_URL", "http://localhost:5000")

HELP_KEYWORDS = {"help", "עזרה"}
GREETING_KEYWORDS = {"hi", "hey", "שלום", "hello"}


def handle_whatsapp_message(from_number: str, body: str) -> str:
    """
    Main entry point. Receives the sender's phone number and the raw
    message body, and returns a formatted WhatsApp-friendly string.
    """
    text = body.strip()
    text_lower = text.lower()

    if text_lower in GREETING_KEYWORDS:
        return _welcome_message()

    if text_lower in HELP_KEYWORDS:
        return _help_message()

    if not text:
        return _help_message()

    user = get_or_create_user(from_number)
    stores = find_stores(text)

    if not stores:
        return _no_stores_message(text)

    parts: list[str] = []
    for store in stores:
        store_block = _format_store_deals(store, user)
        parts.append(store_block)

    response = "\n\n".join(parts)
    response += f"\n\n💡 *Manage your cards at:* {WEB_URL}"

    return response


def _format_store_deals(store: dict, user: dict) -> str:
    """Return a fully-formatted WhatsApp message block for one store."""
    store_id = store["id"]
    user_id = user["id"]

    deals = get_store_deals(store_id, user_id=user_id)

    lines: list[str] = []
    lines.append(f"🏪 *{store['name']}*")

    has_personal = _has_user_deals(deals)
    if has_personal:
        lines.append("")
        lines.append("🎯 *YOUR PERSONALIZED DEALS:*")
        lines.extend(_format_deals_section(
            gift_cards=deals.get("user_gift_cards", []),
            credit_card_deals=deals.get("user_credit_card_deals", []),
            consumer_club_deals=deals.get("user_consumer_club_deals", []),
        ))

    lines.append("")
    lines.append("📋 *ALL AVAILABLE DEALS:*")
    all_section = _format_deals_section(
        gift_cards=deals.get("gift_cards", []),
        credit_card_deals=deals.get("credit_card_deals", []),
        consumer_club_deals=deals.get("consumer_club_deals", []),
    )

    if all_section:
        lines.extend(all_section)
    else:
        lines.append("  No deals found for this store yet.")

    return "\n".join(lines)


def _format_deals_section(
    gift_cards: list[dict],
    credit_card_deals: list[dict],
    consumer_club_deals: list[dict],
) -> list[str]:
    lines: list[str] = []

    if gift_cards:
        names = []
        for gc in gift_cards:
            entry = gc["name"]
            if gc.get("notes"):
                entry += f" ({gc['notes']})"
            names.append(entry)
        lines.append(f"🎁 *Gift Cards:* {', '.join(names)}")

    if credit_card_deals:
        lines.append("💳 *Credit Card Deals:*")
        for deal in credit_card_deals:
            card_label = deal["name"]
            if deal.get("bank"):
                card_label = f"{deal['bank']} {deal['name']}"
            lines.append(f"  • {card_label} - {deal['discount_description']}")

    if consumer_club_deals:
        lines.append("💎 *Club Deals:*")
        for deal in consumer_club_deals:
            lines.append(f"  • {deal['name']} - {deal['discount_description']}")

    return lines


def _has_user_deals(deals: dict) -> bool:
    return bool(
        deals.get("user_gift_cards")
        or deals.get("user_credit_card_deals")
        or deals.get("user_consumer_club_deals")
    )


def _welcome_message() -> str:
    return (
        "👋 *Welcome to the Deals Bot!*\n"
        "\n"
        "Send me a store or restaurant name and I'll show you "
        "all the available deals – gift cards, credit-card discounts, "
        "and club benefits.\n"
        "\n"
        "For example, try sending:\n"
        "  • Castro\n"
        "  • Aroma\n"
        "  • ZARA\n"
        "\n"
        f"💡 *Manage your cards at:* {WEB_URL}\n"
        "Type *help* or *עזרה* for more info."
    )


def _help_message() -> str:
    return (
        "ℹ️ *How to use the Deals Bot*\n"
        "\n"
        "Just type the name of a store or restaurant, and I'll show you:\n"
        "🎁 Gift card options that work there\n"
        "💳 Credit card deals & discounts\n"
        "💎 Consumer club benefits\n"
        "\n"
        "If you've set up your personal cards on the website, "
        "I'll highlight the deals that match *your* cards first!\n"
        "\n"
        "*Commands:*\n"
        "  • Send a store name → see deals\n"
        "  • *help* / *עזרה* → this message\n"
        "  • *hi* / *שלום* → welcome message\n"
        "\n"
        f"🔗 *Set up your cards:* {WEB_URL}"
    )


def _no_stores_message(query: str) -> str:
    return (
        f"🔍 I couldn't find any stores matching *\"{query}\"*.\n"
        "\n"
        "💡 *Tips:*\n"
        "  • Check your spelling\n"
        "  • Try the store's full name\n"
        "  • Try in Hebrew or English\n"
        "\n"
        "Type *help* or *עזרה* for usage instructions."
    )
