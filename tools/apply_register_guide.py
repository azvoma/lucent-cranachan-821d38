#!/usr/bin/env python3
"""Add the short "RFU find a club" guide block and FAQPage JSON-LD to register.html (idempotent). Run from repo root."""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from guide_render import render_block, render_ld, set_head, SITE  # noqa: E402
from content.extras import REGISTER  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TITLE = 'Register Your Rugby Club Free | UK Rugby Club Directory'
META = 'Register your rugby club free in the UK Rugby Club Directory. See how it fits with the RFU find a club tool, what a listing includes and how to fix it.'


def main():
    path = os.path.join(ROOT, 'register.html')
    s = open(path, encoding='utf-8').read()
    assert 50 <= len(TITLE) <= 60 and 140 <= len(META) <= 155, (len(TITLE), len(META))
    s = set_head(s, TITLE, META)
    g = dict(REGISTER, title=TITLE, meta=META, h1='Register Your Club')
    block = f'<section class="sec sec-off guide-wrap" id="guide"><div class="con">\n{render_block(g)}\n</div></section>'
    if '<!--guide:start-->' in s:
        s = re.sub(r'<section class="sec sec-off guide-wrap" id="guide"><div class="con">\s*<!--guide:start-->.*?<!--guide:end-->\s*</div></section>',
                   lambda m: block, s, count=1, flags=re.S)
    else:
        i = s.rfind('</main>')
        s = s[:i] + block + '\n' + s[i:]
    ld = render_ld(g, f'{SITE}/register.html', kind='FAQ')
    if 'id="guide-ld"' in s:
        s = re.sub(r'<script type="application/ld\+json" id="guide-ld">.*?</script>', lambda m: ld, s, count=1, flags=re.S)
    else:
        s = s.replace('</head>', ld + '\n</head>', 1)
    open(path, 'w', encoding='utf-8').write(s)
    print('register.html updated')


if __name__ == '__main__':
    main()
