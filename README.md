# WhatsApp Deals Bot

A WhatsApp bot that helps users find all available deals (gift cards, credit card discounts, and consumer club benefits) for any store or restaurant in Israel.

## How It Works

1. **WhatsApp**: Users send a store name (e.g. "castro", "fox", "aroma") and get back all available deals
2. **Web UI**: Users visit the web dashboard to set up their personal credit cards, gift cards, and consumer clubs
3. **Personalized results**: When a user who has set up their profile queries a store, they see their personal deals highlighted first

## Features

- **64+ Israeli stores** across restaurants, fashion, baby/kids, home, beauty, electronics, and supermarkets
- **12 gift card platforms** including BuyMe variants, Tav Hazahav, Colu, Presto, Lovecard, 10bis
- **8 credit cards** including Cal Visa, Cal Mastercard, Isracard, Max Visa, Max Mastercard, Leumi Card, Diners Club, American Express Israel
- **10 consumer clubs** including Tav Hazahav, Hever, Students Club, Hot Mobile, Partner, Pelephone, Bezeq, Cellcom, Latet, and **Dreamcard (Fox Group)**
- **Dreamcard / Fox Group**: 17 partner brands (Fox, Fox Home, American Eagle, Aerie, Mango, Foot Locker, Laline, Billabong, The Children's Place, Terminal X, Ruby Bay, Flying Tiger, Sunglass Hut, Quiksilver, Shilav, Itay Brands, Jumbo) with 10% cashback and 30% birthday discount
- Hebrew and English search support with aliases

---

## Deploy to Render (Free - Runs 24/7)

This is the recommended way to run the bot without needing to start a server manually.

### Step 1: Push to GitHub

Create a new GitHub repository and push this folder:

```bash
cd whatsapp-deals-bot
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/whatsapp-deals-bot.git
git push -u origin main
```

### Step 2: Deploy on Render

1. Go to [render.com](https://render.com) and sign up (free)
2. Click **New > Web Service**
3. Connect your GitHub repo
4. Render will auto-detect the `render.yaml` config
5. Add your environment variables:
   - `TWILIO_ACCOUNT_SID` - from your Twilio console
   - `TWILIO_AUTH_TOKEN` - from your Twilio console
   - `WEB_BASE_URL` - set to `https://your-app-name.onrender.com`
6. Click **Create Web Service**

Your bot will be live at `https://your-app-name.onrender.com`

### Step 3: Set up Twilio WhatsApp

1. Go to [twilio.com](https://www.twilio.com) and create a free account
2. Navigate to **Messaging > Try it out > Send a WhatsApp message**
3. Follow the sandbox setup (send the join code from your WhatsApp)
4. In **Messaging > Settings > WhatsApp Sandbox Settings**, set the webhook URL to:
   ```
   https://your-app-name.onrender.com/webhook
   ```
5. That's it! Send a store name to the Twilio sandbox number on WhatsApp

> **Note**: On Render's free tier, the service may spin down after 15 minutes of inactivity. The first message after spin-down takes ~30 seconds to respond while the service wakes up. After that, responses are instant.

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

### 3. Set up environment variables

```bash
cp .env.example .env
# Edit .env with your Twilio credentials
```

### 4. Run the server

```bash
python app.py
```

The server starts at:
- **Web UI**: http://localhost:5000
- **WhatsApp Webhook**: http://localhost:5000/webhook

### 5. For local WhatsApp testing with ngrok

```bash
ngrok http 5000
```

Use the ngrok URL (e.g. `https://abc123.ngrok.io/webhook`) as your Twilio webhook URL.

---

## Project Structure

```
whatsapp-deals-bot/
├── app.py                 # Main Flask application
├── database.py            # Database models and queries
├── whatsapp_handler.py    # WhatsApp message handler
├── seed_data.py           # Seed data script
├── deals.db               # SQLite database (created on first run)
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
├── Procfile               # Production server config (gunicorn)
├── render.yaml            # Render.com deployment config
├── templates/
│   ├── base.html          # Base template
│   ├── index.html         # Dashboard / login page
│   └── manage.html        # Manage cards and clubs
└── README.md
```

## Example WhatsApp Conversation

```
User: fox
Bot:
🏪 *Fox (פוקס)*

🎯 *YOUR PERSONALIZED DEALS:*
💎 *Club Deals:*
  • Dreamcard (דרימקארד) - 10% קאשבק + 30% הנחת יום הולדת (עד 500 ₪)

📋 *ALL AVAILABLE DEALS:*
🎁 *Gift Cards:* BuyMe Fashion, BuyMe All, Tav Hazahav, Lovecard
💳 *Credit Card Deals:*
  • Max Visa - 20% הנחה על פריט שני
  • Isracard - 15% הנחה
💎 *Club Deals:*
  • Tav Hazahav - 15% הנחה
  • Hever - 10% הנחה
  • Cellcom Club - 10% הנחה
  • Dreamcard (דרימקארד) - 10% קאשבק + 30% הנחת יום הולדת (עד 500 ₪)
```

## Adding More Data

To add more stores or deals, edit `seed_data.py` and re-run:
```bash
python seed_data.py
```

The seed script clears existing data and re-inserts everything fresh.
