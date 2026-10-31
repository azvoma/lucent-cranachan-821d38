#!/usr/bin/env python3
"""
Accessibility + speed fixes from the Lighthouse audit (31 Oct 2026).  Safe to re-run.
  - big JPG banners -> resized WebP (max 1600px) for on-page <img> and CSS backgrounds
    (og:image / JSON-LD keep the JPG, which social sites prefer)
  - LCP hero image on the homepage loads with high priority
  - skip link has a target: <main id="main">
  - hidden mobile menu is `inert` so keyboard users can't tab into it
  - links whose aria-label hid their visible text (cards, logo, search button) lose the
    aria-label, so screen readers read what sighted users see
"""
import glob, os, re
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIG = ['rugby-union-banner', 'rugby-joints-banner', 'rugby-union-hero', 'home-hero',
       'home-hero-2', 'contact-hero', 'rugby-league-hero', 'rugby-league-banner']


def make_webp():
    for b in BIG:
        src, dst = os.path.join(ROOT, 'imgs', b + '.jpg'), os.path.join(ROOT, 'imgs', b + '.webp')
        if os.path.exists(src) and not os.path.exists(dst):
            im = Image.open(src).convert('RGB')
            if im.width > 1600:
                im = im.resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS)
            im.save(dst, 'WEBP', quality=78, method=6)


def fix_html(s):
    names = '|'.join(BIG)
    # on-page images and inline CSS backgrounds only
    s = re.sub(rf'(<img\b[^>]*\bsrc="[^"]*imgs/)({names})\.jpg"', r'\1\2.webp"', s)
    s = re.sub(rf'(url\([\'"]?[^)\'"]*imgs/)({names})\.jpg', r'\1\2.webp', s)
    # homepage LCP image
    s = re.sub(r'(<div class="hero-split-image">\s*<img\b)(?![^>]*fetchpriority)', r'\1 fetchpriority="high"', s)
    s = re.sub(rf'(<link rel="preload" as="image" href="[^"]*imgs/)({names})\.jpg"', r'\1\2.webp" type="image/webp"', s)
    # fonts are already linked in every page head; the CSS @import loaded them a second time, render-blocking
    s = re.sub(r"@import url\('https://fonts\.googleapis\.com/css2[^']*'\);\n?", '', s)
    s = re.sub(r'<main>', '<main id="main">', s)
    s = s.replace('<nav id="mobile-nav" aria-hidden="true">', '<nav id="mobile-nav" aria-hidden="true" inert>')
    s = re.sub(r'(<a href="[^"]*" class="card-link") aria-label="View [^"]*"', r'\1', s)
    s = re.sub(r'(<a href="[^"]*" class="logo") aria-label="UK Rugby Club Directory"', r'\1', s)
    s = s.replace(' aria-label="Search for a rugby club">Find a Club<', '>Find a Club<')
    return s


def main():
    make_webp()
    n = 0
    files = glob.glob(os.path.join(ROOT, '*.html')) + glob.glob(os.path.join(ROOT, 'club', '*.html')) \
        + glob.glob(os.path.join(ROOT, 'css', '*.css'))
    for p in files:
        s = open(p, encoding='utf-8', errors='surrogateescape').read()
        t = fix_html(s)
        if t != s:
            open(p, 'w', encoding='utf-8', errors='surrogateescape').write(t); n += 1
    print(f'{n} files updated')


if __name__ == '__main__':
    main()
