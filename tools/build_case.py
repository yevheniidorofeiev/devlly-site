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
  ('note', t_uk, t_en, p_uk, p_en) серая плашка с заголовком и абзацем
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

# геометрия скриншотов по классам (см. tools/README.md): натуральный размер
# крупного варианта + ширины в srcset + sizes под верстку конкретного блока
GEOM = {
    'wide':  dict(w=1456, h=821, ws=[800, 1456], sizes='(max-width: 1199px) 100vw, 950px'),
    'sheet': dict(w=1456, h=691, ws=[800, 1456], sizes='(max-width: 1199px) 100vw, 1150px'),
    'app':   dict(w=476, h=906, ws=[320, 476], sizes='(max-width: 1199px) 45vw, 270px'),
    'bot':   dict(w=696, h=878, ws=[480, 696], sizes='(max-width: 767px) 92vw, (max-width: 1199px) 45vw, 565px'),
    'bot1':  dict(w=696, h=878, ws=[480, 696], sizes='(max-width: 767px) 92vw, (max-width: 1199px) 45vw, 470px'),
}


def shot(f, cls, alt_uk, alt_en, cap_uk, cap_en):
    d = dict(GEOM[cls])
    d.update(f=f, alt_uk=alt_uk, alt_en=alt_en, cap_uk=cap_uk, cap_en=cap_en)
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

    ('note', 'Це працюючий продукт, а не макет', 'This is a working product, not a mock-up',
     'На скриншотах - жива система: Mini App працює з бекендом, записи справді пишуться в Google Таблицю, '
     'а нагадування надсилає шедулер за розкладом. Демонстраційні тут лише дані самого салону.',
     'The screenshots show a live system: the Mini App talks to a back end, bookings really are written into the Google Sheet '
     'and the reminders are sent by a scheduler on a timer. The only thing made up here is the salon’s own data.'),
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
</head>
""" % dict(lang='en' if en else 'uk', title=title, desc=desc, kw=kw, url=url,
           uk_url=uk_url, en_url=en_url, og=og, A=A,
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
        elif kind == 'note':
            add('                            <div class="gray--bg tw-rounded-2xl tw-p-8 tw-mt-10">\n'
                '                                <h3 class="tw-text-2xl fw-semibold text-heading tw-mb-3" '
                'data-en="%s">%s</h3>\n'
                '                                <p class="tw-text-lg text-heading mb-0" data-en="%s">%s</p>\n'
                '                            </div>\n' % (blk[2], blk[1], blk[4], blk[3]))
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
