# DonatGo — Free Fire va PUBG Mobile uchun donat sayti

Mobil o'yinlarga donat (top-up) qilish sayti. Python (Flask) va SQLite asosida yozilgan, o'zbek va tojik tillarida ishlaydi.

**Mijoz uchun jarayon:** o'yinni tanlaydi → ID ni kiritadi → paketni tanlaydi → kartaga to'laydi → chek rasmini yuklaydi → buyurtma kodini oladi va holatni kuzatadi.

**Admin uchun jarayon:** telefondan admin panelga kiradi → chekni ko'radi → ID ni bir bosishda nusxalaydi → donatni tushiradi → "Bajarildi" ni bosadi. Mijozning sahifasi o'zi yangilanadi.

## Imkoniyatlar

- Ikki til va ikki valyuta: o'zbekcha (so'm) va tojikcha (somoni)
- Ish vaqti ko'rsatkichi: ish vaqtidan tashqari mijozga buyurtma qachon bajarilishi aytiladi
- Buyurtma holatini kod orqali tekshirish (`DG-XXXXXX`), sahifa avtomatik yangilanadi
- Admin panel: buyurtmalar navbati, chek rasmi, bugungi tushum, narxlarni tahrirlash va paketlarni o'chirish
- Xavfsizlik: CSRF himoyasi, parolni taxmin qilishdan himoya (5 xato → 5 daqiqa blok), cheklar faqat adminga ko'rinadi, faqat haqiqiy rasm fayllari qabul qilinadi
- Telefon uchun moslashtirilgan dizayn

## Texnologiyalar

Python 3.10+, Flask, SQLite, Jinja2, HTML/CSS/JavaScript (frameworksiz)

## Ishga tushirish (VS Code)

1. Papkani VS Code'da oching: `File → Open Folder → donatgo`
2. Terminalni oching (`Ctrl + ~`):
   ```bash
   python -m venv venv
   venv\Scripts\activate          # Windows
   # source venv/bin/activate     # Mac / Linux
   pip install -r requirements.txt
   ```
3. `.env.example` faylidan nusxa olib, uni `.env` deb nomlang. Ichiga parol, karta raqamlari va ish vaqtini yozing.
4. Saytni ishga tushiring:
   ```bash
   python app.py
   ```
5. Brauzerda oching:
   - Sayt: http://127.0.0.1:5000
   - Admin panel: http://127.0.0.1:5000/admin

## Loyiha tuzilishi

```
donatgo/
├── app.py              # sahifalar va admin panel
├── db.py               # baza: paketlar, buyurtmalar
├── i18n.py             # o'zbekcha va tojikcha matnlar
├── config.py           # .env dan sozlamalar
├── templates/          # HTML shablonlar (admin/ — admin panel)
├── static/css, js, img
└── uploads/            # cheklar (GitHub'ga yuklanmaydi)
```

## Internetga joylash

Railway, Render yoki VPS'ga (Timeweb, Beget) joylash mumkin. Ishga tushirish buyrug'i:
```bash
gunicorn -w 2 -b 0.0.0.0:$PORT app:app
```
`.env` dagi o'zgaruvchilarni hosting sozlamalariga kiriting. `data.db` va `uploads/` papkasi doimiy diskda saqlanishi kerak.

## Keyingi rejalar

- Click, Payme yoki Alif orqali avtomatik to'lov
- Ulgurji top-up servisining API'si orqali donatni avtomatik tushirish
- Yangi buyurtma haqida email orqali xabar

---
Sayt Garena, Krafton yoki Tencent bilan bog'liq emas. O'yin nomlari ularning egalariga tegishli.
