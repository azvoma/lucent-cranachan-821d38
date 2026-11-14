#!/usr/bin/env python3
"""
Insert the keyword-gap sections from tools/content/extras.py into the existing guide blocks of
index.html, clubs.html, rugby-union.html, rugby-league.html and south-west-rugby-clubs.html (idempotent).

This is deliberately surgical: it does NOT regenerate the guide, because those pages have been edited
since tools/content/main_pages.py and hubs.py were written. It
  * removes any earlier copy of each new section (by id) and inserts the new one before the FAQ block
  * adds the section to the table of contents when the page has one
  * refreshes the "Last reviewed" date
  * corrects the Est. chip on club cards for the five founding-year corrections (club-contacts.csv)
Run from the repo root after the other apply_* scripts.
"""
import html as H
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from guide_render import render_block, plain, _human  # noqa: E402
from content import extras as X  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = {'index.html': X.HOME_EXTRA, 'clubs.html': X.CLUBS_EXTRA, 'rugby-union.html': X.UNION_EXTRA,
         'rugby-league.html': X.LEAGUE_EXTRA, 'south-west-rugby-clubs.html': X.SW_EXTRA}
YEARS = {'leeds-rhinos': ('1890', '1870'), 'warrington-wolves': ('1879', '1876'), 'folkestone-rfc': ('1929', '1973'),
         'solihull-rfc': ('1924', '1933'), 'eccles-salford-arlfc': ('1921', '1977')}


def section_html(sec):
    out = render_block(dict(updated=X.UPDATED, sections=[sec], byline=False, toc=False))
    m = re.search(r'(<section class="guide-sec".*?</section>)\s*</div>\s*<!--guide:end-->', out, re.S)
    return m.group(1)


def apply(fn, secs):
    path = os.path.join(ROOT, fn)
    s = open(path, encoding='utf-8').read()
    for sec in secs:
        s = re.sub(r'<section class="guide-sec" id="%s".*?</section>\s*' % re.escape(sec['id']), '', s, count=1, flags=re.S)
        s = re.sub(r'<li><a href="#%s">.*?</a></li>' % re.escape(sec['id']), '', s, count=1)
    html = '\n'.join(section_html(x) for x in secs) + '\n'
    i = s.find('<section class="guide-sec guide-faq"')
    if i < 0:
        i = s.find('<p class="guide-related">')
    if i < 0:
        i = s.find('</div>\n<!--guide:end-->')
    assert i >= 0, fn
    s = s[:i] + html + s[i:]
    if '<nav class="guide-toc"' in s:
        toc = ''.join(f'<li><a href="#{x["id"]}">{H.escape(plain(x["h2"]))}</a></li>' for x in secs)
        j = s.find('<li><a href="#guide-faq">')
        j = j if j >= 0 else s.find('</ol></nav>')
        s = s[:j] + toc + s[j:]
    s = re.sub(r'(<p class="guide-meta">.*?<time datetime=")[^"]*(">)[^<]*(</time>)',
               lambda m: m.group(1) + X.UPDATED + m.group(2) + _human(X.UPDATED) + m.group(3), s, count=1)
    s = fix_cards(s)
    open(path, 'w', encoding='utf-8').write(s)


def fix_cards(s):
    for slug, (old, new) in YEARS.items():
        s = re.sub(r'(<a href="club/%s\.html" class="card-link">(?:(?!</article>).)*?<span class="est-chip">Est\. )%s(</span>)' % (re.escape(slug), old),
                   lambda m: m.group(1) + new + m.group(2), s, flags=re.S)
    return s


def main():
    for fn, secs in PAGES.items():
        apply(fn, secs)
        print('extras applied:', fn, [x['id'] for x in secs])
    # hub pages carry club cards too
    for fn in sorted(f for f in os.listdir(ROOT) if f.endswith('.html') and f not in PAGES):
        p = os.path.join(ROOT, fn)
        t = open(p, encoding='utf-8', errors='surrogateescape').read()
        u = fix_cards(t)
        if u != t:
            open(p, 'w', encoding='utf-8', errors='surrogateescape').write(u)
            print('card years fixed:', fn)


if __name__ == '__main__':
    main()
