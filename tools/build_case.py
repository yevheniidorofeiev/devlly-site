# -*- coding: utf-8 -*-
"""
Генератор страниц портфолио-кейсов (/cases/<slug> + /en/cases/<slug>).

Отдельно от блог-пайплайна: build_blog.py / CLUSTERS / RELATED здесь не участвуют.
Общее с ними только одно - движок EN-версии (enify.to_en), чтобы двуязычность
работала ровно так же, как на остальном сайте: разметка пишется по-украински
с data-en, EN-файл статически выпекается из неё.

Оболочка (шапка/подвал/скрипты) берётся из готовой страницы блога, чтобы
хедер, футер, поиск и меню не расходились с остальным сайтом.
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

# ---------------------------------------------------------------- контент кейса
SLUG = 'kvadratnyi-metr'
DATE = '2026-07-28'
IMGDIR = 'images/cases/' + SLUG

CASE = dict(
    h1_uk='CRM-система «Квадратний Метр»',
    h1_en='The Kvadratnyi Metr CRM',
    title_uk='CRM для рієлторів - кейс «Квадратний Метр» | Devlly',
    title_en='CRM for realtors - the Kvadratnyi Metr case study | Devlly',
    desc_uk='Кейс Devlly: CRM-система для рієлторської агенції - облік заявок, воронка продажів, '
            'канбан угод, каталог об’єктів і аналітика по агентах. Приклад інтерфейсу на React + Recharts.',
    desc_en='A Devlly case study: a CRM for a real estate agency - request tracking, a sales funnel, '
            'a deal kanban, a property catalogue and per-agent analytics. An interface example built with React and Recharts.',
    keywords_uk='crm для агентства нерухомості приклад, crm для рієлторів, кейс crm нерухомість, '
                'воронка продажів нерухомість, канбан угод, crm для ріелтора приклад, приклад інтерфейсу crm',
    keywords_en='crm for real estate agency example, crm for realtors, real estate crm case study, '
                'real estate sales funnel, deal kanban, crm interface example',
    # интро
    lead_uk='«Квадратний Метр» - CRM-система для рієлторської агенції: облік заявок, воронка продажів, '
            'аналітика по агентах і джерелах трафіку. Інтерфейс побудований під щоденну роботу відділу '
            'продажів - від першого звернення клієнта до закритої угоди.',
    lead_en='Kvadratnyi Metr is a CRM for a real estate agency: request tracking, a sales funnel and analytics '
            'by agent and by traffic source. The interface is built around the daily routine of a sales team - '
            'from a client’s first enquiry to a closed deal.',
    who_uk='Кому підходить: агенціям нерухомості, які ведуть об’єкти й клієнтів у таблицях і втрачають '
           'заявки через те, що немає єдиної воронки й видимості, на якій стадії стоїть кожна угода.',
    who_en='Who it fits: real estate agencies that keep properties and clients in spreadsheets and lose '
           'requests because there is no single funnel and no visibility into which stage each deal sits at.',
    stack=['React', 'Vite', 'Tailwind CSS', 'Recharts'],
    stack_uk='Стек: React + Vite, Tailwind CSS для інтерфейсу, Recharts для графіків і діаграм.',
    stack_en='Stack: React with Vite, Tailwind CSS for the interface and Recharts for charts and diagrams.',
    note_uk='Це фронтенд-демо на тестових даних - воно ілюструє інтерфейс і логіку роботи CRM. '
            'Цифри, імена, адреси й контакти на скриншотах вигадані й не належать жодному реальному '
            'клієнту чи угоді.',
    note_en='This is a front-end demo running on test data - it illustrates the interface and the logic of the CRM. '
            'The figures, names, addresses and contacts in the screenshots are invented and belong to no real '
            'client or deal.',
)

# 6 самых показательных скриншотов из 9
SHOTS = [
    dict(f='dashboard',
         alt_uk='CRM для рієлторської агенції - дашборд угод з KPI та воронкою продажів',
         alt_en='CRM for a real estate agency - deal dashboard with KPIs and a sales funnel',
         cap_uk='Дашборд: активні угоди, сума в роботі, середній чек і конверсія ліда в угоду. '
                'Поруч - воронка з відсівом на кожному переході, ефективність агентів і час відповіді на заявку.',
         cap_en='Dashboard: active deals, the value in progress, the average deal size and lead-to-deal conversion. '
                'Next to it - the funnel with drop-off at every step, agent performance and response time to a request.'),
    dict(f='kanban',
         alt_uk='Канбан-дошка угод у CRM для нерухомості - стадії від нового ліда до закритої угоди',
         alt_en='Deal kanban board in a real estate CRM - stages from a new lead to a closed deal',
         cap_uk='Канбан-дошка угод: п’ять стадій від нового ліда до закритої угоди. Картку можна перетягнути '
                'у наступну стадію, над кожною колонкою - кількість угод і їхня сума.',
         cap_en='Deal kanban: five stages from a new lead to a closed deal. A card can be dragged into the next '
                'stage, and each column header shows the number of deals and their total value.'),
    dict(f='listings',
         alt_uk='Каталог об’єктів нерухомості у CRM - картки квартир, будинків і комерції з фільтрами',
         alt_en='Property catalogue in the CRM - cards for flats, houses and commercial units with filters',
         cap_uk='Каталог об’єктів: квартири, будинки, комерція й ділянки з фільтрами за типом, статусом продажу, '
                'площею, поверхом і ціною. На кожній картці - кількість переглядів і відповідальний агент.',
         cap_en='Property catalogue: flats, houses, commercial units and land plots, filtered by type, sale status, '
                'area, floor and price. Each card shows the view count and the agent in charge.'),
    dict(f='clients',
         alt_uk='База клієнтів у CRM для рієлторів - покупці та продавці з бюджетом і статусом угоди',
         alt_en='Client database in a CRM for realtors - buyers and sellers with budget and deal status',
         cap_uk='База клієнтів: покупці, продавці й обміни. По кожному записі - запит, бюджет, статус угоди, '
                'відповідальний агент і дата появи в базі; є пошук, фільтри за типом і експорт.',
         cap_en='Client database: buyers, sellers and exchanges. Every record carries the request, the budget, the deal '
                'status, the agent in charge and the date it entered the database; search, type filters and export included.'),
    dict(f='reports',
         alt_uk='Звіти по джерелах заявок у CRM для агентства нерухомості - план/факт і продажі за районами',
         alt_en='Request-source reports in a real estate agency CRM - plan versus actual and sales by district',
         cap_uk='Звіти: план/факт за обсягом угод по місяцях, джерела заявок (OLX, сайт агенції, рекомендації, '
                'Instagram, Google Ads) і розподіл продажів за районами міста.',
         cap_en='Reports: plan versus actual deal volume by month, request sources (OLX, the agency website, referrals, '
                'Instagram, Google Ads) and the distribution of sales across city districts.'),
    dict(f='agents',
         alt_uk='Аналітика по агентах у CRM для нерухомості - закриті угоди, комісія та рейтинг',
         alt_en='Per-agent analytics in a real estate CRM - closed deals, commission and rating',
         cap_uk='Агенти: закриті угоди, обсяг, комісія, середній час відповіді й рейтинг по кожному агенту, '
                'плюс зведений графік результатів команди за місяць.',
         cap_en='Agents: closed deals, volume, commission, average response time and rating for every agent, '
                'plus a combined chart of the team’s results for the month.'),
]

FEATURES = [
    ('Єдина воронка заявок: новий лід → перегляд об’єкта → торг → завдаток → угода закрита, '
     'з наскрізною конверсією і відсівом на кожному переході',
     'A single request funnel: new lead → viewing → negotiation → deposit → deal closed, with end-to-end '
     'conversion and drop-off at every step'),
    ('Канбан-дошка угод із перетягуванням карток між стадіями та сумою угод по кожній стадії',
     'A deal kanban board with drag-and-drop between stages and the total deal value per stage'),
    ('Каталог об’єктів: квартири, будинки, комерція, ділянки - з фільтрами, статусами продажу й переглядами',
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
]


# ------------------------------------------------------------------- сборка head
def head(en=False):
    A = '/assets' if en else '../assets'
    url = '%s/%scases/%s' % (BASE, 'en/' if en else '', SLUG)
    uk_url, en_url = '%s/cases/%s' % (BASE, SLUG), '%s/en/cases/%s' % (BASE, SLUG)
    title = CASE['title_en'] if en else CASE['title_uk']
    desc = CASE['desc_en'] if en else CASE['desc_uk']
    kw = CASE['keywords_en'] if en else CASE['keywords_uk']
    name = CASE['h1_en'] if en else CASE['h1_uk']
    og = '%s/assets/%s/og.jpg' % (BASE, IMGDIR)
    cases_n, home_n = ('Cases', 'Home') if en else ('Кейси', 'Головна')
    cases_url = BASE + ('/en#projects' if en else '/#projects')

    schema = {
        "@context": "https://schema.org", "@type": "CreativeWork",
        "name": name, "headline": name, "description": desc, "image": og,
        "datePublished": DATE, "dateModified": DATE,
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
def figure(sh, i):
    """Скриншот с подписью. Первый - eager, он же LCP."""
    p = '../assets/%s/%s' % (IMGDIR, sh['f'])
    eager = (i == 0)
    return """                            <figure class="tw-mb-12">
                                <img class="w-100 h-auto tw-rounded-2xl border border-neutral-200" %(load)s decoding="async" width="1456" height="821" src="%(p)s-1456w.webp" srcset="%(p)s-800w.webp 800w, %(p)s-1456w.webp 1456w" sizes="(max-width: 1199px) 100vw, 950px" alt="%(alt)s" data-en-alt="%(alt_en)s">
                                <figcaption class="tw-text-base text-heading tw-mt-4 text-center" data-en="%(cap_en)s">%(cap)s</figcaption>
                            </figure>
""" % dict(p=p, load='loading="eager" fetchpriority="high"' if eager else 'loading="lazy"',
           alt=sh['alt_uk'], alt_en=sh['alt_en'], cap=sh['cap_uk'], cap_en=sh['cap_en'])


def main_block():
    badges = '\n'.join(
        '                                    <li><span class="tw-text-sm fw-medium text-heading '
        'border border-neutral-200 tw-py-1 tw-px-4 tw-rounded-md">%s</span></li>' % t
        for t in CASE['stack'])
    feats = '\n'.join(
        '                                <li class="d-flex align-items-start tw-gap-3">'
        '<span class="text-main-two-600 tw-text-xl lh-1">&rarr;</span> '
        '<span class="tw-text-lg text-heading" data-en="%s">%s</span></li>' % (en, uk)
        for uk, en in FEATURES)
    shots = ''.join(figure(sh, i) for i, sh in enumerate(SHOTS))

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
                                        <li><span class="fw-medium text-heading text-uppercase border border-neutral-200 tw-py-1 tw-px-7 tw-rounded-md" data-en="Real estate">Нерухомість</span></li>
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
                            <div class="gray--bg tw-rounded-2xl tw-p-8 tw-mb-12">
                                <p class="tw-text-lg tw-mb-0"><strong data-en="Front-end demo on test data.">Фронтенд-демо на тестових даних.</strong> <span data-en="%(note_en)s">%(note_uk)s</span></p>
                            </div>
                            <h2 class="tw-text-7 fw-semibold text-heading tw-mb-6" data-en="How the interface looks">Як виглядає інтерфейс</h2>
%(shots)s
                            <h2 class="tw-text-7 fw-semibold text-heading tw-mt-10 tw-mb-6" data-en="What the system can do">Що вміє система</h2>
                            <ul class="d-flex flex-column tw-gap-4 tw-mb-10">
%(feats)s
                            </ul>
                            <div class="gray--bg tw-rounded-2xl tw-p-10 tw-mt-15 text-center">
                                <h3 class="tw-text-3xl fw-semibold text-heading tw-mb-6" data-en="Want the same system for your business? Get in touch">Хочете таку ж систему для свого бізнесу? Зв’яжіться з нами</h3>
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
""" % dict(badges=badges, feats=feats, shots=shots, **CASE)


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
if __name__ == '__main__':
    shell = io.open(SHELL, encoding='utf-8').read()
    top = shell[shell.index('<body'):shell.index('            <main>')]
    post = shell[shell.index('            </main>') + len('            </main>\n'):]

    # Переключатель языка ведёт на этот же кейс в другом языке. Прячем оба href за
    # плейсхолдеры ДО EN-переписи: иначе _en_links успевает превратить UK-ссылку в /en/...
    top = top.replace('data-lang="uk" href="%s"' % SHELL_UK_HREF, 'data-lang="uk" href="@@SW_UK@@"')
    top = top.replace('data-lang="en" href="%s"' % SHELL_EN_HREF, 'data-lang="en" href="@@SW_EN@@"')

    def switcher(page):
        return (page.replace('@@SW_UK@@', '/cases/%s' % SLUG)
                    .replace('@@SW_EN@@', '/en/cases/%s' % SLUG))

    body = main_block()

    # --- UK ---
    uk = switcher(head() + top + strip_uk_only(body) + post)
    if not os.path.isdir(ROOT + '/cases'):
        os.makedirs(ROOT + '/cases')
    io.open(ROOT + '/cases/%s.html' % SLUG, 'w', encoding='utf-8', newline='\n').write(uk)

    # --- EN ---
    en = switcher(head(en=True) + rewrite_en(top) + rewrite_en(body) + rewrite_en(post))
    if not os.path.isdir(ROOT + '/en/cases'):
        os.makedirs(ROOT + '/en/cases')
    io.open(ROOT + '/en/cases/%s.html' % SLUG, 'w', encoding='utf-8', newline='\n').write(en)

    # ------------------------------------------------------------------- проверки
    def chk(name, s, en_page):
        print('%s:' % name)
        print('  lang               :', re.search(r'<html lang="(\w+)"', s).group(1))
        print('  остатки data-en    :', s.count('data-en'))
        print('  <img> кейса        :', s.count('/%s/' % SLUG) - s.count('og.jpg'))
        print('  alt пустых у кейса :', len(re.findall(r'cases/%s[^>]*alt=""' % SLUG, s)))
        print('  баланс div         :', s.count('<div') - s.count('</div>'))
        print('  h1                 :', s.count('<h1'))
        if en_page:
            print('  относительн. assets:', s.count('="../assets/'))
            print('  кириллица в тексте :', len(re.findall(r'>[^<>]*[а-яїієґА-ЯЇІЄҐ][^<>]*<', s)))
            print('  кириллица в alt    :', len(re.findall(r'alt="[^"]*[а-яїієґА-ЯЇІЄҐ]', s)))
    chk('cases/%s.html' % SLUG, uk, False)
    chk('en/cases/%s.html' % SLUG, en, True)
