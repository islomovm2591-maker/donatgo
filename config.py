import os
import secrets

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:  # python-dotenv o'rnatilmagan bo'lsa ham ishlaydi
    pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SITE_NAME = os.getenv("SITE_NAME", "DonatGo")
SECRET_KEY = os.getenv("SECRET_KEY") or secrets.token_hex(32)
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "")

# To'lov rekvizitlari: har bir davlat uchun alohida. Bir nechta karta bo'lsa "|" bilan ajrating.
PAYMENT_UZ = os.getenv("PAYMENT_UZ", "Humo: 9860 0000 0000 0000 (Ism F.)")
PAYMENT_TJ = os.getenv("PAYMENT_TJ", "Alif: 0000 0000 0000 0000 (Ism F.)")
SUPPORT_CONTACT = os.getenv("SUPPORT_CONTACT", "@islomog")

# Ish vaqti (soat) va vaqt mintaqasi (Toshkent va Dushanbe: UTC+5)
WORK_START = int(os.getenv("WORK_START", "18"))
WORK_END = int(os.getenv("WORK_END", "23"))
TZ_OFFSET = int(os.getenv("TZ_OFFSET", "5"))

DB_PATH = os.getenv("DB_PATH", os.path.join(BASE_DIR, "data.db"))
UPLOAD_DIR = os.getenv("UPLOAD_DIR", os.path.join(BASE_DIR, "uploads"))
MAX_UPLOAD_MB = 5
