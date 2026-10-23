"""Tarjimalar: uz — o'zbekcha (so'm), tj — tojikcha (somoni).
Yangi matn qo'shsangiz, ikkala tilga ham yozing."""

REGIONS = {
    "uz": {"label": "O'zbekcha", "short": "UZ", "currency": "somon", "html_lang": "uz"},
    "tj": {"label": "Тоҷикӣ", "short": "TJ", "currency": "сомонӣ", "html_lang": "tg"},
}

T = {
    "tagline": {
        "uz": "Free Fire va PUBG Mobile uchun donat",
        "tj": "Донат барои Free Fire ва PUBG Mobile"},
    "hero_title": {
        "uz": "Olmos va UC to'g'ridan-to'g'ri akkauntingizga",
        "tj": "Алмос ва UC мустақиман ба аккаунти шумо"},
    "hero_text": {
        "uz": "Parol kerak emas — faqat o'yindagi ID. Paketni tanlang, kartaga to'lang va chek rasmini yuklang.",
        "tj": "Парол лозим нест — танҳо ID дар бозӣ. Бастаро интихоб кунед, ба корт пардохт кунед ва акси чекро бор кунед."},
    "open_now": {
        "uz": "Hozir ishlayapmiz: buyurtmalar {start}:00–{end}:00 da bajariladi",
        "tj": "Ҳозир кор мекунем: фармоишҳо соати {start}:00–{end}:00 иҷро мешаванд"},
    "closed_now": {
        "uz": "Hozir dam olyapmiz. Buyurtma qoldiring — {start}:00 dan bajaramiz",
        "tj": "Ҳозир истироҳат дорем. Фармоиш гузоред — аз соати {start}:00 иҷро мекунем"},
    "choose_game": {"uz": "O'yinni tanlang", "tj": "Бозиро интихоб кунед"},
    "from_price": {"uz": "{price} dan", "tj": "аз {price}"},
    "ff_desc": {"uz": "Olmoslar (💎)", "tj": "Алмосҳо (💎)"},
    "pubg_desc": {"uz": "Unknown Cash (UC)", "tj": "Unknown Cash (UC)"},
    "check_order": {"uz": "Buyurtma holati", "tj": "Ҳолати фармоиш"},
    "how_title": {"uz": "Qanday ishlaydi", "tj": "Чӣ тавр кор мекунад"},
    "step1": {"uz": "O'yin va paketni tanlang", "tj": "Бозӣ ва бастаро интихоб кунед"},
    "step2": {"uz": "O'yindagi ID ingizni yozing", "tj": "ID-и худро дар бозӣ нависед"},
    "step3": {"uz": "Kartaga to'lab, chek rasmini yuklang", "tj": "Ба корт пардохт карда, акси чекро бор кунед"},
    "step4": {"uz": "Admin tekshiradi va donatni tushiradi", "tj": "Админ месанҷад ва донатро мегузаронад"},
    "faq_title": {"uz": "Ko'p so'raladigan savollar", "tj": "Саволҳои маъмул"},
    "faq": {
        "uz": [("Qancha vaqtda tushadi?", "Ish vaqtida odatda 5–30 daqiqada. Ish vaqtidan tashqari buyurtmalar keyingi ish vaqtida bajariladi."),
               ("ID ni qayerdan topaman?", "O'yinda profilingizni oching — ID ismingiz ostida turadi. Uni nusxalab shu yerga qo'ying."),
               ("Akkaunt parolim kerakmi?", "Yo'q. Faqat ID kerak. Parolingizni hech kimga bermang."),
               ("ID ni xato yozsam-chi?", "Buyurtma hali bajarilmagan bo'lsa, buyurtma kodi bilan yordamga yozing — tuzatamiz.")],
        "tj": [("Дар кадом муддат мерасад?", "Дар вақти корӣ одатан 5–30 дақиқа. Фармоишҳои берун аз вақти корӣ дар вақти кории навбатӣ иҷро мешаванд."),
               ("ID-ро аз куҷо ёбам?", "Дар бозӣ профили худро кушоед — ID дар зери номатон аст. Онро нусха гирифта, ин ҷо гузоред."),
               ("Пароли аккаунт лозим аст?", "Не. Танҳо ID лозим аст. Пароли худро ба касе надиҳед."),
               ("Агар ID-ро хато нависам?", "Агар фармоиш ҳоло иҷро нашуда бошад, бо рамзи фармоиш ба ёрӣ нависед — ислоҳ мекунем.")]},
    # O'yin sahifasi
    "player_id": {"uz": "O'yindagi ID", "tj": "ID дар бозӣ"},
    "player_id_hint": {"uz": "Profil sahifasida, ismingiz ostida. Faqat raqamlar.", "tj": "Дар саҳифаи профил, дар зери номатон. Танҳо рақамҳо."},
    "choose_pack": {"uz": "Paketni tanlang", "tj": "Бастаро интихоб кунед"},
    "payment": {"uz": "To'lov", "tj": "Пардохт"},
    "pay_text": {"uz": "Quyidagi kartaga {amount} o'tkazing:", "tj": "{amount}-ро ба корти зерин гузаронед:"},
    "pay_choose_first": {"uz": "Avval paketni tanlang — summa shu yerda chiqadi.", "tj": "Аввал бастаро интихоб кунед — маблағ дар ин ҷо пайдо мешавад."},
    "copy": {"uz": "Nusxalash", "tj": "Нусха гирифтан"},
    "copied": {"uz": "Nusxalandi", "tj": "Нусха гирифта шуд"},
    "receipt": {"uz": "Chek rasmi", "tj": "Акси чек"},
    "receipt_hint": {"uz": "To'lovdan keyingi skrinshot. JPG, PNG yoki WEBP, 5 MB gacha.", "tj": "Скриншот пас аз пардохт. JPG, PNG ё WEBP, то 5 MB."},
    "choose_file": {"uz": "Rasm tanlash", "tj": "Интихоби акс"},
    "contact": {"uz": "Telefon yoki Telegram", "tj": "Телефон ё Telegram"},
    "optional": {"uz": "ixtiyoriy", "tj": "ихтиёрӣ"},
    "contact_hint": {"uz": "Muammo bo'lsa siz bilan bog'lanishimiz uchun.", "tj": "Барои он ки ҳангоми мушкилот бо шумо тамос гирем."},
    "total": {"uz": "Jami", "tj": "Ҳамагӣ"},
    "place_order": {"uz": "Buyurtma berish", "tj": "Фармоиш додан"},
    "back": {"uz": "Orqaga", "tj": "Бозгашт"},
    # Xatolar
    "err_id": {"uz": "ID faqat raqamlardan iborat bo'lishi kerak ({min}–{max} ta).", "tj": "ID бояд танҳо аз рақамҳо иборат бошад ({min}–{max} адад)."},
    "err_pack": {"uz": "Paketni tanlang.", "tj": "Бастаро интихоб кунед."},
    "err_receipt": {"uz": "Chek rasmini yuklang: JPG, PNG yoki WEBP, 5 MB gacha.", "tj": "Акси чекро бор кунед: JPG, PNG ё WEBP, то 5 MB."},
    "err_form": {"uz": "Sahifa eskirdi. Qaytadan urinib ko'ring.", "tj": "Саҳифа кӯҳна шуд. Аз нав кӯшиш кунед."},
    # Buyurtma holati
    "order_received": {"uz": "Buyurtma qabul qilindi", "tj": "Фармоиш қабул шуд"},
    "save_code": {"uz": "Bu kodni saqlab qo'ying — holatni shu kod bilan tekshirasiz.", "tj": "Ин рамзро нигоҳ доред — ҳолатро бо ҳамин рамз месанҷед."},
    "order": {"uz": "Buyurtma", "tj": "Фармоиш"},
    "status_pending": {"uz": "Tekshirilmoqda", "tj": "Санҷида мешавад"},
    "status_done": {"uz": "Bajarildi", "tj": "Иҷро шуд"},
    "status_rejected": {"uz": "Rad etildi", "tj": "Рад шуд"},
    "pending_text": {"uz": "Chekingiz tekshirilmoqda. Sahifa o'zi yangilanadi.", "tj": "Чеки шумо санҷида мешавад. Саҳифа худаш нав мешавад."},
    "done_text": {"uz": "{pack} akkauntingizga tushirildi. O'yinni qayta ochib tekshiring.", "tj": "{pack} ба аккаунти шумо гузаронида шуд. Бозиро аз нав кушода санҷед."},
    "rejected_text": {"uz": "Buyurtma bajarilmadi. Savollar bo'lsa, buyurtma kodi bilan yozing: {contact}", "tj": "Фармоиш иҷро нашуд. Агар савол бошад, бо рамзи фармоиш нависед: {contact}"},
    "admin_note": {"uz": "Admin izohi", "tj": "Эзоҳи админ"},
    "game": {"uz": "O'yin", "tj": "Бозӣ"},
    "pack": {"uz": "Paket", "tj": "Баста"},
    "price": {"uz": "Summa", "tj": "Маблағ"},
    "created": {"uz": "Vaqti", "tj": "Вақт"},
    "order_code": {"uz": "Buyurtma kodi", "tj": "Рамзи фармоиш"},
    "check": {"uz": "Tekshirish", "tj": "Санҷидан"},
    "not_found": {"uz": "Bu kod bilan buyurtma topilmadi. Kodni tekshirib, qaytadan kiriting.", "tj": "Фармоиш бо ин рамз ёфт нашуд. Рамзро санҷида, аз нав ворид кунед."},
    "new_order": {"uz": "Yana buyurtma berish", "tj": "Боз фармоиш додан"},
    "help": {"uz": "Yordam", "tj": "Ёрӣ"},
    "disclaimer": {
        "uz": "Sayt Garena, Krafton yoki Tencent bilan bog'liq emas. O'yin nomlari ularning egalariga tegishli.",
        "tj": "Сайт бо Garena, Krafton ё Tencent алоқаманд нест. Номҳои бозиҳо ба соҳибонашон тааллуқ доранд."},
}


def translate(key, region, **kw):
    item = T.get(key)
    if item is None:
        return key
    text = item.get(region) or item["uz"]
    return text.format(**kw) if kw and isinstance(text, str) else text
