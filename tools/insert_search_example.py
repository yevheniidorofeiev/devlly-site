# -*- coding: utf-8 -*-
# Добавляет 13 диаспорных статей в поисковый INDEX index.html (uk/ru/en ключевики в поле k)
import io, json, os, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get('DEVLLY_ROOT', os.path.dirname(_HERE))
SCRATCH = os.environ.get('DEVLLY_ARTICLES', os.path.join(_HERE, 'articles'))

# трёхъязычные ключи как запасной слой поверх seo.k из самих статей
K = {
'telegram-bot-dlya-ukraintsiv-v-yevropi':'телеграм бот для українців у європі, бот для бізнесу за кордоном, бізнес без офісу, телеграм бот для украинцев в европе, бот для бизнеса за границей, бизнес без офиса, telegram bot for ukrainians in europe, business without office',
'avtomatyzatsiya-biznesu-za-kordonom':'автоматизація бізнесу за кордоном, бізнес для українців за кордоном, автоматизация бизнеса за границей, бизнес для украинцев за рубежом, business automation abroad, ukrainian entrepreneur abroad',
'viddalene-upravlinnya-biznesom-z-ukrainy':'віддалене управління бізнесом, керувати бізнесом дистанційно з україни, удаленное управление бизнесом, управлять бизнесом дистанционно, remote business management from ukraine',
'crm-dlya-ukrainskoi-diaspory':'crm для української діаспори, бізнес на дві країни, crm для украинской диаспоры, бизнес в двух странах, crm for ukrainian diaspora, business across two countries',
'crm-dlya-biznesu-v-polshchi':'crm для бізнесу в польщі, срм для українців у польщі, оплата в злотих, crm для бизнеса в польше, срм для украинцев в польше, оплата в злотых, crm for business in poland, blik przelewy24 inpost',
'avtomatyzatsiya-ukrainskogo-biznesu-v-nimechchyni':'автоматизація бізнесу в німеччині, український бізнес у німеччині, rechnung, автоматизация бизнеса в германии, украинский бизнес в германии, business automation in germany, kleinunternehmer',
'telegram-bot-zamovlennya-z-polshchi':'телеграм бот для замовлень з польщі, прийом замовлень польща, телеграм бот для заказов из польши, прием заказов польша, telegram bot orders from poland, blik paczkomaty',
'crm-ukrainskyi-biznes-chehiya':'crm для бізнесу в чехії, український бізнес у чехії, крона, crm для бизнеса в чехии, украинский бизнес в чехии, crm for business in czechia, zasilkovna packeta',
'relokatsiya-biznesu-bez-vtraty-klientiv':'релокація бізнесу, перенести бізнес за кордон, міграція бази клієнтів, релокация бизнеса, перенести бизнес за границу, business relocation without losing clients',
'dropshipping-z-polshchi-v-ukrainu':'дропшипінг з польщі, дропшипінг польща україна, дропшиппинг из польши, дропшиппинг польша украина, dropshipping from poland to ukraine, cross border',
'komanda-za-kordonom-avtomatyzatsiya':'команда за кордоном, розподілена команда, автоматизація роботи команди, распределенная команда за границей, удаленная команда, remote team abroad automation',
'eksport-v-yevropu-crm':'crm для експорту, експорт в європу, b2b експорт, crm для экспорта, экспорт в европу, crm for export to europe, b2b export',
'viddalenyi-internet-magazyn-z-ukrainy':'віддалений інтернет-магазин, вести магазин дистанційно, удаленный интернет-магазин, вести магазин дистанционно, remote online store from ukraine',
}
ORDER = ['telegram-bot-dlya-ukraintsiv-v-yevropi','avtomatyzatsiya-biznesu-za-kordonom',
         'viddalene-upravlinnya-biznesom-z-ukrainy','crm-dlya-ukrainskoi-diaspory',
         'crm-dlya-biznesu-v-polshchi','avtomatyzatsiya-ukrainskogo-biznesu-v-nimechchyni',
         'telegram-bot-zamovlennya-z-polshchi','crm-ukrainskyi-biznes-chehiya',
         'relokatsiya-biznesu-bez-vtraty-klientiv','dropshipping-z-polshchi-v-ukrainu',
         'komanda-za-kordonom-avtomatyzatsiya','eksport-v-yevropu-crm',
         'viddalenyi-internet-magazyn-z-ukrainy']

def js(v): return json.dumps(v, ensure_ascii=False)
entries=[]
for slug in ORDER:
    a=json.load(io.open(SCRATCH+'/art_%s.json'%slug,encoding='utf-8'))
    entries.append('  {\n    "t": "b",\n    "uk": %s,\n    "en": %s,\n    "url": %s,\n    "k": %s\n  }'
        %(js(a['title_uk']), js(a['title_en']), js('/blog/'+slug), js(K[slug])))
html=io.open(ROOT+'/index.html',encoding='utf-8').read()
CLOSE='\n  }\n];'
assert html.count(CLOSE)==1, 'close marker count=%d'%html.count(CLOSE)
html=html.replace(CLOSE, '\n  }' + ',\n'+',\n'.join(entries) + '\n];', 1)
io.open(ROOT+'/index.html','w',encoding='utf-8',newline='\n').write(html)
print('search INDEX entries added:', len(entries))
