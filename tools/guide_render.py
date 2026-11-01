#!/usr/bin/env python3
"""
Shared renderer for long-form guide content on ukrugbyclubdirectory.co.uk.

A guide is a dict:
  title, meta, h1, slug            page metadata (standalone pages only)
  takeaways   [str]                 Key takeaways box (markdown inline)
  sections    [dict(h2, id, answer, md, img=(src, alt, w, h))]
              answer = 40-50 word direct-answer block shown in bold under the H2
              md     = markdown body (tables, lists, ### subheadings allowed)
  faqs        [(question, markdown answer)]
  related     [(href, label)]
  updated     'YYYY-MM-DD'

render_block(guide, prefix='')   -> HTML for takeaways + sections + FAQs, wrapped in
                                    <!--guide:start--> ... <!--guide:end--> markers
render_ld(guide, url, kind)      -> JSON-LD (Article or none + FAQPage + Breadcrumb)
inject(path, html, ld)           -> idempotently replace or insert the block in a page
"""
import html as H
import json
import re

import markdown

SITE = 'https://ukrugbyclubdirectory.co.uk'
ORG = {"@type": "Organization", "name": "UK Rugby Club Directory", "url": SITE + '/',
       "logo": {"@type": "ImageObject", "url": SITE + '/apple-touch-icon.png'},
       "email": "hello@ukrugbyclubdirectory.co.uk"}

_md = markdown.Markdown(extensions=['tables', 'sane_lists'])


def md(text, prefix=''):
    _md.reset()
    out = _md.convert(text.strip())
    if prefix:  # make site-relative links work from /club/ pages
        out = re.sub(r'href="(?!https?:|#|/|mailto:|tel:|\.\./)', 'href="' + prefix, out)
    out = out.replace('<table>', '<div class="guide-table-wrap"><table class="guide-table">').replace('</table>', '</table></div>')
    return out


def inline(text, prefix=''):
    return re.sub(r'^<p>|</p>$', '', md(text, prefix))


def plain(text):
    t = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    t = re.sub(r'[*_`]', '', t)
    return H.unescape(re.sub(r'<[^>]+>', '', t)).strip()


def render_block(g, prefix='', heading_level=2):
    h2, h3 = f'h{heading_level}', f'h{heading_level + 1}'
    out = ['<!--guide:start-->', '<div class="guide">']
    if g.get('byline', True):
        out.append(f'<p class="guide-meta">By the UK Rugby Club Directory team · Last reviewed '
                   f'<time datetime="{g["updated"]}">{_human(g["updated"])}</time></p>')
    if g.get('takeaways'):
        out.append('<aside class="guide-takeaways" aria-label="Key takeaways"><p class="guide-takeaways-title">Key takeaways</p><ul>'
                   + ''.join(f'<li>{inline(t, prefix)}</li>' for t in g['takeaways']) + '</ul></aside>')
    secs = g.get('sections', [])
    if len(secs) >= 4 and g.get('toc', True):
        out.append('<nav class="guide-toc" aria-label="On this page"><p class="guide-toc-title">On this page</p><ol>'
                   + ''.join(f'<li><a href="#{s["id"]}">{H.escape(plain(s["h2"]))}</a></li>' for s in secs)
                   + (f'<li><a href="#{g.get("faq_id", "guide-faq")}">FAQs</a></li>' if g.get('faqs') else '') + '</ol></nav>')
    for s in secs:
        out.append(f'<section class="guide-sec" id="{s["id"]}" aria-labelledby="{s["id"]}-h">')
        out.append(f'<{h2} id="{s["id"]}-h">{inline(s["h2"], prefix)}</{h2}>')
        if s.get('answer'):
            out.append(f'<p class="guide-answer"><strong>{inline(s["answer"], prefix)}</strong></p>')
        if s.get('img'):
            src, alt, w, hh = s['img']
            out.append(f'<figure class="guide-fig"><img src="{prefix}{src}" alt="{H.escape(alt, quote=True)}" width="{w}" height="{hh}" loading="lazy" decoding="async"></figure>')
        body = md(s.get('md', ''), prefix)
        body = re.sub(r'<h3>', f'<{h3}>', body).replace('</h3>', f'</{h3}>')
        out.append(body)
        out.append('</section>')
    if g.get('faqs'):
        out.append(f'<section class="guide-sec guide-faq" id="{g.get("faq_id", "guide-faq")}"><{h2}>{H.escape(g.get("faq_title", "Frequently asked questions"))}</{h2}>')
        for q, a in g['faqs']:
            out.append(f'<details class="guide-q"><summary>{H.escape(q)}</summary><div>{md(a, prefix)}</div></details>')
        out.append('</section>')
    if g.get('related'):
        out.append('<p class="guide-related"><strong>Related:</strong> ' + ' · '.join(
            f'<a href="{prefix}{h}">{H.escape(l)}</a>' for h, l in g['related']) + '</p>')
    out.append('</div>')
    out.append('<!--guide:end-->')
    return '\n'.join(out)


def _human(d):
    y, m, dd = d.split('-')
    months = 'January February March April May June July August September October November December'.split()
    return f'{int(dd)} {months[int(m) - 1]} {y}'


def render_ld(g, url, kind='Article', crumbs=None, image=None):
    graph = []
    if kind == 'Article':
        graph.append({"@type": "Article", "@id": url + '#article', "headline": plain(g['h1'])[:110],
                      "description": g['meta'], "url": url, "mainEntityOfPage": url, "inLanguage": "en-GB",
                      "datePublished": g.get('published', g['updated']), "dateModified": g['updated'],
                      "author": ORG, "publisher": ORG,
                      "image": SITE + '/' + (image or 'imgs/rugby-union-hero.jpg'),
                      "about": [{"@type": "Thing", "name": a} for a in g.get('about', [])]})
    if g.get('faqs'):
        graph.append({"@type": "FAQPage", "@id": url + '#faq', "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": plain(a)}}
            for q, a in g['faqs']]})
    if crumbs:
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)]})
    return ('<script type="application/ld+json" id="guide-ld">'
            + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False) + '</script>')


def inject(s, block, ld=None, before=None, after=None):
    """Replace an existing guide block, or insert it before/after an anchor string."""
    s = re.sub(r'<!--guide:start-->.*?<!--guide:end-->', lambda m: block, s, count=1, flags=re.S) \
        if '<!--guide:start-->' in s else _insert(s, block, before, after)
    if ld:
        if 'id="guide-ld"' in s:
            s = re.sub(r'<script type="application/ld\+json" id="guide-ld">.*?</script>', lambda m: ld, s, count=1, flags=re.S)
        else:
            s = s.replace('</head>', ld + '\n</head>', 1)
    return s


def _insert(s, block, before, after):
    if before and before in s:
        i = s.find(before)
        return s[:i] + block + '\n' + s[i:]
    if after and after in s:
        i = s.find(after) + len(after)
        return s[:i] + '\n' + block + s[i:]
    raise ValueError('anchor not found')


def set_head(s, title=None, meta=None):
    if title:
        t = H.escape(H.unescape(title), quote=False)
        s = re.sub(r'<title>.*?</title>', lambda m: f'<title>{t}</title>', s, count=1, flags=re.S)
        s = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + H.escape(H.unescape(title), quote=True), s)
        s = re.sub(r'(<meta name="twitter:title" content=")[^"]*', lambda m: m.group(1) + H.escape(H.unescape(title), quote=True), s)
    if meta:
        m_ = H.escape(meta, quote=True)
        s = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + m_, s, count=1)
        s = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + m_, s)
        s = re.sub(r'(<meta name="twitter:description" content=")[^"]*', lambda m: m.group(1) + m_, s)
    return s
