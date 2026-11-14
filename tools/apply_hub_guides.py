#!/usr/bin/env python3
"""
Add the long-form guide sections in tools/content/hubs.py to city/county hub pages.
Run AFTER build_hubs.py / region_logo_panel.py (it edits their output). Idempotent.

- Optional title / meta / H1 overrides (used for the hand-built hubs)
- Removes the generic site-wide FAQ block (duplicate content across pages)
- Inserts the guide before the hub's own FAQ section
- Hand-built hubs get FAQPage JSON-LD built from their visible FAQ questions
"""
import html as H
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from guide_render import render_block, set_head  # noqa: E402
from content.hubs import HUB_GUIDES, U  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://ukrugbyclubdirectory.co.uk'


def faq_ld(s, url):
    sec = re.search(r'<section class="sec sec-off" id="faq">(.*?)</section>', s, re.S)
    if not sec:
        return None
    qa = re.findall(r'<h3[^>]*>(.*?)</h3>\s*<p[^>]*>(.*?)</p>', sec.group(1), re.S)
    if not qa:
        return None
    clean = lambda t: H.unescape(re.sub(r'<[^>]+>', '', t)).strip()
    return ('<script type="application/ld+json" id="guide-ld">' + json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage", "@id": url + '#faq',
        "mainEntity": [{"@type": "Question", "name": clean(q), "acceptedAnswer": {"@type": "Answer", "text": clean(a)}} for q, a in qa]},
        ensure_ascii=False) + '</script>')


def apply(slug, g):
    path = os.path.join(ROOT, slug + '.html')
    s = open(path, encoding='utf-8').read()
    if g.get('title') or g.get('meta'):
        s = set_head(s, g.get('title'), g.get('meta'))
    if g.get('h1'):
        s = re.sub(r'(<h1[^>]*>).*?(</h1>)', lambda m: m.group(1) + g['h1'] + m.group(2), s, count=1, flags=re.S)
    s = re.sub(r'<section class="faq-reference-section".*?</section>\s*', '', s, count=1, flags=re.S)
    g = dict(g, updated=g.get('updated', U), byline=True, toc=False)
    block = f'<section class="sec guide-wrap" id="guide"><div class="con">\n{render_block(g)}\n</div></section>'
    if '<!--guide:start-->' in s:
        s = re.sub(r'<section class="sec guide-wrap" id="guide"><div class="con">\s*<!--guide:start-->.*?<!--guide:end-->\s*</div></section>',
                   lambda m: block, s, count=1, flags=re.S)
    else:
        anchor = '<section class="sec sec-off" id="faq">'
        i = s.find(anchor)
        if i < 0:
            i = s.rfind('</main>')
        s = s[:i] + block + '\n' + s[i:]
    if '"FAQPage"' not in re.sub(r'<script type="application/ld\+json" id="guide-ld">.*?</script>', '', s, flags=re.S):
        ld = faq_ld(s, f'{SITE}/{slug}.html')
        if ld:
            if 'id="guide-ld"' in s:
                s = re.sub(r'<script type="application/ld\+json" id="guide-ld">.*?</script>', lambda m: ld, s, count=1, flags=re.S)
            else:
                s = s.replace('</head>', ld + '\n</head>', 1)
    open(path, 'w', encoding='utf-8').write(s)


if __name__ == '__main__':
    for slug, g in HUB_GUIDES.items():
        apply(slug, g)
        print('guide added:', slug)
