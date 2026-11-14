#!/usr/bin/env python3
"""
Add a "UK rugby leagues" link to the header Discover dropdown next to "Union league structure"
(idempotent; run from the repo root). rugby-leagues-uk.html had 9 internal links against 683 for the
league-structure page, which is why Google ranks it 60-98 for "rugby leagues uk" while ranking the
club-list pages higher. The link text matches the page's target keyword.
"""
import glob
import re

OLD = re.compile(r'(<a href="((?:\.\./)?)rugby-union-league-structure\.html" class="dp-link dp-tag">Union league structure</a>)')
n = 0
for p in glob.glob('*.html') + glob.glob('club/*.html'):
    if p.endswith('rugby-leagues-uk.html'):
        continue
    s = open(p, encoding='utf-8', errors='surrogateescape').read()
    if 'class="dp-link dp-tag">UK rugby leagues</a>' in s:
        continue
    t = OLD.sub(lambda m: m.group(1) + f'\n        <a href="{m.group(2)}rugby-leagues-uk.html" class="dp-link dp-tag">UK rugby leagues</a>', s, count=1)
    if t != s:
        open(p, 'w', encoding='utf-8', errors='surrogateescape').write(t)
        n += 1
print('pages updated:', n)
