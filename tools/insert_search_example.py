# -*- coding: utf-8 -*-
# Добавляет 13 диаспорных статей в поисковый INDEX index.html (uk/ru/en ключевики в поле k)
import io, json, os, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get('DEVLLY_ROOT', os.path.dirname(_HERE))
SCRATCH = os.environ.get('DEVLLY_ARTICLES', os.path.join(_HERE, 'articles'))

# трёхъязычные ключи как запасной слой поверх seo.k из самих статей
K = {
'crm-systema-dlya-internet-magazynu-porivnyannya':'crm система для інтернет-магазину, яка crm краще для інтернет-магазину, порівняння crm, срм для інтернет-магазину, crm система для интернет-магазина, какая crm лучше для интернет-магазина, сравнение crm, crm for online store, best crm for ecommerce, ecommerce crm comparison',
'avtomatyzatsiya-obrobky-zamovlen-internet-magazyn':'автоматизація обробки замовлень, обробка замовлень інтернет-магазину, автоматизація інтернет-магазину, прийом замовлень, автоматизация обработки заказов, обработка заказов интернет-магазина, прием заказов, order processing automation, online store order management, ecommerce order automation',
'internet-magazyn-crm-chy-google-sheets':'crm чи google таблиці для інтернет-магазину, інтернет-магазин таблиці чи crm, коли потрібна crm магазину, срм чи таблиці, crm или google таблицы для интернет-магазина, интернет-магазин таблицы или crm, crm vs google sheets for online store, ecommerce spreadsheet vs crm',
}
ORDER = ['crm-systema-dlya-internet-magazynu-porivnyannya',
         'avtomatyzatsiya-obrobky-zamovlen-internet-magazyn',
         'internet-magazyn-crm-chy-google-sheets']

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
