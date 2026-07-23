# -*- coding: utf-8 -*-
import io, json, os

# Пути относительно tools/ внутри репозитория (см. tools/README.md).
_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get('DEVLLY_ROOT', os.path.dirname(_HERE))
SCRATCH = os.environ.get('DEVLLY_ARTICLES', os.path.join(_HERE, 'articles'))
BASE = 'https://devlly.dev'

# порядок по дате (зростання), дати - джерело правди
ITEMS = [
 ('telegram-bot-dlya-ukraintsiv-v-yevropi','2026-01-11','1'),
 ('avtomatyzatsiya-biznesu-za-kordonom','2026-01-24','2'),
 ('viddalene-upravlinnya-biznesom-z-ukrainy','2026-02-08','3'),
 ('crm-dlya-ukrainskoi-diaspory','2026-02-19','4'),
 ('crm-dlya-biznesu-v-polshchi','2026-03-05','1'),
 ('avtomatyzatsiya-ukrainskogo-biznesu-v-nimechchyni','2026-03-16','2'),
 ('telegram-bot-zamovlennya-z-polshchi','2026-04-11','3'),
 ('crm-ukrainskyi-biznes-chehiya','2026-04-23','4'),
 ('relokatsiya-biznesu-bez-vtraty-klientiv','2026-05-16','1'),
 ('dropshipping-z-polshchi-v-ukrainu','2026-06-12','2'),
 ('komanda-za-kordonom-avtomatyzatsiya','2026-06-27','3'),
 ('eksport-v-yevropu-crm','2026-07-09','4'),
 ('viddalenyi-internet-magazyn-z-ukrainy','2026-07-22','1'),
]
UA_M = ['СІЧ','ЛЮТ','БЕР','КВІ','ТРА','ЧЕР','ЛИП','СЕР','ВЕР','ЖОВ','ЛИС','ГРУ']
EN_M = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
def dates(iso):
    y,m,d = (int(x) for x in iso.split('-'))
    return '%02d %s %d'%(d,UA_M[m-1],y), '%s %d, %d'%(EN_M[m-1],d,y)

def ea(v): return v.replace('&','&amp;').replace('"','&quot;').replace('<','&lt;').replace('>','&gt;')
def et(v): return v.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

CARD = '''                <div class="col-xl-4 blog-card" style="display:none">
                    <div class="tw-mb-705">
                        <div class="blog-two-wrapper blog-three-item gray--bg tw-rounded-2xl tw-p-8">
                            <div class="blog-three-left">
                                <div class="tw-mb-6">
                                    <h3 class="tw-text-3xl"><a class="cursor-small hover-text-main-two-600" href="blog/{slug}" data-en="{te}">{tu}</a></h3>
                                    <p class="tw-text-lg text-heading tw-mt-4 tw-mb-0" data-en="{de}">{du}</p>
                                </div>
                                <div class="blog-two-main-thumb blog-three-thumb position-relative overflow-hidden tw-rounded-2xl tw-mb-8">
                                <img srcset="assets/images/thumbs/project-three-thumb{th}-480w.webp 480w, assets/images/thumbs/project-three-thumb{th}-785w.webp 785w" sizes="(max-width: 768px) 100vw, 50vw" loading="lazy" decoding="async" width="785" height="500" class="w-img w-100 tw-rounded-xl tw-transition-5" src="assets/images/thumbs/project-three-thumb{th}-785w.webp" alt="blog">
                                <img srcset="assets/images/thumbs/project-three-thumb{th}-480w.webp 480w, assets/images/thumbs/project-three-thumb{th}-785w.webp 785w" sizes="(max-width: 768px) 100vw, 50vw" loading="lazy" decoding="async" width="785" height="500" class="w-img w-100 tw-rounded-xl tw-transition-5" src="assets/images/thumbs/project-three-thumb{th}-785w.webp" alt="" aria-hidden="true">
                                <a aria-hidden="true" tabindex="-1" class="blog-two-card-image-link d-flex align-items-center justify-content-center w-100 h-100 position-absolute z-1 top-0 start-0" href="blog/{slug}"></a>
                                </div>
                                <div>
                                    <div class="blog-three-meta">
                                        <ul class="d-flex align-items-center tw-gap-305">
                                            <li><a class="fw-medium text-heading text-uppercase border border-neutral-200 tw-py-1 tw-px-7 tw-rounded-md hover-bg-main-two-600 hover-text-white hover-border-main-two-600 cursor-small" href="#" data-en="Article">Стаття</a></li>
                                            <li><a class="fw-medium text-heading text-uppercase border border-neutral-200 tw-py-1 tw-px-7 tw-rounded-md hover-bg-main-two-600 hover-text-white hover-border-main-two-600 cursor-small" href="#" data-en="{den}">{dun}</a></li>
                                        </ul>
                                    </div>
                                    <div class="tw-mt-6">
                                        <a aria-label="Читати статтю: {tu_a}" data-en-aria="Read the article: {te_a}" class="bg-main-two-600 cursor-small text--white text-uppercase tw-text-sm fw-bold tw-rounded-md tw-py-2 tw-px-7" href="blog/{slug}" data-en="Read more">Читати</a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
'''

cards = ''
sm = ''
for slug, iso, th in ITEMS:
    a = json.load(io.open(SCRATCH+'/art_%s.json'%slug, encoding='utf-8'))
    du, den = dates(iso)
    cards += CARD.format(slug=slug, te=ea(a['title_en']), tu=et(a['title_uk']),
        de=ea(a['desc_en']), du=et(a['desc_uk']), th=th, den=ea(den), dun=et(du),
        tu_a=ea(a['title_uk']), te_a=ea(a['title_en']))
    for path in ('/blog/%s'%slug, '/en/blog/%s'%slug):
        sm += ('  <url>\n    <loc>%s%s</loc>\n'
               '    <xhtml:link rel="alternate" hreflang="uk" href="%s/blog/%s"/>\n'
               '    <xhtml:link rel="alternate" hreflang="en" href="%s/en/blog/%s"/>\n'
               '    <xhtml:link rel="alternate" hreflang="x-default" href="%s/blog/%s"/>\n'
               '    <lastmod>%s</lastmod>\n    <priority>0.8</priority>\n  </url>\n'
               )%(BASE,path, BASE,slug, BASE,slug, BASE,slug, iso)

# --- вставка карточек в index.html ---
idx = io.open(ROOT+'/index.html', encoding='utf-8').read()
anchor = ('            </div>\n            <div class="row">\n'
          '                <div class="col-12 text-center tw-mt-5">\n'
          '                    <button type="button" id="blog-load-more"')
assert idx.count(anchor) == 1, 'anchor count=%d'%idx.count(anchor)
idx = idx.replace(anchor, cards + anchor, 1)
io.open(ROOT+'/index.html','w',encoding='utf-8',newline='\n').write(idx)

# --- вставка в sitemap.xml ---
sx = io.open(ROOT+'/sitemap.xml', encoding='utf-8').read()
assert sx.count('</urlset>') == 1
sx = sx.replace('</urlset>', sm + '</urlset>', 1)
io.open(ROOT+'/sitemap.xml','w',encoding='utf-8',newline='\n').write(sx)

print('cards inserted: %d'%len(ITEMS))
print('sitemap urls added: %d'%(len(ITEMS)*2))
