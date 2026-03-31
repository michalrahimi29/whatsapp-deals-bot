import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deals.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT UNIQUE NOT NULL,
            name TEXT DEFAULT ''
        );

        CREATE TABLE IF NOT EXISTS gift_card_platforms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT DEFAULT ''
        );

        CREATE TABLE IF NOT EXISTS credit_cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            bank TEXT DEFAULT '',
            description TEXT DEFAULT ''
        );

        CREATE TABLE IF NOT EXISTS consumer_clubs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT DEFAULT ''
        );

        CREATE TABLE IF NOT EXISTS stores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT DEFAULT '',
            aliases TEXT DEFAULT ''
        );

        CREATE TABLE IF NOT EXISTS store_gift_cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            store_id INTEGER NOT NULL,
            gift_card_platform_id INTEGER NOT NULL,
            notes TEXT DEFAULT '',
            FOREIGN KEY (store_id) REFERENCES stores(id) ON DELETE CASCADE,
            FOREIGN KEY (gift_card_platform_id) REFERENCES gift_card_platforms(id) ON DELETE CASCADE,
            UNIQUE(store_id, gift_card_platform_id)
        );

        CREATE TABLE IF NOT EXISTS store_credit_card_deals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            store_id INTEGER NOT NULL,
            credit_card_id INTEGER NOT NULL,
            discount_description TEXT NOT NULL,
            FOREIGN KEY (store_id) REFERENCES stores(id) ON DELETE CASCADE,
            FOREIGN KEY (credit_card_id) REFERENCES credit_cards(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS store_consumer_club_deals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            store_id INTEGER NOT NULL,
            consumer_club_id INTEGER NOT NULL,
            discount_description TEXT NOT NULL,
            FOREIGN KEY (store_id) REFERENCES stores(id) ON DELETE CASCADE,
            FOREIGN KEY (consumer_club_id) REFERENCES consumer_clubs(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS user_gift_cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            gift_card_platform_id INTEGER NOT NULL,
            balance REAL DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (gift_card_platform_id) REFERENCES gift_card_platforms(id) ON DELETE CASCADE,
            UNIQUE(user_id, gift_card_platform_id)
        );

        CREATE TABLE IF NOT EXISTS user_credit_cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            credit_card_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (credit_card_id) REFERENCES credit_cards(id) ON DELETE CASCADE,
            UNIQUE(user_id, credit_card_id)
        );

        CREATE TABLE IF NOT EXISTS user_consumer_clubs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            consumer_club_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (consumer_club_id) REFERENCES consumer_clubs(id) ON DELETE CASCADE,
            UNIQUE(user_id, consumer_club_id)
        );
    """)

    conn.commit()
    conn.close()


# --- Helper functions ---

def get_or_create_user(phone):
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE phone = ?", (phone,)).fetchone()
    if not user:
        conn.execute("INSERT INTO users (phone) VALUES (?)", (phone,))
        conn.commit()
        user = conn.execute("SELECT * FROM users WHERE phone = ?", (phone,)).fetchone()
    conn.close()
    return dict(user)


def find_stores(query):
    """Find stores matching the query by name or aliases (fuzzy-ish match)."""
    conn = get_db()
    query_lower = query.strip().lower()
    stores = conn.execute("SELECT * FROM stores").fetchall()
    results = []
    for store in stores:
        store_name = store["name"].lower()
        aliases = store["aliases"].lower() if store["aliases"] else ""
        if (query_lower in store_name or store_name in query_lower or
                query_lower in aliases or aliases in query_lower):
            results.append(dict(store))
    conn.close()
    return results


def get_store_deals(store_id, user_id=None):
    """Get all deals for a store. If user_id is given, only show deals relevant to user's cards/clubs."""
    conn = get_db()

    # Gift card options
    gift_cards = conn.execute("""
        SELECT gcp.name, sgc.notes
        FROM store_gift_cards sgc
        JOIN gift_card_platforms gcp ON sgc.gift_card_platform_id = gcp.id
        WHERE sgc.store_id = ?
    """, (store_id,)).fetchall()

    # Credit card deals
    cc_deals = conn.execute("""
        SELECT cc.name, cc.bank, sccd.discount_description
        FROM store_credit_card_deals sccd
        JOIN credit_cards cc ON sccd.credit_card_id = cc.id
        WHERE sccd.store_id = ?
    """, (store_id,)).fetchall()

    # Consumer club deals
    club_deals = conn.execute("""
        SELECT ccl.name, sccld.discount_description
        FROM store_consumer_club_deals sccld
        JOIN consumer_clubs ccl ON sccld.consumer_club_id = ccl.id
        WHERE sccld.store_id = ?
    """, (store_id,)).fetchall()

    result = {
        "gift_cards": [dict(g) for g in gift_cards],
        "credit_card_deals": [dict(c) for c in cc_deals],
        "consumer_club_deals": [dict(cl) for cl in club_deals],
    }

    # If user_id provided, filter to only user's cards/clubs
    if user_id:
        user_gc_ids = {r["gift_card_platform_id"] for r in conn.execute(
            "SELECT gift_card_platform_id FROM user_gift_cards WHERE user_id = ?", (user_id,)).fetchall()}
        user_cc_ids = {r["credit_card_id"] for r in conn.execute(
            "SELECT credit_card_id FROM user_credit_cards WHERE user_id = ?", (user_id,)).fetchall()}
        user_club_ids = {r["consumer_club_id"] for r in conn.execute(
            "SELECT consumer_club_id FROM user_consumer_clubs WHERE user_id = ?", (user_id,)).fetchall()}

        user_gift_cards = conn.execute("""
            SELECT gcp.name, sgc.notes
            FROM store_gift_cards sgc
            JOIN gift_card_platforms gcp ON sgc.gift_card_platform_id = gcp.id
            WHERE sgc.store_id = ? AND sgc.gift_card_platform_id IN ({})
        """.format(",".join("?" * len(user_gc_ids)) if user_gc_ids else "NULL"),
            (store_id, *user_gc_ids)).fetchall() if user_gc_ids else []

        user_cc_deals = conn.execute("""
            SELECT cc.name, cc.bank, sccd.discount_description
            FROM store_credit_card_deals sccd
            JOIN credit_cards cc ON sccd.credit_card_id = cc.id
            WHERE sccd.store_id = ? AND sccd.credit_card_id IN ({})
        """.format(",".join("?" * len(user_cc_ids)) if user_cc_ids else "NULL"),
            (store_id, *user_cc_ids)).fetchall() if user_cc_ids else []

        user_club_deals = conn.execute("""
            SELECT ccl.name, sccld.discount_description
            FROM store_consumer_club_deals sccld
            JOIN consumer_clubs ccl ON sccld.consumer_club_id = ccl.id
            WHERE sccld.store_id = ? AND sccld.consumer_club_id IN ({})
        """.format(",".join("?" * len(user_club_ids)) if user_club_ids else "NULL"),
            (store_id, *user_club_ids)).fetchall() if user_club_ids else []

        result["user_gift_cards"] = [dict(g) for g in user_gift_cards]
        result["user_credit_card_deals"] = [dict(c) for c in user_cc_deals]
        result["user_consumer_club_deals"] = [dict(cl) for cl in user_club_deals]

    conn.close()
    return result


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
