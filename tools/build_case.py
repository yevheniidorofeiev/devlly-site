# -*- coding: utf-8 -*-
"""
Генератор страниц портфолио-кейсов (/cases/<slug> + /en/cases/<slug>).

Отдельно от блог-пайплайна: build_blog.py / CLUSTERS / RELATED здесь не участвуют.
Общее с ними только одно - движок EN-версии (enify.to_en), чтобы двуязычность
работала ровно так же, как на остальном сайте: разметка пишется по-украински
с data-en, EN-файл статически выпекается из неё.

Оболочка (шапка/подвал/скрипты) берётся из готовой страницы блога, чтобы
хедер, футер, поиск и меню не расходились с остальным сайтом.

Запуск:  python tools/build_case.py [slug ...]     (без аргументов - все кейсы)

Тело страницы описывается списком блоков `body`, каждый блок - кортеж:
  ('h2',   uk, en)                 заголовок раздела (первый - без верхнего отступа)
  ('h3',   uk, en)                 подзаголовок внутри раздела
  ('p',    uk, en)                 абзац
  ('list', [(uk, en), ...])        список со стрелками
  ('shots', wrap, [ключи])         скриншоты; wrap=None - лентой во всю ширину,
                                   иначе bootstrap-колонка ('col-6 col-xl-3' и т.п.)
"""
import io, os, re, sys, json

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get('DEVLLY_ROOT', os.path.dirname(_HERE))
sys.path.insert(0, _HERE)
from enify import to_en, outside_scripts

BASE = 'https://devlly.dev'
SHELL = ROOT + '/blog/crm-realty.html'      # донор оболочки
SHELL_UK_HREF = '/blog/crm-realty'          # что стоит в переключателе языка донора
SHELL_EN_HREF = '/en/blog/crm-realty'

# Google Ads gtag.js: тот же блок стоит в <head> index.html и всех остальных страниц.
# Правится в одном месте - и в index.html, и здесь, и в build_blog.py (три шаблона head).
GADS = """    <!-- Google tag (gtag.js) - Google Ads AW-18358717051 -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=AW-18358717051"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'AW-18358717051');
    </script>
    <script>
      function gtag_report_conversion(url) {
        var callback = function () {
          if (typeof(url) != 'undefined') {
            window.location = url;
          }
        };
        gtag('event', 'conversion', {
            'send_to': 'AW-18358717051/rS0ACJT4494cEPuUj7JE',
            'event_callback': callback
        });
        return false;
      }
    </script>
"""

# геометрия скриншотов по классам (см. tools/README.md): натуральный размер
# крупного варианта + ширины в srcset + sizes под верстку конкретного блока
GEOM = {
    'wide':  dict(w=1456, h=821, ws=[800, 1456], sizes='(max-width: 1199px) 100vw, 950px'),
    'sheet': dict(w=1456, h=691, ws=[800, 1456], sizes='(max-width: 1199px) 100vw, 1150px'),
    'app':   dict(w=476, h=906, ws=[320, 476], sizes='(max-width: 1199px) 45vw, 270px'),
    'bot':   dict(w=696, h=878, ws=[480, 696], sizes='(max-width: 767px) 92vw, (max-width: 1199px) 45vw, 565px'),
    'bot1':  dict(w=696, h=878, ws=[480, 696], sizes='(max-width: 767px) 92vw, (max-width: 1199px) 45vw, 470px'),
    # снимки экрана телефона и Mini App: высота у каждого своя, передаётся через override
    'phone': dict(w=476, h=1030, ws=[320, 476], sizes='(max-width: 1199px) 45vw, 270px'),
    # окно десктопной программы: крупный вариант = нативная ширина, апскейл только мылит текст
    'win':   dict(w=1196, h=819, ws=[800, 1196], sizes='(max-width: 1199px) 100vw, 1150px'),
}


def shot(f, cls, alt_uk, alt_en, cap_uk, cap_en, **over):
    d = dict(GEOM[cls])
    d.update(f=f, alt_uk=alt_uk, alt_en=alt_en, cap_uk=cap_uk, cap_en=cap_en)
    d.update(over)          # w/h под нестандартный размер конкретного снимка
    return d


CASES = {}

# ---------------------------------------------------------------- Квадратний Метр
CASES['kvadratnyi-metr'] = dict(
    date='2026-07-28',
    tag_uk='Нерухомість', tag_en='Real estate',
    cta_uk='Хочете таку ж систему для свого бізнесу? Звʼяжіться з нами',
    cta_en='Want the same system for your business? Get in touch',
    h1_uk='CRM-система «Квадратний Метр»',
    h1_en='The Kvadratnyi Metr CRM',
    title_uk='CRM для рієлторів - кейс «Квадратний Метр» | Devlly',
    title_en='CRM for realtors - the Kvadratnyi Metr case study | Devlly',
    desc_uk='Кейс Devlly: CRM-система для рієлторської агенції - облік заявок, воронка продажів, '
            'канбан угод, каталог обʼєктів і аналітика по агентах. Приклад інтерфейсу на React + Recharts.',
    desc_en='A Devlly case study: a CRM for a real estate agency - request tracking, a sales funnel, '
            'a deal kanban, a property catalogue and per-agent analytics. An interface example built with React and Recharts.',
    keywords_uk='crm для агентства нерухомості приклад, crm для рієлторів, кейс crm нерухомість, '
                'воронка продажів нерухомість, канбан угод, crm для ріелтора приклад, приклад інтерфейсу crm',
    keywords_en='crm for real estate agency example, crm for realtors, real estate crm case study, '
                'real estate sales funnel, deal kanban, crm interface example',
    lead_uk='«Квадратний Метр» - CRM-система для рієлторської агенції: облік заявок, воронка продажів, '
            'аналітика по агентах і джерелах трафіку. Інтерфейс побудований під щоденну роботу відділу '
            'продажів - від першого звернення клієнта до закритої угоди.',
    lead_en='Kvadratnyi Metr is a CRM for a real estate agency: request tracking, a sales funnel and analytics '
            'by agent and by traffic source. The interface is built around the daily routine of a sales team - '
            'from a client’s first enquiry to a closed deal.',
    who_uk='Кому підходить: агенціям нерухомості, які ведуть обʼєкти й клієнтів у таблицях і втрачають '
           'заявки через те, що немає єдиної воронки й видимості, на якій стадії стоїть кожна угода.',
    who_en='Who it fits: real estate agencies that keep properties and clients in spreadsheets and lose '
           'requests because there is no single funnel and no visibility into which stage each deal sits at.',
    stack=['React', 'Vite', 'Tailwind CSS', 'Recharts'],
    stack_uk='Стек: React + Vite, Tailwind CSS для інтерфейсу, Recharts для графіків і діаграм.',
    stack_en='Stack: React with Vite, Tailwind CSS for the interface and Recharts for charts and diagrams.',
    shots={},
)

# 6 самых показательных скриншотов из 9
for _f, _a_uk, _a_en, _c_uk, _c_en in [
    ('dashboard',
     'CRM для рієлторської агенції - дашборд угод з KPI та воронкою продажів',
     'CRM for a real estate agency - deal dashboard with KPIs and a sales funnel',
     'Дашборд: активні угоди, сума в роботі, середній чек і конверсія ліда в угоду. '
     'Поруч - воронка з відсівом на кожному переході, ефективність агентів і час відповіді на заявку.',
     'Dashboard: active deals, the value in progress, the average deal size and lead-to-deal conversion. '
     'Next to it - the funnel with drop-off at every step, agent performance and response time to a request.'),
    ('kanban',
     'Канбан-дошка угод у CRM для нерухомості - стадії від нового ліда до закритої угоди',
     'Deal kanban board in a real estate CRM - stages from a new lead to a closed deal',
     'Канбан-дошка угод: пʼять стадій від нового ліда до закритої угоди. Картку можна перетягнути '
     'у наступну стадію, над кожною колонкою - кількість угод і їхня сума.',
     'Deal kanban: five stages from a new lead to a closed deal. A card can be dragged into the next '
     'stage, and each column header shows the number of deals and their total value.'),
    ('listings',
     'Каталог обʼєктів нерухомості у CRM - картки квартир, будинків і комерції з фільтрами',
     'Property catalogue in the CRM - cards for flats, houses and commercial units with filters',
     'Каталог обʼєктів: квартири, будинки, комерція й ділянки з фільтрами за типом, статусом продажу, '
     'площею, поверхом і ціною. На кожній картці - кількість переглядів і відповідальний агент.',
     'Property catalogue: flats, houses, commercial units and land plots, filtered by type, sale status, '
     'area, floor and price. Each card shows the view count and the agent in charge.'),
    ('clients',
     'База клієнтів у CRM для рієлторів - покупці та продавці з бюджетом і статусом угоди',
     'Client database in a CRM for realtors - buyers and sellers with budget and deal status',
     'База клієнтів: покупці, продавці й обміни. По кожному записі - запит, бюджет, статус угоди, '
     'відповідальний агент і дата появи в базі; є пошук, фільтри за типом і експорт.',
     'Client database: buyers, sellers and exchanges. Every record carries the request, the budget, the deal '
     'status, the agent in charge and the date it entered the database; search, type filters and export included.'),
    ('reports',
     'Звіти по джерелах заявок у CRM для агентства нерухомості - план/факт і продажі за районами',
     'Request-source reports in a real estate agency CRM - plan versus actual and sales by district',
     'Звіти: план/факт за обсягом угод по місяцях, джерела заявок (OLX, сайт агенції, рекомендації, '
     'Instagram, Google Ads) і розподіл продажів за районами міста.',
     'Reports: plan versus actual deal volume by month, request sources (OLX, the agency website, referrals, '
     'Instagram, Google Ads) and the distribution of sales across city districts.'),
    ('agents',
     'Аналітика по агентах у CRM для нерухомості - закриті угоди, комісія та рейтинг',
     'Per-agent analytics in a real estate CRM - closed deals, commission and rating',
     'Агенти: закриті угоди, обсяг, комісія, середній час відповіді й рейтинг по кожному агенту, '
     'плюс зведений графік результатів команди за місяць.',
     'Agents: closed deals, volume, commission, average response time and rating for every agent, '
     'plus a combined chart of the team’s results for the month.'),
]:
    CASES['kvadratnyi-metr']['shots'][_f] = shot(_f, 'wide', _a_uk, _a_en, _c_uk, _c_en)

CASES['kvadratnyi-metr']['body'] = [
    ('h2', 'Як виглядає інтерфейс', 'How the interface looks'),
    ('shots', None, ['dashboard', 'kanban', 'listings', 'clients', 'reports', 'agents']),
    ('h2', 'Що вміє система', 'What the system can do'),
    ('list', [
        ('Єдина воронка заявок: новий лід → перегляд обʼєкта → торг → завдаток → угода закрита, '
         'з наскрізною конверсією і відсівом на кожному переході',
         'A single request funnel: new lead → viewing → negotiation → deposit → deal closed, with end-to-end '
         'conversion and drop-off at every step'),
        ('Канбан-дошка угод із перетягуванням карток між стадіями та сумою угод по кожній стадії',
         'A deal kanban board with drag-and-drop between stages and the total deal value per stage'),
        ('Каталог обʼєктів: квартири, будинки, комерція, ділянки - з фільтрами, статусами продажу й переглядами',
         'A property catalogue: flats, houses, commercial units and land plots - with filters, sale statuses and view counts'),
        ('База покупців і продавців: тип клієнта, запит, бюджет, відповідальний агент, дата в базі',
         'A buyer and seller database: client type, request, budget, agent in charge and the date added'),
        ('Аналітика по агентах: закриті угоди, обсяг, комісія, середній час відповіді, рейтинг',
         'Per-agent analytics: closed deals, volume, commission, average response time and rating'),
        ('Звіти план/факт за обсягом угод і розподіл продажів за районами міста',
         'Plan-versus-actual reports on deal volume and the distribution of sales across city districts'),
        ('Джерела заявок з часткою кожного канала - видно, який трафік реально приносить угоди',
         'Request sources with the share of each channel - it shows which traffic actually brings deals'),
        ('Контроль часу відповіді на заявку: норматив, факт і графік за останні 14 днів',
         'Response-time control: the target, the actual value and a chart for the last 14 days'),
        ('Пошук за адресою, клієнтом і номером заявки та експорт бази й звітів',
         'Search by address, client and request number, plus export of the database and reports'),
    ]),
]

# ------------------------------------------------------------------ Velvet Studio
CASES['zapys-salon-krasy'] = dict(
    date='2026-08-09',
    tag_uk='Бʼюті та послуги', tag_en='Beauty and services',
    cta_uk='Хочете такий самий сервіс запису для свого бізнесу? Звʼяжіться з нами',
    cta_en='Want the same booking service for your business? Get in touch',
    h1_uk='Telegram Mini App для запису в бʼюті-салон «Velvet Studio»',
    h1_en='A Telegram Mini App for booking a beauty salon: Velvet Studio',
    title_uk='Telegram Mini App для запису в салон краси - кейс | Devlly',
    title_en='Telegram Mini App for beauty salon booking - case study | Devlly',
    desc_uk='Кейс Devlly: Telegram Mini App для запису в бʼюті-салон - вибір послуги, майстра і вільного часу, '
            'Google Таблиця замість адмінки, бот власника зі статистикою і автоматичні нагадування клієнтам.',
    desc_en='A Devlly case study: a Telegram Mini App for booking a beauty salon - choosing a service, a specialist '
            'and a free slot, a Google Sheet instead of an admin panel, an owner bot with statistics and automatic reminders.',
    keywords_uk='telegram mini app для салону краси, онлайн запис у салон краси, бот для запису клієнтів, '
                'автоматизація салону краси, запис до майстра через telegram, кейс mini app для бʼюті-салону, '
                'система онлайн запису на послуги',
    keywords_en='telegram mini app for a beauty salon, online booking for a beauty salon, appointment booking bot, '
                'beauty salon automation, telegram booking system, mini app case study, service booking system',
    lead_uk='«Velvet Studio» - сервіс запису в салон краси, який живе повністю в Telegram. Клієнт відкриває Mini App, '
            'обирає послугу, майстра і вільний час, підтверджує запис і одразу отримує деталі візиту в чат. '
            'Запис лягає в Google Таблицю салону, а власник бачить розклад і статистику в тому самому боті. '
            'Ані дзвінків, ані окремого застосунку, ані паперового журналу.',
    lead_en='Velvet Studio is a beauty salon booking service that lives entirely inside Telegram. A client opens the Mini App, '
            'picks a service, a specialist and a free slot, confirms the booking and instantly receives the visit details in chat. '
            'The booking lands in the salon’s Google Sheet, while the owner sees the schedule and the statistics in the same bot. '
            'No phone calls, no separate app, no paper diary.',
    who_uk='Кому підходить: салонам краси, барбершопам, студіям манікюру, масажним і косметологічним кабінетам, '
           'а також будь-якому бізнесу, що працює за записом - від СТО до репетиторів. Особливо тим, хто досі '
           'приймає записи в директі й вручну звіряє, чи вільний майстер.',
    who_en='Who it fits: beauty salons, barbershops, nail studios, massage and cosmetology practices, and any other '
           'business that runs on appointments - from car services to private tutors. Especially those still taking '
           'bookings in direct messages and checking a specialist’s availability by hand.',
    stack=['Python', 'aiogram', 'FastAPI', 'Telegram Mini App', 'Google Sheets API', 'APScheduler'],
    stack_uk='Стек: Python і aiogram для бота, FastAPI для бекенду Mini App, Google Sheets API замість бази даних, '
             'APScheduler для нагадувань.',
    stack_en='Stack: Python with aiogram for the bot, FastAPI for the Mini App back end, the Google Sheets API instead of '
             'a database and APScheduler for reminders.',
    shots={},
)

for _f, _cls, _a_uk, _a_en, _c_uk, _c_en in [
    ('app-start', 'app',
     'Telegram Mini App для запису в салон краси - головний екран з адресою і графіком роботи',
     'Telegram Mini App for booking a beauty salon - home screen with the address and opening hours',
     'Головний екран: опис салону, адреса, години роботи і телефон. Кнопка «Записатися» відкриває сценарій запису.',
     'Home screen: a short description of the salon, the address, the opening hours and the phone number. '
     'The booking flow starts from the button below.'),
    ('app-service', 'app',
     'Онлайн запис у салон краси - вибір послуги з ціною і тривалістю в Telegram Mini App',
     'Online beauty salon booking - choosing a service with its price and duration in a Telegram Mini App',
     'Крок 1: перелік послуг із ціною, тривалістю і категорією. Дані підтягуються з Google Таблиці салону.',
     'Step 1: the list of services with the price, the duration and the category. The data is pulled from the salon’s Google Sheet.'),
    ('app-datetime', 'app',
     'Telegram Mini App запис у салон краси - календар з вільними слотами і вибір часу',
     'Telegram Mini App beauty salon booking - a calendar with free slots and time selection',
     'Крок 3: календар показує лише робочі дні майстра, а сітка часу - лише слоти, що реально вільні.',
     'Step 3: the calendar only shows the days the specialist works, and the time grid only shows slots that are genuinely free.'),
    ('app-success', 'app',
     'Підтвердження онлайн запису в салон краси - деталі візиту в Telegram Mini App',
     'Confirmed beauty salon booking - the visit details inside the Telegram Mini App',
     'Екран успіху: номер запису, послуга, майстер, дата і час, адреса та сума до сплати.',
     'Success screen: the booking number, the service, the specialist, the date and time, the address and the amount due.'),
    ('bot-client-notice', 'bot1',
     'Telegram-бот салону краси - повідомлення клієнту про підтверджений запис',
     'Beauty salon Telegram bot - the booking confirmation message sent to the client',
     'Одразу після запису клієнт отримує підтвердження в чат, а за добу до візиту - нагадування тим самим ботом.',
     'Right after booking the client receives a confirmation in chat, and a day before the visit the same bot sends a reminder.'),
    ('sheet-bookings', 'sheet',
     'Google Таблиця як бекофіс салону краси - аркуш записів клієнтів зі статусами',
     'A Google Sheet as the beauty salon back office - the bookings sheet with statuses',
     'Аркуш «Записи»: кожен запис - окремий рядок з ID, контактами клієнта, послугою, майстром, датою, '
     'ціною, статусом і позначкою про надіслане нагадування.',
     'The bookings sheet: every booking is a row carrying an ID, the client’s contacts, the service, the specialist, '
     'the date, the price, the status and a flag for the reminder already sent.'),
    ('bot-panel', 'bot',
     'Бот-панель власника салону краси - меню керування записами в Telegram',
     'Owner bot panel for a beauty salon - the booking management menu in Telegram',
     'Панель власника: записи на сьогодні і завтра, вибір довільного дня, вільні слоти, статистика '
     'і примусове перечитування даних з таблиці.',
     'The owner panel: today’s and tomorrow’s bookings, any other day on request, free slots, statistics '
     'and a forced re-read of the sheet.'),
    ('bot-stats', 'bot',
     'Бот-панель власника салону - статистика записів, виручки і топ майстрів за період',
     'Owner bot panel for a salon - booking, revenue and top specialist statistics for a period',
     'Статистика за 30 днів: записи в розрізі статусів, унікальні клієнти, зароблена й очікувана сума, '
     'топ послуг і топ майстрів.',
     'Statistics for 30 days: bookings by status, unique clients, the amount earned and the amount pending, '
     'the top services and the top specialists.'),
]:
    CASES['zapys-salon-krasy']['shots'][_f] = shot(_f, _cls, _a_uk, _a_en, _c_uk, _c_en)

CASES['zapys-salon-krasy']['body'] = [
    ('h2', 'Як влаштована система', 'How the system is put together'),
    ('p', 'Система складається з трьох частин, які працюють з одними й тими самими даними: Mini App, у якому '
          'записується клієнт, Google Таблиця, де ці записи живуть, і Telegram-бот, через який салон їх бачить '
          'і рахує. Жодну з частин не треба відкривати окремо - усе всередині Telegram.',
          'The system has three parts working on the same data: the Mini App where the client books, the Google Sheet '
          'where those bookings live, and the Telegram bot the salon uses to see and count them. None of the parts '
          'needs to be opened separately - everything sits inside Telegram.'),

    ('h3', '1. Mini App для клієнта', '1. The Mini App for the client'),
    ('p', 'Запис відкривається прямо з чату бота і виглядає як застосунок салону, а не як переписка. '
          'Сценарій - пʼять кроків: послуга, майстер, дата і час, контактні дані, підтвердження. Ціна і тривалість '
          'видно з першого кроку, тож клієнт розуміє, у що обійдеться візит, ще до того, як його підтвердить.',
          'Booking opens straight from the bot chat and looks like the salon’s own app rather than a conversation. '
          'The flow has five steps: service, specialist, date and time, contact details, confirmation. The price and '
          'the duration are visible from the first step, so the client knows the cost of the visit before confirming it.'),
    ('p', 'Список майстрів фільтрується під обрану послугу - клієнт бачить лише тих, хто її виконує. Календар '
          'відкриває тільки робочі дні майстра, а сітка часу враховує тривалість послуги, індивідуальний графік '
          'і вже наявні записи, тому зайнятих годин у ній просто немає.',
          'The list of specialists is filtered by the chosen service, so the client only sees the people who actually '
          'perform it. The calendar only opens the days that specialist works, and the time grid accounts for the length '
          'of the service, the individual schedule and the existing bookings - busy hours simply never appear.'),
    ('shots', 'col-6 col-xl-3', ['app-start', 'app-service', 'app-datetime', 'app-success']),
    ('shots', 'col-12 col-md-8 col-xl-5 mx-auto', ['bot-client-notice']),

    ('h3', '2. Google Таблиця як бекофіс', '2. A Google Sheet as the back office'),
    ('p', 'Окремої адмінки в системі немає, і це свідоме рішення. Бекофісом працює звичайна Google Таблиця з '
          'аркушів «Майстри», «Послуги», «Записи» і «Налаштування». Адміністратор редагує її так само, як редагував '
          'би будь-яку таблицю, - вчити новий інтерфейс не треба нікому.',
          'There is no separate admin panel, and that is a deliberate choice. The back office is an ordinary Google Sheet '
          'with tabs for specialists, services, bookings and settings. The administrator edits it exactly as they would edit '
          'any spreadsheet - nobody has to learn a new interface.'),
    ('p', 'Змінили ціну послуги, додали майстра або закрили день - Mini App і бот бачать це відразу. Кожен запис '
          'лягає окремим рядком, який можна відсортувати, відфільтрувати чи вивантажити, а історія лишається в '
          'акаунті салону, а не в чужій системі.',
          'Change a price, add a specialist or close a day - the Mini App and the bot pick it up at once. Every booking '
          'is a separate row that can be sorted, filtered or exported, and the history stays in the salon’s own account '
          'rather than in somebody else’s system.'),
    ('shots', None, ['sheet-bookings']),

    ('h3', '3. Telegram-бот для власника', '3. The Telegram bot for the owner'),
    ('p', 'Власник керує салоном з того самого бота. Команда запуску відкриває панель: записи на сьогодні і на завтра, '
          'вибір довільного дня, вільні слоти і статистика. Окрема кнопка примусово перечитує таблицю, якщо '
          'адміністратор щойно щось у ній змінив.',
          'The owner runs the salon from the same bot. The start command opens the panel: today’s and tomorrow’s bookings, '
          'any other day, free slots and statistics. A separate button forces a re-read of the sheet if the administrator '
          'has just changed something in it.'),
    ('p', 'Статистика рахується за період - сьогодні, наступні сім днів, останні сім або тридцять. У зведенні: '
          'кількість записів у розрізі статусів, унікальні клієнти, зароблена й очікувана сума, топ послуг і топ '
          'майстрів. Цифри беруться з тих самих рядків таблиці, тому звіряти їх ні з чим не треба.',
          'Statistics are calculated per period - today, the next seven days, the last seven or the last thirty. The summary '
          'shows the number of bookings by status, unique clients, the amount earned and the amount pending, the top services '
          'and the top specialists. The figures come from the very same rows of the sheet, so there is nothing to reconcile.'),
    ('shots', 'col-md-6', ['bot-panel', 'bot-stats']),

    ('h2', 'Ключова логіка', 'The logic that matters'),
    ('list', [
        ('Захист від подвійного запису: слот перевіряється ще раз у момент підтвердження, тож двоє клієнтів не '
         'потраплять до одного майстра на одну годину, навіть якщо записуються одночасно',
         'Double-booking protection: the slot is checked again at the moment of confirmation, so two clients cannot land '
         'on the same specialist at the same hour even if they book simultaneously'),
        ('Статуси запису: очікує → підтверджено → завершено або скасовано. Статус змінюється в таблиці, і статистика '
         'перераховується за ним автоматично',
         'Booking statuses: pending → confirmed → completed or cancelled. The status is changed in the sheet and the '
         'statistics are recalculated from it automatically'),
        ('Автоматичне нагадування за 24 години до візиту: шедулер сам знаходить завтрашні записи, надсилає клієнту '
         'повідомлення і ставить у таблиці позначку, щоб не надіслати його вдруге',
         'An automatic reminder 24 hours before the visit: the scheduler finds tomorrow’s bookings, sends the client a '
         'message and marks the row so the reminder is never sent twice'),
    ]),

    ('h2', 'Що вміє система', 'What the system can do'),
    ('list', [
        ('Запис у пʼять кроків прямо в Telegram - без сайту, окремого застосунку і дзвінків',
         'A five-step booking right inside Telegram - no website, no separate app, no phone calls'),
        ('Каталог послуг з ціною, тривалістю, описом і категорією, який редагується в таблиці',
         'A service catalogue with price, duration, description and category, all editable in the sheet'),
        ('Картки майстрів: спеціалізація, рейтинг, графік по днях тижня, вихідні і власний перелік послуг',
         'Specialist profiles: specialisation, rating, a weekday schedule, days off and their own list of services'),
        ('Фільтрація майстрів під обрану послугу - клієнт бачить лише тих, хто її виконує',
         'Specialists filtered by the chosen service - the client only sees those who perform it'),
        ('Сітка вільного часу з урахуванням тривалості послуги, графіка майстра і вже наявних записів',
         'A free-slot grid that accounts for the length of the service, the specialist’s schedule and existing bookings'),
        ('Підтвердження клієнту в Telegram з номером запису, послугою, майстром, адресою і сумою',
         'A Telegram confirmation for the client with the booking number, the service, the specialist, the address and the amount'),
        ('Панель власника: записи на сьогодні, на завтра і на будь-який обраний день, а також вільні слоти',
         'An owner panel: bookings for today, for tomorrow and for any chosen day, plus the free slots'),
        ('Статистика за період: записи по статусах, унікальні клієнти, виручка, топ послуг і топ майстрів',
         'Statistics per period: bookings by status, unique clients, revenue, top services and top specialists'),
        ('Google Таблиця замість адмінки: дані салону лишаються в його власному акаунті',
         'A Google Sheet instead of an admin panel: the salon’s data stays in the salon’s own account'),
    ]),
]


# ------------------------------------------------------------------- DropUnion App
CASES['dropunion-app'] = dict(
    date='2026-08-23',
    tag_uk='Ecommerce і дропшипінг', tag_en='Ecommerce and dropshipping',
    cta_uk='Хочете свій магазин або таку саму платформу? Звʼяжіться з нами',
    cta_en='Want your own store or the same platform? Get in touch',
    h1_uk='DropUnion App - магазин у Telegram для продавців одягу',
    h1_en='DropUnion App - a Telegram store for clothing sellers',
    title_uk='Telegram-магазин з Mini App - кейс DropUnion App | Devlly',
    title_en='A Telegram store with a Mini App - the DropUnion App case study | Devlly',
    desc_uk='Кейс Devlly: SaaS-платформа, у якій продавець за кілька хвилин отримує власний магазин '
            'у Telegram - вітрина Mini App, каталог з MyDrop або Google Sheets, замовлення зі статусами, '
            'Нова пошта і підписка з автосписанням.',
    desc_en='A Devlly case study: a SaaS platform where a seller gets their own Telegram store in minutes - '
            'a Mini App storefront, a catalogue from MyDrop or Google Sheets, orders with statuses, '
            'Nova Poshta delivery and a recurring subscription.',
    keywords_uk='telegram магазин, mini app інтернет-магазин, бот для продажу одягу, дропшипінг у телеграм, '
                'інтеграція mydrop, telegram mini app магазин приклад, кейс telegram магазину, '
                'saas платформа для продавців',
    keywords_en='telegram store, mini app online store, bot for selling clothes, dropshipping in telegram, '
                'mydrop integration, telegram mini app store example, telegram store case study, '
                'saas platform for sellers',
    lead_uk='DropUnion App - це не один магазин, а платформа, з якої їх виростає скільки завгодно. '
            'Продавець реєструється в боті, отримує персональне посилання - і покупець, відкривши його, '
            'потрапляє у вітрину саме цього магазину прямо в Telegram. Каталог можна вести руками, '
            'а можна підтягнути з MyDrop чи Google Таблиці; замовлення, статуси, доставка Новою поштою '
            'і оплата підписки працюють автоматично.',
    lead_en='DropUnion App is not a single store but a platform that grows any number of them. '
            'A seller registers in the bot and receives a personal link - and a buyer who opens it lands '
            'in that specific storefront right inside Telegram. The catalogue can be kept by hand or pulled '
            'from MyDrop or a Google Sheet; orders, statuses, Nova Poshta delivery and subscription billing '
            'run on their own.',
    who_uk='Кому підходить: продавцям одягу, взуття й аксесуарів, які торгують з Instagram і Telegram та '
           'приймають замовлення в директі; дропшиперам, що працюють на чужому складі; а також тим, хто хоче '
           'запустити власну платформу з підпискою, а не один магазин.',
    who_en='Who it fits: clothing, footwear and accessory sellers who trade through Instagram and Telegram and '
           'take orders in direct messages; dropshippers working off somebody else’s stock; and anyone who wants '
           'to launch a subscription platform of their own rather than a single store.',
    stack=['Python', 'aiogram', 'FastAPI', 'PostgreSQL', 'React', 'Telegram Mini App',
           'MyDrop API', 'Nova Poshta API', 'WayForPay'],
    stack_uk='Стек: Python і aiogram для бота, FastAPI і PostgreSQL на бекенді, React + Vite для Mini App, '
             'інтеграції з MyDrop, Google Sheets, Новою поштою і WayForPay.',
    stack_en='Stack: Python with aiogram for the bot, FastAPI and PostgreSQL on the back end, React with Vite '
             'for the Mini App, and integrations with MyDrop, Google Sheets, Nova Poshta and WayForPay.',
    shots={},
)

for _f, _h, _a_uk, _a_en, _c_uk, _c_en in [
    ('app-home', 1015,
     'Вітрина Telegram-магазину одягу - головний екран Mini App з банером і категоріями',
     'A Telegram clothing store front - the Mini App home screen with a banner and categories',
     'Головна вітрини: банер із власним фото і текстом магазину, категорії, які збираються з категорій '
     'товарів, і блок популярного. Акцентний колір кнопок продавець задає сам у боті.',
     'The storefront home: a banner with the shop’s own photo and text, categories assembled from the '
     'product categories, and a popular block. The seller picks the accent colour in the bot.'),
    ('app-catalog', 1014,
     'Каталог товарів у Telegram Mini App - пошук, фільтри і картки з цінами',
     'Product catalogue in a Telegram Mini App - search, filters and cards with prices',
     'Каталог: пошук, фільтри «Новинки», «Популярне» і «Знижки», підвантаження порціями. У цього магазину '
     '4 849 позицій - каталог підтягнутий з MyDrop, а не заведений руками.',
     'The catalogue: search, the New, Popular and Sale filters, and paged loading. This shop holds 4,849 '
     'items - the catalogue is pulled from MyDrop rather than typed in by hand.'),
    ('app-product', 1014,
     'Картка товару в Telegram-магазині - фото, ціна, вибір розміру і кнопки купівлі',
     'Product page in a Telegram store - photo, price, size picker and purchase buttons',
     'Картка товару: фото, ціна, вибір розміру з тих, що є в наявності, кількість і дві дії - «Купити зараз» '
     'одразу на оформлення або «Додати в кошик». Якщо на товар є знижка, стара ціна показується закресленою.',
     'The product page: photos, price, a size picker limited to what is in stock, quantity and two actions - '
     'buy now, straight to checkout, or add to cart. If the item is on sale, the old price is struck through.'),
    ('app-cart', 1016,
     'Кошик у Telegram Mini App - список товарів, доставка і сума замовлення',
     'Cart in a Telegram Mini App - the item list, delivery and the order total',
     'Кошик: обраний розмір і колір видно в кожному рядку, кількість змінюється на місці, доставка й сума '
     'перераховуються одразу. Далі - чекаут з автокомплітом міста і відділення Нової пошти.',
     'The cart: the chosen size and colour show in every row, quantity changes in place, delivery and the total '
     'are recalculated at once. Checkout follows, with autocomplete for the Nova Poshta city and branch.'),
    ('bot-menu', 1030,
     'Бот продавця Telegram-магазину - головне меню з товарами і замовленнями',
     'Seller bot of a Telegram store - the main menu with products and orders',
     'Головне меню продавця: товари, замовлення, персональне посилання на магазин, налаштування і довідка. '
     'У вітанні - скільки днів лишилось до кінця оплаченого періоду.',
     'The seller’s main menu: products, orders, the personal shop link, settings and the manual. The greeting '
     'shows how many days are left in the paid period.'),
    ('bot-settings', 1030,
     'Налаштування магазину в Telegram-боті - реквізити, вітрина, інтеграції та підписка',
     'Store settings in a Telegram bot - payment details, storefront, integrations and subscription',
     'Налаштування магазину: реквізити, на які покупці переказують оплату, вигляд вітрини (акцентний колір, '
     'банер і текст під назвою), джерела каталогу та підписка. Зміни у вітрині покупці бачать одразу.',
     'Store settings: the payment details buyers transfer to, the storefront look (accent colour, banner and the '
     'line under the name), the catalogue sources and the subscription. Storefront changes reach buyers at once.'),
    ('bot-link', 1030,
     'Персональне посилання на Telegram-магазин продавця у боті платформи',
     'The seller’s personal Telegram store link inside the platform bot',
     'Персональне посилання магазину. Один бот обслуговує всіх продавців: токен усередині посилання й вирішує, '
     'чию вітрину відкриє покупець. На знімку токен приховано - посилання робоче.',
     'The shop’s personal link. One bot serves every seller: the token inside the link decides whose storefront '
     'the buyer opens. The token is masked in the screenshot because the link is live.'),
    ('bot-guide', 1030,
     'Вбудована інструкція для продавця в Telegram-боті - розділи довідки',
     'The built-in seller manual in the Telegram bot - the help sections',
     'Довідка вбудована в бот і розбита на розділи - початок роботи, налаштування магазину, товари, інтеграції, '
     'замовлення й підписка. Продавцю не треба шукати інструкцію деінде.',
     'The manual is built into the bot and split into sections - getting started, store settings, products, '
     'integrations, orders and the subscription. The seller never has to look for instructions elsewhere.'),
]:
    CASES['dropunion-app']['shots'][_f] = shot(_f, 'phone', _a_uk, _a_en, _c_uk, _c_en, h=_h)

CASES['dropunion-app']['body'] = [
    ('h2', 'Як влаштована платформа', 'How the platform is put together'),
    ('p', 'Ключове рішення - один бот на всіх. Продавець не отримує окремого бота, якого треба реєструвати, '
          'хостити й оновлювати: він реєструється в спільному боті платформи і отримує посилання зі своїм '
          'токеном. Покупець відкриває це посилання і бачить вітрину саме цього магазину - з його товарами, '
          'банером і кольорами. Магазинів у системі може бути скільки завгодно, і жоден не знає про інші.',
          'The key decision is a single bot for everyone. A seller does not get a separate bot to register, host '
          'and update: they sign up in the platform’s shared bot and receive a link carrying their own token. '
          'A buyer opens that link and sees exactly that shop - its products, its banner, its colours. The system '
          'can hold any number of stores, and none of them knows about the others.'),
    ('p', 'Далі система розпадається на дві половини, які працюють з однією базою: вітрина, у якій купує клієнт, '
          'і бот, у якому продавець веде магазин. Ані клієнту, ані продавцю не треба ставити застосунок чи '
          'відкривати сайт - усе відбувається всередині Telegram.',
          'From there the system splits into two halves working on one database: the storefront where the client '
          'buys and the bot where the seller runs the shop. Neither side installs an app or opens a website - it '
          'all happens inside Telegram.'),

    ('h3', '1. Вітрина покупця', '1. The buyer’s storefront'),
    ('p', 'Вітрина - це Telegram Mini App на React: головна з банером і категоріями, каталог з пошуком і '
          'фільтрами, картка товару з розмірами й кольорами, кошик і чекаут. Категорії окремо ніхто не заводить - '
          'вони збираються з категорій самих товарів, тож список у вітрині завжди відповідає тому, що є в '
          'наявності.',
          'The storefront is a React Telegram Mini App: a home screen with a banner and categories, a catalogue '
          'with search and filters, a product page with sizes and colours, a cart and checkout. Nobody maintains '
          'the category list separately - it is assembled from the products themselves, so it always matches '
          'what is actually in stock.'),
    ('p', 'Оформлення замовлення враховує українську специфіку: місто й відділення Нової пошти підказуються з '
          'локальної бази відділень, а не запитом до чужого API на кожну літеру. Якщо продавець увімкнув '
          'підтвердження оплати, покупець зобовʼязаний прикріпити скріншот переказу - без нього замовлення '
          'просто не створиться.',
          'Checkout is built for the Ukrainian market: the Nova Poshta city and branch are suggested from a local '
          'copy of the branch database rather than an external API call on every keystroke. If the seller has '
          'turned on payment confirmation, the buyer must attach a screenshot of the transfer - without it the '
          'order is simply not created.'),
    ('shots', 'col-6 col-xl-3', ['app-home', 'app-catalog', 'app-product', 'app-cart']),

    ('h3', '2. Бот продавця замість адмінки', '2. The seller bot instead of an admin panel'),
    ('p', 'Окремої адмінки в системі немає - магазин повністю керується з бота. Товари додаються покроково '
          '(назва, опис, ціна, категорія, фото, розміри, кольори, наявність), будь-який крок можна пропустити, '
          'а вже додану картку - відредагувати по одному полю, сховати з вітрини або видалити.',
          'There is no separate admin panel - the shop is run entirely from the bot. Products are added step by '
          'step (name, description, price, category, photos, sizes, colours, availability), any step can be '
          'skipped, and an existing card can be edited field by field, hidden from the storefront or deleted.'),
    ('p', 'Вигляд вітрини теж налаштовується з бота: акцентний колір кнопок, фото банера і рядок під назвою '
          'магазину. Змінили - покупці бачать це одразу, нічого перезапускати не треба. Довідка теж живе '
          'усередині бота, тож продавцю не доводиться шукати інструкцію деінде.',
          'The storefront look is configured from the bot as well: the accent colour of the buttons, the banner '
          'photo and the line under the shop name. Change it and buyers see the result at once, with nothing to '
          'restart. The manual lives inside the bot too, so the seller never has to look for instructions '
          'elsewhere.'),
    ('shots', 'col-6 col-xl-3', ['bot-menu', 'bot-settings', 'bot-link', 'bot-guide']),

    ('h3', '3. Звідки береться каталог', '3. Where the catalogue comes from'),
    ('p', 'Каталог можна вести руками, але сенс платформи в іншому: підключити готове джерело і не займатися '
          'товарами взагалі. Джерел три - MyDrop у ролі постачальника (свій склад), MyDrop у ролі дропшипера '
          '(чужий склад плюс ваша націнка у відсотках або фіксованою сумою), YML-фід і звичайна Google Таблиця, '
          'у якій бот сам визначає, де яка колонка.',
          'The catalogue can be kept by hand, but the point of the platform is different: connect a ready source '
          'and stop dealing with products at all. There are three sources - MyDrop as a vendor (your own stock), '
          'MyDrop as a dropshipper (somebody else’s stock plus your markup, as a percentage or a fixed amount), '
          'a YML feed and an ordinary Google Sheet in which the bot works out the columns by itself.'),
    ('p', 'Активним може бути лише одне джерело, і при перемиканні попередній імпорт видаляється, щоб у вітрині '
          'не лишалося товарів, яких уже ніхто не постачає. Товари, додані руками, при цьому лишаються на місці. '
          'Каталог і залишки оновлюються самі раз на пів години.',
          'Only one source can be active at a time, and switching wipes the previous import so the storefront '
          'never keeps items nobody supplies any more. Manually added products stay where they are. The catalogue '
          'and stock levels refresh themselves every half hour.'),

    ('h3', '4. Замовлення, доставка й гроші', '4. Orders, delivery and money'),
    ('p', 'Щойно покупець оформив замовлення, продавцю приходить картка з контактами, переліком товарів, містом '
          'і способом доставки - і скріншотом оплати, якщо той увімкнений. Статуси змінюються кнопками просто '
          'під карткою, і на кожній зміні покупець автоматично отримує повідомлення від імені магазину.',
          'The moment a buyer places an order, the seller receives a card with the contacts, the items, the city '
          'and the delivery method - plus the payment screenshot if that option is on. Statuses change with '
          'buttons right under the card, and every change automatically notifies the buyer on behalf of the shop.'),
    ('p', 'Якщо підключено MyDrop, статуси синхронізуються в обидва боки, а номер накладної підтягується сам - '
          'продавцю не треба переносити замовлення руками ні туди, ні назад.',
          'With MyDrop connected, statuses sync both ways and the waybill number is pulled in automatically - '
          'the seller never moves an order between systems by hand.'),

    ('h3', '5. Підписка як бізнес-модель', '5. The subscription as the business model'),
    ('p', 'Платформа заробляє на підписці: перші дні безкоштовні й без картки, далі вмикається автосписання '
          'через WayForPay. Якщо платіж не пройшов, система пробує ще, до трьох разів, і пише продавцю причину; '
          'після скасування магазин працює до кінця вже оплаченого періоду, а не вимикається тієї ж хвилини.',
          'The platform earns from subscriptions: the first days are free and require no card, after which '
          'recurring billing through WayForPay kicks in. If a payment fails, the system retries up to three times '
          'and tells the seller why; after a cancellation the shop keeps working until the end of the period '
          'already paid for rather than shutting down on the spot.'),

    ('h2', 'Ключова логіка', 'The logic that matters'),
    ('list', [
        ('Мультитенантність на одному боті: токен у посиланні визначає магазин, тому запуск нового продавця '
         'не потребує ані нового бота, ані окремого деплою',
         'Multi-tenancy on a single bot: the token in the link identifies the shop, so onboarding a new seller '
         'needs neither a new bot nor a separate deployment'),
        ('Ручні й імпортовані товари розділені: зміна або скидання джерела каталогу не чіпає те, що продавець '
         'завів сам',
         'Manual and imported products are kept apart: changing or resetting the catalogue source never touches '
         'what the seller entered by hand'),
        ('Автосписання з повторними спробами і зрозумілим повідомленням про причину відмови замість тихого '
         'відключення магазину',
         'Recurring billing with retries and a clear message about why a charge failed, instead of silently '
         'switching the shop off'),
        ('Відділення Нової пошти зберігаються локально й оновлюються за розкладом - чекаут не залежить від '
         'доступності зовнішнього API',
         'Nova Poshta branches are stored locally and refreshed on a schedule - checkout does not depend on an '
         'external API being up'),
    ]),

    ('h2', 'Що вміє платформа', 'What the platform can do'),
    ('list', [
        ('Власний магазин у Telegram для кожного продавця - вітрина Mini App за персональним посиланням',
         'A personal Telegram store for every seller - a Mini App storefront behind their own link'),
        ('Каталог з пошуком, фільтрами новинок, популярного і знижок та підвантаженням порціями',
         'A catalogue with search, filters for new, popular and discounted items, and paged loading'),
        ('Картка товару з кількома фото, розмірами, кольорами, залишками і закресленою старою ціною при знижці',
         'A product page with multiple photos, sizes, colours, stock levels and a struck-through old price on sale'),
        ('Кошик і чекаут з автокомплітом міста та відділення Нової пошти',
         'A cart and checkout with autocomplete for the Nova Poshta city and branch'),
        ('Імпорт каталогу з MyDrop (постачальник або дропшипер з націнкою), YML-фіда чи Google Таблиці',
         'Catalogue import from MyDrop (vendor or dropshipper with a markup), a YML feed or a Google Sheet'),
        ('Автооновлення цін і залишків кожні 30 хвилин без участі продавця',
         'Automatic price and stock updates every 30 minutes with no seller involvement'),
        ('Замовлення зі статусами нове → підтверджено → відправлено → доставлено і автосповіщенням покупцю',
         'Orders with statuses new → confirmed → shipped → delivered and automatic buyer notifications'),
        ('Двобічна синхронізація статусів і накладних з MyDrop',
         'Two-way synchronisation of statuses and waybills with MyDrop'),
        ('Налаштування вигляду вітрини з бота: акцентний колір, банер і текст під назвою магазину',
         'Storefront styling from the bot: accent colour, banner and the line under the shop name'),
        ('Підписка з безкоштовним періодом, автосписанням WayForPay, повторними спробами і скасуванням у два кліки',
         'A subscription with a free period, WayForPay recurring billing, retries and a two-click cancellation'),
    ]),
]


# ---------------------------------------------------------------- NovaFit Ads Dashboard
CASES['novafit-ads-dashboard'] = dict(
    date='2026-09-20',
    tag_uk='Маркетинг і аналітика', tag_en='Marketing and analytics',
    cta_uk='Хочете такий самий контроль над своєю рекламою? Звʼяжіться з нами',
    cta_en='Want the same control over your ad spend? Get in touch',
    h1_uk='NovaFit - моніторинг реклами Google Ads і Meta Ads',
    h1_en='NovaFit - Google Ads and Meta Ads performance monitoring',
    title_uk='Моніторинг реклами з алертами в Telegram - кейс NovaFit | Devlly',
    title_en='Ad performance monitoring with Telegram alerts - the NovaFit case study | Devlly',
    desc_uk='Кейс Devlly: дашборд ефективності реклами Google Ads і Meta Ads у Google Таблиці, автоматична '
            'детекція відхилень CPA і ROAS за ковзною медіаною та Telegram-бот зі щоденним звітом і алертами.',
    desc_en='A Devlly case study: a Google Ads and Meta Ads performance dashboard in a Google Sheet, automatic '
            'CPA and ROAS anomaly detection against a rolling median, and a Telegram bot with a daily report and alerts.',
    keywords_uk='моніторинг реклами, дашборд google ads meta ads, алерти cpa roas, контроль рекламного бюджету, '
                'звіт по рекламі в telegram, аналітика реклами в google таблиці, автоматизація маркетингу кейс',
    keywords_en='ad performance monitoring, google ads meta ads dashboard, cpa roas alerts, ad budget control, '
                'telegram ad report, ad analytics in google sheets, marketing automation case study',
    lead_uk='NovaFit крутить рекламу одночасно в Google Ads і Meta Ads, і до цієї системи стан кампаній перевірявся '
            'руками - у двох кабінетах, по черзі, коли до цього доходили руки. Тепер щоранку система сама забирає '
            'вчорашні цифри з обох рекламних кабінетів, кладе їх у Google Таблицю з готовим дашбордом, порівнює кожну кампанію з її ж '
            'медіаною за тиждень і, якщо CPA чи ROAS вийшли за поріг, пише про це в Telegram. Дорогий день видно '
            'наступного ранку, а не в кінці місяця.',
    lead_en='NovaFit runs ads on Google Ads and Meta Ads at the same time, and before this system the campaigns were '
            'checked by hand - in two ad accounts, one after the other, whenever somebody found the time. Now every '
            'morning the system pulls yesterday’s numbers from both ad accounts on its own, drops them into a Google Sheet with a ready-made '
            'dashboard, compares every campaign with its own median for the week and, if CPA or ROAS crossed a '
            'threshold, says so in Telegram. An expensive day shows up the next morning, not at the end of the month.',
    who_uk='Кому підходить: будь-якому бізнесу, що витрачає на рекламу відчутні гроші у двох і більше каналах - '
           'інтернет-магазинам, фітнес-клубам, школам, клінікам, сервісам за підпискою. Особливо тим, у кого немає '
           'штатного аналітика, а підрядник надсилає звіт раз на місяць.',
    who_en='Who it fits: any business spending real money on ads across two or more channels - online stores, '
           'fitness clubs, schools, clinics, subscription services. Especially those with no analyst on staff whose '
           'agency sends a report once a month.',
    stack=['Python', 'Google Ads API', 'Meta Marketing API', 'Google Sheets API', 'aiogram', 'APScheduler'],
    stack_uk='Стек: Python, конектори до Google Ads API і Meta Marketing API, Google Sheets API як сховище й '
             'дашборд, aiogram для Telegram-бота, APScheduler для щоденного запуску.',
    stack_en='Stack: Python, connectors to the Google Ads API and the Meta Marketing API, the Google Sheets API as '
             'both storage and dashboard, aiogram for the Telegram bot and APScheduler for the daily run.',
    shots={},
)

_TG = dict(w=664, h=855, ws=[480, 664], sizes='(max-width: 767px) 92vw, (max-width: 1199px) 45vw, 370px')
for _f, _cls, _over, _a_uk, _a_en, _c_uk, _c_en in [
    ('dash-top', 'wide', dict(h=819),
     'Дашборд ефективності реклами Google Ads і Meta Ads у Google Таблиці - KPI, канали, кампанії',
     'Google Ads and Meta Ads performance dashboard in a Google Sheet - KPIs, channels, campaigns',
     'Верх дашборда: пʼять KPI за вчора з відхиленням від медіани за 7 днів, зведення по каналах і таблиця кампаній '
     'зі статусом. Кампанія, що вийшла за поріг, підсвічується червоним прямо в рядку.',
     'The top of the dashboard: five KPIs for yesterday with the deviation from the 7-day median, a channel summary '
     'and a campaign table with a status. A campaign that crossed a threshold is highlighted red right in its row.'),
    ('dash-charts', 'wide', dict(h=819),
     'Графіки динаміки витрат, CPA, ROAS і конверсій по днях та журнал останніх алертів',
     'Daily charts of spend, CPA, ROAS and conversions plus the log of recent alerts',
     'Низ дашборда: чотири графіки по днях - витрати, CPA, ROAS і конверсії в розрізі каналів - і останні алерти '
     'за тиждень з рівнем, метрикою, значенням проти медіани і текстом повідомлення.',
     'The bottom of the dashboard: four daily charts - spend, CPA, ROAS and conversions by channel - and the alerts '
     'for the week, each with its level, metric, value against the median and message text.'),
    ('sheet-data', 'sheet', dict(h=710),
     'Аркуш «Дані» - рядки по кампаніях за кожен день з витратами, конверсіями, CPA та ROAS',
     'The data sheet - one row per campaign per day with spend, conversions, CPA and ROAS',
     'Аркуш «Дані»: один рядок на кампанію на день - витрати, покази, кліки, CTR, конверсії, CPA і ROAS. Дохід '
     'і позначка алерту рахуються формулами, тож таблицю можна фільтрувати й перевіряти як звичайну.',
     'The data sheet: one row per campaign per day - spend, impressions, clicks, CTR, conversions, CPA and ROAS. '
     'Revenue and the alert flag are formulas, so the sheet can be filtered and checked like any other.'),
    ('sheet-incident', 'sheet', dict(h=710),
     'Інцидент у таблиці: кампанія Meta Ads три дні поспіль підсвічена як критична за CPA і ROAS',
     'An incident in the sheet: a Meta Ads campaign flagged critical on CPA and ROAS three days in a row',
     'Так виглядає інцидент у даних: у «Холодної аудиторії» 9 вересня CPA піднявся на 67 % до медіани - жовта '
     '«Увага», а з 10 по 12 вересня тримався на +130…+190 % при ROAS нижче 1,3x - три червоні «Критично» поспіль.',
     'This is what an incident looks like in the data: on 9 September the cold-audience campaign’s CPA rose 67 % '
     'above its median - a yellow warning - and from 10 to 12 September it stayed at +130…+190 % with ROAS below '
     '1.3x - three red criticals in a row.'),
    ('tg-start', 'bot', _TG,
     'Telegram-бот моніторингу реклами - команди, підписка на алерти й перше критичне сповіщення',
     'The ad monitoring Telegram bot - commands, alert subscription and the first critical notification',
     'Після /start чат підписується на алерти. Кожне сповіщення - рівень, канал, кампанія, значення проти медіани '
     'і посилання на дашборд.',
     'After /start the chat is subscribed to alerts. Every notification carries the level, the channel, the campaign, '
     'the value against the median and a link to the dashboard.'),
    ('tg-report', 'bot', _TG,
     'Щоденний звіт по рекламі в Telegram - витрати, конверсії, CPA і ROAS по каналах з відхиленням від медіани',
     'The daily ad report in Telegram - spend, conversions, CPA and ROAS by channel with deviation from the median',
     '/report - зведення за вчора по кожному каналу: витрати, покази, кліки, CTR, конверсії, CPA, ROAS з ✅ або ⚠️ '
     'проти медіани, найбільша кампанія і кількість алертів за день.',
     '/report - yesterday’s summary per channel: spend, impressions, clicks, CTR, conversions, CPA and ROAS marked ✅ or '
     '⚠️ against the median, the biggest campaign and the number of alerts for the day.'),
    ('tg-alerts', 'bot', _TG,
     'Список відхилень CPA і ROAS за 14 днів у Telegram-боті з рівнями «Увага» і «Критично»',
     'The 14-day list of CPA and ROAS anomalies in the Telegram bot with warning and critical levels',
     '/alerts - усі відхилення за 14 днів у зворотному порядку, з рівнем і поясненням. Внизу - правила, за якими '
     'вони спрацьовують, щоб не треба було памʼятати пороги.',
     '/alerts - every anomaly from the last 14 days, newest first, with its level and explanation. The rules they fire '
     'on are printed at the bottom so nobody has to remember the thresholds.'),
]:
    CASES['novafit-ads-dashboard']['shots'][_f] = shot(_f, _cls, _a_uk, _a_en, _c_uk, _c_en, **_over)

CASES['novafit-ads-dashboard']['body'] = [
    ('h2', 'Як влаштована система', 'How the system is put together'),
    ('p', 'Три частини, одна таблиця. Google Таблиця - і сховище, і дашборд: у неї лягають денні рядки по кампаніях, '
          'а оформлення, формули й графіки живуть прямо в ній. Модуль детекції читає ці ж рядки й вирішує, чи є '
          'відхилення. Telegram-бот показує зведення на запит і розсилає нові алерти. Щоранку о 09:00 за Києвом '
          'планувальник проганяє весь ланцюжок: забрати вчорашній день з Google Ads і Meta Ads - записати - перерахувати - перевірити - '
          'сповістити.',
          'Three parts, one sheet. The Google Sheet is both the storage and the dashboard: the daily campaign rows land '
          'in it, and the styling, formulas and charts live right there. The detection module reads those same rows and '
          'decides whether anything deviates. The Telegram bot shows summaries on request and sends out new alerts. '
          'Every morning at 09:00 Kyiv time the scheduler runs the whole chain: fetch yesterday from Google Ads and Meta Ads - write - recalculate - '
          'check - notify.'),
    ('p', 'Цифри беруться напряму з рекламних кабінетів: конектор до Google Ads API забирає денні метрики по '
          'кампаніях з Google, конектор до Meta Marketing API - з Meta. Обидва ховаються за одним інтерфейсом з '
          'єдиним методом - віддати рядки метрик за період, - тому третій канал, скажімо TikTok Ads, додається '
          'ще одним класом, а сховище, детекція, бот і оформлення таблиці при цьому не змінюються.',
          'The numbers come straight from the ad accounts: a Google Ads API connector pulls the daily campaign '
          'metrics from Google, a Meta Marketing API connector pulls them from Meta. Both sit behind one interface '
          'with a single method - return the metric rows for a period - so a third channel, say TikTok Ads, is one '
          'more class, while the storage, detection, bot and sheet styling stay untouched.'),

    ('h3', '1. Дашборд у Google Таблиці', '1. The dashboard in a Google Sheet'),
    ('p', 'Аркуш «Дашборд» зверстаний під екран 1920x1080, щоб його можна було відкрити на моніторі чи телевізорі '
          'в офісі і не гортати. Зверху - пʼять KPI за вчора (витрати, конверсії, CPA, ROAS, CTR), кожен з '
          'відхиленням від медіани за 7 днів. Нижче - зведення по каналах і таблиця кампаній: витрати, кліки, CTR, '
          'конверсії, CPA, ROAS, зміна до попереднього тижня і статус «У нормі» або «Критично».',
          'The dashboard sheet is laid out for a 1920x1080 screen so it can be opened on an office monitor or TV '
          'without scrolling. At the top - five KPIs for yesterday (spend, conversions, CPA, ROAS, CTR), each with its '
          'deviation from the 7-day median. Below - a channel summary and a campaign table: spend, clicks, CTR, '
          'conversions, CPA, ROAS, the change against the previous week and a status of either normal or critical.'),
    ('p', 'Далі чотири графіки по днях - витрати, CPA, ROAS і конверсії, кожен у розрізі Google / Meta / разом - і '
          'журнал останніх алертів. Окремого BI-інструмента й ліцензії немає: клієнт відкриває звичайну таблицю у '
          'своєму акаунті, може відфільтрувати, скопіювати чи вивантажити що завгодно. Локаль - українська: суми в '
          'гривнях, десяткова кома, дати дд.мм.рррр.',
          'Then four daily charts - spend, CPA, ROAS and conversions, each split into Google / Meta / total - and the '
          'log of recent alerts. There is no separate BI tool and no licence: the client opens an ordinary sheet in '
          'their own account and can filter, copy or export whatever they need. The locale is Ukrainian: amounts in '
          'hryvnia, a decimal comma, dd.mm.yyyy dates.'),
    ('shots', None, ['dash-top', 'dash-charts']),

    ('h3', '2. Дані та формули', '2. Data and formulas'),
    ('p', 'Під дашбордом - три робочі аркуші. «Дані» тримає один рядок на кампанію на день з усіма метриками; дохід '
          'і позначка алерту в ньому рахуються формулами, а не записуються кодом, тож будь-яке число можна '
          'перевірити кліком. «Щоденно» згортає ті самі рядки в денні агрегати по Google, Meta і разом. «Алерти» - '
          'журнал відхилень з датою, рівнем, значенням, медіаною і текстом повідомлення.',
          'Under the dashboard sit three working sheets. The data sheet holds one row per campaign per day with every '
          'metric; revenue and the alert flag are calculated by formulas rather than written by code, so any figure can '
          'be checked with a click. The daily sheet rolls those same rows up into per-day aggregates for Google, Meta '
          'and both. The alerts sheet is the anomaly log with the date, level, value, median and message text.'),
    ('shots', None, ['sheet-data']),

    ('h3', '3. Як ловляться відхилення', '3. How anomalies are caught'),
    ('p', 'Для кожної кампанії і кожного дня береться медіана CPA і ROAS за 7 попередніх днів - поточний день у '
          'вікно не входить - і поточне значення порівнюється з нею. Саме медіана, а не середнє: один аномальний '
          'день усередині вікна не зсуває базу, тож система не звикає до поганого.',
          'For every campaign and every day the system takes the median CPA and ROAS of the 7 previous days - the '
          'current day is left out of the window - and compares the current value against it. The median rather than '
          'the mean on purpose: one anomalous day inside the window does not shift the baseline, so the system never '
          'gets used to bad numbers.'),
    ('p', 'Пороги два. «Увага» - CPA на 60 % вище медіани або ROAS на 40 % нижче, і лише якщо це тримається два дні '
          'поспіль: один поганий день - ще не інцидент. «Критично» - CPA на 120 % вище або ROAS на 60 % нижче, '
          'спрацьовує одразу; нуль конверсій при витратах теж критично. На кампанію за день формується один алерт: '
          'CPA основна метрика, ROAS додаткова.',
          'There are two thresholds. Warning - CPA 60 % above the median or ROAS 40 % below, and only if it holds for '
          'two days in a row: one bad day is not yet an incident. Critical - CPA 120 % above or ROAS 60 % below, fires '
          'immediately; zero conversions with spend is critical too. One alert per campaign per day: CPA is the primary '
          'metric, ROAS the secondary.'),
    ('shots', None, ['sheet-incident']),

    ('h3', '4. Telegram-бот', '4. The Telegram bot'),
    ('p', 'Бот - те, що власник бачить щодня. Після /start чат підписується на алерти й отримує їх автоматично після '
          'ранкового оновлення. /report показує зведення за вчора по кожному каналу з позначками ✅ і ⚠️ проти '
          'медіани, /alerts - усі відхилення за 14 днів. У кожному повідомленні є посилання «Відкрити дашборд», '
          'тож від алерту до таблиці - один дотик.',
          'The bot is what the owner sees every day. After /start the chat is subscribed to alerts and receives them '
          'automatically after the morning update. /report shows yesterday’s summary per channel with ✅ and ⚠️ marks '
          'against the median, /alerts lists every anomaly from the last 14 days. Every message carries an "Open the '
          'dashboard" link, so it is one tap from an alert to the sheet.'),
    ('shots', 'col-md-6 col-xl-4', ['tg-start', 'tg-report', 'tg-alerts']),

    ('h2', 'Ключова логіка', 'The logic that matters'),
    ('list', [
        ('База порівняння - медіана за 7 попередніх днів по кожній кампанії окремо, а не середнє по акаунту: '
         'дорога кампанія не маскується дешевою',
         'The baseline is the 7-day median of each campaign on its own, not the account average: an expensive '
         'campaign cannot hide behind a cheap one'),
        ('Два рівні з різною чутливістю: «Увага» вимагає підтвердження другим днем, «Критично» спрацьовує одразу - '
         'менше шуму, але серйозне не пропускається',
         'Two levels with different sensitivity: a warning needs a second day to confirm, a critical fires at once - '
         'less noise, yet nothing serious slips through'),
        ('Дедуплікація за датою і кампанією: розсилаються лише нові алерти, повторний запуск не спамить старими',
         'Deduplication by date and campaign: only new alerts are sent, a re-run never spams old ones'),
        ('Google Таблиця замість BI: жодних ліцензій, дані лишаються в акаунті клієнта, формули можна перевірити',
         'A Google Sheet instead of BI: no licences, the data stays in the client’s account, the formulas can be audited'),
        ('Формули пишуться в коді в en_US-синтаксисі й перекладаються під локаль таблиці перед записом - таблиця '
         'лишається українською',
         'Formulas are written in code in en_US syntax and translated to the sheet’s locale before writing - the sheet '
         'stays Ukrainian'),
        ('Google Ads і Meta Ads за одним інтерфейсом: конектори до обох API взаємозамінні, новий канал - ще один '
         'клас без змін у решті системи',
         'Google Ads and Meta Ads behind one interface: the two API connectors are interchangeable, and a new channel '
         'is one more class with no changes elsewhere'),
    ]),

    ('h2', 'Що вміє система', 'What the system can do'),
    ('list', [
        ('Щоденне автоматичне вивантаження метрик з Google Ads API і Meta Marketing API о 09:00 за Києвом',
         'Automatic daily metric pull from the Google Ads API and the Meta Marketing API at 09:00 Kyiv time'),
        ('Дашборд у Google Таблиці під екран 1920x1080: KPI, канали, кампанії, чотири графіки, останні алерти',
         'A Google Sheet dashboard laid out for 1920x1080: KPIs, channels, campaigns, four charts, recent alerts'),
        ('Порівняння кожного показника з медіаною за 7 днів прямо в KPI-плитках і таблицях',
         'Every metric compared with its 7-day median right in the KPI tiles and tables'),
        ('Статус кампанії «У нормі» або «Критично» з підсвіткою рядка',
         'A campaign status of normal or critical with the row highlighted'),
        ('Аркуш даних з одним рядком на кампанію на день і формулами доходу та алерту',
         'A data sheet with one row per campaign per day and formulas for revenue and the alert flag'),
        ('Денні агрегати по Google, Meta і разом на окремому аркуші',
         'Daily aggregates for Google, Meta and both on a separate sheet'),
        ('Журнал алертів з рівнем, метрикою, значенням, медіаною, відхиленням і часом фіксації',
         'An alert log with the level, metric, value, median, deviation and the time it was recorded'),
        ('Детекція відхилень CPA і ROAS за ковзною медіаною з двома рівнями і правилом двох днів для «Уваги»',
         'CPA and ROAS anomaly detection against a rolling median with two levels and a two-day rule for warnings'),
        ('Telegram-бот: /report за вчора по каналах, /alerts за 14 днів, підписка й відписка від сповіщень',
         'A Telegram bot: /report for yesterday by channel, /alerts for 14 days, subscribe and unsubscribe'),
        ('Автоматична розсилка лише нових алертів після кожного оновлення',
         'Automatic delivery of new alerts only, after every refresh'),
        ('CLI для ручних операцій: завантажити історію, додати день, перевірити, розіслати',
         'A CLI for manual operations: load history, add a day, check, send'),
    ]),
]


# ------------------------------------------------------------------- MarginTracker
CASES['margintracker'] = dict(
    date='2026-10-05',
    tag_uk='Фінанси та аналітика', tag_en='Finance and analytics',
    cta_uk='Зводите звіт руками? Розкажіть про свої дані - подивимось, що можна автоматизувати',
    cta_en='Still building the report by hand? Tell us about your data and we will see what can be automated',
    h1_uk='MarginTracker - звіт по маржі з трьох CRM і Нової Пошти',
    h1_en='MarginTracker - a margin report from three CRMs and Nova Poshta',
    title_uk='Програма для звіту по маржі з CRM - кейс MarginTracker | Devlly',
    title_en='A desktop app for margin reporting from CRMs - the MarginTracker case study | Devlly',
    desc_uk='Кейс Devlly: десктопна програма, що збирає замовлення з двох CRM-систем, додає собівартість '
            'і вартість зворотної доставки Новою Поштою та записує фінансовий звіт по кожному сайту '
            'у Google Таблицю.',
    desc_en='A Devlly case study: a desktop app that collects orders from two CRM systems, adds product cost '
            'and the price of return shipping with Nova Poshta, and writes a per-site financial report into '
            'a Google Sheet.',
    keywords_uk='звіт по маржі, автоматизація фінансового звіту, облік собівартості товарів, вивантаження '
                'замовлень з crm, інтеграція lp-crm salesdrive, вартість повернення нова пошта, '
                'десктопна програма для бізнесу, звіт у google таблицю',
    keywords_en='margin report, financial report automation, product cost accounting, exporting orders from crm, '
                'lp-crm salesdrive integration, nova poshta return cost, desktop app for business, '
                'report into google sheets',
    lead_uk='MarginTracker - програма для Windows, яка раз на місяць робить те, на що раніше йшли робочі дні. '
            'Вона збирає замовлення з двох CRM-систем, у які падають заявки з кількох інтернет-магазинів, '
            'підставляє собівартість товарів, витягує з Нової Пошти вартість доставки по кожному поверненню '
            'і записує готовий звіт у Google Таблицю - рядок на кожен сайт плюс підсумковий «РАЗОМ».',
    lead_en='MarginTracker is a Windows app that does in one pass what used to take working days. It collects '
            'orders from the two CRM systems the online stores feed into, fills in product cost, pulls the '
            'shipping cost of every return out of Nova Poshta, and writes the finished report into a Google '
            'Sheet - one row per store plus a grand total.',
    who_uk='Кому підходить: товарному бізнесу з кількома магазинами, у якого замовлення живуть у різних CRM, '
           'частина посилок повертається, а маржу досі зводять в Excel руками. Чим більше замовлень за місяць, '
           'тим дорожча ручна робота і тим дешевше обходиться помилка, якої не сталося.',
    who_en='Who it fits: product businesses running several stores whose orders live in different CRMs, where '
           'some parcels come back and the margin is still pieced together in Excel by hand. The more orders a '
           'month, the more the manual work costs - and the more an avoided mistake is worth.',
    stack=['Python 3', 'CustomTkinter', 'requests', 'openpyxl', 'gspread', 'PyInstaller'],
    stack_uk='Стек: Python 3, CustomTkinter для інтерфейсу, requests для роботи з API, openpyxl для локального '
             'сховища собівартості, gspread і google-auth для запису в таблицю. Збірка в один exe через '
             'PyInstaller - у замовника на машині нічого ставити не треба.',
    stack_en='Stack: Python 3, CustomTkinter for the interface, requests for the APIs, openpyxl for the local '
             'cost storage, gspread and google-auth for writing to the sheet. Packaged into a single exe with '
             'PyInstaller - nothing to install on the client’s machine.',
    shots={},
)

_WARN = dict(w=656, h=579, ws=[480, 656], sizes='(max-width: 767px) 92vw, 640px')
for _f, _cls, _over, _a_uk, _a_en, _c_uk, _c_en in [
    ('step1-collecting', 'win', {},
     'Програма для звіту по маржі - крок збору замовлень з CRM, прогрес і журнал виконання',
     'Margin reporting app - the order collection step with a progress bar and an execution log',
     'Крок 1 під час збору: обраний період, прогрес і журнал по кожному джерелу. Поки триває збір, навігація '
     'заблокована - на наступний крок не можна піти з напівзібраними даними.',
     'Step 1 while collecting: the chosen period, the progress bar and a log per source. While the collection '
     'runs the navigation is locked - you cannot move on with half the data.'),
    ('step1-done', 'win', {},
     'Підсумок збору замовлень: кількість замовлень по кожному акаунту CRM, сайтів і унікальних товарів',
     'Collection summary: the order count for each CRM account, the number of stores and unique products',
     'Той самий екран після збору: скільки замовлень віддало кожне джерело окремо - два акаунти LP-CRM і '
     'SalesDrive - плюс кількість сайтів і унікальних товарів за період.',
     'The same screen once collection is done: how many orders each source returned on its own - two LP-CRM '
     'accounts and SalesDrive - plus the number of stores and unique products for the period.'),
    ('step2-costs', 'win', {},
     'Таблиця собівартості товарів: заповнені позиції з минулих місяців і нові підсвічені жовтим',
     'The product cost table: items carried over from previous months and new ones highlighted in yellow',
     'Крок 2: редагована таблиця собівартості. Товари, які вже заповнювали раніше, підтягуються самі, нові '
     'підсвічені жовтим. Є пошук, фільтр «лише без собівартості» і лічильник незаповнених у правому куті.',
     'Step 2: the editable cost table. Items filled in before are pulled in automatically, new ones are '
     'highlighted yellow. There is a search box, a "missing cost only" filter and a counter in the corner.'),
    ('step2-collisions-btn', 'win', {},
     'Кнопка «Колізії: 2 потребують уваги» на екрані собівартості',
     'The "Collisions: 2 need attention" button on the cost screen',
     'Той самий екран з кнопкою «Колізії: 2 потребують уваги». Вона зʼявляється тоді, коли CRM віддала під '
     'одним номером замовлення не повністю - про це нижче.',
     'The same screen with a "Collisions: 2 need attention" button. It appears when the CRM returned only part '
     'of what lives under one order number - more on that below.'),
    ('collisions-window', 'win', dict(w=1136, h=659, ws=[800, 1136]),
     'Ручний етап для колізій order_id: версії замовлень під одним номером і форма введення',
     'The manual stage for order_id collisions: the versions living under one number and the input form',
     'Ручний етап для колізій. Зліва по кожному номеру видно, що саме віддало API, і чого бракує. Справа - '
     'картка вже отриманого замовлення і форма, у якій поля змінюються залежно від обраного статусу: для '
     'продажу це сайт, товар, кількість і сума.',
     'The manual stage for collisions. On the left, for every number, what the API actually returned and what '
     'is missing. On the right, the order already received and a form whose fields change with the chosen '
     'status: for a sale that is the store, the product, the quantity and the amount.'),
    ('step3-report', 'win', {},
     'Порахований фінансовий звіт: виручка, собівартість, розділена маржа і доставка по поверненнях',
     'The calculated financial report: revenue, cost, split margin and delivery costs on returns',
     'Крок 3: звіт порахований. Виручка, собівартість, маржа окремо по основному товару і по допродажах, '
     'кількість повернень і те, скільки зʼїла доставка по них. Нижче - зауваження, які програма знайшла сама.',
     'Step 3: the report is calculated. Revenue, cost, margin split between the main product and upsells, the '
     'number of returns and how much their delivery ate. Below it - the remarks the program found by itself.'),
    ('step3-sheet-preview', 'win', {},
     'Попередній перегляд вмісту Google Таблиці: рядок на кожен сайт і підсумковий «РАЗОМ»',
     'A preview of the Google Sheet contents: one row per store plus a grand total row',
     'Той самий екран, прокручений донизу: попередження про подвійний облік ТТН і точний вміст, який піде в '
     'Google Таблицю - рядок на кожен сайт і підсумковий «РАЗОМ» з усіма колонками звіту.',
     'The same screen scrolled down: a warning about double-counted waybills and the exact content that will '
     'go into the Google Sheet - one row per store and a grand total with every column of the report.'),
    ('report-warnings', 'win', _WARN,
     'Вікно зауважень до звіту: товари без собівартості й необроблені колізії з прикладами',
     'The report remarks dialog: products without a cost and unprocessed collisions with examples',
     'Розбір проблем перед записом. Розрахунок не зупиняється - програма показує, що саме може зробити цифри '
     'неточними, з конкретними прикладами, і дає вибір: прийняти як є або повернутись і виправити.',
     'The problem review before writing. The calculation does not stop - the program shows exactly what could '
     'make the figures inaccurate, with concrete examples, and offers a choice: accept as is, or go back and fix.'),
]:
    CASES['margintracker']['shots'][_f] = shot(_f, _cls, _a_uk, _a_en, _c_uk, _c_en, **_over)

CASES['margintracker']['body'] = [
    ('h2', 'Яка була задача', 'The problem'),
    ('p', 'Замовник - товарний бізнес із кількома інтернет-магазинами. Заявки з лендінгів падають у дві різні '
          'CRM-системи, товар їде Новою Поштою, частина посилок повертається. Щоб зрозуміти, скільки реально '
          'заробили за місяць, звіт зводили руками: вивантажували замовлення з кожної CRM окремо, зліплювали в '
          'Excel, підставляли собівартість і окремо рахували, скільки зʼїли повернення. На кілька тисяч '
          'замовлень це займало робочі дні, і кожен перенос цифри був шансом на помилку.',
          'The client is a product business running several online stores. Leads from landing pages fall into two '
          'different CRM systems, the goods travel with Nova Poshta and some parcels come back. To find out what '
          'the month actually earned, the report was assembled by hand: export the orders from each CRM, glue '
          'them together in Excel, fill in the cost and work out separately how much the returns ate. For a few '
          'thousand orders that took working days, and every number carried over by hand was a chance to slip.'),
    ('p', 'Складність тут не в арифметиці. Вона в тому, що дані треба зібрати з трьох різних API з різними '
          'обмеженнями, звести докупи різні написання одного й того ж товару та сайту - і дістати вартість '
          'зворотної доставки, якої немає ні в CRM, ні в жодному звіті перевізника.',
          'The hard part is not the arithmetic. It is that the data has to be collected from three different APIs '
          'with different limits, that the same product and the same store are spelled differently in each of '
          'them, and that the cost of return shipping exists neither in the CRM nor in any report the carrier '
          'provides.'),

    ('h2', 'Як це працює', 'How it works'),
    ('p', 'Програма веде користувача трьома кроками, і перейти далі, не закривши поточний, не можна. Збір - '
          'собівартість - звіт. Усе локально, у вікні на робочому столі: один exe, зібраний PyInstaller, '
          'нічого встановлювати не треба.',
          'The app walks the user through three steps, and you cannot move on before the current one is done. '
          'Collect - cost - report. Everything runs locally in a desktop window: a single exe built with '
          'PyInstaller, nothing to install.'),
    ('p', 'Усі цифри, сайти, товари й номери на знімках нижче - вигадані. Це демо-режим програми, у якому можна '
          'пройти всі три кроки без жодного ключа API: інтерфейс і розрахунки справжні, дані згенеровані '
          'спеціально для портфоліо і не перетинаються з даними замовника.',
          'Every figure, store, product and number in the screenshots below is invented. This is the app’s demo '
          'mode, where all three steps can be walked through without a single API key: the interface and the '
          'calculations are real, the data was generated for this portfolio and has nothing to do with the '
          'client’s own.'),

    ('h3', '1. Збір замовлень', '1. Collecting the orders'),
    ('p', 'Користувач обирає період і тисне «Зібрати». Програма по черзі опитує джерела і показує, що саме '
          'зараз робить. LP-CRM віддає дані в три заходи: спочатку довідник статусів, потім по кожному статусу '
          'список номерів, потім самі замовлення пачками по сто. У SalesDrive жорсткі ліміти - порядку сотні '
          'запитів на годину, - тому збір іде з паузами і контролем залишку квоти, а назви кастомних полів '
          'мапляться через конфіг, бо в кожного акаунта вони свої.',
          'The user picks a period and presses "Collect". The app queries the sources one by one and shows what '
          'it is doing. LP-CRM gives up its data in three passes: the status reference first, then the list of '
          'order numbers per status, then the orders themselves in batches of a hundred. SalesDrive has hard '
          'limits - on the order of a hundred requests an hour - so collection runs with pauses and a quota '
          'check, and the custom field names are mapped through a config because every account names them '
          'differently.'),
    ('shots', None, ['step1-collecting', 'step1-done']),

    ('h3', '2. Собівартість товарів', '2. Product cost'),
    ('p', 'Другий крок - редагована таблиця всіх товарів періоду. Те, що заповнювали минулого місяця, '
          'підставляється саме; нові позиції підсвічені жовтим, щоб їх не можна було пропустити. Введені ціни '
          'лягають у локальний xlsx і живуть між запусками, а запис у файли атомарний: обрив на півдорозі не '
          'псує сховище.',
          'The second step is an editable table of every product in the period. Whatever was filled in last month '
          'is pre-filled; new items are highlighted yellow so they cannot be missed. The entered prices go into a '
          'local xlsx and survive between runs, and writes to the local files are atomic: an interruption '
          'halfway through does not corrupt the storage.'),
    ('shots', None, ['step2-costs', 'step2-collisions-btn']),

    ('h3', '3. Звіт', '3. The report'),
    ('p', 'На третьому кроці програма рахує метрики, підтягує вартість доставки по поверненнях і показує '
          'точний вміст, який піде в таблицю. Рядок на кожен сайт і підсумковий «РАЗОМ»: кількість заявок і '
          'забраних, виручка, собівартість, маржа допродаж, маржа основна, кількість повернень і доставка по '
          'них, а також скільки ТТН не пораховано і скільки товарів лишилось без собівартості.',
          'On the third step the app calculates the metrics, pulls in the delivery cost of the returns and shows '
          'the exact content that will go into the sheet. One row per store plus a grand total: the number of '
          'leads and of collected orders, revenue, cost, upsell margin, main margin, the number of returns and '
          'their delivery cost, plus how many waybills went uncounted and how many products are still missing a '
          'cost.'),
    ('p', 'Маржа розділена на дві навмисно. Основний товар продає реклама, допродаж продає оператор - для '
          'бізнесу це різні гроші, і дивляться на них окремо. Статуси замовлень зводяться у три групи через '
          'конфіг: успішні йдуть у виручку, повернення рахуються окремо, решта свідомо не враховується. Статус, '
          'якого немає в жодній групі, нічого не ламає: програма дорахує звіт і покаже список нових статусів '
          'окремим зауваженням.',
          'The margin is split in two on purpose. Advertising sells the main product, the operator sells the '
          'upsell - for the business these are different money and they are looked at separately. Order statuses '
          'are folded into three groups through a config: successful ones go into revenue, returns are counted '
          'separately, the rest is deliberately ignored. A status that belongs to no group breaks nothing: the '
          'app finishes the report and lists the new statuses as a separate remark.'),
    ('p', 'Запис у Google Таблицю йде через службовий акаунт і пакетно - кілька запитів на весь звіт, а не '
          'рядок за рядком, інакше впираєшся в квоту API. Таблицю можна щомісяця створювати нову або дописувати '
          'в наявну.',
          'Writing into the Google Sheet goes through a service account and in batches - a few requests for the '
          'whole report rather than row by row, otherwise you hit the API quota. The sheet can be created fresh '
          'every month or appended to.'),
    ('shots', None, ['step3-report', 'step3-sheet-preview']),

    ('h2', 'Дві задачі, яких немає в документації API',
           'Two problems the API documentation does not mention'),
    ('p', 'Найцінніше в цьому проєкті - не інтерфейс. Це дві речі, на які немає ні методу в API, ні рядка в '
          'документації, і які довелось розбирати з нуля.',
          'The most valuable part of this project is not the interface. It is two things with no API method and '
          'no line of documentation behind them, which had to be worked out from scratch.'),

    ('h3', 'Зникаючі замовлення: колізії order_id', 'Disappearing orders: order_id collisions'),
    ('p', 'Симптом: клієнт стверджував, що в звіті щомісяця бракує кількох замовлень. Розбір логів показав, що '
          'API CRM справді віддає менше записів, ніж у нього просили.',
          'The symptom: the client kept saying a few orders were missing from the report every month. Going '
          'through the logs showed the CRM API really did return fewer records than it was asked for.'),
    ('p', 'Причина виявилась у генераторі номерів на лендінгу: номер складається з часу з точністю до десятої '
          'секунди. Два замовлення, оформлені в ту саму десяту секунди, отримують однаковий номер, і API віддає '
          'під ним лише одне. Гірше того - у пачці зі ста номерів таке замовлення детерміновано «зʼїдає» ще '
          'один запис, найбільший номер у пачці, через те як у CRM стоїть обмеження вибірки після зʼєднання '
          'таблиць.',
          'The cause turned out to be the number generator on the landing page: the number is built from the '
          'timestamp down to a tenth of a second. Two orders placed within the same tenth of a second get the '
          'same number, and the API returns only one of them. Worse - inside a batch of a hundred numbers such '
          'an order deterministically eats one more record, the largest number in the batch, because of how the '
          'CRM limits the selection after joining its tables.'),
    ('p', 'Що зроблено. «Зʼїдений» запис відловлюється повторним запитом меншими пачками. Для справжніх дублів '
          'зроблено ручний етап: програма сама визначає, скільки замовлень живе під одним номером, і показує '
          'вікно, де менеджер вписує те, чого API не віддало. Вписане зберігається назавжди і підставляється в '
          'наступних прогонах - але лише якщо колізія на місці, статус зниклого замовлення збігається і API '
          'віддає те саме замовлення, що й під час заповнення. Якщо хоч щось із цього змінилось, запис '
          'відкладається і показується менеджеру знову, замість того щоб тихо підставити стару цифру. Причину '
          'передали клієнту: на частині лендінгів генератор номера вже містить випадковий суфікс, і колізій там '
          'рівно нуль.',
          'What was done. The eaten record is caught by repeating the request in smaller batches. For genuine '
          'duplicates there is a manual stage: the app works out how many orders live under one number and opens '
          'a window where the manager types in what the API withheld. What is typed is kept forever and reused in '
          'later runs - but only while the collision is still there, the missing order’s status still matches and '
          'the API still returns the same order as it did when the form was filled. If any of that changed, the '
          'record is set aside and shown to the manager again instead of quietly reusing a stale figure. The '
          'cause was passed back to the client: on some of the landing pages the number generator already adds a '
          'random suffix, and there the collision count is exactly zero.'),
    ('shots', None, ['collisions-window']),

    ('h3', 'Вартість зворотної доставки', 'The cost of return shipping'),
    ('p', 'У CRM цієї суми немає взагалі, а перевізник не віддає її жодним окремим методом. Перевірили три '
          'місця: заявки на повернення, список власних накладних і калькулятор ціни. У перших двох поле '
          'вартості порожнє, третій не приймає номер накладної.',
          'The CRM does not hold this figure at all, and the carrier exposes it through no dedicated method. '
          'Three places were checked: the return requests, the list of own waybills and the price calculator. In '
          'the first two the cost field is empty, the third does not accept a waybill number.'),
    ('p', 'Робоча схема виявилась такою: вартість лежить у картці накладної, а повна сума повернення - це пряме '
          'плече плюс зворотне плюс платне зберігання на відділенні, яке нараховується після семи безкоштовних '
          'днів. Зберігання в кабінеті перевізника показується на обох накладних, тому рахувати його треба один '
          'раз на посилку, інакше сума подвоюється. Схему звірили по контрольній вибірці накладних з точністю '
          'до копійки.',
          'The scheme that works is this: the cost sits in the waybill card, and the full price of a return is '
          'the outbound leg plus the return leg plus the paid storage at the branch, which starts after seven '
          'free days. The carrier’s dashboard shows that storage on both waybills, so it has to be counted once '
          'per parcel or the sum doubles. The scheme was reconciled against a control sample of waybills down to '
          'the kopeck.'),

    ('h2', 'Програма не вдає, що дані ідеальні', 'The app does not pretend the data is clean'),
    ('p', 'Перед записом звіту програма показує те, що може зробити цифри неточними: товари без собівартості, '
          'замовлення без товарів, повернення без ТТН або з ТТН, якої немає в перевізника, один і той самий ТТН '
          'у двох замовленнях, нові статуси, незаповнені колізії. Розрахунок при цьому не зупиняється - можна '
          'подивитись приклади, прийняти як є або повернутись і виправити.',
          'Before writing the report the app shows whatever could make the figures inaccurate: products without a '
          'cost, orders without products, returns with no waybill or with one the carrier does not know, the same '
          'waybill on two orders, new statuses, unfilled collisions. The calculation does not stop - you can look '
          'at the examples, accept them as they are, or go back and fix them.'),
    ('p', 'Сенс простий: звіт на кілька тисяч замовлень або правильний, або нічого не вартий. Тому користувач '
          'має бачити, де саме цифра може бути кривою, а не отримувати мовчазне «порахувалось».',
          'The reasoning is simple: a report over a few thousand orders is either right or worthless. So the user '
          'should see exactly where a number may be off, rather than get a silent "done".'),
    ('shots', 'col-12 col-md-10 col-xl-8 mx-auto', ['report-warnings']),

    ('h2', 'Ключова логіка', 'The logic that matters'),
    ('list', [
        ('Ручні записи по колізіях перевіряються щоразу заново: змінився статус або відповідь API - запис '
         'відкладається і показується людині, а не підставляється тихо',
         'Manual collision entries are re-validated on every run: if the status or the API response changed, the '
         'entry is set aside and shown to a human instead of being reused silently'),
        ('Платне зберігання на відділенні рахується один раз на посилку, хоча перевізник показує його на обох '
         'накладних - інакше сума повернення подвоюється',
         'Paid storage at the branch is counted once per parcel even though the carrier shows it on both '
         'waybills - otherwise the cost of a return doubles'),
        ('Маржа розділена на основну й допродажну: їх створюють різні люди, тож і дивляться на них окремо',
         'The margin is split into main and upsell: different people generate them, so they are looked at '
         'separately'),
        ('Невідомий статус замовлення не ламає розрахунок - звіт дораховується, а список нових статусів іде '
         'в зауваження',
         'An unknown order status does not break the calculation - the report is finished and the new statuses '
         'go into the remarks'),
        ('Запис у Google Таблицю пакетний: кілька запитів на весь звіт замість рядка за рядком, інакше квота API',
         'Writing to the Google Sheet is batched: a few requests for the whole report instead of row by row, '
         'otherwise the API quota bites'),
        ('Атомарний запис локальних файлів: обрив посеред збереження не псує сховище собівартості й ручних записів',
         'Atomic writes to the local files: an interruption mid-save does not corrupt the cost storage or the '
         'manual entries'),
        ('Помилки API доходять до користувача людською мовою, а не трейсбеком, і запит повторюється з паузою',
         'API errors reach the user in plain language rather than as a traceback, and the request is retried '
         'after a pause'),
    ]),

    ('h2', 'Що вміє програма', 'What the app can do'),
    ('list', [
        ('Збір замовлень за період з двох CRM-систем - двох акаунтів LP-CRM і SalesDrive - в одному проході',
         'Collecting a period’s orders from two CRM systems - two LP-CRM accounts and SalesDrive - in one pass'),
        ('Дотримання лімітів запитів з паузами й контролем залишку квоти',
         'Respecting request limits with pauses and a check on the remaining quota'),
        ('Мапінг кастомних полів замовлення через конфіг - під назви конкретного акаунта',
         'Mapping custom order fields through a config, to the names of the specific account'),
        ('Редагована таблиця собівартості з пошуком, фільтром незаповнених і підсвіткою нових товарів',
         'An editable cost table with search, a missing-only filter and new products highlighted'),
        ('Перенесення собівартості між місяцями: заповнене раніше підставляється автоматично',
         'Carrying cost between months: whatever was filled in before is applied automatically'),
        ('Ручний етап для колізій order_id з перевіркою записів при кожному наступному прогоні',
         'A manual stage for order_id collisions, with the entries re-validated on every later run'),
        ('Розрахунок вартості доставки по кожному поверненню з накладних Нової Пошти',
         'Calculating the delivery cost of every return from the Nova Poshta waybills'),
        ('Фінансовий звіт по кожному сайту й підсумковий, з розділеною маржею та повну статистику повернень',
         'A financial report per store and in total, with the margin split and the full return statistics'),
        ('Зауваження до даних перед записом - з прикладами й вибором «прийняти як є» чи виправити',
         'Data remarks before writing - with examples and a choice between accepting them and fixing them'),
        ('Запис у Google Таблицю з форматуванням: нова таблиця щомісяця або дозапис у наявну',
         'Writing into a formatted Google Sheet: a fresh sheet every month or an append to an existing one'),
        ('Демо-режим: усі три кроки проходяться на згенерованих даних без жодного ключа API',
         'A demo mode: all three steps can be walked through on generated data without a single API key'),
        ('Власний набір самоперевірок на 354 перевірки, що проганяється однією командою і ловить регресії '
         'в розрахунках, мапінгу статусів і логіці ручних записів',
         'An in-house self-test suite of 354 checks, run with a single command, that catches regressions in the '
         'calculations, the status mapping and the manual-entry logic'),
    ]),
]


# ------------------------------------------------------------------- сборка head
def head(slug, en=False):
    C = CASES[slug]
    imgdir = 'images/cases/' + slug
    A = '/assets' if en else '../assets'
    url = '%s/%scases/%s' % (BASE, 'en/' if en else '', slug)
    uk_url, en_url = '%s/cases/%s' % (BASE, slug), '%s/en/cases/%s' % (BASE, slug)
    title = C['title_en'] if en else C['title_uk']
    desc = C['desc_en'] if en else C['desc_uk']
    kw = C['keywords_en'] if en else C['keywords_uk']
    name = C['h1_en'] if en else C['h1_uk']
    og = '%s/assets/%s/og.jpg' % (BASE, imgdir)
    cases_n, home_n = ('Cases', 'Home') if en else ('Кейси', 'Головна')
    cases_url = BASE + ('/en#projects' if en else '/#projects')

    schema = {
        "@context": "https://schema.org", "@type": "CreativeWork",
        "name": name, "headline": name, "description": desc, "image": og,
        "datePublished": C['date'], "dateModified": C['date'],
        "inLanguage": "en" if en else "uk",
        "keywords": kw,
        "creator": {"@type": "Organization", "name": "Devlly", "url": BASE + ('/en' if en else '/')},
        "about": {"@type": "SoftwareApplication",
                  "name": name,
                  "applicationCategory": "BusinessApplication",
                  "operatingSystem": "Web"},
        "mainEntityOfPage": {"@type": "WebPage", "@id": url}, "url": url,
    }
    crumbs = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": home_n, "item": BASE + ('/en' if en else '/')},
            {"@type": "ListItem", "position": 2, "name": cases_n, "item": cases_url},
            {"@type": "ListItem", "position": 3, "name": name, "item": url},
        ],
    }
    J = lambda d: json.dumps(d, ensure_ascii=False, indent=2)
    return """<!DOCTYPE html>
<html lang="%(lang)s">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>%(title)s</title>
    <meta name="description" content="%(desc)s">
    <meta name="keywords" content="%(kw)s">
    <meta name="robots" content="INDEX,FOLLOW">
    <link rel="canonical" href="%(url)s">
    <link rel="alternate" hreflang="uk" href="%(uk_url)s">
    <link rel="alternate" hreflang="en" href="%(en_url)s">
    <link rel="alternate" hreflang="x-default" href="%(uk_url)s">
    <meta property="og:type" content="article">
    <meta property="og:site_name" content="Devlly">
    <meta property="og:title" content="%(title)s">
    <meta property="og:description" content="%(desc)s">
    <meta property="og:url" content="%(url)s">
    <meta property="og:image" content="%(og)s">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:locale" content="%(locale)s">
    <meta name="twitter:card" content="summary_large_image">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="preload" as="font" type="font/woff2" href="%(A)s/fonts/Thunder-SemiBoldLC.woff2" crossorigin>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Funnel+Display:wght@300..800&display=swap" media="print" onload="this.media='all'">
    <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Funnel+Display:wght@300..800&display=swap"></noscript>
    <link rel="icon" type="image/svg+xml" href="%(A)s/images/logo/favicon.svg">
    <link rel="icon" href="%(A)s/images/logo/favicon.ico" sizes="any">
    <link rel="icon" type="image/png" href="%(A)s/images/logo/favicon.png">
    <link rel="apple-touch-icon" href="%(A)s/images/logo/apple-touch-icon.png">
    <link rel="stylesheet" href="%(A)s/css/bootstrap.min.css">
    <link rel="stylesheet" href="%(A)s/css/main.css">
    <link rel="stylesheet" href="%(A)s/css/aos.css">
    <link rel="stylesheet" href="%(A)s/css/phosphor.css">
    <script type="application/ld+json">
%(schema)s
    </script>
    <script type="application/ld+json">
%(crumbs)s
    </script>
%(gads)s</head>
""" % dict(lang='en' if en else 'uk', title=title, desc=desc, kw=kw, url=url,
           uk_url=uk_url, en_url=en_url, og=og, A=A, gads=GADS,
           locale='en_US' if en else 'uk_UA', schema=J(schema), crumbs=J(crumbs))


# ------------------------------------------------------------------- сборка main
def figure(slug, sh, eager, pad, mb):
    """Скриншот с подписью. Самый первый на странице - eager, он же LCP."""
    p = '../assets/images/cases/%s/%s' % (slug, sh['f'])
    srcset = ', '.join('%s-%dw.webp %dw' % (p, w, w) for w in sh['ws'])
    return ("""%(i)s<figure class="%(mb)s">
%(i)s    <img class="w-100 h-auto tw-rounded-2xl border border-neutral-200" %(load)s decoding="async" width="%(w)d" height="%(h)d" src="%(p)s-%(big)dw.webp" srcset="%(srcset)s" sizes="%(sizes)s" alt="%(alt)s" data-en-alt="%(alt_en)s">
%(i)s    <figcaption class="tw-text-base text-heading tw-mt-4 text-center" data-en="%(cap_en)s">%(cap)s</figcaption>
%(i)s</figure>
""" % dict(i=' ' * pad, mb=mb, p=p, big=sh['ws'][-1], srcset=srcset, w=sh['w'], h=sh['h'],
           sizes=sh['sizes'], load='loading="eager" fetchpriority="high"' if eager else 'loading="lazy"',
           alt=sh['alt_uk'], alt_en=sh['alt_en'], cap=sh['cap_uk'], cap_en=sh['cap_en']))


def main_block(slug):
    C = CASES[slug]
    out = []
    seen_h2 = [False]
    first_shot = [True]

    def add(s):
        out.append(s)

    for blk in C['body']:
        kind = blk[0]
        if kind == 'h2':
            mt = '' if not seen_h2[0] else ' tw-mt-10'
            seen_h2[0] = True
            add('                            <h2 class="tw-text-7 fw-semibold text-heading%s tw-mb-6" '
                'data-en="%s">%s</h2>\n' % (mt, blk[2], blk[1]))
        elif kind == 'h3':
            add('                            <h3 class="tw-text-3xl fw-semibold text-heading tw-mt-10 tw-mb-4" '
                'data-en="%s">%s</h3>\n' % (blk[2], blk[1]))
        elif kind == 'p':
            add('                            <p class="tw-text-lg tw-mb-6" data-en="%s">%s</p>\n' % (blk[2], blk[1]))
        elif kind == 'list':
            items = '\n'.join(
                '                                <li class="d-flex align-items-start tw-gap-3">'
                '<span class="text-main-two-600 tw-text-xl lh-1">&rarr;</span> '
                '<span class="tw-text-lg text-heading" data-en="%s">%s</span></li>' % (en, uk)
                for uk, en in blk[1])
            add('                            <ul class="d-flex flex-column tw-gap-4 tw-mb-10">\n%s\n'
                '                            </ul>\n' % items)
        elif kind == 'shots':
            wrap, keys = blk[1], blk[2]
            if wrap is None:
                for k in keys:
                    add(figure(slug, C['shots'][k], first_shot[0], 28, 'tw-mb-12'))
                    first_shot[0] = False
            else:
                add('                            <div class="row gy-4 tw-mb-10">\n')
                for k in keys:
                    add('                                <div class="%s">\n' % wrap)
                    add(figure(slug, C['shots'][k], first_shot[0], 36, 'mb-0'))
                    first_shot[0] = False
                    add('                                </div>\n')
                add('                            </div>\n')
        else:
            raise ValueError('unknown block %r' % kind)

    badges = '\n'.join(
        '                                    <li><span class="tw-text-sm fw-medium text-heading '
        'border border-neutral-200 tw-py-1 tw-px-4 tw-rounded-md">%s</span></li>' % t
        for t in C['stack'])

    return """            <main>
            <article class="blog-details-area py-120 tw-mt-15">
                <div class="container">
                    <div class="row justify-content-center">
                        <div class="col-xl-10">
                            <nav class="tw-mb-8" aria-label="breadcrumb">
                                <ul class="d-flex flex-wrap align-items-center justify-content-center tw-gap-2 tw-text-sm fw-medium">
                                    <li><a class="text-heading hover-text-main-two-600 cursor-small" href="/" data-en="Home">Головна</a></li>
                                    <li class="text-heading">/</li>
                                    <li><a class="text-heading hover-text-main-two-600 cursor-small" href="/#projects" data-en="Cases">Кейси</a></li>
                                    <li class="text-heading">/</li>
                                    <li class="text-main-two-600" data-en="%(h1_en)s">%(h1_uk)s</li>
                                </ul>
                            </nav>
                            <div class="tw-mb-10 text-center">
                                <div class="blog-three-meta d-flex justify-content-center tw-mb-6">
                                    <ul class="d-flex align-items-center justify-content-center tw-gap-305">
                                        <li><a class="fw-medium text-heading text-uppercase border border-neutral-200 tw-py-1 tw-px-7 tw-rounded-md hover-bg-main-two-600 hover-text-white hover-border-main-two-600 cursor-small" href="/#projects" data-en="Case">Кейс</a></li>
                                        <li><span class="fw-medium text-heading text-uppercase border border-neutral-200 tw-py-1 tw-px-7 tw-rounded-md" data-en="%(tag_en)s">%(tag_uk)s</span></li>
                                    </ul>
                                </div>
                                <h1 class="tw-text-13 fw-bold text-heading" data-en="%(h1_en)s">%(h1_uk)s</h1>
                            </div>
                            <p class="tw-text-lg tw-mb-6" data-en="%(lead_en)s">%(lead_uk)s</p>
                            <p class="tw-text-lg tw-mb-6" data-en="%(who_en)s">%(who_uk)s</p>
                            <p class="tw-text-lg tw-mb-6" data-en="%(stack_en)s">%(stack_uk)s</p>
                            <ul class="d-flex flex-wrap tw-gap-2 tw-mb-10">
%(badges)s
                            </ul>
%(body)s                            <div class="gray--bg tw-rounded-2xl tw-p-10 tw-mt-15 text-center">
                                <h3 class="tw-text-3xl fw-semibold text-heading tw-mb-6" data-en="%(cta_en)s">%(cta_uk)s</h3>
                                <div class="d-flex align-items-center justify-content-center tw-gap-4 flex-wrap">
                                    <a class="tw-hover-btn bg-main-two-600 text-white justify-content-center text-capitalize cursor-small fw-semibold tw-py-4 tw-px-8 d-inline-flex align-items-center tw-gap-3 hover-text-white hover-border-main-600 tw-rounded-xl" href="/#contact"><span data-en="Send a request">Залишити заявку</span></a>
                                    <a class="tw-hover-btn bg-black text-white justify-content-center text-capitalize cursor-small fw-semibold tw-py-4 tw-px-8 d-inline-flex align-items-center tw-gap-3 hover-text-white tw-rounded-xl" href="https://t.me/devllydev" target="_blank" rel="noopener"><span>Telegram</span></a>
                                </div>
                            </div>
                            <div class="tw-mt-15 text-center">
                                <a class="tw-hover-btn bg-black text-white justify-content-center text-capitalize cursor-small fw-semibold tw-py-4 tw-px-8 d-inline-flex align-items-center tw-gap-3 hover-text-white tw-rounded-xl" href="/#projects" data-en="All cases">Усі кейси</a>
                            </div>
                        </div>
                    </div>
                </div>
            </article>
            </main>
""" % dict(badges=badges, body=''.join(out), h1_uk=C['h1_uk'], h1_en=C['h1_en'],
           tag_uk=C['tag_uk'], tag_en=C['tag_en'], lead_uk=C['lead_uk'], lead_en=C['lead_en'],
           who_uk=C['who_uk'], who_en=C['who_en'], stack_uk=C['stack_uk'], stack_en=C['stack_en'],
           cta_uk=C['cta_uk'], cta_en=C['cta_en'])


# ------------------------------------------------------------------ EN-переписи
def _en_links(x):
    for a in ['about', 'services', 'blog', 'contact', 'projects']:
        x = x.replace('href="#%s"' % a, 'href="/en#%s"' % a)
        x = x.replace('href="/#%s"' % a, 'href="/en#%s"' % a)
    x = x.replace('href="blog/', 'href="/en/blog/')
    x = x.replace('href="/blog/', 'href="/en/blog/')
    x = x.replace('href="/cases/', 'href="/en/cases/')
    x = x.replace('href="/"', 'href="/en"')
    x = x.replace('data-lang="uk" href="/en"', 'data-lang="uk" href="/"')
    return x


def to_en_alt(s):
    """data-en-alt -> alt (enify такого атрибута не знает: у него только текст, placeholder и aria)."""
    def f(m):
        return re.sub(r'\salt="[^"]*"', ' alt="%s"' % m.group(1), m.group(0), count=1)
    s = re.sub(r'<img[^>]*?\sdata-en-alt="([^"]*)"[^>]*?>', f, s)
    return re.sub(r'\sdata-en-alt="[^"]*"', '', s)


def rewrite_en(b):
    b = to_en_alt(b)
    b = to_en(b)
    # /en/cases/<slug>: относительные пути не работают - база стала бы /en/, а не корнем.
    # Бьём ../assets/ безусловно: во srcset второй URL стоит после ", ", а не после кавычки.
    b = b.replace('../assets/', '/assets/')
    b = re.sub(r'(?<![./\w])assets/', '/assets/', b)
    return outside_scripts(b, _en_links)


def strip_uk_only(b):
    """UK-страница: служебный data-en-alt в вывод не идёт."""
    return re.sub(r'\sdata-en-alt="[^"]*"', '', b)


# ------------------------------------------------------------------------- сборка
def build(slug, shell):
    top = shell[shell.index('<body'):shell.index('            <main>')]
    post = shell[shell.index('            </main>') + len('            </main>\n'):]

    # Переключатель языка ведёт на этот же кейс в другом языке. Прячем оба href за
    # плейсхолдеры ДО EN-переписи: иначе _en_links успевает превратить UK-ссылку в /en/...
    top = top.replace('data-lang="uk" href="%s"' % SHELL_UK_HREF, 'data-lang="uk" href="@@SW_UK@@"')
    top = top.replace('data-lang="en" href="%s"' % SHELL_EN_HREF, 'data-lang="en" href="@@SW_EN@@"')

    def switcher(page):
        return (page.replace('@@SW_UK@@', '/cases/%s' % slug)
                    .replace('@@SW_EN@@', '/en/cases/%s' % slug))

    body = main_block(slug)

    uk = switcher(head(slug) + top + strip_uk_only(body) + post)
    if not os.path.isdir(ROOT + '/cases'):
        os.makedirs(ROOT + '/cases')
    io.open(ROOT + '/cases/%s.html' % slug, 'w', encoding='utf-8', newline='\n').write(uk)

    en = switcher(head(slug, en=True) + rewrite_en(top) + rewrite_en(body) + rewrite_en(post))
    if not os.path.isdir(ROOT + '/en/cases'):
        os.makedirs(ROOT + '/en/cases')
    io.open(ROOT + '/en/cases/%s.html' % slug, 'w', encoding='utf-8', newline='\n').write(en)
    return uk, en


if __name__ == '__main__':
    slugs = sys.argv[1:] or list(CASES)
    shell = io.open(SHELL, encoding='utf-8').read()

    def chk(name, slug, s, en_page):
        print('%s:' % name)
        print('  lang               :', re.search(r'<html lang="(\w+)"', s).group(1))
        print('  остатки data-en    :', s.count('data-en'))
        print('  <img> кейса        :', s.count('/%s/' % slug) - s.count('og.jpg'))
        print('  alt пустых у кейса :', len(re.findall(r'cases/%s[^>]*alt=""' % slug, s)))
        print('  баланс div         :', s.count('<div') - s.count('</div>'))
        print('  h1                 :', s.count('<h1'))
        if en_page:
            print('  относительн. assets:', s.count('="../assets/'))
            print('  кириллица в тексте :', len(re.findall(r'>[^<>]*[а-яїієґА-ЯЇІЄҐ][^<>]*<', s)))
            print('  кириллица в alt    :', len(re.findall(r'alt="[^"]*[а-яїієґА-ЯЇІЄҐ]', s)))

    for slug in slugs:
        uk, en = build(slug, shell)
        chk('cases/%s.html' % slug, slug, uk, False)
        chk('en/cases/%s.html' % slug, slug, en, True)
