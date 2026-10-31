#!/usr/bin/env python3
"""
Hero logo panel for club and business pages.  Safe to re-run.

1. Logos that were stretched across the hero's right panel (root-level files such as
   "bath rugby copy.png") are copied into /badges/{slug}.png - trimmed, squared, max 600px -
   so tools/apply_badges.py also puts them on cards and in search.
2. Every club/business page gets the same right panel: the navy pattern with the official
   logo centred on a white card.  No logo -> plain pattern (stock photos removed).
Run tools/apply_badges.py afterwards (main() does it) so the small badge beside the name,
cards and the search index use the same file.
"""
import glob, html, json, os, re, subprocess, sys
from PIL import Image, ImageChops, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from update_club_pages import find_div_block  # noqa: E402

PATTERN = '<div class="lh-right lh-pattern" aria-hidden="true" style="position:absolute;right:0;top:0;bottom:0;width:42%"></div>'


def badge_for(slug):
    for f in glob.glob(os.path.join(ROOT, 'badges', slug + '.*')):
        if re.search(r'\.(png|jpe?g|webp|svg)$', f, re.I):
            return os.path.basename(f)
    return None


def import_logo(src, slug):
    """Trim borders, pad to a square, cap at 600px, save as badges/{slug}.png."""
    im = Image.open(src).convert('RGBA')
    alpha_bbox = im.getchannel('A').point(lambda a: 255 if a > 8 else 0).getbbox()
    if alpha_bbox and alpha_bbox != (0, 0) + im.size:
        im = im.crop(alpha_bbox)
    elif im.getchannel('A').getextrema()[0] == 255:  # fully opaque: trim a near-uniform border
        bg = Image.new('RGB', im.size, im.convert('RGB').getpixel((0, 0)))
        diff = ImageChops.difference(im.convert('RGB'), bg).convert('L').point(lambda v: 255 if v > 24 else 0)
        bb = diff.getbbox()
        if bb and (bb[2] - bb[0]) * (bb[3] - bb[1]) > 0.25 * im.size[0] * im.size[1]:
            im = im.crop(bb)
    for _pass in range(2):
        # light, flat background (e.g. a grey square saved behind the logo) -> transparent, flood-filled from the corners
        rgb = im.convert('RGB'); w, h = im.size
        if _pass and im.getchannel('A').getextrema()[0] != 255: break
        corners = [rgb.getpixel(c) for c in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1))]
        if im.getchannel('A').getextrema()[0] == 255 and all(sum(c) / 3 > 170 for c in corners) \
                and max(max(c) - min(c) for c in zip(*corners)) < 30:
            from PIL import ImageDraw
            mask = rgb.copy()
            for c in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)):
                ImageDraw.floodfill(mask, c, (255, 0, 255), thresh=40)
            px, mp = im.load(), mask.load()
            for y in range(h):
                for x in range(w):
                    if mp[x, y] == (255, 0, 255): px[x, y] = (0, 0, 0, 0)
            bb = im.getchannel('A').getbbox()
            if bb: im = im.crop(bb)
    side = max(im.size)
    sq = Image.new('RGBA', (side, side), (0, 0, 0, 0))
    sq.paste(im, ((side - im.width) // 2, (side - im.height) // 2))
    if side > 600:
        sq = sq.resize((600, 600), Image.LANCZOS)
    sq.save(os.path.join(ROOT, 'badges', slug + '.png'), optimize=True)
    return slug + '.png'


def main():
    recs = {r['slug']: r for r in json.load(open(os.path.join(ROOT, 'tools', 'clubs.json')))}
    imported = changed = with_logo = 0
    for p in sorted(glob.glob(os.path.join(ROOT, 'club', '*.html'))):
        slug = os.path.basename(p)[:-5]
        rec = recs.get(slug)
        if not rec or rec['type'] not in ('SportsTeam', 'LocalBusiness'):
            continue
        s = open(p, encoding='utf-8', errors='surrogateescape').read()
        i = s.find('<div class="lh-right')
        if i < 0:
            continue
        j = find_div_block(s, i)
        block = s[i:j]
        logo = badge_for(slug)
        if not logo and 'lh-logo-card' not in block:
            m = re.search(r'<img[^>]*src="([^"]+)"', block)
            if m and 'imgs/' not in m.group(1):
                src = os.path.normpath(os.path.join(ROOT, 'club', html.unescape(m.group(1)).replace('%20', ' ')))
                if os.path.exists(src):
                    logo = import_logo(src, slug); imported += 1
        if logo:
            name = html.escape(rec['name'])
            new = (f'<div class="lh-right lh-pattern lh-logo-panel" style="position:absolute;right:0;top:0;bottom:0;width:42%">'
                   f'<div class="lh-logo-card"><img src="../badges/{logo}" alt="{name} logo" width="180" height="180" '
                   f'fetchpriority="high"></div></div>')
            with_logo += 1
        else:
            new = PATTERN
        if new != block:
            s = s[:i] + new + s[j:]
            open(p, 'w', encoding='utf-8', errors='surrogateescape').write(s); changed += 1
    print(f'{imported} logos imported to /badges; {with_logo} pages with a logo panel; {changed} pages changed')
    subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'apply_badges.py')], check=True)


if __name__ == '__main__':
    main()
