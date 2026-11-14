#!/usr/bin/env python3
"""
Apply tools/content/club_guides.py to the 14 club pages (idempotent). Run from the repo root.

Order:  update_club_pages.py  ->  apply_club_guides.py  ->  club_content.py
(update_club_pages applies founding-year corrections from club-contacts.csv; club_content rebuilds the
FAQPage JSON-LD from the visible #faq items, which include the extra FAQs added here.)

Per page this script
  * sets <title>, meta description, og/twitter copies (set_head)
  * replaces the "About the Club" paragraphs and the History paragraph (stat boxes untouched)
  * inserts a guide block (answer, sections, "How we checked this page") before the FAQ section
  * adds extra FAQ items to the visible #faq section (data-faq="guide-N")
Nothing else in the page (layout, hero, sidebar, nearby clubs, contact) is changed.
"""
import html as H
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
sys.path.insert(0, os.path.join(ROOT, 'tools', 'content'))
from guide_render import render_block, set_head, plain, _human  # noqa: E402
from club_guides import CLUBS, UPDATED  # noqa: E402

CLUB_INFO = {c['slug']: c for c in json.load(open(os.path.join(ROOT, 'tools', 'clubs.json'))) if c.get('type') == 'SportsTeam'}


def esc(t):
    return H.escape(t, quote=False)


def paras(items):
    return '\n'.join(f'            <p>{p}</p>' for p in items)


def sources_md(g):
    lines = [f'- [{l}]({u})' for l, u in g['sources']]
    return ('This page was reviewed on ' + _human(UPDATED) + ' by the UK Rugby Club Directory team. Facts come from the '
            'club\'s own site, its governing body or a public register where one exists, and Wikipedia for background. '
            'We write the copy ourselves and do not copy source text. League names come from England Rugby (31 October 2026).\n\n'
            + '\n'.join(lines) + '\n\nSpotted something out of date? Use the [contact page](contact-us.html) and we will check it '
            'and correct the listing.')


def build(slug, g):
    sections = list(g['sections'])
    sections.append(dict(id='how-we-checked', h2='How we checked this page', md=sources_md(g)))
    sec0 = dict(id=sections[0]['id'])
    guide = dict(updated=UPDATED, sections=sections)
    inner = render_block(guide, prefix='../', heading_level=2)
    inner = inner.replace('<!--guide:start-->\n', '').replace('\n<!--guide:end-->', '')
    # direct-answer paragraph first, then the sections
    answer = f'<p class="guide-answer"><strong>{esc(g["answer"])}</strong></p>'
    info = CLUB_INFO.get(slug, {})
    related = [('rugby-league.html', 'UK rugby league clubs')] if 'League' in info.get('sport', '') else \
              [('rugby-union.html', 'UK rugby union clubs')]
    rel = '<p class="guide-related"><strong>Related:</strong> ' + ' · '.join(
        f'<a href="../{h}">{H.escape(l)}</a>' for h, l in related + [('clubs.html', 'All UK rugby clubs')]) + '</p>'
    inner = inner.replace('<div class="guide">', '<div class="guide">\n' + answer, 1)
    inner = inner[:inner.rfind('</div>')] + rel + '\n</div>'
    return ('<!--guide:start-->\n<section class="sec" id="club-guide"><div class="con"><div style="max-width:860px;margin:0 auto">\n'
            + inner + '\n</div></div></section>\n<!--guide:end-->')


def faq_items(g, s):
    items = []
    have_league = 'data-faq="league"' in s
    n = 0
    for q, a in g['faqs']:
        if have_league and re.match(r'What league does', q):
            continue
        n += 1
        items.append(f'<div class="faq-item" data-faq="guide-{n}" style="margin-bottom:1.25rem"><h3 style="font-size:1.05rem;margin-bottom:.35rem">{esc(q)}</h3><p>{esc(a)}</p></div>')
    return ''.join(items)


def apply(slug, g):
    path = os.path.join(ROOT, 'club', slug + '.html')
    s = open(path, encoding='utf-8', errors='surrogateescape').read()
    assert 50 <= len(g["title"]) <= 60 and 140 <= len(g['meta']) <= 155, slug
    s = set_head(s, g['title'], g['meta'])
    # About
    s, n1 = re.subn(r'(<h2>About [^<]*</h2>\s*<div class="rich-text">).*?(</div>)',
                    lambda m: m.group(1) + '\n' + paras(g['about']) + '\n          ' + m.group(2), s, count=1, flags=re.S)
    # History (keep the stat boxes that follow the rich-text div)
    s, n2 = re.subn(r'(<div class="about-block" id="history">.*?<div class="rich-text">).*?(</div>)',
                    lambda m: m.group(1) + '\n' + paras(g['history']) + '\n          ' + m.group(2), s, count=1, flags=re.S)
    assert n1 == 1, (slug, n1)
    if n2 == 0:  # business-style listing with no History block (IRFU): fold the history into About
        s = re.sub(r'(<h2>About [^<]*</h2>\s*<div class="rich-text">).*?(</div>)',
                   lambda m: m.group(1) + '\n' + paras(g['about'] + g['history']) + '\n          ' + m.group(2), s, count=1, flags=re.S)
    # guide block before FAQ section
    block = build(slug, g)
    if '<!--guide:start-->' in s:
        s = re.sub(r'<!--guide:start-->.*?<!--guide:end-->', lambda m: block, s, count=1, flags=re.S)
    else:
        i = s.find('<!-- ══ FAQ')
        if i < 0:
            i = s.find('<section class="sec" id="faq">')
        assert i >= 0, slug
        s = s[:i] + block + '\n' + s[i:]
    # extra FAQ items (replace any earlier guide-N items)
    s = re.sub(r'<div class="faq-item" data-faq="guide-\d+"[^>]*>.*?</div>', '', s, flags=re.S)
    m = re.search(r'(<section class="sec" id="faq">.*?<div style="max-width:860px;margin:0 auto">)', s, re.S)
    assert m, slug
    s = s[:m.end()] + faq_items(g, s) + s[m.end():]
    sec = re.search(r'<section class="sec" id="faq">(.*?)</section>', s, re.S)
    qa = re.findall(r'<h3[^>]*>(.*?)</h3>\s*<p[^>]*>(.*?)</p>', sec.group(1), re.S)
    cl = lambda t: H.unescape(re.sub(r'<[^>]+>', '', t)).strip()
    ld = ('<script type="application/ld+json" id="guide-ld">' + json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage", "@id": f'https://ukrugbyclubdirectory.co.uk/club/{slug}.html#faq',
        "mainEntity": [{"@type": "Question", "name": cl(q), "acceptedAnswer": {"@type": "Answer", "text": cl(a)}} for q, a in qa]},
        ensure_ascii=False) + '</script>')
    if 'id="guide-ld"' in s:
        s = re.sub(r'<script type="application/ld\+json" id="guide-ld">.*?</script>', lambda m: ld, s, count=1, flags=re.S)
    else:
        s = s.replace('</head>', ld + '\n</head>', 1)
    open(path, 'w', encoding='utf-8', errors='surrogateescape').write(s)


def main():
    for slug, g in CLUBS.items():
        apply(slug, g)
    print('club guides applied:', len(CLUBS))


if __name__ == '__main__':
    main()
