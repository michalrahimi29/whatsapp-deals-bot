"""
Telegram bot for the Israeli deals finder.

Uses python-telegram-bot library with polling mode.
Reuses the same database and deal-lookup logic as the WhatsApp handler.
"""

import os
import logging
import threading

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from database import get_or_create_user, find_stores, get_store_deals, init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

WEB_URL = os.environ.get("WEB_BASE_URL", "http://localhost:5000")

GREETING_KEYWORDS = {"hi", "hey", "hello"}
HELP_KEYWORDS = {"help"}


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    await update.message.reply_text(
        _welcome_message(),
        parse_mode="Markdown",
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command."""
    await update.message.reply_text(
        _help_message(),
        parse_mode="Markdown",
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle any text message - search for store deals."""
    text = update.message.text.strip()
    text_lower = text.lower()

    if text_lower in GREETING_KEYWORDS:
        await update.message.reply_text(_welcome_message(), parse_mode="Markdown")
        return

    if text_lower in HELP_KEYWORDS:
        await update.message.reply_text(_help_message(), parse_mode="Markdown")
        return

    if not text:
        await update.message.reply_text(_help_message(), parse_mode="Markdown")
        return

    # Use Telegram user ID as phone number for user tracking
    telegram_id = str(update.message.from_user.id)
    user = get_or_create_user(telegram_id)
    stores = find_stores(text)

    if not stores:
        await update.message.reply_text(
            _no_stores_message(text),
            parse_mode="Markdown",
        )
        return

    parts = []
    for store in stores:
        store_block = _format_store_deals(store, user)
        parts.append(store_block)

    response = "\n\n".join(parts)
    response += f"\n\n\U0001f4a1 *Manage your cards at:* {WEB_URL}"

    # Telegram has a 4096 char limit per message
    if len(response) > 4000:
        for part in parts:
            await update.message.reply_text(part, parse_mode="Markdown")
        await update.message.reply_text(
            f"\U0001f4a1 *Manage your cards at:* {WEB_URL}",
            parse_mode="Markdown",
        )
    else:
        await update.message.reply_text(response, parse_mode="Markdown")


def _format_store_deals(store: dict, user: dict) -> str:
    """Return a formatted message block for one store."""
    store_id = store["id"]
    user_id = user["id"]

    deals = get_store_deals(store_id, user_id=user_id)

    lines = []
    lines.append(f"\U0001f3ea *{store['name']}*")

    has_personal = bool(
        deals.get("user_gift_cards")
        or deals.get("user_credit_card_deals")
        or deals.get("user_consumer_club_deals")
    )

    if has_personal:
        lines.append("")
        lines.append("\U0001f3af *YOUR PERSONALIZED DEALS:*")
        lines.extend(_format_deals_section(
            gift_cards=deals.get("user_gift_cards", []),
            credit_card_deals=deals.get("user_credit_card_deals", []),
            consumer_club_deals=deals.get("user_consumer_club_deals", []),
        ))

    lines.append("")
    lines.append("\U0001f4cb *ALL AVAILABLE DEALS:*")
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


def _format_deals_section(gift_cards, credit_card_deals, consumer_club_deals):
    lines = []

    if gift_cards:
        names = []
        for gc in gift_cards:
            entry = gc["name"]
            if gc.get("notes"):
                entry += f" ({gc['notes']})"
            names.append(entry)
        lines.append(f"\U0001f381 *Gift Cards:* {', '.join(names)}")

    if credit_card_deals:
        lines.append("\U0001f4b3 *Credit Card Deals:*")
        for deal in credit_card_deals:
            card_label = deal["name"]
            if deal.get("bank"):
                card_label = f"{deal['bank']} {deal['name']}"
            lines.append(f"  \u2022 {card_label} - {deal['discount_description']}")

    if consumer_club_deals:
        lines.append("\U0001f48e *Club Deals:*")
        for deal in consumer_club_deals:
            lines.append(f"  \u2022 {deal['name']} - {deal['discount_description']}")

    return lines


def _welcome_message():
    return (
        "\U0001f44b *Welcome to the Deals Bot!*\n"
        "\n"
        "Send me a store or restaurant name and I'll show you "
        "all the available deals \u2013 gift cards, credit-card discounts, "
        "and club benefits.\n"
        "\n"
        "For example, try sending:\n"
        "  \u2022 Fox\n"
        "  \u2022 Aroma\n"
        "  \u2022 Castro\n"
        "\n"
        f"\U0001f4a1 *Manage your cards at:* {WEB_URL}\n"
        "Type /help for more info."
    )


def _help_message():
    return (
        "\u2139\ufe0f *How to use the Deals Bot*\n"
        "\n"
        "Just type the name of a store or restaurant, and I'll show you:\n"
        "\U0001f381 Gift card options that work there\n"
        "\U0001f4b3 Credit card deals & discounts\n"
        "\U0001f48e Consumer club benefits\n"
        "\n"
        "If you've set up your personal cards on the website, "
        "I'll highlight the deals that match *your* cards first!\n"
        "\n"
        "*Commands:*\n"
        "  \u2022 Send a store name \u2192 see deals\n"
        "  \u2022 /help \u2192 this message\n"
        "  \u2022 /start \u2192 welcome message\n"
        "\n"
        f"\U0001f517 *Set up your cards:* {WEB_URL}"
    )


def _no_stores_message(query):
    return (
        f"\U0001f50d I couldn't find any stores matching *\"{query}\"*.\n"
        "\n"
        "\U0001f4a1 *Tips:*\n"
        "  \u2022 Check your spelling\n"
        "  \u2022 Try the store's full name\n"
        "  \u2022 Try in Hebrew or English\n"
        "\n"
        "Type /help for usage instructions."
    )


def run_telegram_bot():
    """Start the Telegram bot (blocking - run in a thread)."""
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.warning("TELEGRAM_BOT_TOKEN not set - Telegram bot disabled")
        return

    init_db()
    logger.info("Starting Telegram bot...")

    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling(drop_pending_updates=True)


def start_telegram_bot_thread():
    """Start the Telegram bot in a background thread."""
    thread = threading.Thread(target=run_telegram_bot, daemon=True)
    thread.start()
    return thread


if __name__ == "__main__":
    run_telegram_bot()
