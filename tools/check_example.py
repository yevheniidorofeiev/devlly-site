# -*- coding: utf-8 -*-
import io, json, os, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
_HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.environ.get('DEVLLY_ARTICLES', os.path.join(_HERE, 'articles'))
AP = '\u02bc'
# (title_uk, seo.t, desc_uk)  — должны совпадать дословно с ТЗ агентам
FIXED = {
'telegram-bot-dlya-ukraintsiv-v-yevropi':(
  'Telegram-бот для українців у Європі: бізнес без офісу',
  'Telegram-бот для українців у Європі: автоматизація | Devlly',
  'Як українцям у Європі запустити Telegram-бота для прийому замовлень і клієнтів: працює з будь-якої країни, українською, без привʼязки до офісу.'),
'avtomatyzatsiya-biznesu-za-kordonom':(
  'Автоматизація бізнесу за кордоном: інструменти для українців',
  'Автоматизація бізнесу за кордоном для українців | Devlly',
  'Які процеси українському підприємцю за кордоном варто автоматизувати першими: заявки, база клієнтів, платежі і команда. Практичний план без зайвих витрат.'),
'viddalene-upravlinnya-biznesom-z-ukrainy':(
  'Віддалене управління бізнесом з України: як не втратити контроль',
  'Віддалене управління бізнесом з України | Devlly',
  'Як керувати бізнесом дистанційно з України: контроль замовлень, команди і фінансів через CRM і Telegram. Все під рукою навіть за тисячі кілометрів.'),
'crm-dlya-ukrainskoi-diaspory':(
  'CRM для української діаспори: бізнес на дві країни',
  'CRM для української діаспори: клієнти і замовлення | Devlly',
  'CRM для підприємців з української діаспори: вести клієнтів в Україні і Європі одночасно, у різних валютах і часових поясах, в одній системі.'),
'crm-dlya-biznesu-v-polshchi':(
  'CRM для бізнесу в Польщі: облік клієнтів і замовлень',
  'CRM для бізнесу в Польщі для українців | Devlly',
  'CRM для українського бізнесу в Польщі: облік клієнтів, замовлення, оплати в злотих та інтеграції з польськими сервісами доставки. Розробка під ключ.'),
'avtomatyzatsiya-ukrainskogo-biznesu-v-nimechchyni':(
  'Автоматизація українського бізнесу в Німеччині',
  'Автоматизація бізнесу в Німеччині для українців | Devlly',
  'Як автоматизувати український бізнес у Німеччині: облік клієнтів, рахунки, вимоги до документів і платежі в євро. З урахуванням німецької специфіки.'),
'telegram-bot-zamovlennya-z-polshchi':(
  'Telegram-бот для замовлень з Польщі: прийом і доставка',
  'Telegram-бот для прийому замовлень з Польщі | Devlly',
  'Telegram-бот для прийому замовлень з Польщі: меню, оплата в злотих, розрахунок доставки і сповіщення клієнту. Для українського бізнесу в Польщі.'),
'crm-ukrainskyi-biznes-chehiya':(
  'CRM для українського бізнесу в Чехії: клієнти і продажі',
  'CRM для українського бізнесу в Чехії | Devlly',
  'CRM для українців з бізнесом у Чехії: облік клієнтів, замовлення в кронах, локальні платіжні і поштові сервіси. Система під ваш процес продажів.'),
'relokatsiya-biznesu-bez-vtraty-klientiv':(
  'Релокація бізнесу без втрати клієнтів: як зберегти базу',
  'Релокація бізнесу без втрати клієнтів і бази | Devlly',
  'Як перенести бізнес за кордон і не втратити клієнтів: міграція бази, збереження історії замовлень і безперервний звʼязок через CRM і Telegram.'),
'dropshipping-z-polshchi-v-ukrainu':(
  'Дропшипінг з Польщі в Україну: як налаштувати процес',
  'Дропшипінг з Польщі в Україну: автоматизація | Devlly',
  'Як налаштувати дропшипінг з Польщі в Україну: постачальники, прийом замовлень, оплати і трекінг доставки через кордон. Автоматизація без ручної роботи.'),
'komanda-za-kordonom-avtomatyzatsiya':(
  'Команда за кордоном: автоматизація роботи і контролю',
  'Автоматизація роботи команди за кордоном | Devlly',
  'Як організувати роботу розподіленої команди за кордоном: постановка задач, контроль виконання і звіти через Telegram, без нескінченних дзвінків.'),
'eksport-v-yevropu-crm':(
  'CRM для експорту в Європу: угоди, документи і клієнти',
  'CRM для експорту в Європу для українців | Devlly',
  'CRM для експорту з України в Європу: облік B2B-клієнтів, угоди в євро, документи і контроль поставок. Система під експортний процес бізнесу.'),
'viddalenyi-internet-magazyn-z-ukrainy':(
  'Віддалений інтернет-магазин з України: керувати звідусіль',
  'Віддалений інтернет-магазин з України: автоматизація | Devlly',
  'Як вести інтернет-магазин з України дистанційно: прийом замовлень, склад, доставка і клієнти в одній системі. Контроль з будь-якої точки світу.'),
}
REQ_TOP=['title_uk','title_en','desc_uk','desc_en','cta_uk','cta_en','seo','blocks']
REQ_SEO=['t','te','d','de','k']
allok=True
for slug in FIXED:
    p=SCRATCH+'/art_%s.json'%slug
    try: a=json.load(io.open(p,encoding='utf-8'))
    except Exception as e:
        print('FAIL %-46s load: %s'%(slug,e)); allok=False; continue
    errs=[]
    for k in REQ_TOP:
        if k not in a: errs.append('miss '+k)
    for k in REQ_SEO:
        if k not in a.get('seo',{}): errs.append('miss seo.'+k)
    blocks=a.get('blocks',[])
    if not blocks or blocks[0].get('t')!='lead': errs.append('blocks[0]!=lead')
    h2=sum(1 for b in blocks if b.get('t')=='h2')
    if h2!=5: errs.append('h2=%d'%h2)
    words=sum(len(b.get('uk','').split()) for b in blocks)
    if not (800<=words<=1200): errs.append('words=%d'%words)
    joined=json.dumps(a,ensure_ascii=False)
    if '\u2014' in joined: errs.append('EM DASH')
    if '\u2013' in joined: errs.append('EN DASH')
    if 'devlly.official' in joined or 't.me/' in joined: errs.append('CONTACT in blocks')
    uk_all=' '.join(b.get('uk','') for b in blocks)
    if '\u2019' in uk_all or "'" in uk_all: errs.append('bad apostrophe in UK')
    for b in blocks:
        if not b.get('uk','').strip() or not b.get('en','').strip(): errs.append('block miss uk/en')
    tu,st,du=FIXED[slug]
    if a.get('title_uk')!=tu: errs.append('title_uk!=fixed')
    if a.get('seo',{}).get('t')!=st: errs.append('seo.t!=fixed')
    if a.get('desc_uk')!=du: errs.append('desc_uk!=fixed')
    if a.get('seo',{}).get('d')!=a.get('desc_uk'): errs.append('seo.d!=desc_uk')
    if a.get('seo',{}).get('de')!=a.get('desc_en'): errs.append('seo.de!=desc_en')
    k=a.get('seo',{}).get('k','')
    if 'Devlly' not in uk_all: errs.append('no Devlly')
    st_='OK  ' if not errs else 'FAIL'
    if errs: allok=False
    print('%s %-46s w=%-4d h2=%d %s'%(st_,slug,words,h2,'; '.join(errs)))
print('RESULT:', 'ALL OK' if allok else 'HAS ERRORS')
