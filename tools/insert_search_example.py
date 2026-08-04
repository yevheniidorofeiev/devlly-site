# -*- coding: utf-8 -*-
# Добавляет новые статьи в поисковый INDEX index.html (uk/ru/en ключевики в поле k)
import io, json, os, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get('DEVLLY_ROOT', os.path.dirname(_HERE))
SCRATCH = os.environ.get('DEVLLY_ARTICLES', os.path.join(_HERE, 'articles'))

# трёхъязычные ключи как запасной слой поверх seo.k из самих статей
K = {
'crm-dlya-dropshippingu':'crm для дропшипінгу, система обліку замовлень дропшипінг, облік замовлень без складу, картка замовлення дропшипінг, маржа в дропшипінгу, кілька постачальників в одній системі, crm для дропшиппинга, учет заказов дропшиппинг, система для дропшиппера, маржа в дропшиппинге, dropshipping crm, dropshipping order management, dropshipping profit tracking',
'dropshipping-postachalnyky-ukraina':'дропшипінг постачальники україна, постачальники для дропшипінгу, як знайти постачальника дропшипінг, перевірка постачальника, умови дропшипінгу, синхронізація залишків постачальника, дропшиппинг поставщики украина, поставщики для дропшиппинга, как найти поставщика дропшиппинг, dropshipping suppliers ukraine, how to find dropshipping supplier, supplier stock sync',
'avtomatyzatsiya-dropshipping-aliexpress':'автоматизація дропшипінгу з aliexpress, дропшипінг aliexpress україна, імпорт товарів з aliexpress, ціноутворення дропшипінг, трекінг посилок з китаю, оформлення замовлень постачальнику, автоматизация дропшиппинга aliexpress, дропшиппинг с алиэкспресс, импорт товаров алиэкспресс, aliexpress dropshipping automation, product import aliexpress, order tracking china',
}
ORDER = ['crm-dlya-dropshippingu','dropshipping-postachalnyky-ukraina',
         'avtomatyzatsiya-dropshipping-aliexpress']

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
