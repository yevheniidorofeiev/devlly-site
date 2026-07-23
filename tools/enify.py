# -*- coding: utf-8 -*-
"""
Движок EN-версии.

to_en(html) повторяет РОВНО ту логику, что делал JS-переключатель:
  [data-en]     -> textContent = data-en   (для <meta> -> атрибут content)
  [data-en-ph]  -> placeholder = data-en-ph
затем служебные атрибуты вычищаются, т.к. на /en/ они уже не нужны.
"""
import io, re, html as H

VOID = {'meta', 'link', 'input', 'img', 'br', 'hr', 'source'}
OPEN_EN = re.compile(r'<(?P<tag>[a-zA-Z][\w-]*)(?P<attrs>[^>]*?\sdata-en="(?P<en>[^"]*)"[^>]*?)>')


def _esc_text(v):
    """data-en хранится HTML-экранированным; раскодируем и снова экранируем как текст."""
    v = H.unescape(v)
    return v.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def _close_of(s, tag, start):
    """Ищем закрывающий тег с учётом вложенности одноимённых."""
    depth = 1
    pat = re.compile(r'<(/?)%s\b' % re.escape(tag), re.I)
    pos = start
    while True:
        m = pat.search(s, pos)
        if not m:
            raise ValueError('no closing </%s>' % tag)
        if m.group(1):
            depth -= 1
            if depth == 0:
                return m.start(), s.index('>', m.end()) + 1
        else:
            depth += 1
        pos = m.end()


def to_en(s):
    # идём с конца, чтобы индексы не съезжали
    for m in reversed(list(OPEN_EN.finditer(s))):
        tag = m.group('tag').lower()
        en = m.group('en')
        if tag == 'meta':
            new_open = re.sub(r'\scontent="[^"]*"', ' content="%s"' % en, m.group(0), count=1)
            s = s[:m.start()] + new_open + s[m.end():]
        elif tag in VOID:
            continue
        else:
            c0, c1 = _close_of(s, tag, m.end())
            s = s[:m.end()] + _esc_text(en) + s[c0:]

    # placeholder'ы
    def ph(m):
        return re.sub(r'\splaceholder="[^"]*"', ' placeholder="%s"' % m.group(1), m.group(0), count=1)
    s = re.sub(r'<[a-zA-Z][^>]*?\sdata-en-ph="([^"]*)"[^>]*?>', ph, s)

    # aria-label (кнопки «Читати» ведут на разные статьи — скринридеру нужны разные имена)
    def aria(m):
        return re.sub(r'\saria-label="[^"]*"', ' aria-label="%s"' % m.group(1), m.group(0), count=1)
    s = re.sub(r'<[a-zA-Z][^>]*?\sdata-en-aria="([^"]*)"[^>]*?>', aria, s)

    # чистим служебные атрибуты
    s = re.sub(r'\sdata-en(?:-ph|-aria)?="[^"]*"', '', s)
    return s


def outside_scripts(s, fn):
    """Применяет fn только вне <script>…</script>.
    Критично: в инлайн-JS есть селектор a[href="/"] — слепая замена href его сломала бы."""
    parts = re.split(r'(<script\b[^>]*>.*?</script>)', s, flags=re.S)
    return ''.join(p if p.startswith('<script') else fn(p) for p in parts)


def rewrite_root(s):
    """Пути для /en/index.html — делаем корне-абсолютными.
    Относительные ломаются, т.к. trailingSlash:false и URL выглядит как /en (без слэша),
    поэтому базой стал бы корень сайта, а не /en/."""
    s = s.replace('<html lang="uk">', '<html lang="en">')
    # баннер «перейти на EN» на самой EN-странице бессмыслен — вырезаем разметку совсем
    s = re.sub(r'\n\s*<!-- Пропозиція англомовним.*?</div>\n', '\n', s, flags=re.S, count=1)
    # ловим и href/src, и КАЖДЫЙ url внутри srcset ("a.webp 480w, b.webp 800w")
    s = re.sub(r'(?<![./\w])assets/', '/assets/', s)

    def links(x):
        x = x.replace('href="blog/', 'href="/en/blog/')
        x = x.replace('href="/"', 'href="/en"')                       # логотип и «Головна»
        x = x.replace('data-lang="uk" href="/en"', 'data-lang="uk" href="/"')  # ...кроме UA в переключателе
        return x
    s = outside_scripts(s, links)
    s = s.replace('href="https://devlly.dev/"', 'href="https://devlly.dev/en"')   # canonical
    s = s.replace('content="https://devlly.dev/"', 'content="https://devlly.dev/en"')  # og:url
    # hreflang оставляем как есть: uk=/, en=/en, x-default=/ — они одинаковы для обеих версий,
    # но canonical выше уже заменён, поэтому чиним обратно те три строки:
    s = s.replace('<link rel="alternate" hreflang="uk" href="https://devlly.dev/en">',
                  '<link rel="alternate" hreflang="uk" href="https://devlly.dev/">')
    s = s.replace('<link rel="alternate" hreflang="x-default" href="https://devlly.dev/en">',
                  '<link rel="alternate" hreflang="x-default" href="https://devlly.dev/">')
    # JSON-LD
    s = s.replace('"description": "Студія розробки. Автоматизуємо бізнес: Telegram-боти, CRM/ERP, Mini Apps, AI-інтеграції, парсинг даних."',
                  '"description": "Software studio. We automate business: Telegram bots, CRM/ERP, Mini Apps, AI integrations, data parsing."')
    s = s.replace('"name": "Головна", "item": "https://devlly.dev/"',
                  '"name": "Home", "item": "https://devlly.dev/en"')
    s = s.replace('"@type": "WebSite",\n      "name": "Devlly",\n      "url": "https://devlly.dev/"',
                  '"@type": "WebSite",\n      "name": "Devlly",\n      "url": "https://devlly.dev/en",\n      "inLanguage": "en"')
    return s


if __name__ == '__main__':
    import os
    _HERE = os.path.dirname(os.path.abspath(__file__))
    ROOT = os.environ.get('DEVLLY_ROOT', os.path.dirname(_HERE))
    src = io.open(ROOT + '/index.html', encoding='utf-8').read()
    out = rewrite_root(to_en(src))
    if not os.path.isdir(ROOT + '/en'):
        os.makedirs(ROOT + '/en')
    io.open(ROOT + '/en/index.html', 'w', encoding='utf-8', newline='\n').write(out)

    print('en/index.html:')
    print('  lang=en           :', '<html lang="en">' in out)
    print('  остатки data-en   :', out.count('data-en'))
    print('  кириллица в тексте:', len(re.findall(r'>[^<>]*[а-яїієґА-ЯЇІЄҐ][^<>]*<', out)))
    print('  canonical /en     :', 'canonical" href="https://devlly.dev/en"' in out)
    print('  hreflang uk=/     :', 'hreflang="uk" href="https://devlly.dev/">' in out)
    print('  ссылок blog/      :', out.count('href="/en/blog/'))
    print('  относительных assets:', out.count('="assets/'))
    print('  баланс div        :', out.count('<div') - out.count('</div>'))
