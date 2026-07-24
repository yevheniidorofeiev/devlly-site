# -*- coding: utf-8 -*-
import io, json, os, re, sys

# Пути вычисляются относительно этого файла: tools/ внутри репозитория.
# ROOT    = корень репо (на уровень выше tools/)
# SCRATCH = tools/articles/ — источники статей art_<slug>.json
_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get('DEVLLY_ROOT', os.path.dirname(_HERE))
SCRATCH = os.environ.get('DEVLLY_ARTICLES', os.path.join(_HERE, 'articles'))
BASE = 'https://devlly.dev'
OGIMG = BASE + '/assets/images/thumbs/feature-three-thumb.png'
EMAIL = 'devlly.official@gmail.com'
TG = 'https://t.me/devllydev'
PILL = 'fw-medium text-heading text-uppercase border border-neutral-200 tw-py-1 tw-px-7 tw-rounded-md hover-bg-main-two-600 hover-text-white hover-border-main-two-600 cursor-small'
BTN = 'tw-hover-btn bg-main-two-600 text-white justify-content-center text-capitalize cursor-small fw-semibold tw-py-4 tw-px-8 d-inline-flex align-items-center tw-gap-3 hover-text-white hover-border-main-600 tw-rounded-xl'
BTN2 = 'tw-hover-btn bg-black text-white justify-content-center text-capitalize cursor-small fw-semibold tw-py-4 tw-px-8 d-inline-flex align-items-center tw-gap-3 hover-text-white tw-rounded-xl'

SLUGS = ['crm-or-sheets','telegram-bot-saves-time','crm-vs-erp','what-to-automate-first',
         'telegram-mini-app','data-parsing','ai-bot-requests','automate-or-lose-money']

# --- 20 нишевых статей (SEO берётся из самих json: ключ "seo") ---
NEW = ['telegram-bot-salon','telegram-bot-delivery','telegram-bot-fitness','telegram-bot-realty',
       'telegram-bot-shop','telegram-bot-dental','mini-app-shop','mini-app-taxi','mini-app-booking',
       'crm-realty','crm-salon','crm-construction','crm-legal','hr-automation','shop-automation',
       'accounting-automation','support-automation','ai-chatbot-shop','price-parsing','b2b-leads']
SLUGS = SLUGS + NEW

# --- 9 статей: HR-автоматизація + юридичні CRM + обробка заявок (SEO внутри json) ---
NEW3 = ['hr-telegram-recruitment','hr-bot-small-business','hr-onboarding-automation',
        'hr-telegram-form','hr-crm-vs-sheets','crm-dlya-yuristov','crm-dlya-yuridychnykh-kompaniy',
        'avtomatizaciya-zayavok','obrobka-zayavok-klientiv']
SLUGS = SLUGS + NEW3

# --- 8 статей із пошукових запитів (SEO внутри json) ---
NEW4 = ['crm-dlya-yuridychnoi-firmy','crm-salon-krasoty','hr-bot','proektna-crm',
        'chatbot-prodazhi','boty-buhgalteriya','vedennya-bazy-klientiv','baza-klientiv']
SLUGS = SLUGS + NEW4

# --- 5 порівняльних статей (SEO внутри json) ---
NEW5 = ['crm-vs-excel','telegram-bot-vs-mobile-app','saas-vs-custom-crm',
        'crm-vs-google-sheets','crm-vs-trello']
SLUGS = SLUGS + NEW5

# --- 6 таргетованих статей: юристи / салони / HR (SEO внутри json) ---
NEW6 = ['crm-yuridychna-firma-vprovadzhennya','crm-dlya-advokata',
        'salon-krasoty-telegram-zapis','salon-krasoty-nagaduvannya',
        'hr-bot-telegram-nalashtuvannya','hr-bot-functions']
SLUGS = SLUGS + NEW6

# --- 18 нішевих статей: салони / HR / магазин / дропшипінг / кавʼярня / ресторан / нерухомість / клініка / база (SEO внутри json) ---
NEW7 = ['programa-dlya-salonu-krasy','programy-dlya-saloniv-krasy',
        'hr-systema-dlya-malogo-biznesu','avtomatyzatsiya-recruiting',
        'avtomatyzatsiya-internet-magazyn-odyagu','crm-dlya-internet-magazynu',
        'avtomatyzatsiya-dropshipping','telegram-bot-dropshipping',
        'avtomatyzatsiya-kaviarni','crm-dlya-kaviarni','telegram-bot-kaviarnya',
        'avtomatyzatsiya-restoranu','telegram-bot-dostavka-yizhi',
        'crm-dlya-rieltoriva','telegram-bot-nerukhomist',
        'crm-dlya-kliniky','telegram-bot-klinika','spreadsheets-to-crm']
SLUGS = SLUGS + NEW7

# --- 4 статті про обробку заявок (SEO внутри json) ---
NEW8 = ['obrobka-zayavok','pryom-zayavok-vid-klientiv',
        'avtomatyzatsiya-zayavok','crm-dlya-obrobky-zayavok']
SLUGS = SLUGS + NEW8

# --- 6 нішевих статей: фітнес / склад / туризм / логістика / автосервіс / страхування (SEO внутри json) ---
NEW9 = ['crm-dlya-fitnes-klubu','avtomatyzatsiya-skladu','crm-dlya-turagentstva',
        'avtomatyzatsiya-lohistyky','telegram-bot-avtoservis','crm-dlya-strakhovoyi']
SLUGS = SLUGS + NEW9

# --- 13 статей під українську діаспору в ЄС (SEO внутри json) ---
NEW10 = ['telegram-bot-dlya-ukraintsiv-v-yevropi','avtomatyzatsiya-biznesu-za-kordonom',
         'viddalene-upravlinnya-biznesom-z-ukrainy','crm-dlya-ukrainskoi-diaspory',
         'crm-dlya-biznesu-v-polshchi','avtomatyzatsiya-ukrainskogo-biznesu-v-nimechchyni',
         'telegram-bot-zamovlennya-z-polshchi','crm-ukrainskyi-biznes-chehiya',
         'relokatsiya-biznesu-bez-vtraty-klientiv','dropshipping-z-polshchi-v-ukrainu',
         'komanda-za-kordonom-avtomatyzatsiya','eksport-v-yevropu-crm',
         'viddalenyi-internet-magazyn-z-ukrainy']
SLUGS = SLUGS + NEW10

# --- 1 стаття: кальянна (SEO внутри json) ---
NEW11 = ['avtomatyzatsiya-kalyanoi']
SLUGS = SLUGS + NEW11

SEO = {
'crm-or-sheets':{'t':'CRM чи таблиці: коли бізнесу потрібна власна система | Devlly','te':'CRM or spreadsheets: when a business needs its own system | Devlly',
 'd':'Розбираємо коли Google Таблиці вже гальмують бізнес і коли час переходити на CRM. Чіткі ознаки і практичні поради.','de':"We break down when Google Sheets start slowing your business down and when it's time to move to a CRM. Clear signs and practical tips.",
 'k':'CRM, Google Таблиці, коли потрібна CRM, власна CRM система, автоматизація бізнесу'},
'telegram-bot-saves-time':{'t':'Як Telegram-бот економить години роботи менеджерів | Devlly','te':"How a Telegram bot saves hours of managers' work | Devlly",
 'd':'Реальний приклад як автоматизація через Telegram-бота замінила 3 години ручної роботи на 10 хвилин щодня.','de':'A real example of how automation via a Telegram bot replaced 3 hours of manual work with 10 minutes a day.',
 'k':'Telegram-бот, автоматизація бізнесу, бот для заявок, економія часу, чат-бот'},
'crm-vs-erp':{'t':'ERP і CRM: у чому різниця і що обрати для свого бізнесу','te':'ERP vs CRM: Key Differences and How to Choose for Your Business',
 'd':'Пояснюємо різницю між ERP і CRM простими словами. Коли достатньо CRM, а коли потрібна повноцінна ERP система. Практичний гайд для власників бізнесу.','de':'We explain the difference between ERP and CRM in plain language. When CRM is enough and when you need a full ERP system. Practical guide for business owners.',
 'k':'CRM, ERP, різниця CRM і ERP, CRM чи ERP, система для бізнесу'},
'what-to-automate-first':{'t':'5 процесів які варто автоматизувати першими у бізнесі | Devlly','te':'5 processes worth automating first in your business | Devlly',
 'd':'Де бізнес втрачає найбільше часу і грошей. 5 конкретних процесів які можна автоматизувати вже зараз.','de':'Where businesses lose the most time and money. 5 specific processes you can automate right now.',
 'k':'автоматизація бізнесу, які процеси автоматизувати, автоматизація процесів, оптимізація бізнесу'},
'telegram-mini-app':{'t':'Telegram Mini App для бізнесу: що це і як працює | Devlly','te':'Telegram Mini App for business: what it is and how it works | Devlly',
 'd':'Повноцінний застосунок прямо в Telegram без завантаження. Пояснюємо що таке Mini App і навіщо це вашому бізнесу.','de':'A full-featured app right inside Telegram with no download. We explain what a Mini App is and why your business needs it.',
 'k':'Telegram Mini App, міні-застосунок Telegram, застосунок у Telegram, Mini App для бізнесу'},
'data-parsing':{'t':'Парсинг даних: як моніторити конкурентів автоматично | Devlly','te':'Data parsing: how to monitor competitors automatically | Devlly',
 'd':'Як автоматично збирати ціни і дані конкурентів без ручної роботи. Що таке парсинг і як використати це для бізнесу.','de':"How to automatically collect competitors' prices and data without manual work. What parsing is and how to use it for business.",
 'k':'парсинг даних, моніторинг конкурентів, збір даних, парсинг цін, веб-скрапінг'},
'ai-bot-requests':{'t':'AI бот для обробки заявок: замінює менеджера цілодобово','te':'AI Bot for Request Processing: Replace Your Manager 24/7',
 'd':'Як AI бот обробляє заявки клієнтів без участі менеджера: відповідає, класифікує і передає далі. Цілодобово, без вихідних і без помилок.','de':'How an AI bot handles client requests without a manager: responds, classifies and escalates. 24/7, no days off, no missed requests.',
 'k':'AI-бот, штучний інтелект, обробка заявок, чат-бот з AI, автоматизація підтримки'},
'automate-or-lose-money':{'t':'Автоматизація бізнесу: скільки коштує ручна робота | Devlly','te':'Business automation: how much manual work really costs | Devlly',
 'd':'Типові процеси які малий бізнес досі робить вручну і скільки це реально коштує. Що можна автоматизувати вже зараз.','de':'Typical processes small businesses still do by hand and how much it really costs. What you can automate right now.',
 'k':'автоматизація бізнесу, вартість ручної роботи, оптимізація витрат, автоматизація процесів'},
}
ISODATE = {
'crm-or-sheets':'2025-02-12','telegram-bot-saves-time':'2025-03-28','crm-vs-erp':'2025-04-15',
'what-to-automate-first':'2025-05-03','telegram-mini-app':'2025-06-20','data-parsing':'2025-07-08',
'ai-bot-requests':'2025-08-14','automate-or-lose-money':'2025-09-02',
'telegram-bot-salon':'2026-01-09','telegram-bot-delivery':'2026-01-16','telegram-bot-fitness':'2026-01-27',
'telegram-bot-realty':'2026-02-05','telegram-bot-shop':'2026-02-13','telegram-bot-dental':'2026-02-24',
'mini-app-shop':'2026-03-04','mini-app-taxi':'2026-03-12','mini-app-booking':'2026-03-23',
'crm-realty':'2026-04-02','crm-salon':'2026-04-09','crm-construction':'2026-04-17','crm-legal':'2026-04-28',
'hr-automation':'2026-05-06','shop-automation':'2026-05-14','accounting-automation':'2026-05-21',
'support-automation':'2026-05-29','ai-chatbot-shop':'2026-06-05','price-parsing':'2026-06-15',
'b2b-leads':'2026-06-25',
'hr-telegram-recruitment':'2026-06-11','crm-dlya-yuristov':'2026-06-16','hr-bot-small-business':'2026-06-20',
'avtomatizaciya-zayavok':'2026-06-24','hr-onboarding-automation':'2026-06-30','crm-dlya-yuridychnykh-kompaniy':'2026-07-02',
'hr-telegram-form':'2026-07-07','obrobka-zayavok-klientiv':'2026-07-10','hr-crm-vs-sheets':'2026-07-14',
'crm-dlya-yuridychnoi-firmy':'2026-01-13','baza-klientiv':'2026-01-22','vedennya-bazy-klientiv':'2026-02-10',
'crm-salon-krasoty':'2026-02-27','proektna-crm':'2026-03-17','chatbot-prodazhi':'2026-04-14',
'boty-buhgalteriya':'2026-05-19','hr-bot':'2026-07-16',
'crm-vs-excel':'2026-01-31','crm-vs-google-sheets':'2026-03-06','crm-vs-trello':'2026-04-22',
'telegram-bot-vs-mobile-app':'2026-05-27','saas-vs-custom-crm':'2026-07-11',
'crm-yuridychna-firma-vprovadzhennya':'2026-01-20','crm-dlya-advokata':'2026-02-17',
'salon-krasoty-telegram-zapis':'2026-03-24','salon-krasoty-nagaduvannya':'2026-04-25',
'hr-bot-telegram-nalashtuvannya':'2026-05-22','hr-bot-functions':'2026-06-18',
'programa-dlya-salonu-krasy':'2026-01-15','programy-dlya-saloniv-krasy':'2026-01-29',
'hr-systema-dlya-malogo-biznesu':'2026-02-03','avtomatyzatsiya-recruiting':'2026-02-20',
'avtomatyzatsiya-internet-magazyn-odyagu':'2026-03-02','crm-dlya-internet-magazynu':'2026-03-10',
'avtomatyzatsiya-dropshipping':'2026-03-19','telegram-bot-dropshipping':'2026-03-27',
'avtomatyzatsiya-kaviarni':'2026-04-06','crm-dlya-kaviarni':'2026-04-13','telegram-bot-kaviarnya':'2026-04-20',
'avtomatyzatsiya-restoranu':'2026-05-05','telegram-bot-dostavka-yizhi':'2026-05-12',
'crm-dlya-rieltoriva':'2026-05-25','telegram-bot-nerukhomist':'2026-06-02',
'crm-dlya-kliniky':'2026-06-09','telegram-bot-klinika':'2026-06-22','spreadsheets-to-crm':'2026-07-06',
'obrobka-zayavok':'2026-01-08','pryom-zayavok-vid-klientiv':'2026-03-31',
'avtomatyzatsiya-zayavok':'2026-05-18','crm-dlya-obrobky-zayavok':'2026-07-13',
'crm-dlya-fitnes-klubu':'2026-01-19','avtomatyzatsiya-skladu':'2026-02-06',
'crm-dlya-turagentstva':'2026-03-13','avtomatyzatsiya-lohistyky':'2026-04-08',
'telegram-bot-avtoservis':'2026-05-13','crm-dlya-strakhovoyi':'2026-06-08',
'telegram-bot-dlya-ukraintsiv-v-yevropi':'2026-01-11','avtomatyzatsiya-biznesu-za-kordonom':'2026-01-24',
'viddalene-upravlinnya-biznesom-z-ukrainy':'2026-02-08','crm-dlya-ukrainskoi-diaspory':'2026-02-19',
'crm-dlya-biznesu-v-polshchi':'2026-03-05','avtomatyzatsiya-ukrainskogo-biznesu-v-nimechchyni':'2026-03-16',
'telegram-bot-zamovlennya-z-polshchi':'2026-04-11','crm-ukrainskyi-biznes-chehiya':'2026-04-23',
'relokatsiya-biznesu-bez-vtraty-klientiv':'2026-05-16','dropshipping-z-polshchi-v-ukrainu':'2026-06-12',
'komanda-za-kordonom-avtomatyzatsiya':'2026-06-27','eksport-v-yevropu-crm':'2026-07-09',
'viddalenyi-internet-magazyn-z-ukrainy':'2026-07-22',
'avtomatyzatsiya-kalyanoi':'2026-07-24',
}
UA_M = ['СІЧ','ЛЮТ','БЕР','КВІ','ТРА','ЧЕР','ЛИП','СЕР','ВЕР','ЖОВ','ЛИС','ГРУ']
EN_M = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
def dates(slug):
    y, m, d = (int(x) for x in ISODATE[slug].split('-'))
    return '%02d %s %d' % (d, UA_M[m-1], y), '%s %d, %d' % (EN_M[m-1], d, y)
RELATED = {
'crm-or-sheets':['crm-vs-erp','what-to-automate-first','automate-or-lose-money'],
'telegram-bot-saves-time':['telegram-mini-app','ai-bot-requests','what-to-automate-first'],
'crm-vs-erp':['crm-or-sheets','what-to-automate-first','automate-or-lose-money'],
'what-to-automate-first':['automate-or-lose-money','crm-or-sheets','telegram-bot-saves-time'],
'telegram-mini-app':['telegram-bot-saves-time','ai-bot-requests','crm-vs-erp'],
'data-parsing':['automate-or-lose-money','what-to-automate-first','ai-bot-requests'],
'ai-bot-requests':['telegram-bot-saves-time','telegram-mini-app','data-parsing'],
'automate-or-lose-money':['what-to-automate-first','crm-or-sheets','data-parsing'],
'telegram-bot-salon':['crm-salon','mini-app-booking','telegram-bot-dental'],
'telegram-bot-delivery':['telegram-bot-shop','mini-app-taxi','shop-automation'],
'telegram-bot-fitness':['mini-app-booking','crm-salon','telegram-bot-salon'],
'telegram-bot-realty':['crm-realty','ai-bot-requests','b2b-leads'],
'telegram-bot-shop':['mini-app-shop','shop-automation','ai-chatbot-shop'],
'telegram-bot-dental':['mini-app-booking','telegram-bot-salon','support-automation'],
'mini-app-shop':['telegram-bot-shop','telegram-mini-app','shop-automation'],
'mini-app-taxi':['telegram-mini-app','telegram-bot-delivery','mini-app-booking'],
'mini-app-booking':['telegram-bot-salon','telegram-bot-fitness','telegram-mini-app'],
'crm-realty':['telegram-bot-realty','crm-vs-erp','crm-or-sheets'],
'crm-salon':['telegram-bot-salon','crm-or-sheets','crm-vs-erp'],
'crm-construction':['crm-vs-erp','crm-legal','automate-or-lose-money'],
'crm-legal':['crm-or-sheets','crm-construction','hr-automation'],
'hr-automation':['what-to-automate-first','support-automation','accounting-automation'],
'shop-automation':['telegram-bot-shop','ai-chatbot-shop','price-parsing'],
'accounting-automation':['automate-or-lose-money','hr-automation','what-to-automate-first'],
'support-automation':['ai-chatbot-shop','ai-bot-requests','hr-automation'],
'ai-chatbot-shop':['support-automation','ai-bot-requests','telegram-bot-shop'],
'price-parsing':['data-parsing','shop-automation','b2b-leads'],
'b2b-leads':['data-parsing','price-parsing','crm-or-sheets'],
'hr-telegram-recruitment':['hr-telegram-form','hr-bot-small-business','hr-automation'],
'hr-bot-small-business':['hr-automation','hr-telegram-recruitment','hr-onboarding-automation'],
'hr-onboarding-automation':['hr-bot-small-business','hr-automation','hr-crm-vs-sheets'],
'hr-telegram-form':['hr-telegram-recruitment','hr-crm-vs-sheets','hr-automation'],
'hr-crm-vs-sheets':['hr-automation','crm-or-sheets','hr-bot-small-business'],
'crm-dlya-yuristov':['crm-dlya-yuridychnykh-kompaniy','crm-legal','crm-or-sheets'],
'crm-dlya-yuridychnykh-kompaniy':['crm-dlya-yuristov','crm-legal','crm-vs-erp'],
'avtomatizaciya-zayavok':['obrobka-zayavok-klientiv','ai-bot-requests','support-automation'],
'obrobka-zayavok-klientiv':['avtomatizaciya-zayavok','ai-bot-requests','what-to-automate-first'],
'crm-dlya-yuridychnoi-firmy':['crm-dlya-yuristov','crm-dlya-yuridychnykh-kompaniy','crm-legal'],
'crm-salon-krasoty':['crm-salon','telegram-bot-salon','crm-or-sheets'],
'hr-bot':['hr-bot-small-business','hr-telegram-recruitment','hr-onboarding-automation'],
'proektna-crm':['crm-vs-erp','crm-or-sheets','crm-construction'],
'chatbot-prodazhi':['ai-bot-requests','ai-chatbot-shop','b2b-leads'],
'boty-buhgalteriya':['accounting-automation','automate-or-lose-money','telegram-bot-saves-time'],
'vedennya-bazy-klientiv':['baza-klientiv','crm-or-sheets','crm-vs-erp'],
'baza-klientiv':['vedennya-bazy-klientiv','b2b-leads','crm-or-sheets'],
'crm-vs-excel':['crm-or-sheets','crm-vs-google-sheets','crm-vs-erp'],
'telegram-bot-vs-mobile-app':['telegram-mini-app','telegram-bot-saves-time','mini-app-shop'],
'saas-vs-custom-crm':['crm-vs-erp','crm-or-sheets','proektna-crm'],
'crm-vs-google-sheets':['crm-or-sheets','vedennya-bazy-klientiv','crm-vs-excel'],
'crm-vs-trello':['proektna-crm','crm-vs-erp','crm-or-sheets'],
'crm-yuridychna-firma-vprovadzhennya':['crm-legal','crm-dlya-yuridychnoi-firmy','crm-dlya-advokata'],
'crm-dlya-advokata':['crm-legal','crm-dlya-yuridychnoi-firmy','crm-yuridychna-firma-vprovadzhennya'],
'salon-krasoty-telegram-zapis':['crm-salon','crm-salon-krasoty','salon-krasoty-nagaduvannya'],
'salon-krasoty-nagaduvannya':['crm-salon','crm-salon-krasoty','salon-krasoty-telegram-zapis'],
'hr-bot-telegram-nalashtuvannya':['hr-automation','hr-bot','hr-bot-functions'],
'hr-bot-functions':['hr-automation','hr-bot','hr-bot-telegram-nalashtuvannya'],
'programa-dlya-salonu-krasy':['crm-salon','crm-salon-krasoty','programy-dlya-saloniv-krasy'],
'programy-dlya-saloniv-krasy':['crm-salon-krasoty','telegram-bot-salon','programa-dlya-salonu-krasy'],
'hr-systema-dlya-malogo-biznesu':['hr-automation','hr-bot-small-business','avtomatyzatsiya-recruiting'],
'avtomatyzatsiya-recruiting':['hr-telegram-recruitment','hr-bot','hr-systema-dlya-malogo-biznesu'],
'avtomatyzatsiya-internet-magazyn-odyagu':['shop-automation','crm-dlya-internet-magazynu','telegram-bot-shop'],
'crm-dlya-internet-magazynu':['shop-automation','avtomatyzatsiya-internet-magazyn-odyagu','mini-app-shop'],
'avtomatyzatsiya-dropshipping':['telegram-bot-dropshipping','crm-dlya-internet-magazynu','shop-automation'],
'telegram-bot-dropshipping':['avtomatyzatsiya-dropshipping','telegram-bot-shop','mini-app-shop'],
'avtomatyzatsiya-kaviarni':['crm-dlya-kaviarni','telegram-bot-kaviarnya','avtomatyzatsiya-restoranu'],
'crm-dlya-kaviarni':['avtomatyzatsiya-kaviarni','telegram-bot-kaviarnya','baza-klientiv'],
'telegram-bot-kaviarnya':['avtomatyzatsiya-kaviarni','crm-dlya-kaviarni','telegram-bot-delivery'],
'avtomatyzatsiya-restoranu':['telegram-bot-dostavka-yizhi','telegram-bot-delivery','avtomatyzatsiya-kaviarni'],
'telegram-bot-dostavka-yizhi':['avtomatyzatsiya-restoranu','telegram-bot-delivery','telegram-bot-kaviarnya'],
'crm-dlya-rieltoriva':['crm-realty','telegram-bot-nerukhomist','telegram-bot-realty'],
'telegram-bot-nerukhomist':['telegram-bot-realty','crm-dlya-rieltoriva','crm-realty'],
'crm-dlya-kliniky':['telegram-bot-klinika','telegram-bot-dental','baza-klientiv'],
'telegram-bot-klinika':['crm-dlya-kliniky','telegram-bot-dental','mini-app-booking'],
'spreadsheets-to-crm':['crm-vs-excel','crm-vs-google-sheets','vedennya-bazy-klientiv'],
'obrobka-zayavok':['obrobka-zayavok-klientiv','avtomatizaciya-zayavok','crm-dlya-obrobky-zayavok'],
'pryom-zayavok-vid-klientiv':['obrobka-zayavok','avtomatizaciya-zayavok','ai-bot-requests'],
'avtomatyzatsiya-zayavok':['avtomatizaciya-zayavok','obrobka-zayavok','crm-dlya-obrobky-zayavok'],
'crm-dlya-obrobky-zayavok':['obrobka-zayavok','obrobka-zayavok-klientiv','baza-klientiv'],
'crm-dlya-fitnes-klubu':['telegram-bot-fitness','mini-app-booking','baza-klientiv'],
'avtomatyzatsiya-skladu':['shop-automation','accounting-automation','avtomatyzatsiya-lohistyky'],
'crm-dlya-turagentstva':['baza-klientiv','obrobka-zayavok','chatbot-prodazhi'],
'avtomatyzatsiya-lohistyky':['telegram-bot-delivery','avtomatyzatsiya-skladu','telegram-bot-dostavka-yizhi'],
'telegram-bot-avtoservis':['mini-app-booking','salon-krasoty-nagaduvannya','telegram-bot-klinika'],
'crm-dlya-strakhovoyi':['baza-klientiv','vedennya-bazy-klientiv','crm-dlya-yuristov'],
'telegram-bot-dlya-ukraintsiv-v-yevropi':['telegram-bot-shop','avtomatyzatsiya-biznesu-za-kordonom','crm-dlya-ukrainskoi-diaspory'],
'avtomatyzatsiya-biznesu-za-kordonom':['viddalene-upravlinnya-biznesom-z-ukrainy','crm-dlya-ukrainskoi-diaspory','what-to-automate-first'],
'viddalene-upravlinnya-biznesom-z-ukrainy':['komanda-za-kordonom-avtomatyzatsiya','avtomatyzatsiya-biznesu-za-kordonom','crm-dlya-obrobky-zayavok'],
'crm-dlya-ukrainskoi-diaspory':['crm-dlya-biznesu-v-polshchi','eksport-v-yevropu-crm','baza-klientiv'],
'crm-dlya-biznesu-v-polshchi':['crm-ukrainskyi-biznes-chehiya','telegram-bot-zamovlennya-z-polshchi','crm-dlya-ukrainskoi-diaspory'],
'avtomatyzatsiya-ukrainskogo-biznesu-v-nimechchyni':['crm-dlya-biznesu-v-polshchi','crm-ukrainskyi-biznes-chehiya','avtomatyzatsiya-biznesu-za-kordonom'],
'telegram-bot-zamovlennya-z-polshchi':['crm-dlya-biznesu-v-polshchi','telegram-bot-shop','telegram-bot-delivery'],
'crm-ukrainskyi-biznes-chehiya':['crm-dlya-biznesu-v-polshchi','avtomatyzatsiya-ukrainskogo-biznesu-v-nimechchyni','crm-dlya-ukrainskoi-diaspory'],
'relokatsiya-biznesu-bez-vtraty-klientiv':['viddalene-upravlinnya-biznesom-z-ukrainy','baza-klientiv','avtomatyzatsiya-biznesu-za-kordonom'],
'dropshipping-z-polshchi-v-ukrainu':['avtomatyzatsiya-dropshipping','telegram-bot-dropshipping','crm-dlya-biznesu-v-polshchi'],
'komanda-za-kordonom-avtomatyzatsiya':['viddalene-upravlinnya-biznesom-z-ukrainy','hr-automation','avtomatyzatsiya-biznesu-za-kordonom'],
'eksport-v-yevropu-crm':['crm-dlya-ukrainskoi-diaspory','b2b-leads','crm-dlya-biznesu-v-polshchi'],
'viddalenyi-internet-magazyn-z-ukrainy':['viddalene-upravlinnya-biznesom-z-ukrainy','crm-dlya-internet-magazynu','shop-automation'],
}

# --- Внутрішня перелінковка по тематичних кластерах ---------------------------
# Кожна стаття кластера лінкує на 3 сусідів ЗІ СВОГО кластера (циклічно): це
# рівномірно розподіляє ланки (кожна стаття отримує рівно 3 вхідні + 3 вихідні),
# без сиріт і без міжкластерних «випадкових» зв'язків. Перевизначає RELATED вище
# лише для статей, що входять у кластери; решта статей лишаються як були.
CLUSTERS = [
  # Салон краси
  ['crm-salon','crm-salon-krasoty','programa-dlya-salonu-krasy','programy-dlya-saloniv-krasy',
   'salon-krasoty-telegram-zapis','salon-krasoty-nagaduvannya','telegram-bot-salon'],
  # Юристи
  ['crm-legal','crm-dlya-yuristov','crm-dlya-yuridychnykh-kompaniy','crm-dlya-yuridychnoi-firmy',
   'crm-yuridychna-firma-vprovadzhennya','crm-dlya-advokata'],
  # Нерухомість
  ['crm-realty','crm-dlya-rieltoriva','telegram-bot-realty','telegram-bot-nerukhomist'],
  # HR
  ['hr-automation','hr-bot','hr-bot-small-business','hr-onboarding-automation','hr-telegram-recruitment',
   'hr-telegram-form','hr-crm-vs-sheets','hr-systema-dlya-malogo-biznesu','avtomatyzatsiya-recruiting',
   'hr-bot-telegram-nalashtuvannya','hr-bot-functions'],
  # Кавʼярня / ресторан / громадське харчування (+ кальянна)
  ['avtomatyzatsiya-kaviarni','crm-dlya-kaviarni','telegram-bot-kaviarnya','avtomatyzatsiya-restoranu',
   'telegram-bot-dostavka-yizhi','avtomatyzatsiya-kalyanoi'],
  # Інтернет-магазин / дропшипінг
  ['crm-dlya-internet-magazynu','avtomatyzatsiya-internet-magazyn-odyagu','avtomatyzatsiya-dropshipping',
   'telegram-bot-dropshipping','shop-automation','ai-chatbot-shop','mini-app-shop','telegram-bot-shop'],
  # Заявки / база клієнтів
  ['obrobka-zayavok','obrobka-zayavok-klientiv','pryom-zayavok-vid-klientiv','avtomatizaciya-zayavok',
   'avtomatyzatsiya-zayavok','crm-dlya-obrobky-zayavok','ai-bot-requests','baza-klientiv','vedennya-bazy-klientiv'],
  # Діаспора / закордон (13)
  ['telegram-bot-dlya-ukraintsiv-v-yevropi','avtomatyzatsiya-biznesu-za-kordonom',
   'viddalene-upravlinnya-biznesom-z-ukrainy','crm-dlya-ukrainskoi-diaspory','crm-dlya-biznesu-v-polshchi',
   'avtomatyzatsiya-ukrainskogo-biznesu-v-nimechchyni','telegram-bot-zamovlennya-z-polshchi',
   'crm-ukrainskyi-biznes-chehiya','relokatsiya-biznesu-bez-vtraty-klientiv','dropshipping-z-polshchi-v-ukrainu',
   'komanda-za-kordonom-avtomatyzatsiya','eksport-v-yevropu-crm','viddalenyi-internet-magazyn-z-ukrainy'],
]
def _cluster_related(cluster, n=3):
    L=len(cluster)
    return {s:[cluster[(i+j)%L] for j in range(1,n+1)] for i,s in enumerate(cluster)}
for _cl in CLUSTERS:
    RELATED.update(_cluster_related(_cl))
# Нова стаття про кальянну - явно на кавʼярня/ресторан кластер (за ТЗ)
RELATED['avtomatyzatsiya-kalyanoi']=['avtomatyzatsiya-kaviarni','crm-dlya-kaviarni','avtomatyzatsiya-restoranu']
# Кожен slug у кожному кластері й у RELATED має бути в SLUGS (інакше KeyError у ART)
_missing=sorted({s for cl in CLUSTERS for s in cl} - set(SLUGS))
assert not _missing, 'cluster slugs not in SLUGS: %s'%_missing

def ea(v): return v.replace('&','&amp;').replace('"','&quot;').replace('<','&lt;').replace('>','&gt;')
def et(v): return v.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

idx = io.open(ROOT+'/index.html', encoding='utf-8').read().split('\n')
def find(sub, frm=0):
    for i in range(frm, len(idx)):
        if sub in idx[i]: return i
    raise ValueError('not found: '+sub)
i_body=next(i for i,l in enumerate(idx) if l.startswith('<body'))
i_smooth=find('id="smooth-content"'); i_footer=find('Footer Start Here')
i_jquery=find('Jquery js'); i_bclose=next(i for i,l in enumerate(idx) if l.strip()=='</body>')
RAW_TOP='\n'.join(idx[i_body:i_smooth+1]); RAW_FOOTER='\n'.join(idx[i_footer:i_jquery]); RAW_SCRIPTS='\n'.join(idx[i_jquery:i_bclose])
def rewrite(b):
    b=b.replace('assets/','../assets/')
    for a in ['about','services','blog','contact','projects']:
        b=b.replace('href="#%s"'%a,'href="/#%s"'%a)
    return b
TOP,FOOTER,SCRIPTS=rewrite(RAW_TOP),rewrite(RAW_FOOTER),rewrite(RAW_SCRIPTS)

# --- EN-версия шапки/подвала/скриптов: тот же движок, что и для en/index.html ---
sys.path.insert(0, SCRATCH)
from enify import to_en, outside_scripts
def _en_links(x):
    for a in ['about','services','blog','contact','projects']:
        x=x.replace('href="#%s"'%a,'href="/en#%s"'%a)
    x=x.replace('href="/#blog"','href="/en#blog"')
    x=x.replace('href="/"','href="/en"')                     # логотип / «Головна»
    x=x.replace('data-lang="uk" href="/en"','data-lang="uk" href="/"')
    return x
def rewrite_en(b):
    b=to_en(b)
    b=re.sub(r'(?<![./\w])assets/', '/assets/', b)          # /en/blog/x - база не /en/, нужен корень
    return outside_scripts(b, _en_links)                     # внутрь <script> не лезем
TOP_EN,FOOTER_EN,SCRIPTS_EN=rewrite_en(RAW_TOP),rewrite_en(RAW_FOOTER),rewrite_en(RAW_SCRIPTS)

# load all articles (for titles used in "Read also")
ART={}
for slug in SLUGS:
    a=json.load(io.open(SCRATCH+'/art_%s.json'%slug, encoding='utf-8'))
    if slug not in SEO:                      # у новых статей SEO лежит внутри json
        SEO[slug]=a['seo']
    a['date_uk'], a['date_en'] = dates(slug) # единый источник правды - ISODATE
    ART[slug]=a

def head(slug, en=False):
    s=SEO[slug]; a=ART[slug]
    uk_url='%s/blog/%s'%(BASE,slug); en_url='%s/en/blog/%s'%(BASE,slug)
    url = en_url if en else uk_url
    A = '/assets' if en else '../assets'          # /en/blog/x: относительные пути не работают
    title  = s['te'] if en else s['t']
    desc   = s['de'] if en else s['d']
    headln = a['title_en'] if en else a['title_uk']
    schema={"@context":"https://schema.org","@type":"Article","headline":headln,
            "description":desc,"image":OGIMG,"datePublished":ISODATE[slug],"dateModified":ISODATE[slug],
            "inLanguage":"en" if en else "uk",
            "author":{"@type":"Organization","name":"Devlly Team"},
            "publisher":{"@type":"Organization","name":"Devlly","logo":{"@type":"ImageObject","url":BASE+"/assets/images/logo/favicon.png"}},
            "mainEntityOfPage":{"@type":"WebPage","@id":url},"url":url}
    home_n, blog_n = ('Home','Blog') if en else ('Головна','Блог')
    home_u = BASE+('/en' if en else '/')
    blog_u = BASE+('/en#blog' if en else '/#blog')
    crumbs={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":home_n,"item":home_u},
        {"@type":"ListItem","position":2,"name":blog_n,"item":blog_u},
        {"@type":"ListItem","position":3,"name":headln,"item":url}]}
    ld=('    <script type="application/ld+json">\n'+json.dumps(schema,ensure_ascii=False,indent=2)+'\n    </script>\n'
        '    <script type="application/ld+json">\n'+json.dumps(crumbs,ensure_ascii=False,indent=2)+'\n    </script>\n')
    kw = '' if en else '    <meta name="keywords" content="%s">\n'%ea(s['k'])
    # заголовок/описание уже на нужном языке; data-en оставляем только в UA-версии
    da_t = ' data-en="%s"'%ea(s['te']) if not en else ''
    da_d = ' data-en="%s"'%ea(s['de']) if not en else ''
    hreflang=('    <link rel="alternate" hreflang="uk" href="%s">\n'
              '    <link rel="alternate" hreflang="en" href="%s">\n'
              '    <link rel="alternate" hreflang="x-default" href="%s">\n')%(uk_url,en_url,uk_url)
    return ('<!DOCTYPE html>\n<html lang="%s">\n<head>\n'
    '    <meta charset="UTF-8">\n'
    '    <meta http-equiv="X-UA-Compatible" content="IE=edge">\n'
    '    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
    '    <title%s>%s</title>\n'
    '    <meta name="description" content="%s"%s>\n'
    '%s'
    '    <meta name="robots" content="INDEX,FOLLOW">\n'
    '    <link rel="canonical" href="%s">\n'
    '%s'
    '    <meta property="og:type" content="article">\n'
    '    <meta property="og:site_name" content="Devlly">\n'
    '    <meta property="og:title" content="%s">\n'
    '    <meta property="og:description" content="%s">\n'
    '    <meta property="og:url" content="%s">\n'
    '    <meta property="og:image" content="%s">\n'
    '    <meta property="og:locale" content="%s">\n'
    '    <meta name="twitter:card" content="summary_large_image">\n'
    '    <link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '    <link rel="preload" as="font" type="font/woff2" href="%s/fonts/Thunder-SemiBoldLC.woff2" crossorigin>\n'
    '    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Funnel+Display:wght@300..800&display=swap" media="print" onload="this.media=\'all\'">\n'
    '    <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Funnel+Display:wght@300..800&display=swap"></noscript>\n'
    '    <link rel="icon" type="image/svg+xml" href="%s/images/logo/favicon.svg">\n'
    '    <link rel="icon" href="%s/images/logo/favicon.ico" sizes="any">\n'
    '    <link rel="icon" type="image/png" href="%s/images/logo/favicon.png">\n'
    '    <link rel="apple-touch-icon" href="%s/images/logo/apple-touch-icon.png">\n'
    '    <link rel="stylesheet" href="%s/css/bootstrap.min.css">\n'
    '    <link rel="stylesheet" href="%s/css/main.css">\n'
    '    <link rel="stylesheet" href="%s/css/aos.css">\n'
    '    <link rel="stylesheet" href="%s/css/phosphor.css">\n'
    '%s'
    '</head>\n')%('en' if en else 'uk', da_t, et(title), ea(desc), da_d, kw, url, hreflang,
                  ea(title), ea(desc), url, OGIMG, 'en_US' if en else 'uk_UA',
                  A,A,A,A,A,A,A,A,A, ld)

def block_html(b):
    t,uk,en=b['t'],b['uk'],b['en']; da=' data-en="%s"'%ea(en)
    if t=='lead': return '                            <p class="tw-text-xl text-heading fw-medium tw-mb-8"%s>%s</p>'%(da,et(uk))
    if t=='h2':   return '                            <h2 class="tw-text-7 fw-semibold text-heading tw-mt-10 tw-mb-5"%s>%s</h2>'%(da,et(uk))
    return '                            <p class="tw-text-lg tw-mb-6"%s>%s</p>'%(da,et(uk))

def related(slug):
    items='\n'.join(
      '                                    <li><a class="tw-text-xl fw-medium text-heading hover-text-main-two-600 cursor-small d-inline-flex align-items-start tw-gap-3" href="%s"><span class="text-main-two-600">&rarr;</span> <span data-en="%s">%s</span></a></li>'
      %(r, ea(ART[r]['title_en']), et(ART[r]['title_uk'])) for r in RELATED[slug])
    return ('''                            <div class="tw-mt-15">
                                <h2 class="tw-text-7 fw-semibold text-heading tw-mb-6" data-en="Read also">Читайте також</h2>
                                <ul class="d-flex flex-column tw-gap-4">
%s
                                </ul>
                            </div>''')%items

def cta(slug=None):
    a = ART.get(slug, {}) if slug else {}
    h_uk = a.get('cta_uk', 'Потрібна розробка для вашого бізнесу? Пишіть нам')
    h_en = a.get('cta_en', 'Need software for your business? Get in touch')
    return ('''                            <div class="gray--bg tw-rounded-2xl tw-p-10 tw-mt-15 text-center">
                                <h3 class="tw-text-3xl fw-semibold text-heading tw-mb-6" data-en="%s">%s</h3>''' % (ea(h_en), et(h_uk)) + '''
                                <div class="d-flex align-items-center justify-content-center tw-gap-4 flex-wrap">
                                    <a class="%s" href="mailto:%s"><span data-en="Email us">Написати на пошту</span></a>
                                    <a class="%s" href="%s" target="_blank"><span>Telegram</span></a>
                                </div>
                            </div>''')%(BTN,EMAIL,BTN2,TG)

def article_main(slug):
    a=ART[slug]
    body='\n'.join(block_html(b) for b in a['blocks'])
    crumb=('<nav class="tw-mb-8" aria-label="breadcrumb">\n'
    '                                <ul class="d-flex flex-wrap align-items-center justify-content-center tw-gap-2 tw-text-sm fw-medium">\n'
    '                                    <li><a class="text-heading hover-text-main-two-600 cursor-small" href="/" data-en="Home">Головна</a></li>\n'
    '                                    <li class="text-heading">/</li>\n'
    '                                    <li><a class="text-heading hover-text-main-two-600 cursor-small" href="/#blog" data-en="Blog">Блог</a></li>\n'
    '                                    <li class="text-heading">/</li>\n'
    '                                    <li class="text-main-two-600" data-en="%s">%s</li>\n'
    '                                </ul>\n'
    '                            </nav>')%(ea(a['title_en']),et(a['title_uk']))
    return ('''
            <main>
            <article class="blog-details-area py-120 tw-mt-15">
                <div class="container">
                    <div class="row justify-content-center">
                        <div class="col-xl-8">
                            %s
                            <div class="tw-mb-10 text-center">
                                <div class="blog-three-meta d-flex justify-content-center tw-mb-6">
                                    <ul class="d-flex align-items-center justify-content-center tw-gap-305">
                                        <li><a class="%s" href="/#blog" data-en="Article">Стаття</a></li>
                                        <li><a class="%s" href="#" data-en="%s">%s</a></li>
                                    </ul>
                                </div>
                                <h1 class="tw-text-13 fw-bold text-heading" data-en="%s">%s</h1>
                            </div>
                            <div class="blog-details-content">
%s
%s
%s
                            </div>
                            <div class="tw-mt-15 text-center">
                                <a class="%s" href="/#blog" data-en="Back to all articles">Усі статті</a>
                            </div>
                        </div>
                    </div>
                </div>
            </article>
            </main>
''')%(crumb,PILL,PILL,ea(a['date_en']),et(a['date_uk']),ea(a['title_en']),et(a['title_uk']),
      body, related(slug), cta(slug), BTN2)

def switcher(page, slug, en):
    """Переключатель ведёт на ту же статью в другом языке, а не на главную."""
    page=page.replace('data-lang="uk" href="/"','data-lang="uk" href="/blog/%s"'%slug)
    page=page.replace('data-lang="en" href="/en"','data-lang="en" href="/en/blog/%s"'%slug)
    return page

if not os.path.isdir(ROOT+'/en/blog'): os.makedirs(ROOT+'/en/blog')

built=0
for slug in SLUGS:
    # --- UA ---
    page=head(slug)+TOP+article_main(slug)+FOOTER+'\n'+SCRIPTS+'\n</body>\n</html>\n'
    io.open(ROOT+'/blog/%s.html'%slug,'w',encoding='utf-8',newline='\n').write(switcher(page,slug,False))
    # --- EN: тот же движок data-en, что и у бывшего JS-переключателя ---
    body_en=outside_scripts(to_en(article_main(slug)), _en_links)
    page_en=head(slug,en=True)+TOP_EN+body_en+FOOTER_EN+'\n'+SCRIPTS_EN+'\n</body>\n</html>\n'
    io.open(ROOT+'/en/blog/%s.html'%slug,'w',encoding='utf-8',newline='\n').write(switcher(page_en,slug,True))
    w=sum(len(b['uk'].split()) for b in ART[slug]['blocks'])
    print('built %-26s uk+en words=%d h2=%d'%(slug,w,sum(1 for b in ART[slug]['blocks'] if b['t']=='h2')))
    built+=1
print('TOTAL built: %d UA + %d EN'%(built,built))
