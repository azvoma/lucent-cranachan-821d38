"""Extract a structured record for every club/business page in /club/ into tools/clubs.json."""
import re, json, glob, html, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = []
for f in sorted(glob.glob(os.path.join(ROOT, 'club', '*.html'))):
    s = open(f, encoding='utf-8', errors='ignore').read()
    slug = os.path.basename(f)[:-5]
    rec = {'slug': slug}
    m = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S)
    rec['name'] = html.unescape(re.sub('<[^>]+>', '', m.group(1)).strip()) if m else slug
    ld = {}
    for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            j = json.loads(blk)
        except Exception:
            continue
        for node in j.get('@graph', [j]):
            if node.get('@type') in ('SportsTeam', 'LocalBusiness', 'SportsOrganization', 'Organization'):
                ld = node; break
        if ld: break
    rec['type'] = ld.get('@type', '')
    rec['sport'] = ld.get('sport', '')
    addr = ((ld.get('location') or {}).get('address') or ld.get('address') or {})
    rec['town'] = addr.get('addressLocality', '')
    rec['county'] = addr.get('addressRegion', '')
    rec['founded'] = str(ld.get('foundingDate', '') or '')
    rec['ld_website'] = ld.get('sameAs') or ''
    rec['has_tel'] = 'href="tel:' in s
    rec['has_mail'] = 'mailto:' in s
    m = re.search(r'<meta name="description" content="([^"]*)"', s)
    rec['meta'] = html.unescape(m.group(1)) if m else ''
    m = re.search(r'<p class="club-desc">(.*?)</p>', s)
    rec['canonical'] = (re.search(r'<link rel="canonical" href="([^"]+)"', s) or [None, ''])[1]
    out.append(rec)
json.dump(out, open(os.path.join(ROOT, 'tools', 'clubs.json'), 'w'), indent=1)
print(len(out), 'records')
