"""DonatGo — Free Fire va PUBG Mobile uchun donat sayti (Flask)."""
import hmac
import os
import re
import secrets
import time
import uuid
from functools import wraps

from flask import (Flask, abort, flash, jsonify, redirect, render_template, request, send_from_directory,
                   session, url_for)

import config
import db
from i18n import REGIONS, translate

app = Flask(__name__)
app.config.update(
    SECRET_KEY=config.SECRET_KEY,
    MAX_CONTENT_LENGTH=(config.MAX_UPLOAD_MB + 1) * 1024 * 1024,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)
os.makedirs(config.UPLOAD_DIR, exist_ok=True)
db.init_db()


# ---------- Yordamchi funksiyalar ----------

def region():
    r = session.get("region")
    return r if r in REGIONS else "uz"


def t(key, **kw):
    return translate(key, region(), **kw)


def fmt_price(amount, currency):
    return f"{amount:,}".replace(",", " ") + " " + currency


def price_for(pkg, reg):
    return pkg["price_tjs"] if reg == "uz" else pkg["price_tjs"]


def is_open():
    h = db.now().hour
    s, e = config.WORK_START, config.WORK_END
    return s <= h < e if s < e else (h >= s or h < e)


def csrf_token():
    if "csrf" not in session:
        session["csrf"] = secrets.token_urlsafe(32)
    return session["csrf"]


def check_csrf():
    sent = request.form.get("csrf", "")
    return bool(sent) and hmac.compare_digest(sent, session.get("csrf", ""))


def image_kind(head: bytes):
    if head.startswith(b"\xff\xd8\xff"):
        return "jpg"
    if head.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if head[:4] == b"RIFF" and head[8:12] == b"WEBP":
        return "webp"
    return None


@app.context_processor
def inject():
    reg = region()
    return dict(t=t, region=reg, regions=REGIONS, currency=REGIONS[reg]["currency"], games=db.GAMES,
                site_name=config.SITE_NAME, support=config.SUPPORT_CONTACT, csrf_token=csrf_token,
                fmt_price=fmt_price, is_open=is_open(), work_start=config.WORK_START, work_end=config.WORK_END)


@app.after_request
def security_headers(resp):
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["X-Frame-Options"] = "DENY"
    resp.headers["Referrer-Policy"] = "same-origin"
    return resp


# ---------- Mijoz sahifalari ----------

@app.route("/")
def index():
    reg = region()
    min_prices = {}
    for g in db.GAMES:
        pk = db.packages(g)
        min_prices[g] = min((price_for(p, reg) for p in pk), default=None)
    return render_template("index.html", min_prices=min_prices)


@app.route("/lang/<reg>")
def set_lang(reg):
    if reg in REGIONS:
        session["region"] = reg
    nxt = request.args.get("next", "/")
    return redirect(nxt if nxt.startswith("/") and not nxt.startswith("//") else "/")


@app.route("/game/<game>", methods=["GET", "POST"])
def game_page(game):
    if game not in db.GAMES:
        abort(404)
    reg = region()
    pkgs = db.packages(game)
    errors, form = {}, {}
    if request.method == "POST":
        form = request.form
        if not check_csrf():
            errors["form"] = t("err_form")
        lo, hi = db.GAMES[game]["id_len"]
        player_id = re.sub(r"\s+", "", form.get("player_id", ""))
        if not re.fullmatch(rf"\d{{{lo},{hi}}}", player_id):
            errors["player_id"] = t("err_id", min=lo, max=hi)
        pkg = db.get_package(form.get("package", "0") if form.get("package", "").isdigit() else 0)
        if not pkg or pkg["game"] != game or not pkg["active"]:
            errors["package"] = t("err_pack")
        file = request.files.get("receipt")
        kind = None
        if file and file.filename:
            head = file.stream.read(16)
            file.stream.seek(0, os.SEEK_END)
            size = file.stream.tell()
            file.stream.seek(0)
            kind = image_kind(head) if size <= config.MAX_UPLOAD_MB * 1024 * 1024 else None
        if not kind:
            errors["receipt"] = t("err_receipt")
        if not errors:
            fname = f"{uuid.uuid4().hex}.{kind}"
            file.save(os.path.join(config.UPLOAD_DIR, fname))
            contact = form.get("contact", "").strip()[:64]
            code = db.create_order(game, pkg["label"], player_id, reg, price_for(pkg, reg),
                                   REGIONS[reg]["currency"], contact, fname)
            session.setdefault("my_orders", [])
            session["my_orders"] = ([code] + session["my_orders"])[:10]
            return redirect(url_for("order_page", code=code, new=1))
    payment = (config.PAYMENT_UZ if reg == "uz" else config.PAYMENT_TJ).split("|")
    return render_template("game.html", game=game, g=db.GAMES[game], pkgs=pkgs, price_for=price_for,
                           payment=[p.strip() for p in payment if p.strip()], errors=errors, form=form)


@app.route("/order/<code>")
def order_page(code):
    order = db.get_order(code)
    if not order:
        return render_template("check.html", not_found=True, code=code), 404
    return render_template("order.html", o=order, new=request.args.get("new"))


@app.route("/api/order/<code>")
def order_api(code):
    order = db.get_order(code)
    if not order:
        return jsonify(error="not_found"), 404
    return jsonify(status=order["status"])


@app.route("/check")
def check():
    code = request.args.get("code", "").strip().upper()
    if code:
        if not code.startswith("DG-"):
            code = "DG-" + code
        if db.get_order(code):
            return redirect(url_for("order_page", code=code))
        return render_template("check.html", not_found=True, code=code), 404
    return render_template("check.html", my_orders=session.get("my_orders", []))


@app.errorhandler(413)
def too_large(_):
    flash(t("err_receipt"))
    return redirect(request.path)


# ---------- Admin panel ----------

_fails = {}  # IP -> (urinishlar soni, blok tugash vaqti)


def admin_required(view):
    @wraps(view)
    def wrapper(*a, **kw):
        if not session.get("admin"):
            return redirect(url_for("admin_login"))
        return view(*a, **kw)
    return wrapper


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    error = None
    if request.method == "POST":
        ip = request.remote_addr or "?"
        fails, until = _fails.get(ip, (0, 0))
        if until > time.time():
            error = "Ko'p marta xato kiritildi. 5 daqiqadan keyin urinib ko'ring."
        elif not config.ADMIN_PASSWORD:
            error = ".env faylida ADMIN_PASSWORD yozilmagan."
        elif check_csrf() and hmac.compare_digest(request.form.get("password", ""), config.ADMIN_PASSWORD):
            _fails.pop(ip, None)
            session.clear()
            session["admin"] = True
            session.permanent = True
            return redirect(url_for("admin_orders"))
        else:
            fails += 1
            _fails[ip] = (fails, time.time() + 300 if fails >= 5 else 0)
            error = "Parol noto'g'ri."
    return render_template("admin/login.html", error=error)


@app.route("/admin/logout", methods=["POST"])
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("admin_login"))


@app.route("/admin")
@admin_required
def admin_orders():
    status = request.args.get("status", "pending")
    orders = db.list_orders(None if status == "all" else status)
    return render_template("admin/orders.html", orders=orders, status=status, counts=db.counts(),
                           revenue=db.revenue_today())


@app.route("/admin/api/pending")
@admin_required
def admin_pending():
    return jsonify(pending=db.counts()["pending"])


@app.route("/admin/order/<code>", methods=["GET", "POST"])
@admin_required
def admin_order(code):
    order = db.get_order(code)
    if not order:
        abort(404)
    if request.method == "POST" and check_csrf():
        action = request.form.get("action")
        if action in ("done", "rejected", "pending"):
            db.set_status(code, action, request.form.get("note", "").strip()[:300])
            flash({"done": "Bajarildi deb belgilandi.", "rejected": "Rad etildi.",
                   "pending": "Qayta tekshiruvga qaytarildi."}[action])
            nxt = db.list_orders("pending", limit=1)
            if action != "pending" and nxt:
                return redirect(url_for("admin_order", code=nxt[0]["code"]))
            return redirect(url_for("admin_orders"))
    return render_template("admin/order.html", o=order, counts=db.counts())


@app.route("/admin/receipt/<name>")
@admin_required
def admin_receipt(name):
    if not re.fullmatch(r"[0-9a-f]{32}\.(jpg|png|webp)", name):
        abort(404)
    return send_from_directory(config.UPLOAD_DIR, name)


@app.route("/admin/packages", methods=["GET", "POST"])
@admin_required
def admin_packages():
    if request.method == "POST" and check_csrf():
        for p in db.all_packages():
            pid = p["id"]
            try:
                uzs = int(request.form.get(f"uzs_{pid}", p["price_uzs"]))
                tjs = int(request.form.get(f"tjs_{pid}", p["price_tjs"]))
            except ValueError:
                continue
            db.update_package(pid, max(uzs, 0), max(tjs, 0), request.form.get(f"active_{pid}") == "1")
        flash("Narxlar saqlandi.")
        return redirect(url_for("admin_packages"))
    return render_template("admin/packages.html", pkgs=db.all_packages(), counts=db.counts())


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG") == "1", host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
