"""SQLite bilan ishlash: paketlar va buyurtmalar."""
import secrets
import sqlite3
from datetime import datetime, timedelta, timezone

from config import DB_PATH, TZ_OFFSET

TZ = timezone(timedelta(hours=TZ_OFFSET))

GAMES = {
    "freefire": {"name": "Free Fire", "unit": "💎", "id_len": (6, 13)},
    "pubg": {"name": "PUBG Mobile", "unit": "UC", "id_len": (8, 12)},
}

# Boshlang'ich paketlar: (o'yin, miqdor, nom, narx so'm, narx somoni). Narxlar namunaviy — admin paneldan o'zgartiring.
DEFAULT_PACKAGES = [
    ("freefire", 100, "100 💎", 13000, 10), ("freefire", 310, "310 💎", 37000, 32),
    ("freefire", 520, "520 💎", 62000, 52), ("freefire", 1060, "1060 💎", 124000, 104),
    ("freefire", 2180, "2180 💎", 248000, 207), ("freefire", 5600, "5600 💎", 620000, 499),
    ("freefire", 0, "Weekly Lite", 0, 5), ("freefire", 0, "Weekly", 0, 21),
    ("freefire", 0, "Monthly", 0, 75),
    ("pubg", 60, "60 UC", 13000, 9), ("pubg", 325, "325 UC", 63000, 46),
    ("pubg", 660, "660 UC", 125000, 92), ("pubg", 1800, "1800 UC", 315000, 230),
    ("pubg", 3850, "3850 UC", 630000, 460), ("pubg", 8100, "8100 UC", 1260000, 915),
] 


def now():
    return datetime.now(TZ)


def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with connect() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS packages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game TEXT NOT NULL, amount INTEGER NOT NULL, label TEXT NOT NULL,
            price_uzs INTEGER NOT NULL, price_tjs INTEGER NOT NULL,
            active INTEGER NOT NULL DEFAULT 1);
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL, game TEXT NOT NULL, package_label TEXT NOT NULL,
            player_id TEXT NOT NULL, region TEXT NOT NULL, price INTEGER NOT NULL,
            currency TEXT NOT NULL, contact TEXT, receipt TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending', admin_note TEXT,
            created_at TEXT NOT NULL, updated_at TEXT);
        CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
        """)
        if c.execute("SELECT COUNT(*) FROM packages").fetchone()[0] == 0:
            c.executemany("INSERT INTO packages (game, amount, label, price_uzs, price_tjs) VALUES (?,?,?,?,?)",
                          DEFAULT_PACKAGES)


# ---------- Paketlar ----------

def packages(game, only_active=True):
    q = "SELECT * FROM packages WHERE game = ?" + (" AND active = 1" if only_active else "") + " ORDER BY amount"
    with connect() as c:
        return c.execute(q, (game,)).fetchall()


def all_packages():
    with connect() as c:
        return c.execute("SELECT * FROM packages ORDER BY game, amount").fetchall()


def get_package(pid):
    with connect() as c:
        return c.execute("SELECT * FROM packages WHERE id = ?", (pid,)).fetchone()


def update_package(pid, price_uzs, price_tjs, active):
    with connect() as c:
        c.execute("UPDATE packages SET price_uzs=?, price_tjs=?, active=? WHERE id=?",
                  (price_uzs, price_tjs, int(active), pid))


# ---------- Buyurtmalar ----------

def _new_code(c):
    alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"  # chalkash belgilarsiz (0/O, 1/I)
    while True:
        code = "DG-" + "".join(secrets.choice(alphabet) for _ in range(6))
        if not c.execute("SELECT 1 FROM orders WHERE code = ?", (code,)).fetchone():
            return code


def create_order(game, package_label, player_id, region, price, currency, contact, receipt):
    with connect() as c:
        code = _new_code(c)
        c.execute("""INSERT INTO orders (code, game, package_label, player_id, region, price, currency,
                     contact, receipt, created_at) VALUES (?,?,?,?,?,?,?,?,?,?)""",
                  (code, game, package_label, player_id, region, price, currency, contact, receipt,
                   now().strftime("%Y-%m-%d %H:%M")))
        return code


def get_order(code):
    with connect() as c:
        return c.execute("SELECT * FROM orders WHERE code = ?", (code.strip().upper(),)).fetchone()


def list_orders(status=None, limit=200):
    with connect() as c:
        if status:
            return c.execute("SELECT * FROM orders WHERE status=? ORDER BY id DESC LIMIT ?", (status, limit)).fetchall()
        return c.execute("SELECT * FROM orders ORDER BY id DESC LIMIT ?", (limit,)).fetchall()


def set_status(code, status, note=None):
    with connect() as c:
        c.execute("UPDATE orders SET status=?, admin_note=?, updated_at=? WHERE code=?",
                  (status, note or None, now().strftime("%Y-%m-%d %H:%M"), code))


def counts():
    with connect() as c:
        rows = c.execute("SELECT status, COUNT(*) n FROM orders GROUP BY status").fetchall()
    res = {"pending": 0, "done": 0, "rejected": 0}
    res.update({r["status"]: r["n"] for r in rows})
    res["all"] = sum(res.values())
    return res


def revenue_today():
    today = now().strftime("%Y-%m-%d")
    with connect() as c:
        rows = c.execute("""SELECT currency, SUM(price) s, COUNT(*) n FROM orders
                            WHERE status='done' AND created_at LIKE ? GROUP BY currency""", (today + "%",)).fetchall()
    return {r["currency"]: (r["s"], r["n"]) for r in rows}
