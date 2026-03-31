# Telegram Deals Bot

A Telegram bot that helps users find all available deals (gift cards, credit card discounts, and consumer club benefits) for any store or restaurant in Israel.

## How It Works

1. **Telegram**: Send a store name (e.g. "fox", "aroma", "castro") and get back all available deals
2. **Web UI**: Visit the web dashboard to set up your personal credit cards, gift cards, and consumer clubs
3. **Personalized results**: After setting up your profile, the bot highlights your personal deals first

## Features

- **64+ Israeli stores** across restaurants, fashion, baby/kids, home, beauty, electronics, and supermarkets
- **12 gift card platforms** including BuyMe variants, Tav Hazahav, Colu, Presto, Lovecard, 10bis
- **8 credit cards** including Cal Visa, Cal Mastercard, Isracard, Max Visa, Max Mastercard, Leumi Card, Diners Club, American Express Israel
- **10 consumer clubs** including Tav Hazahav, Hever, Students Club, Hot Mobile, Partner, Pelephone, Bezeq, Cellcom, Latet, and **Dreamcard (Fox Group)**
- **Dreamcard / Fox Group**: 17 partner brands (Fox, Fox Home, American Eagle, Aerie, Mango, Foot Locker, Laline, Billabong, The Children's Place, Terminal X, Ruby Bay, Flying Tiger, Sunglass Hut, Quiksilver, Shilav, Itay Brands, Jumbo) with 10% cashback and 30% birthday discount
- Hebrew and English search support with aliases

---

## Quick Setup (3 Steps)

### Step 1: Create a Telegram Bot (30 seconds)

1. Open Telegram and search for **@BotFather**
2. Send `/newbot`
3. Choose a name (e.g. "Israel Deals Bot")
4. Choose a username (e.g. "il_deals_bot")
5. BotFather gives you a **token** like `123456789:ABCdefGHI...` - save this!

### Step 2: Deploy to Render (Free - Runs 24/7)

1. Push this repo to your GitHub (or fork it)
2. Go to [render.com](https://render.com) and sign up (free, no credit card)
3. Click **New > Web Service** and connect your GitHub repo
4. Render auto-detects the config. Add one environment variable:
   - `TELEGRAM_BOT_TOKEN` = the token from BotFather
5. Click **Create Web Service**

That's it! Your bot is live and running 24/7.

### Step 3: Use It

Open Telegram, find your bot by the username you chose, and send a store name like `fox` or `aroma`.

> **Note**: On Render's free tier, the service may sleep after 15 minutes of inactivity. The first message after sleep takes ~30 seconds. After that, responses are instant.

---

## Local Development

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Seed the database

```bash
python seed_data.py
```

### 3. Set up environment

```bash
cp .env.example .env
# Edit .env - add your TELEGRAM_BOT_TOKEN
```

### 4. Run

```bash
python app.py
```

Or run just the Telegram bot (no web UI):
```bash
python telegram_bot.py
```

---

## Project Structure

```
whatsapp-deals-bot/
├── app.py                 # Flask web UI + Telegram bot startup
├── telegram_bot.py        # Telegram bot handler
├── database.py            # Database models and queries
├── whatsapp_handler.py    # Legacy WhatsApp handler (kept for reference)
├── seed_data.py           # Seed data script
├── deals.db               # SQLite database (created on first run)
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
├── Procfile               # Production server config
├── render.yaml            # Render.com deployment config
├── templates/
│   ├── base.html          # Base template
│   ├── index.html         # Dashboard / login page
│   └── manage.html        # Manage cards and clubs
└── README.md
```

## Example Telegram Conversation

```
User: fox
Bot:
🏪 Fox (פוקס)

📋 ALL AVAILABLE DEALS:
🎁 Gift Cards: BuyMe Fashion, BuyMe All, Tav Hazahav, Lovecard
💳 Credit Card Deals:
  • Max Visa - 20% הנחה על פריט שני
  • Isracard - 15% הנחה
💎 Club Deals:
  • Tav Hazahav - 15% הנחה
  • Hever - 10% הנחה
  • Cellcom Club - 10% הנחה
  • Dreamcard (דרימקארד) - 10% קאשבק + 30% הנחת יום הולדת (עד 500 ₪)
```

## Adding More Data

Edit `seed_data.py` and re-run:
```bash
python seed_data.py
```
