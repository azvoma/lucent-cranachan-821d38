#!/usr/bin/env python3
"""
Merge a duplicate club page into the one we keep:
    python3 tools/merge_duplicate.py <drop-slug> <keep-slug>
Adds a 301 in _redirects, removes the dropped club's cards, list items, inline links and
ItemList entries from every page, fixes "<County> has N ... clubs" counts on pages that
listed it, and removes it from the sitemap, search index and tools/clubs.json.
"""
import glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main(drop, keep):
    href = rf'(?:\.\./|/)?club/{re.escape(drop)}\.html'
    files = glob.glob(os.path.join(ROOT, '*.html')) + glob.glob(os.path.join(ROOT, 'club', '*.html'))
    changed = 0
    for p in files:
        if os.path.basename(p) == f'{drop}.html' and '/club/' in p:
            continue
        s = open(p, encoding='utf-8', errors='surrogateescape').read()
        o = s
        # cards
        while True:
            m = re.search(rf'<div><article class="club-card card"><a href="{href}" class="card-link">', s)
            if not m: break
            j = s.find('</article></div>', m.end())
            s = s[:m.start()] + s[j + len('</article></div>'):]
        while True:
            m = re.search(rf'<div class="club-card-wrap"[^>]*><article class="club-card card">\s*<a href="{href}"', s)
            if not m: break
            j = s.find('</article></div>', m.end())
            s = s[:m.start()] + s[j + len('</article></div>'):].lstrip('\n')
        # list items and inline links
        s = re.sub(rf'<li><a href="{href}">[^<]*</a>(?: <span[^>]*>[^<]*</span>)?</li>', '', s)
        s = re.sub(rf',\s*<a href="{href}">[^<]*</a>', '', s)
        s = re.sub(rf'<a href="{href}">[^<]*</a>,\s*', '', s)
        # ItemList entries (renumber)
        def ld(m):
            try: j = json.loads(m.group(1))
            except Exception: return m.group(0)
            hit = False
            for n in (j.get('@graph', [j]) if isinstance(j, dict) else j):
                if isinstance(n, dict) and n.get('@type') == 'ItemList':
                    items = [i for i in n.get('itemListElement', []) if f'/club/{drop}.html' not in json.dumps(i)]
                    if len(items) != len(n.get('itemListElement', [])):
                        for k, i in enumerate(items, 1): i['position'] = k
                        n['itemListElement'] = items
                        if 'numberOfItems' in n: n['numberOfItems'] = len(items)
                        hit = True
            return '<script type="application/ld+json">' + json.dumps(j, ensure_ascii=False) + '</script>' if hit else m.group(0)
        s = re.sub(r'<script type="application/ld\+json">(.*?)</script>', ld, s, flags=re.S)
        if s != o:
            # this page listed the club: its "has N clubs" counts drop by one
            s = re.sub(r'(has |In total, [A-Za-z ]+ has |all )(\d+)( rugby union clubs)',
                       lambda m: m.group(1) + str(int(m.group(2)) - 1) + m.group(3), s)
            open(p, 'w', encoding='utf-8', errors='surrogateescape').write(s); changed += 1
    # redirect
    red = os.path.join(ROOT, '_redirects')
    r = open(red, encoding='utf-8').read()
    line = f'/club/{drop}.html  /club/{keep}.html  301!'
    if line not in r:
        r = r.replace('/club/:slug  /club/:slug.html  301', line + '\n/club/:slug  /club/:slug.html  301', 1)
        open(red, 'w', encoding='utf-8').write(r)
    # sitemap, search index, clubs.json
    sm = os.path.join(ROOT, 'sitemap.xml')
    x = open(sm, encoding='utf-8').read()
    x = re.sub(rf'\s*<url>\s*<loc>[^<]*/club/{re.escape(drop)}\.html</loc>.*?</url>', '', x, flags=re.S)
    open(sm, 'w', encoding='utf-8').write(x)
    for path, key in ((os.path.join(ROOT, 'js', 'clubs-index.json'), 's'), (os.path.join(ROOT, 'tools', 'clubs.json'), 'slug')):
        d = json.load(open(path, encoding='utf-8'))
        d = [e for e in d if e.get(key) != drop]
        json.dump(d, open(path, 'w', encoding='utf-8'), separators=(',', ':') if key == 's' else None,
                  ensure_ascii=False, indent=None if key == 's' else 1)
    f = os.path.join(ROOT, 'club', f'{drop}.html')
    if os.path.exists(f): os.remove(f)
    print(f'{changed} pages updated; {drop} -> {keep}')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
