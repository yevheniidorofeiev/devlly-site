# tools/ - генератор блога Devlly

Скрипты сборки статичного блога devlly.dev. Раньше жили только во временной
папке сессии и рисковали потеряться - теперь в репозитории.

## Источник правды

- `../index.html` - источник правды для главной (UA). `en/index.html`,
  `blog/*.html`, `en/blog/*.html` - ГЕНЕРИРУЮТСЯ, руками не редактируются.
- `articles/art_<slug>.json` - источник правды для КАЖДОЙ статьи блога.
  Схема: `{title_uk, title_en, desc_uk, desc_en, cta_uk, cta_en,
  seo:{t, te, d, de, k}, blocks:[{t:'lead'|'h2'|'p', uk, en}, ...]}`.
  Первый блок всегда `lead`, обычно ровно 5 `h2`, у каждого блока есть и `uk`, и `en`.

## Пути

Скрипты сами вычисляют пути относительно `tools/`:
- `ROOT` = корень репо (на уровень выше `tools/`)
- `SCRATCH`/articles = `tools/articles/`

Переопределить можно переменными окружения `DEVLLY_ROOT` и `DEVLLY_ARTICLES`.

## Полный цикл сборки (из корня репо)

```
python tools/build_blog.py          # articles/*.json -> blog/ + en/blog/
python tools/add_cards.py           # карточки в index.html + URL в sitemap.xml
python tools/insert_search_example.py   # запись статей в поисковый INDEX index.html
python tools/enify.py               # index.html -> en/index.html
```

Порядок важен: `enify.py` запускается последним, т.к. переносит финальный
`index.html` (с карточками и поиском) в `en/index.html`.

## Как добавить статью

1. Написать `articles/art_<slug>.json` по схеме.
2. Провалидировать: `python tools/check_example.py` (адаптировать список слагов).
3. В `build_blog.py` дописать slug в `SLUGS`, дату в `ISODATE`, 2-3 связи в `RELATED`
   (каждый слаг из RELATED обязан быть в SLUGS, иначе KeyError).
4. Прогнать полный цикл сборки выше.
5. Проверить счётчики, `git add . && commit && push`. Push в `main` -> авто-деплой на Vercel.

## Ключевые детали генератора (`build_blog.py`)

- `SEO` (словарь) хранит meta ПЕРВЫХ 8 статей - для них meta берётся ОТСЮДА, а не
  из art json (словарь имеет приоритет). Для остальных - из `art_json["seo"]`.
- `ISODATE` - дата публикации (единый источник даты).
- `RELATED` - блок «Читайте також» (2-3 ссылки на статью).
- `cta()` сам подставляет email и Telegram-кнопки - в тексте блоков контактов быть НЕ должно.
- EN-страницы собираются через `from enify import to_en, outside_scripts`.

## Правила контента (строго, весь сайт)

- Только короткий дефис `-`, НИКОГДА `—`/`–` (в т.ч. в числовых диапазонах: `10-15`).
- Кавычки-гильеметы `« »`.
- Апостроф в укр. словах - символ U+02BC (`ʼ`), не прямой `'` и не кудрявый.
- Объём 800-1200 слов, один h1 с ключом, 4-5 h2 с ключами.
- Поле `seo.k` - трёхъязычные (uk/ru/en) ключевики: сайт поддерживает трёхъязычный поиск.

## Файлы

- `build_blog.py` - генератор статей (blog + en/blog).
- `enify.py` - генератор `en/index.html` из `index.html` (data-en, пути, canonical, hreflang, JSON-LD).
- `add_cards.py` - карточки статей в index.html + URL в sitemap.xml.
- `insert_search_example.py` - шаблон вставки статей в поисковый INDEX (правь `K`/`ORDER` под свою партию).
- `check_example.py` - шаблон валидатора (схема, объём, запрет тире, апострофы, uk+en).
- `articles/` - все `art_<slug>.json` (источники статей).
