import os
from flask import Flask, request, session, redirect, url_for, render_template, flash
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv

from database import get_db, init_db, get_or_create_user
from whatsapp_handler import handle_whatsapp_message

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")


# --- WhatsApp Webhook ---

@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    """Twilio WhatsApp webhook endpoint."""
    incoming_msg = request.values.get("Body", "").strip()
    from_number = request.values.get("From", "").replace("whatsapp:", "")

    response_text = handle_whatsapp_message(from_number, incoming_msg)

    resp = MessagingResponse()
    resp.message(response_text)
    return str(resp)


# --- Web UI Routes ---

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        phone = request.form.get("phone", "").strip()
        if phone:
            if not phone.startswith("+"):
                phone = "+972" + phone.lstrip("0")
            user = get_or_create_user(phone)
            session["user_id"] = user["id"]
            session["phone"] = user["phone"]
            return redirect(url_for("index"))

    user = None
    stats = {}
    if "user_id" in session:
        conn = get_db()
        user_row = conn.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],)).fetchone()
        if user_row:
            user = dict(user_row)
            stats["gift_cards"] = conn.execute(
                "SELECT COUNT(*) as c FROM user_gift_cards WHERE user_id = ?", (user["id"],)
            ).fetchone()["c"]
            stats["credit_cards"] = conn.execute(
                "SELECT COUNT(*) as c FROM user_credit_cards WHERE user_id = ?", (user["id"],)
            ).fetchone()["c"]
            stats["consumer_clubs"] = conn.execute(
                "SELECT COUNT(*) as c FROM user_consumer_clubs WHERE user_id = ?", (user["id"],)
            ).fetchone()["c"]
        conn.close()

    return render_template("index.html", user=user, stats=stats)


@app.route("/manage")
def manage():
    if "user_id" not in session:
        return redirect(url_for("index"))

    conn = get_db()
    user = dict(conn.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],)).fetchone())

    gift_card_platforms = [dict(r) for r in conn.execute("SELECT * FROM gift_card_platforms ORDER BY name").fetchall()]
    credit_cards = [dict(r) for r in conn.execute("SELECT * FROM credit_cards ORDER BY bank, name").fetchall()]
    consumer_clubs = [dict(r) for r in conn.execute("SELECT * FROM consumer_clubs ORDER BY name").fetchall()]

    user_gift_cards = [dict(r) for r in conn.execute(
        "SELECT * FROM user_gift_cards WHERE user_id = ?", (user["id"],)).fetchall()]
    user_credit_cards = [dict(r) for r in conn.execute(
        "SELECT * FROM user_credit_cards WHERE user_id = ?", (user["id"],)).fetchall()]
    user_consumer_clubs = [dict(r) for r in conn.execute(
        "SELECT * FROM user_consumer_clubs WHERE user_id = ?", (user["id"],)).fetchall()]

    conn.close()

    return render_template("manage.html",
                           user=user,
                           gift_card_platforms=gift_card_platforms,
                           credit_cards=credit_cards,
                           consumer_clubs=consumer_clubs,
                           user_gift_cards=user_gift_cards,
                           user_credit_cards=user_credit_cards,
                           user_consumer_clubs=user_consumer_clubs)


@app.route("/save_gift_cards", methods=["POST"])
def save_gift_cards():
    if "user_id" not in session:
        return redirect(url_for("index"))

    user_id = session["user_id"]
    conn = get_db()

    conn.execute("DELETE FROM user_gift_cards WHERE user_id = ?", (user_id,))

    platforms = conn.execute("SELECT id FROM gift_card_platforms").fetchall()
    for p in platforms:
        pid = p["id"]
        if request.form.get(f"gc_{pid}"):
            balance = request.form.get(f"balance_{pid}", 0)
            try:
                balance = float(balance) if balance else 0
            except ValueError:
                balance = 0
            conn.execute(
                "INSERT INTO user_gift_cards (user_id, gift_card_platform_id, balance) VALUES (?, ?, ?)",
                (user_id, pid, balance)
            )

    conn.commit()
    conn.close()
    flash("Gift cards updated successfully!", "success")
    return redirect(url_for("manage"))


@app.route("/save_credit_cards", methods=["POST"])
def save_credit_cards():
    if "user_id" not in session:
        return redirect(url_for("index"))

    user_id = session["user_id"]
    conn = get_db()

    conn.execute("DELETE FROM user_credit_cards WHERE user_id = ?", (user_id,))

    cards = conn.execute("SELECT id FROM credit_cards").fetchall()
    for c in cards:
        cid = c["id"]
        if request.form.get(f"cc_{cid}"):
            conn.execute(
                "INSERT INTO user_credit_cards (user_id, credit_card_id) VALUES (?, ?)",
                (user_id, cid)
            )

    conn.commit()
    conn.close()
    flash("Credit cards updated successfully!", "success")
    return redirect(url_for("manage"))


@app.route("/save_consumer_clubs", methods=["POST"])
def save_consumer_clubs():
    if "user_id" not in session:
        return redirect(url_for("index"))

    user_id = session["user_id"]
    conn = get_db()

    conn.execute("DELETE FROM user_consumer_clubs WHERE user_id = ?", (user_id,))

    clubs = conn.execute("SELECT id FROM consumer_clubs").fetchall()
    for cl in clubs:
        clid = cl["id"]
        if request.form.get(f"club_{clid}"):
            conn.execute(
                "INSERT INTO user_consumer_clubs (user_id, consumer_club_id) VALUES (?, ?)",
                (user_id, clid)
            )

    conn.commit()
    conn.close()
    flash("Consumer clubs updated successfully!", "success")
    return redirect(url_for("manage"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# --- Admin routes for managing stores/deals (optional, for later) ---

@app.route("/admin/stores")
def admin_stores():
    conn = get_db()
    stores = [dict(r) for r in conn.execute("SELECT * FROM stores ORDER BY category, name").fetchall()]
    conn.close()
    return render_template("admin_stores.html", stores=stores) if os.path.exists(
        os.path.join(app.template_folder, "admin_stores.html")) else str(stores)


# --- Init ---

with app.app_context():
    init_db()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"
    print(f"\n{'='*50}")
    print(f"  WhatsApp Deals Bot Server")
    print(f"  Web UI: http://localhost:{port}")
    print(f"  WhatsApp Webhook: http://localhost:{port}/webhook")
    print(f"{'='*50}\n")
    app.run(host="0.0.0.0", port=port, debug=debug)
