"""
seed_data.py – Populate the Israeli WhatsApp deals-bot database with
comprehensive reference data: gift-card platforms, credit cards,
consumer clubs, stores, and the many-to-many deal relationships
between them.

Usage:
    python seed_data.py
"""

from database import get_db, init_db


GIFT_CARD_PLATFORMS = [
    ("BuyMe All (ביימי אול)", "כרטיס מתנה כללי – מתקבל בכל בתי העסק של BuyMe"),
    ("BuyMe Baby (ביימי בייבי)", "כרטיס מתנה לחנויות תינוקות וילדים"),
    ("BuyMe Restaurant (ביימי מסעדות)", "כרטיס מתנה למסעדות בלבד"),
    ("BuyMe Fashion (ביימי אופנה)", "כרטיס מתנה לחנויות אופנה"),
    ("BuyMe Home (ביימי בית)", "כרטיס מתנה לבית וריהוט"),
    ("BuyMe Experience (ביימי חוויות)", "כרטיס מתנה לחוויות ופעילויות"),
    ("BuyMe Beauty (ביימי ביוטי)", "כרטיס מתנה ליופי וקוסמטיקה"),
    ("Tav Hazahav (תו הזהב)", "תו הזהב – כרטיס מתנה / מועדון צרכנות גדול"),
    ("Colu (קולו)", "ארנק דיגיטלי ומטבע מקומי"),
    ("Presto", "כרטיס מתנה פרסטו"),
    ("Lovecard", "כרטיס מתנה לאבקארד"),
    ("10bis / TenBis (תן ביס)", "כרטיס ארוחות למסעדות ומשלוחים"),
]

CREDIT_CARDS = [
    ("Cal Visa (כאל ויזה)", "Cal (כאל)", "כרטיס ויזה של חברת כאל"),
    ("Cal Mastercard", "Cal (כאל)", "כרטיס מאסטרקארד של חברת כאל"),
    ("Isracard (ישראכרט)", "Isracard", "כרטיס ישראכרט"),
    ("Max Visa (מקס)", "Max (לאומי קארד)", "כרטיס ויזה של מקס / לאומי קארד"),
    ("Max Mastercard", "Max (לאומי קארד)", "כרטיס מאסטרקארד של מקס"),
    ("Leumi Card (לאומי קארד)", "Bank Leumi (בנק לאומי)", "כרטיס לאומי קארד"),
    ("Diners Club", "Cal (כאל)", "כרטיס דיינרס קלאב – מופעל ע\"י כאל"),
    ("American Express Israel", "Isracard", "כרטיס אמריקן אקספרס ישראל – מופעל ע\"י ישראכרט"),
]

CONSUMER_CLUBS = [
    ("Tav Hazahav (תו הזהב)", "מועדון תו הזהב – הטבות לחברי המועדון ברשתות שונות"),
    ("Hever (חבר)", "מועדון חבר – עובדי מדינה, ביטחון והוראה"),
    ("Latet (לתת)", "מועדון לתת – הטבות למשפחות"),
    ("Hot Mobile Club", "מועדון לקוחות הוט מובייל"),
    ("Partner Club", "מועדון לקוחות פרטנר"),
    ("Pelephone Club", "מועדון לקוחות פלאפון"),
    ("Bezeq Club", "מועדון לקוחות בזק"),
    ("Cellcom Club", "מועדון לקוחות סלקום"),
    ("Students Club (מועדון סטודנטים)", "מועדון סטודנטים – הטבות לסטודנטים"),
    ("Dreamcard (דרימקארד)", "מועדון הטבות של קבוצת פוקס – 10% קאשבק, 30% הנחת יום הולדת ב-Fox, American Eagle, Mango, Foot Locker, Laline ועוד"),
]

STORES = [
    # --- Restaurants ---
    ("Tokyo Nei (טוקיו ניי)", "restaurants", "tyoto nei,tokyo nei,tyoto,טוקיו ניי,טוקיו"),
    ("Oshi Oshi (אושי אושי)", "restaurants", "oshi oshi,אושי אושי,אושי"),
    ("Shipudei Hatikva (שיפודי התקווה)", "restaurants", "shipudei hatikva,שיפודי התקווה,שיפודי,shipudei"),
    ("Greg Cafe (גרג קפה)", "restaurants", "greg,greg cafe,גרג,גרג קפה"),
    ("Cafe Cafe (קפה קפה)", "restaurants", "cafe cafe,קפה קפה,cafecafe"),
    ("Aroma (ארומה)", "restaurants", "aroma,ארומה,ארומה ישראל"),
    ("Landwer Cafe (לנדוור)", "restaurants", "landwer,לנדוור,לנדוור קפה,cafe landwer"),
    ("Japanika (ג'פניקה)", "restaurants", "japanika,ג'פניקה,japnika"),
    ("Benedict (בנדיקט)", "restaurants", "benedict,בנדיקט"),
    ("Moses (מוזס)", "restaurants", "moses,מוזס,מוזס בורגר"),
    ("Vitrina (ויטרינה)", "restaurants", "vitrina,ויטרינה"),
    ("Boya (בויה)", "restaurants", "boya,בויה"),
    ("12 Chairs (12 כסאות)", "restaurants", "12 chairs,12 כסאות,שתים עשרה כסאות"),
    ("BBB (בי בי בי)", "restaurants", "bbb,בי בי בי,burgersbar,בורגרס בר"),
    ("Humus Abu Hassan", "restaurants", "humus abu hassan,חומוס אבו חסן,abu hassan"),
    ("Cafe Neto", "restaurants", "cafe neto,קפה נטו,neto"),
    # --- Fashion / Clothing ---
    ("Castro (קסטרו)", "fashion", "castro,קסטרו"),
    ("Zara", "fashion", "zara,זארה"),
    ("H&M", "fashion", "h&m,hm,אייצ אנד אם"),
    ("Golf (גולף)", "fashion", "golf,גולף,golf&co"),
    ("Fox (פוקס)", "fashion", "fox,פוקס"),
    ("Renuar (רנואר)", "fashion", "renuar,רנואר"),
    ("Honigman (הוניגמן)", "fashion", "honigman,הוניגמן"),
    ("Mango", "fashion", "mango,מנגו"),
    ("Pull&Bear", "fashion", "pull&bear,pullandbear,פול אנד בר"),
    ("Bershka", "fashion", "bershka,ברשקה"),
    ("American Eagle", "fashion", "american eagle,אמריקן איגל,ae"),
    ("TNT", "fashion", "tnt,טי אן טי"),
    ("Billabong", "fashion", "billabong,בילבונג"),
    # --- Dreamcard / Fox Group Partner Brands ---
    ("Fox Home (פוקס הום)", "home_furniture", "fox home,פוקס הום,foxhome"),
    ("Aerie (אירי)", "fashion", "aerie,אירי"),
    ("Foot Locker (פוט לוקר)", "fashion", "foot locker,פוט לוקר,footlocker"),
    ("Laline (לליין)", "beauty_cosmetics", "laline,לליין"),
    ("The Children's Place", "baby_kids", "the children's place,דה צ'ילדרנס פלייס,childrens place"),
    ("Ruby Bay (רובי ביי)", "fashion", "ruby bay,רובי ביי"),
    ("Flying Tiger Copenhagen", "home_furniture", "flying tiger,פליינג טייגר,flying tiger copenhagen"),
    ("Sunglass Hut (סאנגלס האט)", "fashion", "sunglass hut,סאנגלס האט,sunglasshut"),
    ("Quiksilver (קוויקסילבר)", "fashion", "quiksilver,קוויקסילבר,quicksilver"),
    ("Itay Brands (איתי ברנדס)", "fashion", "itay brands,איתי ברנדס,itay"),
    ("Jumbo (ג'מבו)", "home_furniture", "jumbo,ג'מבו"),
    ("Terminal X (טרמינל X)", "fashion", "terminal x,טרמינל איקס,terminalx"),
    # --- Baby / Kids ---
    ("Shilav (שילב)", "baby_kids", "shilav,שילב"),
    ("Baby Place", "baby_kids", "baby place,בייבי פלייס"),
    ("Toys R Us Israel", "baby_kids", "toys r us,toysrus,טויס אר אס"),
    ("Bugaboo IL", "baby_kids", "bugaboo,בוגבו"),
    # --- Home & Furniture ---
    ("IKEA (איקאה)", "home_furniture", "ikea,איקאה,איקיאה"),
    ("Ace (אייס)", "home_furniture", "ace,אייס"),
    ("Kitan (כיתן)", "home_furniture", "kitan,כיתן"),
    ("HomeCentre", "home_furniture", "homecentre,home centre,הום סנטר"),
    ("Super-Pharm Home", "home_furniture", "super-pharm home,סופר פארם בית"),
    # --- Beauty / Cosmetics ---
    ("Super-Pharm (סופר-פארם)", "beauty_cosmetics", "super-pharm,סופר-פארם,סופר פארם,superpharm"),
    ("Be (בי פארם)", "beauty_cosmetics", "be,בי,בי פארם,be pharm"),
    ("MAC", "beauty_cosmetics", "mac,מאק"),
    ("Sephora", "beauty_cosmetics", "sephora,ספורה"),
    ("The Body Shop", "beauty_cosmetics", "the body shop,בודי שופ,body shop"),
    # --- Electronics ---
    ("KSP (קיי.אס.פי)", "electronics", "ksp,קיי.אס.פי,קיי אס פי"),
    ("Bug (באג)", "electronics", "bug,באג"),
    ("Ivory (אייבורי)", "electronics", "ivory,אייבורי"),
    ("iDigital (איי דיגיטל)", "electronics", "idigital,איי דיגיטל,אייdigital"),
    # --- Supermarkets ---
    ("Shufersal (שופרסל)", "supermarket", "shufersal,שופרסל,שופר-סל"),
    ("Rami Levy (רמי לוי)", "supermarket", "rami levy,רמי לוי"),
    ("Victory (ויקטורי)", "supermarket", "victory,ויקטורי"),
    ("Yochananof (יוחננוף)", "supermarket", "yochananof,יוחננוף"),
]

STORE_GIFT_CARDS = {
    "Tokyo Nei (טוקיו ניי)": [
        ("BuyMe Restaurant (ביימי מסעדות)", "ניתן לשלם עד מלוא הסכום"),
        ("BuyMe All (ביימי אול)", ""),
        ("10bis / TenBis (תן ביס)", "הזמנה דרך האפליקציה"),
    ],
    "Oshi Oshi (אושי אושי)": [
        ("BuyMe Restaurant (ביימי מסעדות)", ""),
        ("BuyMe All (ביימי אול)", ""),
        ("10bis / TenBis (תן ביס)", ""),
        ("Colu (קולו)", "בסניפים נבחרים"),
    ],
    "Shipudei Hatikva (שיפודי התקווה)": [
        ("BuyMe Restaurant (ביימי מסעדות)", ""),
        ("BuyMe All (ביימי אול)", ""),
    ],
    "Greg Cafe (גרג קפה)": [
        ("BuyMe Restaurant (ביימי מסעדות)", ""),
        ("BuyMe All (ביימי אול)", ""),
        ("10bis / TenBis (תן ביס)", ""),
        ("Colu (קולו)", ""),
    ],
    "Cafe Cafe (קפה קפה)": [
        ("BuyMe Restaurant (ביימי מסעדות)", ""),
        ("BuyMe All (ביימי אול)", ""),
        ("10bis / TenBis (תן ביס)", ""),
    ],
    "Aroma (ארומה)": [
        ("BuyMe Restaurant (ביימי מסעדות)", ""),
        ("BuyMe All (ביימי אול)", ""),
        ("10bis / TenBis (תן ביס)", ""),
        ("Colu (קולו)", "בסניפים נבחרים"),
    ],
    "Landwer Cafe (לנדוור)": [
        ("BuyMe Restaurant (ביימי מסעדות)", ""),
        ("BuyMe All (ביימי אול)", ""),
        ("10bis / TenBis (תן ביס)", ""),
    ],
    "Japanika (ג'פניקה)": [
        ("BuyMe Restaurant (ביימי מסעדות)", ""),
        ("BuyMe All (ביימי אול)", ""),
        ("10bis / TenBis (תן ביס)", ""),
    ],
    "Benedict (בנדיקט)": [
        ("BuyMe Restaurant (ביימי מסעדות)", ""),
        ("BuyMe All (ביימי אול)", ""),
        ("10bis / TenBis (תן ביס)", ""),
    ],
    "Moses (מוזס)": [
        ("BuyMe Restaurant (ביימי מסעדות)", ""),
        ("BuyMe All (ביימי אול)", ""),
    ],
    "Vitrina (ויטרינה)": [
        ("BuyMe Restaurant (ביימי מסעדות)", ""),
        ("BuyMe All (ביימי אול)", ""),
    ],
    "Boya (בויה)": [
        ("BuyMe Restaurant (ביימי מסעדות)", ""),
        ("BuyMe All (ביימי אול)", ""),
    ],
    "12 Chairs (12 כסאות)": [
        ("BuyMe Restaurant (ביימי מסעדות)", ""),
        ("BuyMe All (ביימי אול)", ""),
    ],
    "BBB (בי בי בי)": [
        ("BuyMe Restaurant (ביימי מסעדות)", ""),
        ("BuyMe All (ביימי אול)", ""),
        ("10bis / TenBis (תן ביס)", ""),
        ("Tav Hazahav (תו הזהב)", ""),
    ],
    "Humus Abu Hassan": [
        ("10bis / TenBis (תן ביס)", "בסניף יפו בלבד"),
    ],
    "Cafe Neto": [
        ("BuyMe Restaurant (ביימי מסעדות)", ""),
        ("BuyMe All (ביימי אול)", ""),
        ("10bis / TenBis (תן ביס)", ""),
    ],
    "Castro (קסטרו)": [
        ("BuyMe Fashion (ביימי אופנה)", ""),
        ("BuyMe All (ביימי אול)", ""),
        ("Tav Hazahav (תו הזהב)", "ניתן לשלם עד 50% מהסכום"),
    ],
    "Zara": [
        ("BuyMe Fashion (ביימי אופנה)", "בסניפים נבחרים"),
        ("BuyMe All (ביימי אול)", ""),
    ],
    "H&M": [
        ("BuyMe Fashion (ביימי אופנה)", ""),
        ("BuyMe All (ביימי אול)", ""),
    ],
    "Golf (גולף)": [
        ("BuyMe Fashion (ביימי אופנה)", ""),
        ("BuyMe All (ביימי אול)", ""),
        ("Tav Hazahav (תו הזהב)", ""),
    ],
    "Fox (פוקס)": [
        ("BuyMe Fashion (ביימי אופנה)", ""),
        ("BuyMe All (ביימי אול)", ""),
        ("Tav Hazahav (תו הזהב)", ""),
        ("Lovecard", ""),
    ],
    "Renuar (רנואר)": [
        ("BuyMe Fashion (ביימי אופנה)", ""),
        ("BuyMe All (ביימי אול)", ""),
        ("Tav Hazahav (תו הזהב)", ""),
    ],
    "Honigman (הוניגמן)": [
        ("BuyMe Fashion (ביימי אופנה)", ""),
        ("BuyMe All (ביימי אול)", ""),
        ("Tav Hazahav (תו הזהב)", ""),
    ],
    "Mango": [
        ("BuyMe Fashion (ביימי אופנה)", ""),
        ("BuyMe All (ביימי אול)", ""),
    ],
    "Pull&Bear": [
        ("BuyMe Fashion (ביימי אופנה)", ""),
        ("BuyMe All (ביימי אול)", ""),
    ],
    "Bershka": [
        ("BuyMe Fashion (ביימי אופנה)", ""),
        ("BuyMe All (ביימי אול)", ""),
    ],
    "American Eagle": [
        ("BuyMe Fashion (ביימי אופנה)", ""),
        ("BuyMe All (ביימי אול)", ""),
    ],
    "TNT": [
        ("BuyMe Fashion (ביימי אופנה)", ""),
        ("BuyMe All (ביימי אול)", ""),
    ],
    "Billabong": [
        ("BuyMe Fashion (ביימי אופנה)", ""),
        ("BuyMe All (ביימי אול)", ""),
    ],
    "Shilav (שילב)": [
        ("BuyMe Baby (ביימי בייבי)", ""),
        ("BuyMe All (ביימי אול)", ""),
        ("Tav Hazahav (תו הזהב)", ""),
    ],
    "Baby Place": [
        ("BuyMe Baby (ביימי בייבי)", ""),
        ("BuyMe All (ביימי אול)", ""),
    ],
    "Toys R Us Israel": [
        ("BuyMe Baby (ביימי בייבי)", ""),
        ("BuyMe All (ביימי אול)", ""),
    ],
    "Bugaboo IL": [
        ("BuyMe Baby (ביימי בייבי)", ""),
        ("BuyMe All (ביימי אול)", ""),
    ],
    "IKEA (איקאה)": [
        ("BuyMe Home (ביימי בית)", ""),
        ("BuyMe All (ביימי אול)", ""),
    ],
    "Ace (אייס)": [
        ("BuyMe Home (ביימי בית)", ""),
        ("BuyMe All (ביימי אול)", ""),
        ("Tav Hazahav (תו הזהב)", ""),
    ],
    "Kitan (כיתן)": [
        ("BuyMe Home (ביימי בית)", ""),
        ("BuyMe All (ביימי אול)", ""),
        ("Tav Hazahav (תו הזהב)", ""),
    ],
    "HomeCentre": [
        ("BuyMe Home (ביימי בית)", ""),
        ("BuyMe All (ביימי אול)", ""),
    ],
    "Super-Pharm Home": [
        ("BuyMe Home (ביימי בית)", ""),
        ("BuyMe All (ביימי אול)", ""),
    ],
    "Super-Pharm (סופר-פארם)": [
        ("BuyMe Beauty (ביימי ביוטי)", ""),
        ("BuyMe All (ביימי אול)", ""),
        ("Tav Hazahav (תו הזהב)", ""),
    ],
    "Be (בי פארם)": [
        ("BuyMe Beauty (ביימי ביוטי)", ""),
        ("BuyMe All (ביימי אול)", ""),
    ],
    "MAC": [
        ("BuyMe Beauty (ביימי ביוטי)", ""),
        ("BuyMe All (ביימי אול)", ""),
    ],
    "Sephora": [
        ("BuyMe Beauty (ביימי ביוטי)", ""),
        ("BuyMe All (ביימי אול)", ""),
    ],
    "The Body Shop": [
        ("BuyMe Beauty (ביימי ביוטי)", ""),
        ("BuyMe All (ביימי אול)", ""),
        ("Tav Hazahav (תו הזהב)", ""),
    ],
    "KSP (קיי.אס.פי)": [
        ("BuyMe All (ביימי אול)", ""),
    ],
    "Bug (באג)": [
        ("BuyMe All (ביימי אול)", ""),
    ],
    "Ivory (אייבורי)": [
        ("BuyMe All (ביימי אול)", ""),
    ],
    "iDigital (איי דיגיטל)": [
        ("BuyMe All (ביימי אול)", ""),
    ],
    "Shufersal (שופרסל)": [
        ("Colu (קולו)", "במסגרת קולו שכונתי"),
        ("Tav Hazahav (תו הזהב)", ""),
    ],
    "Rami Levy (רמי לוי)": [
        ("Presto", ""),
        ("Colu (קולו)", "בסניפים נבחרים"),
    ],
    "Victory (ויקטורי)": [
        ("Tav Hazahav (תו הזהב)", ""),
        ("Colu (קולו)", ""),
    ],
    "Yochananof (יוחננוף)": [
        ("Colu (קולו)", ""),
        ("Presto", "בסניפים נבחרים"),
    ],
}

STORE_CREDIT_CARD_DEALS = {
    "Tokyo Nei (טוקיו ניי)": [
        ("Cal Visa (כאל ויזה)", "15% הנחה בימי ראשון-חמישי"),
        ("Max Visa (מקס)", "10% הנחה בכל יום"),
    ],
    "Oshi Oshi (אושי אושי)": [
        ("Isracard (ישראכרט)", "10% הנחה על התפריט"),
        ("Cal Visa (כאל ויזה)", "1+1 על קוקטיילים בימי שלישי"),
    ],
    "Shipudei Hatikva (שיפודי התקווה)": [
        ("Diners Club", "10% הנחה"),
    ],
    "Greg Cafe (גרג קפה)": [
        ("Max Visa (מקס)", "10% הנחה על החשבון"),
        ("Leumi Card (לאומי קארד)", "1+1 על שתייה חמה"),
    ],
    "Cafe Cafe (קפה קפה)": [
        ("Cal Visa (כאל ויזה)", "10% הנחה"),
        ("Isracard (ישראכרט)", "מנה ראשונה חינם בהזמנת מנה עיקרית"),
    ],
    "Aroma (ארומה)": [
        ("Max Visa (מקס)", "5% הנחה קבועה"),
        ("Leumi Card (לאומי קארד)", "10% הנחה בימי שישי"),
    ],
    "Landwer Cafe (לנדוור)": [
        ("Cal Mastercard", "10% הנחה על התפריט"),
    ],
    "Japanika (ג'פניקה)": [
        ("Cal Visa (כאל ויזה)", "15% הנחה על סושי"),
        ("Max Mastercard", "10% הנחה"),
    ],
    "Benedict (בנדיקט)": [
        ("Isracard (ישראכרט)", "10% הנחה"),
        ("American Express Israel", "15% הנחה בימי חול"),
    ],
    "Moses (מוזס)": [
        ("Cal Visa (כאל ויזה)", "10% הנחה"),
    ],
    "Vitrina (ויטרינה)": [
        ("Max Visa (מקס)", "10% הנחה"),
    ],
    "Boya (בויה)": [
        ("Diners Club", "15% הנחה בימי ראשון-רביעי"),
    ],
    "12 Chairs (12 כסאות)": [
        ("American Express Israel", "10% הנחה"),
    ],
    "BBB (בי בי בי)": [
        ("Cal Visa (כאל ויזה)", "10% הנחה"),
        ("Max Visa (מקס)", "1+1 על המבורגר בימי שני"),
    ],
    "Cafe Neto": [
        ("Isracard (ישראכרט)", "5% הנחה"),
    ],
    "Castro (קסטרו)": [
        ("Cal Visa (כאל ויזה)", "20% הנחה על הקולקציה החדשה"),
        ("Max Visa (מקס)", "15% הנחה"),
        ("Isracard (ישראכרט)", "10% הנחה על פריט שני"),
    ],
    "Zara": [
        ("American Express Israel", "10% הנחה בסוף עונה"),
    ],
    "H&M": [
        ("Max Visa (מקס)", "10% הנחה"),
        ("Cal Visa (כאל ויזה)", "15% הנחה על קניה מעל 300 ₪"),
    ],
    "Golf (גולף)": [
        ("Cal Visa (כאל ויזה)", "15% הנחה"),
        ("Leumi Card (לאומי קארד)", "10% הנחה"),
    ],
    "Fox (פוקס)": [
        ("Max Visa (מקס)", "20% הנחה על פריט שני"),
        ("Isracard (ישראכרט)", "15% הנחה"),
    ],
    "Renuar (רנואר)": [
        ("Cal Visa (כאל ויזה)", "15% הנחה"),
        ("Max Mastercard", "10% הנחה"),
    ],
    "Honigman (הוניגמן)": [
        ("Cal Visa (כאל ויזה)", "20% הנחה"),
        ("Leumi Card (לאומי קארד)", "15% הנחה"),
    ],
    "Mango": [
        ("American Express Israel", "10% הנחה"),
    ],
    "Pull&Bear": [
        ("Cal Visa (כאל ויזה)", "10% הנחה"),
    ],
    "Bershka": [
        ("Max Visa (מקס)", "10% הנחה"),
    ],
    "American Eagle": [
        ("Isracard (ישראכרט)", "15% הנחה"),
        ("Cal Visa (כאל ויזה)", "10% הנחה"),
    ],
    "TNT": [
        ("Cal Visa (כאל ויזה)", "10% הנחה"),
    ],
    "Billabong": [
        ("Max Visa (מקס)", "15% הנחה"),
    ],
    "Shilav (שילב)": [
        ("Cal Visa (כאל ויזה)", "10% הנחה"),
        ("Max Visa (מקס)", "5% הנחה נוספת על מבצעים"),
    ],
    "Baby Place": [
        ("Isracard (ישראכרט)", "10% הנחה"),
    ],
    "Toys R Us Israel": [
        ("Cal Visa (כאל ויזה)", "15% הנחה על צעצועים נבחרים"),
        ("Max Visa (מקס)", "10% הנחה"),
    ],
    "Bugaboo IL": [
        ("Leumi Card (לאומי קארד)", "5% הנחה + 12 תשלומים ללא ריבית"),
        ("American Express Israel", "10% הנחה"),
    ],
    "IKEA (איקאה)": [
        ("Leumi Card (לאומי קארד)", "10% הנחה לחברי Hever"),
        ("Cal Visa (כאל ויזה)", "עד 24 תשלומים ללא ריבית"),
        ("Max Visa (מקס)", "5% הנחה על ריהוט"),
    ],
    "Ace (אייס)": [
        ("Isracard (ישראכרט)", "10% הנחה על כלי עבודה"),
        ("Max Visa (מקס)", "12 תשלומים ללא ריבית"),
    ],
    "Kitan (כיתן)": [
        ("Cal Visa (כאל ויזה)", "15% הנחה"),
        ("Max Visa (מקס)", "10% הנחה"),
    ],
    "HomeCentre": [
        ("Leumi Card (לאומי קארד)", "10% הנחה"),
        ("Isracard (ישראכרט)", "12 תשלומים ללא ריבית"),
    ],
    "Super-Pharm Home": [
        ("Cal Visa (כאל ויזה)", "10% הנחה"),
    ],
    "Super-Pharm (סופר-פארם)": [
        ("Cal Visa (כאל ויזה)", "10% הנחה על מוצרי טיפוח"),
        ("Isracard (ישראכרט)", "1+1 על מוצרים נבחרים"),
        ("Max Visa (מקס)", "5% הנחה קבועה"),
    ],
    "Be (בי פארם)": [
        ("Max Visa (מקס)", "10% הנחה"),
        ("Cal Visa (כאל ויזה)", "15% הנחה על בשמים"),
    ],
    "MAC": [
        ("American Express Israel", "15% הנחה"),
        ("Diners Club", "10% הנחה"),
    ],
    "Sephora": [
        ("Cal Visa (כאל ויזה)", "10% הנחה"),
        ("Isracard (ישראכרט)", "15% הנחה על מותגים נבחרים"),
    ],
    "The Body Shop": [
        ("Max Visa (מקס)", "15% הנחה"),
        ("Cal Visa (כאל ויזה)", "10% הנחה"),
    ],
    "KSP (קיי.אס.פי)": [
        ("Cal Visa (כאל ויזה)", "עד 36 תשלומים ללא ריבית"),
        ("Max Visa (מקס)", "עד 24 תשלומים ללא ריבית"),
        ("Isracard (ישראכרט)", "5% הנחה על אביזרים"),
    ],
    "Bug (באג)": [
        ("Cal Visa (כאל ויזה)", "עד 24 תשלומים ללא ריבית"),
        ("Leumi Card (לאומי קארד)", "10% הנחה על אביזרים"),
    ],
    "Ivory (אייבורי)": [
        ("Max Visa (מקס)", "עד 18 תשלומים ללא ריבית"),
        ("Isracard (ישראכרט)", "5% הנחה"),
    ],
    "iDigital (איי דיגיטל)": [
        ("Cal Visa (כאל ויזה)", "עד 36 תשלומים ללא ריבית על מוצרי Apple"),
        ("American Express Israel", "10% הנחה על אביזרים"),
    ],
    "Shufersal (שופרסל)": [
        ("Isracard (ישראכרט)", "0.5% קאשבק"),
        ("Max Visa (מקס)", "הטענת ארנק דיגיטלי בהנחה"),
    ],
    "Rami Levy (רמי לוי)": [
        ("Cal Visa (כאל ויזה)", "1% קאשבק"),
    ],
    "Victory (ויקטורי)": [
        ("Leumi Card (לאומי קארד)", "הנחות שבועיות בלעדיות"),
    ],
    "Yochananof (יוחננוף)": [
        ("Isracard (ישראכרט)", "הנחות מועדון בלעדיות"),
    ],
}

STORE_CONSUMER_CLUB_DEALS = {
    "Tokyo Nei (טוקיו ניי)": [
        ("Hever (חבר)", "10% הנחה"),
        ("Students Club (מועדון סטודנטים)", "15% הנחה בימי ראשון-רביעי"),
    ],
    "Oshi Oshi (אושי אושי)": [
        ("Hever (חבר)", "10% הנחה"),
        ("Tav Hazahav (תו הזהב)", "10% הנחה"),
        ("Students Club (מועדון סטודנטים)", "10% הנחה"),
    ],
    "Shipudei Hatikva (שיפודי התקווה)": [
        ("Hever (חבר)", "10% הנחה"),
    ],
    "Greg Cafe (גרג קפה)": [
        ("Tav Hazahav (תו הזהב)", "10% הנחה"),
        ("Students Club (מועדון סטודנטים)", "15% הנחה + שתייה חמה חינם"),
    ],
    "Cafe Cafe (קפה קפה)": [
        ("Hever (חבר)", "10% הנחה"),
        ("Students Club (מועדון סטודנטים)", "10% הנחה"),
    ],
    "Aroma (ארומה)": [
        ("Students Club (מועדון סטודנטים)", "10% הנחה"),
        ("Tav Hazahav (תו הזהב)", "5% הנחה"),
        ("Cellcom Club", "10% הנחה בימי שלישי"),
    ],
    "Landwer Cafe (לנדוור)": [
        ("Hever (חבר)", "10% הנחה"),
        ("Students Club (מועדון סטודנטים)", "10% הנחה"),
    ],
    "Japanika (ג'פניקה)": [
        ("Students Club (מועדון סטודנטים)", "15% הנחה"),
        ("Hever (חבר)", "10% הנחה"),
    ],
    "Benedict (בנדיקט)": [
        ("Tav Hazahav (תו הזהב)", "10% הנחה"),
        ("Partner Club", "10% הנחה"),
    ],
    "Moses (מוזס)": [
        ("Hever (חבר)", "10% הנחה"),
        ("Students Club (מועדון סטודנטים)", "10% הנחה"),
    ],
    "Vitrina (ויטרינה)": [
        ("Students Club (מועדון סטודנטים)", "10% הנחה"),
    ],
    "Boya (בויה)": [
        ("Hot Mobile Club", "10% הנחה"),
    ],
    "12 Chairs (12 כסאות)": [
        ("Tav Hazahav (תו הזהב)", "10% הנחה"),
    ],
    "BBB (בי בי בי)": [
        ("Hever (חבר)", "10% הנחה"),
        ("Students Club (מועדון סטודנטים)", "15% הנחה + תוספת חינם"),
        ("Tav Hazahav (תו הזהב)", "10% הנחה"),
    ],
    "Humus Abu Hassan": [
        ("Students Club (מועדון סטודנטים)", "חומוס חצי חינם ברכישת מנה"),
    ],
    "Cafe Neto": [
        ("Hot Mobile Club", "10% הנחה"),
        ("Pelephone Club", "10% הנחה"),
    ],
    "Castro (קסטרו)": [
        ("Hever (חבר)", "10% הנחה"),
        ("Tav Hazahav (תו הזהב)", "15% הנחה"),
        ("Students Club (מועדון סטודנטים)", "10% הנחה"),
    ],
    "Zara": [
        ("Hever (חבר)", "5% הנחה על קולקציה חדשה"),
    ],
    "H&M": [
        ("Students Club (מועדון סטודנטים)", "10% הנחה"),
        ("Hever (חבר)", "10% הנחה"),
    ],
    "Golf (גולף)": [
        ("Tav Hazahav (תו הזהב)", "15% הנחה"),
        ("Hever (חבר)", "10% הנחה"),
        ("Partner Club", "10% הנחה"),
    ],
    "Renuar (רנואר)": [
        ("Tav Hazahav (תו הזהב)", "10% הנחה"),
        ("Hever (חבר)", "15% הנחה"),
    ],
    "Honigman (הוניגמן)": [
        ("Tav Hazahav (תו הזהב)", "15% הנחה"),
        ("Hever (חבר)", "10% הנחה"),
    ],
    "Pull&Bear": [
        ("Students Club (מועדון סטודנטים)", "10% הנחה"),
    ],
    "Bershka": [
        ("Students Club (מועדון סטודנטים)", "10% הנחה"),
    ],
    "TNT": [
        ("Students Club (מועדון סטודנטים)", "10% הנחה"),
    ],
    "Baby Place": [
        ("Hever (חבר)", "10% הנחה"),
        ("Latet (לתת)", "10% הנחה"),
    ],
    "Toys R Us Israel": [
        ("Tav Hazahav (תו הזהב)", "10% הנחה"),
        ("Hever (חבר)", "15% הנחה"),
        ("Students Club (מועדון סטודנטים)", "10% הנחה"),
    ],
    "Bugaboo IL": [
        ("Hever (חבר)", "5% הנחה + משלוח חינם"),
    ],
    "IKEA (איקאה)": [
        ("Hever (חבר)", "10% הנחה על ריהוט"),
        ("Tav Hazahav (תו הזהב)", "5% הנחה"),
        ("Bezeq Club", "10% הנחה על מוצרי חשמל לבית"),
    ],
    "Ace (אייס)": [
        ("Hever (חבר)", "10% הנחה"),
        ("Tav Hazahav (תו הזהב)", "10% הנחה"),
    ],
    "Kitan (כיתן)": [
        ("Tav Hazahav (תו הזהב)", "15% הנחה"),
        ("Hever (חבר)", "10% הנחה"),
    ],
    "HomeCentre": [
        ("Hever (חבר)", "10% הנחה"),
        ("Partner Club", "5% הנחה"),
    ],
    "Super-Pharm Home": [
        ("Hever (חבר)", "10% הנחה"),
    ],
    "Super-Pharm (סופר-פארם)": [
        ("Hever (חבר)", "1+1 על מוצרים נבחרים"),
        ("Tav Hazahav (תו הזהב)", "10% הנחה"),
        ("Students Club (מועדון סטודנטים)", "10% הנחה"),
        ("Hot Mobile Club", "10% הנחה על קוסמטיקה"),
    ],
    "Be (בי פארם)": [
        ("Students Club (מועדון סטודנטים)", "15% הנחה"),
        ("Hever (חבר)", "10% הנחה"),
    ],
    "MAC": [
        ("Hever (חבר)", "10% הנחה"),
    ],
    "Sephora": [
        ("Tav Hazahav (תו הזהב)", "10% הנחה"),
        ("Hever (חבר)", "10% הנחה"),
        ("Pelephone Club", "5% הנחה"),
    ],
    "The Body Shop": [
        ("Tav Hazahav (תו הזהב)", "15% הנחה"),
        ("Hever (חבר)", "10% הנחה"),
        ("Students Club (מועדון סטודנטים)", "10% הנחה"),
    ],
    "KSP (קיי.אס.פי)": [
        ("Hever (חבר)", "5% הנחה על אביזרים"),
        ("Students Club (מועדון סטודנטים)", "5% הנחה"),
        ("Partner Club", "עד 10% הנחה על מוצרים נבחרים"),
    ],
    "Bug (באג)": [
        ("Hever (חבר)", "5% הנחה"),
        ("Cellcom Club", "עד 10% הנחה"),
    ],
    "Ivory (אייבורי)": [
        ("Hever (חבר)", "5% הנחה"),
        ("Hot Mobile Club", "5% הנחה"),
    ],
    "iDigital (איי דיגיטל)": [
        ("Hever (חבר)", "5% הנחה על אביזרים"),
        ("Students Club (מועדון סטודנטים)", "10% הנחה על אביזרים"),
    ],
    "Shufersal (שופרסל)": [
        ("Hever (חבר)", "הנחות שבועיות בלעדיות"),
        ("Tav Hazahav (תו הזהב)", "5% הנחה"),
    ],
    "Rami Levy (רמי לוי)": [
        ("Hever (חבר)", "הנחות חודשיות בלעדיות"),
        ("Latet (לתת)", "5% הנחה"),
    ],
    "Victory (ויקטורי)": [
        ("Hever (חבר)", "הנחות שבועיות"),
        ("Tav Hazahav (תו הזהב)", "5% הנחה"),
    ],
    "Yochananof (יוחננוף)": [
        ("Hever (חבר)", "הנחות שבועיות"),
        ("Bezeq Club", "5% הנחה"),
    ],
    # --- Dreamcard (Fox Group) consumer club deals ---
    "Fox (פוקס)": [
        ("Tav Hazahav (תו הזהב)", "15% הנחה"),
        ("Hever (חבר)", "10% הנחה"),
        ("Cellcom Club", "10% הנחה"),
        ("Dreamcard (דרימקארד)", "10% קאשבק + 30% הנחת יום הולדת (עד 500 ₪)"),
    ],
    "Fox Home (פוקס הום)": [
        ("Dreamcard (דרימקארד)", "10% קאשבק + 30% הנחת יום הולדת (עד 500 ₪)"),
    ],
    "American Eagle": [
        ("Students Club (מועדון סטודנטים)", "15% הנחה"),
        ("Hever (חבר)", "10% הנחה"),
        ("Dreamcard (דרימקארד)", "10% קאשבק + 30% הנחת יום הולדת (עד 500 ₪)"),
    ],
    "Aerie (אירי)": [
        ("Dreamcard (דרימקארד)", "10% קאשבק + 30% הנחת יום הולדת (עד 500 ₪)"),
    ],
    "Mango": [
        ("Hever (חבר)", "5% הנחה"),
        ("Dreamcard (דרימקארד)", "10% קאשבק + 30% הנחת יום הולדת (עד 500 ₪)"),
    ],
    "Foot Locker (פוט לוקר)": [
        ("Dreamcard (דרימקארד)", "10% קאשבק + 30% הנחת יום הולדת (עד 500 ₪)"),
    ],
    "Laline (לליין)": [
        ("Dreamcard (דרימקארד)", "10% קאשבק + 30% הנחת יום הולדת (עד 500 ₪)"),
    ],
    "Billabong": [
        ("Hot Mobile Club", "10% הנחה"),
        ("Dreamcard (דרימקארד)", "10% קאשבק + 30% הנחת יום הולדת (עד 500 ₪)"),
    ],
    "The Children's Place": [
        ("Dreamcard (דרימקארד)", "10% קאשבק + 30% הנחת יום הולדת (עד 500 ₪)"),
    ],
    "Terminal X (טרמינל X)": [
        ("Dreamcard (דרימקארד)", "10% קאשבק + 30% הנחת יום הולדת (עד 500 ₪)"),
    ],
    "Ruby Bay (רובי ביי)": [
        ("Dreamcard (דרימקארד)", "10% קאשבק + 30% הנחת יום הולדת (עד 500 ₪)"),
    ],
    "Flying Tiger Copenhagen": [
        ("Dreamcard (דרימקארד)", "10% קאשבק + 30% הנחת יום הולדת (עד 500 ₪)"),
    ],
    "Sunglass Hut (סאנגלס האט)": [
        ("Dreamcard (דרימקארד)", "10% קאשבק + 30% הנחת יום הולדת (עד 500 ₪)"),
    ],
    "Quiksilver (קוויקסילבר)": [
        ("Dreamcard (דרימקארד)", "10% קאשבק + 30% הנחת יום הולדת (עד 500 ₪)"),
    ],
    "Shilav (שילב)": [
        ("Hever (חבר)", "10% הנחה"),
        ("Tav Hazahav (תו הזהב)", "10% הנחה"),
        ("Latet (לתת)", "15% הנחה על מוצרי תינוקות"),
        ("Dreamcard (דרימקארד)", "10% קאשבק + 30% הנחת יום הולדת (עד 500 ₪)"),
    ],
    "Itay Brands (איתי ברנדס)": [
        ("Dreamcard (דרימקארד)", "10% קאשבק + 30% הנחת יום הולדת (עד 500 ₪)"),
    ],
    "Jumbo (ג'מבו)": [
        ("Dreamcard (דרימקארד)", "10% קאשבק + 30% הנחת יום הולדת (עד 500 ₪)"),
    ],
}


def seed():
    """Seed the database with comprehensive Israeli deals data."""
    print("=" * 60)
    print("  WhatsApp Deals Bot - Database Seeder")
    print("=" * 60)

    init_db()
    print("\n[OK] Database schema initialised.")

    conn = get_db()
    cur = conn.cursor()

    tables_to_clear = [
        "store_consumer_club_deals",
        "store_credit_card_deals",
        "store_gift_cards",
        "stores",
        "consumer_clubs",
        "credit_cards",
        "gift_card_platforms",
    ]
    for tbl in tables_to_clear:
        cur.execute(f"DELETE FROM {tbl}")
    conn.commit()
    print("[OK] Cleared existing seed data.\n")

    gc_map = {}
    for name, desc in GIFT_CARD_PLATFORMS:
        cur.execute(
            "INSERT INTO gift_card_platforms (name, description) VALUES (?, ?)",
            (name, desc),
        )
        gc_map[name] = cur.lastrowid
    conn.commit()
    print(f"  Inserted {len(gc_map)} gift-card platforms.")

    cc_map = {}
    for name, bank, desc in CREDIT_CARDS:
        cur.execute(
            "INSERT INTO credit_cards (name, bank, description) VALUES (?, ?, ?)",
            (name, bank, desc),
        )
        cc_map[name] = cur.lastrowid
    conn.commit()
    print(f"  Inserted {len(cc_map)} credit cards.")

    club_map = {}
    for name, desc in CONSUMER_CLUBS:
        cur.execute(
            "INSERT INTO consumer_clubs (name, description) VALUES (?, ?)",
            (name, desc),
        )
        club_map[name] = cur.lastrowid
    conn.commit()
    print(f"  Inserted {len(club_map)} consumer clubs.")

    store_map = {}
    for name, category, aliases in STORES:
        cur.execute(
            "INSERT INTO stores (name, category, aliases) VALUES (?, ?, ?)",
            (name, category, aliases),
        )
        store_map[name] = cur.lastrowid
    conn.commit()
    print(f"  Inserted {len(store_map)} stores.")

    gc_link_count = 0
    for store_name, links in STORE_GIFT_CARDS.items():
        store_id = store_map[store_name]
        for gc_name, notes in links:
            cur.execute(
                "INSERT INTO store_gift_cards (store_id, gift_card_platform_id, notes) "
                "VALUES (?, ?, ?)",
                (store_id, gc_map[gc_name], notes),
            )
            gc_link_count += 1
    conn.commit()
    print(f"  Inserted {gc_link_count} store <-> gift-card links.")

    cc_link_count = 0
    for store_name, links in STORE_CREDIT_CARD_DEALS.items():
        store_id = store_map[store_name]
        for cc_name, discount in links:
            cur.execute(
                "INSERT INTO store_credit_card_deals (store_id, credit_card_id, discount_description) "
                "VALUES (?, ?, ?)",
                (store_id, cc_map[cc_name], discount),
            )
            cc_link_count += 1
    conn.commit()
    print(f"  Inserted {cc_link_count} store <-> credit-card deals.")

    club_link_count = 0
    for store_name, links in STORE_CONSUMER_CLUB_DEALS.items():
        store_id = store_map[store_name]
        for club_name, discount in links:
            cur.execute(
                "INSERT INTO store_consumer_club_deals (store_id, consumer_club_id, discount_description) "
                "VALUES (?, ?, ?)",
                (store_id, club_map[club_name], discount),
            )
            club_link_count += 1
    conn.commit()
    print(f"  Inserted {club_link_count} store <-> consumer-club deals.")

    conn.close()

    total_deals = gc_link_count + cc_link_count + club_link_count
    print("\n" + "=" * 60)
    print("  Seed Summary")
    print("=" * 60)
    print(f"  Gift-card platforms : {len(gc_map)}")
    print(f"  Credit cards        : {len(cc_map)}")
    print(f"  Consumer clubs      : {len(club_map)}")
    print(f"  Stores              : {len(store_map)}")
    print(f"  -----------------------------------")
    print(f"  Gift-card links     : {gc_link_count}")
    print(f"  Credit-card deals   : {cc_link_count}")
    print(f"  Club deals          : {club_link_count}")
    print(f"  -----------------------------------")
    print(f"  Total deal records  : {total_deals}")
    print("=" * 60)
    print("\n[OK] Seeding complete!")


if __name__ == "__main__":
    seed()
