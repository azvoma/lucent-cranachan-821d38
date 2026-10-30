#!/usr/bin/env python3
"""
Put real club badges on the site.

1. Save each badge into /badges/ named after the club's page slug,
   e.g. badges/wanstead-rfc.png  (png, jpg, webp or svg).
   The slug is the club page's file name: club/wanstead-rfc.html -> wanstead-rfc
2. Run from the repo root:   python3 tools/apply_badges.py

For every badge file this:
  - shows it in the club page header instead of the initial,
  - shows it on that club's cards on every listing, hub and club page,
  - adds it to the club's structured data (logo),
  - updates the search index (js/clubs-index.json).
Safe to re-run; replace a file and re-run to update it.
"""
import glob, html, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BADGES = os.path.join(ROOT, 'badges')
SITE = 'https://ukrugbyclubdirectory.co.uk'


def live_pages():
    redirected = set()
    for line in open(os.path.join(ROOT, '_redirects'), encoding='utf-8'):
        p = line.split()
        if len(p) >= 3 and p[0].startswith('/') and p[2].startswith('301'):
            redirected.add(p[0].lstrip('/'))
    pages = [os.path.relpath(f, ROOT) for f in glob.glob(os.path.join(ROOT, '*.html')) + glob.glob(os.path.join(ROOT, 'club', '*.html'))]
    return [p for p in pages if p not in redirected]


def main():
    if not os.path.isdir(BADGES):
        print('No /badges folder yet.'); return
    badges = {}
    for f in sorted(os.listdir(BADGES)):
        m = re.match(r'([a-z0-9-]+)\.(png|jpe?g|webp|svg)$', f, re.I)
        if m and os.path.exists(os.path.join(ROOT, 'club', m.group(1) + '.html')):
            badges[m.group(1)] = f
        elif m:
            print(f'  ! {f}: no page club/{m.group(1)}.html — check the file name')
    recs = {r['slug']: r for r in json.load(open(os.path.join(ROOT, 'tools', 'clubs.json')))}
    changed = 0
    for page in live_pages():
        path = os.path.join(ROOT, page)
        s = open(path, encoding='utf-8', errors='surrogateescape').read()
        o = s
        prefix = '../' if page.startswith('club/') else ''
        for slug, fname in badges.items():
            name = html.escape(recs.get(slug, {}).get('name', slug))
            src = f'{prefix}badges/{fname}'
            # cards linking to this club
            def card(m):
                return re.sub(r"<div class=['\"]badge-fallback['\"](?: style=['\"][^'\"]*['\"])?>[^<]*</div>",
                              f'<img src="{src}" alt="{name} club badge" class="club-badge" loading="lazy" width="100" height="100">',
                              m.group(0), count=1)
            s = re.sub(rf'href="(?:\.\./)?club/{re.escape(slug)}\.html" class="card-link".{{0,600}}?<div class=[\'"]badge-fallback[\'"][^>]*>[^<]*</div>', card, s, flags=re.S)
            # the club's own page header
            if page == f'club/{slug}.html':
                s = re.sub(r'<div class="hero-badge-fallback"[^>]*>[^<]*</div>',
                           f'<img src="{src}" alt="{name} club badge" class="hero-badge-img" width="56" height="56" '
                           f'style="width:56px;height:56px;object-fit:contain;background:#fff;border-radius:50%;padding:5px;flex-shrink:0">',
                           s, count=1)
                def ld(m):
                    try:
                        j = json.loads(m.group(1))
                    except Exception:
                        return m.group(0)
                    hit = False
                    for n in j.get('@graph', [j]):
                        if n.get('@type') in ('SportsTeam', 'LocalBusiness'):
                            n['logo'] = f'{SITE}/badges/{fname}'; hit = True
                    return '<script type="application/ld+json">' + json.dumps(j, ensure_ascii=False) + '</script>' if hit else m.group(0)
                s = re.sub(r'<script type="application/ld\+json">(.*?)</script>', ld, s, flags=re.S)
        if s != o:
            open(path, 'w', encoding='utf-8', errors='surrogateescape').write(s); changed += 1
    idx = os.path.join(ROOT, 'js', 'clubs-index.json')
    d = json.load(open(idx, encoding='utf-8'))
    for r in d:
        if r.get('s') in badges:
            r['b'] = f'/badges/{badges[r["s"]]}'
    json.dump(d, open(idx, 'w', encoding='utf-8'), separators=(',', ':'), ensure_ascii=False)
    print(f'{len(badges)} badge(s) applied; {changed} page(s) updated')


if __name__ == '__main__':
    main()
