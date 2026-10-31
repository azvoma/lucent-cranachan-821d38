#!/usr/bin/env python3
"""
Official regional rugby body logo on the right of each region page's hero.
Mapping: tools/region-badges.csv (page -> body).  Logo files: badges/regions/{body_slug}.png
(prepare a downloaded logo with:  python3 tools/region_logo_panel.py --import <file> <body_slug>).
Pages whose logo files aren't all present keep the plain pattern.  Safe to re-run; run it after
tools/build_hubs.py, which rebuilds ten of these pages.
"""
import csv, glob, html, os, re, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from update_club_pages import find_div_block   # noqa: E402
from hero_logo_panel import import_logo         # noqa: E402

PATTERN = '<div class="lh-right lh-pattern" aria-hidden="true" style="position:absolute;right:0;top:0;bottom:0;width:42%"></div>'


def is_light(path):
    """True when the logo is white/very light (needs the dark card to be seen)."""
    im = Image.open(path).convert('RGBA'); im.thumbnail((120, 120))
    px = [p for p in im.get_flattened_data() if p[3] > 128] if hasattr(im, 'get_flattened_data') else [p for p in im.getdata() if p[3] > 128]
    light = sum(1 for r, g, b, a in px if 0.299 * r + 0.587 * g + 0.114 * b > 200)
    return bool(px) and light / len(px) > 0.95


def main():
    if len(sys.argv) == 4 and sys.argv[1] == '--import':
        out = import_logo(sys.argv[2], sys.argv[3], square=False)               # writes badges/{slug}.png
        os.replace(os.path.join(ROOT, 'badges', out), os.path.join(ROOT, 'badges', 'regions', out))
        print('saved badges/regions/' + out); return
    pages = {}
    for r in csv.DictReader(open(os.path.join(ROOT, 'tools', 'region-badges.csv'), encoding='utf-8')):
        pages.setdefault(r['page'], []).append(r)
    done = 0
    for page, bodies in pages.items():
        p = os.path.join(ROOT, page + '.html')
        if not os.path.exists(p): continue
        files = [os.path.join(ROOT, 'badges', 'regions', b['body_slug'] + '.png') for b in bodies]
        s = open(p, encoding='utf-8', errors='surrogateescape').read()
        i = s.find('<div class="lh-right')
        if i < 0: continue
        j = find_div_block(s, i)
        if all(os.path.exists(f) for f in files):
            imgs = ''.join(f'<img src="badges/regions/{b["body_slug"]}.png" alt="{html.escape(b["body_name"])} logo" '
                           f'title="{html.escape(b["body_name"])}" width="180" height="180" fetchpriority="high">' for b in bodies)
            dark = ' dark' if all(is_light(f) for f in files) else ''
            duo = ' duo' if len(bodies) > 1 else ''
            if not duo:
                w, h = Image.open(files[0]).size
                duo = ' wide' if w / h > 1.6 else ''
            new = (f'<div class="lh-right lh-pattern lh-logo-panel" style="position:absolute;right:0;top:0;bottom:0;width:42%">'
                   f'<div class="lh-logo-card{duo}{dark}">{imgs}</div></div>')
        else:
            new = s[i:j] if 'lh-logo-panel' not in s[i:j] else PATTERN
        if new != s[i:j]:
            s = s[:i] + new + s[j:]
            open(p, 'w', encoding='utf-8', errors='surrogateescape').write(s); done += 1
    have = len(glob.glob(os.path.join(ROOT, 'badges', 'regions', '*.png')))
    print(f'{have} region logo file(s) present; {done} page(s) updated')


if __name__ == '__main__':
    main()
