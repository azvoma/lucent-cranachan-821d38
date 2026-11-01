#!/usr/bin/env python3
"""
Apply the long-form guide content in tools/content/main_pages.py to the home page,
clubs.html, rugby-union.html and rugby-league.html. Idempotent.

- Updates <title>, meta description (and og/twitter copies) and the H1
- Replaces the old "SEO Content Block" above each listing with a short intro
- Removes the old microdata FAQ section (its questions move into the guide)
- Inserts the guide (takeaways, direct-answer sections, tables, FAQs) before </main>
- Adds FAQPage JSON-LD (id="guide-ld")
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from guide_render import render_block, render_ld, set_head, SITE  # noqa: E402
from content.main_pages import PAGES  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INTRO_P = '<p class="listing-intro" style="max-width:860px;margin:0 auto 1.5rem;font-size:1rem;line-height:1.7;color:var(--text-secondary)">{}</p>'


def apply(g):
    path = os.path.join(ROOT, g['file'])
    s = open(path, encoding='utf-8').read()
    s = set_head(s, g['title'], g['meta'])
    # H1
    if g['file'] == 'index.html':
        s = re.sub(r'(<h1 class="hero-split-title"[^>]*>).*?(</h1>)', lambda m: m.group(1) + g['h1_html'] + m.group(2), s, count=1, flags=re.S)
    else:
        s = re.sub(r'(<h1[^>]*>).*?(</h1>)', lambda m: m.group(1) + g['h1'] + m.group(2), s, count=1, flags=re.S)
    # old SEO block -> short intro (listing pages) or nothing (home)
    intro = INTRO_P.format(g['intro']) if g.get('intro') else ''
    s = re.sub(r'<!-- SEO Content Block.*?<!-- END SEO Content Block -->\s*', lambda m: intro + '\n', s, count=1, flags=re.S)
    # old microdata FAQ section
    s = re.sub(r'<section class="faq-reference-section".*?</section>\s*', '', s, count=1, flags=re.S)
    url = SITE + '/' + ('' if g['file'] == 'index.html' else g['file'])
    block = render_block(g)
    wrapped = f'<section class="sec sec-off guide-wrap" id="guide"><div class="con">\n{block}\n</div></section>'
    if '<!--guide:start-->' in s:
        s = re.sub(r'<section class="sec sec-off guide-wrap" id="guide"><div class="con">\s*<!--guide:start-->.*?<!--guide:end-->\s*</div></section>',
                   lambda m: wrapped, s, count=1, flags=re.S)
    else:
        i = s.rfind('</main>')
        s = s[:i] + wrapped + '\n' + s[i:]
    ld = render_ld(g, url, kind=None)
    if 'id="guide-ld"' in s:
        s = re.sub(r'<script type="application/ld\+json" id="guide-ld">.*?</script>', lambda m: ld, s, count=1, flags=re.S)
    else:
        s = s.replace('</head>', ld + '\n</head>', 1)
    open(path, 'w', encoding='utf-8').write(s)


if __name__ == '__main__':
    for g in PAGES:
        apply(g)
        print('updated', g['file'])
