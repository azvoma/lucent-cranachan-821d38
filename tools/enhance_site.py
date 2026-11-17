#!/usr/bin/env python3
"""
Site enhancer for ukrugbyclubdirectory.co.uk  (UX + SEO pass, Nov 2026)
=======================================================================

Run from the repo root, AFTER update_club_pages.py / club_content.py / apply_*guides.py:

    python3 tools/update_club_pages.py
    python3 tools/enhance_site.py

Every step is idempotent (safe to re-run) and only rewrites markup.  It never
touches <title>, meta tags, canonical URLs, robots rules or the sitemap, and it
keeps every sentence and link that was visible on the page (text is moved or
folded into <details>, not deleted), so indexable content is preserved.

Club pages (/club/*.html, live ones only)
  1. Removes the empty "Photos coming soon" gallery (and the badge-only gallery,
     which repeats the hero logo).
  2. Removes the "1865 / 160+ years" stat tiles that repeat the key-facts strip.
  3. Merges the "Other clubs nearby" list and the "Clubs near X" cards into one
     section (the #county anchor is kept so existing links still work).
  4. Adds a static "Venue hire & events" section (weddings, parties, wakes,
     corporate days...) worded as "may be able to host" - clubs set their own terms.
  5. Converts the FAQ to an accordion (<details>), adds a venue-hire question,
     gives professional clubs a tickets / get-involved question instead of
     "how can I join", and rebuilds the FAQPage JSON-LD so it matches the page.
  6. Adds ground details (name, address, capacity, travel) for clubs listed in
     tools/club-grounds.csv + tools/club-contacts.csv: sidebar row, a "Matchday"
     block and a more useful "Where does X play?" answer.
  7. Stops the contact band leaving half its width empty.
Other pages
  8. FAQ items on hub / guide pages become the same accordion.
  9. Homepage: each long guide section keeps its heading and its one-paragraph
     answer visible and folds the rest under "Read more"; adds a "Follow the
     game" strip with official fixtures / table links; fixes the duplicate
     id="areas".
 10. Footer copyright year.
"""
import csv, glob, html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from update_club_pages import find_div_block, load_contacts, load_er  # noqa: E402

YEAR = '2026'
STATS = {}


def bump(k, n=1):
    STATS[k] = STATS.get(k, 0) + n


def read(p):
    return open(p, encoding='utf-8', errors='surrogateescape').read()


def write(p, s):
    open(p, 'w', encoding='utf-8', errors='surrogateescape').write(s)


def esc(t):
    return html.escape(t, quote=False)


def text_of(h):
    return html.unescape(re.sub(r'<[^>]+>', '', h)).strip()


# ───────────────────────────── FAQ accordion ─────────────────────────────

DIV_ITEM = re.compile(r'<div class="faq-item"([^>]*)>')
DET_ITEM = re.compile(r'<details class="faq-item"([^>]*)><summary><h3>(.*?)</h3></summary><div class="faq-a">(.*?)</div></details>', re.S)


def details_html(attrs, q, a, is_open=False):
    attrs = re.sub(r'\s*style="[^"]*"', '', attrs or '').strip()
    attrs = (' ' + attrs) if attrs else ''
    return (f'<details class="faq-item"{attrs}{" open" if is_open else ""}><summary><h3>{q}</h3></summary>'
            f'<div class="faq-a">{a}</div></details>')


def convert_faq_items(s):
    """<div class="faq-item"><h3>Q</h3><p>A</p></div>  ->  accordion <details>. Returns (s, n)."""
    out, pos, n = [], 0, 0
    for m in DIV_ITEM.finditer(s):
        if m.start() < pos:
            continue
        j = find_div_block(s, m.start())
        if j < 0:
            continue
        blk = s[m.start():j]
        mm = re.match(r'<div class="faq-item"([^>]*)>\s*<h3[^>]*>(.*?)</h3>\s*((?:<p[^>]*>.*?</p>\s*)+)</div>\s*$', blk, re.S)
        if not mm:                      # pricing.html etc. have their own accordion markup
            continue
        attrs, q, a = mm.groups()
        a = re.sub(r'<p [^>]*>', '<p>', a.strip())
        out.append(s[pos:m.start()])
        out.append(details_html(attrs, q.strip(), a))
        pos = j
        n += 1
    out.append(s[pos:])
    return ''.join(out), n


def close_faq(s):
    """Accordion answers start collapsed (the text stays in the DOM, so it is still indexable)."""
    return re.sub(r'(<details class="faq-item"[^>]*?) open>', r'\1>', s)


# ───────────────────────────── club-page pieces ─────────────────────────────

PIN = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>'
PEOPLE = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>'

PRO_LEAGUE = re.compile(r'PREM Rugby|Champ Rugby|Super League|Premiership', re.I)


def strip_gallery(s):
    i = s.find('<div class="gallery-inline"')
    if i < 0:
        return s
    j = find_div_block(s, i)
    blk = s[i:j]
    # drop every "coming soon" slot first
    while True:
        k = blk.find('<div class="gallery-coming-soon"')
        if k < 0:
            break
        slot = blk.rfind('<div class="gallery-slot"', 0, k)
        if slot < 0:
            break
        e = find_div_block(blk, slot)
        blk = blk[:slot] + blk[e:]
    imgs = re.findall(r'<img[^>]*>', blk)
    real = [t for t in imgs if not re.search(r'badge|logo', t, re.I)]
    k = s.rfind('<!-- ★ GALLERY', 0, i)
    start = k if 0 <= k and i - k < 120 else i
    if real:                              # keep genuine photos, just without the placeholders
        s = s[:i] + blk + s[j:]
    else:                                 # badge-only gallery repeats the hero logo
        s = s[:start].rstrip(' \t') + s[j:].lstrip('\n')
    bump('gallery')
    return s


def strip_history_tiles(s):
    h = s.find('id="history"')
    if h < 0:
        return s
    m = re.compile(r'<div style="display:flex;gap:1rem;flex-wrap:wrap;margin-top:1\.5rem">').search(s, h)
    if not m or 'Years of History' not in s[m.start():m.start() + 1600]:
        return s
    j = find_div_block(s, m.start())
    bump('history_tiles')
    return s[:m.start()].rstrip(' \t') + s[j:].lstrip('\n')


def merge_nearby(s, rec):
    if 'class="nearby-more"' in s:
        return s
    a = s.find('<section class="sec sec-off" id="county">')
    b = s.find('<section class="sec" id="nearby">')
    if a < 0 or b < 0:
        return s
    a_end = s.find('</section>', a) + len('</section>')
    b_end = s.find('</section>', b) + len('</section>')
    county, near = s[a:a_end], s[b:b_end]
    cards = set(re.findall(r'href="\.\./club/([^"]+)\.html" class="card-link"', near))
    inner = re.search(r'<div style="max-width:860px;margin:0 auto">(.*)</div>\s*</div>\s*</section>', county, re.S)
    if not inner or '<div class="nearby-cta">' not in near:
        return s
    body = inner.group(1)
    ul = re.search(r'<ul class="county-club-list"[^>]*>(.*?)</ul>', body, re.S)
    lis = re.findall(r'<li>.*?</li>', ul.group(1), re.S) if ul else []
    rest = [li for li in lis
            if (re.search(r'club/([^"]+)\.html', li) or [None, None])[1] not in cards | {rec['slug']}]
    paras = re.findall(r'<p[^>]*>.*?</p>', re.sub(r'<ul.*?</ul>', '', body, flags=re.S), re.S)
    county_name = rec.get('county') or 'the area'
    more = ''
    if rest:
        more = (f'<h3 style="font-size:1.05rem;margin:1.25rem 0 .25rem">More clubs in {esc(county_name)}</h3>'
                f'<ul class="county-club-list" style="columns:2;column-gap:2rem;list-style:none;padding:0;margin:.5rem 0 0;line-height:2">'
                + ''.join(rest) + '</ul>')
    intro = [p for p in paras if ('Compare every club' in p or 'In total' in p)]
    links = [p for p in paras if p not in intro]
    block = '<div class="nearby-more" id="county">' + ''.join(intro) + more + ''.join(links) + '</div>'
    near2 = near.replace('<div class="nearby-cta">', block + '\n    <div class="nearby-cta">', 1)
    s = s[:a] + s[a_end:]
    s = s.replace(near, near2, 1)
    bump('nearby_merged')
    return s


OCCASIONS = ['Weddings &amp; receptions', 'Birthday &amp; anniversary parties', 'Christenings &amp; baby showers',
             'Wakes &amp; celebrations of life', 'Corporate &amp; team-building days', 'Meetings &amp; conferences',
             'Charity &amp; fundraising nights', 'Pitch &amp; training-facility hire']


def venue_section(rec, pro):
    name, town = esc(rec['name']), esc(rec['town'] or rec['county'] or 'your area')
    if pro:
        intro = (f'Professional clubs often use their stadium for more than matchdays. {name} in {town} may be able to host '
                 f'weddings, parties, conferences and corporate events, so it is worth asking the club.')
    else:
        intro = (f'Rugby clubs are community hubs, and many hire out their clubhouse, function room or pitches to the public. '
                 f'{name} in {town} may be able to host your next celebration or event, so it is worth asking.')
    items = ''.join(f'<li>{o}</li>' for o in OCCASIONS)
    return f'''<!-- ══ VENUE HIRE & EVENTS ═══════════════════════════════ -->
<section class="sec sec-off" id="venue-hire">
  <div class="con"><div class="venue-compact">
    <span class="ey" style="font-family:Oswald,sans-serif;font-size:.72rem;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--violet)">Venue Hire &amp; Events</span>
    <h2>Weddings, parties &amp; events at {name}</h2>
    <p class="venue-intro">{intro}</p>
    <ul class="venue-chips" aria-label="Occasions a rugby club venue is often used for">{items}</ul>
    <p class="venue-note">Availability, capacity, licensing and prices are set by each club. We do not take bookings and cannot confirm what {name} offers, so contact the club directly to check.</p>
    <div class="venue-cta"><a href="#contact" class="btn btn-navy btn-sm">Ask {name} about hiring</a><a href="../claim.html">Club official? Add your venue details</a></div>
  </div></div>
</section>
'''


def add_venue(s, rec, pro):
    if 'venue-compact' in s:
        return s
    s = re.sub(r'<!-- ══ VENUE HIRE &amp; EVENTS.*?</section>\n|<!-- ══ VENUE HIRE & EVENTS.*?</section>\n', '', s, count=1, flags=re.S)
    k = s.find('<!-- ══ JOIN + CONTACT')
    if k < 0:
        k = s.find('<section class="sec sec-navy" id="contact">')
    if k < 0:
        return s
    bump('venue_section')
    return s[:k] + venue_section(rec, pro) + s[k:]


def get_pro(s):
    m = re.search(r'League \(\d{4}-\d{2}\)</th><td>([^<]*)', s)
    return bool(m and PRO_LEAGUE.search(m.group(1)))


def ground_answer(rec, c, g):
    cap = f' It holds {esc(g["capacity"])} supporters.' if g.get('capacity') else ''
    place = esc(c.get('ground_address') or g.get('ground_name') or '')
    pc = f', {esc(c["postcode"])}' if c.get('postcode') and c['postcode'] not in place else ''
    return (f'<p>{esc(rec["name"])} play home matches at {place}{pc}.{cap} '
            f'Use the directions link on this page, or see the Matchday section for travel tips.</p>')


def rebuild_faq(s, rec, c, g, pro):
    sec = re.search(r'<section class="sec[^"]*" id="faq">.*?</section>', s, re.S)
    if not sec:
        return s
    block = sec.group(0)
    w = re.search(r'<div style="max-width:\d+px;margin:0 auto">', block)
    if not w:
        return s
    wend = find_div_block(block, w.start())
    inner = block[w.end():wend - len('</div>')]
    inner, n_conv = convert_faq_items(inner)
    items = [list(m.groups()) for m in DET_ITEM.finditer(inner)]
    if not items:
        return s
    name = esc(rec['name'])
    web = c.get('website')
    out, have_venue = [], any('data-faq="venue"' in i[0] for i in items)
    for attrs, q, a in items:
        qt = text_of(q)
        if qt.startswith('Where does') and g:
            a = ground_answer(rec, c, g)
        if pro and qt.startswith('How can I join'):
            site = (f' through the <a href="{html.escape(web)}" target="_blank" rel="noopener noreferrer">club\'s official website</a>'
                    if web else ' through the club')
            out.append(['data-faq="tickets"', f'How can I watch {name} and get tickets?',
                        f'<p>{name} home matches are ticketed. Check fixtures and kick-off times with the Fixtures &amp; Results link on this page, then buy tickets{site}.</p>'])
            q = f'How can I get involved with {name}?'
            a = (f'<p>{name} is a professional club, so first-team places are by selection. For community, youth, women\'s '
                 f'or supporter opportunities, ask the club directly using the contact details on this page.</p>')
            attrs = 'data-faq="involved"'
        if qt.startswith('Which other') and not have_venue:
            out.append(venue_faq(rec, pro))
            have_venue = True
        out.append([attrs, q, a])
    if not have_venue:
        out.append(venue_faq(rec, pro))
    # de-duplicate (re-runs): keep first of each data-faq key
    seen, final = set(), []
    for attrs, q, a in out:
        key = re.search(r'data-faq="([^"]+)"', attrs)
        key = key.group(1) if key else text_of(q)
        if key in seen:
            continue
        seen.add(key)
        final.append([attrs, q, a])
    new_inner = ''.join(details_html(at, q, a) for at, q, a in final)
    new_block = block[:w.end()] + new_inner + block[wend - len('</div>'):]
    s = s.replace(block, new_block, 1)
    s = set_faq_jsonld(s, final)
    bump('faq_accordion')
    return s


def venue_faq(rec, pro):
    name = esc(rec['name'])
    if pro:
        a = (f'<p>Many professional clubs run conferences, weddings, parties and corporate events at their stadium, and {name} may be able to help. '
             f'Availability, capacity and prices are set by the club, so contact them using the details on this page to ask.</p>')
    else:
        a = (f'<p>Many rugby clubs hire out their clubhouse, function room or pitches for weddings, parties, christenings, wakes and corporate events, '
             f'and {name} may be able to help. Availability, capacity and prices are set by the club, so contact them using the details on this page to ask.</p>')
    return ['data-faq="venue"', f'Can I hire {name} for a wedding, party or event?', a]


def set_faq_jsonld(s, items):
    def fix(m):
        try:
            j = json.loads(m.group(2))
        except Exception:
            return m.group(0)
        nodes = j.get('@graph', [j])
        for n in nodes:
            if n.get('@type') == 'FAQPage':
                n['mainEntity'] = [{"@type": "Question", "name": text_of(q),
                                    "acceptedAnswer": {"@type": "Answer", "text": text_of(a)}} for _, q, a in items]
                return m.group(1) + json.dumps(j, ensure_ascii=False) + '</script>'
        return m.group(0)
    return re.sub(r'(<script type="application/ld\+json"[^>]*>)(.*?)</script>', fix, s, flags=re.S)


def add_ground(s, rec, c, g, er):
    """Sidebar capacity row + Matchday block + quick link (only for clubs with ground data)."""
    if not g:
        return s
    if 'ground-cap' not in s and g.get('capacity'):
        i = s.find('<div class="ground-mini-card">')
        if i >= 0:
            j = find_div_block(s, i)
            card = s[i:j]
            rows = list(re.finditer(r'<div class="ground-mini-row">.*?</div>', card, re.S))
            if rows:
                at = rows[-1].end()
                row = f'<div class="ground-mini-row ground-cap">{PEOPLE}<span>Capacity: {esc(g["capacity"])}</span></div>'
                s = s[:i] + card[:at] + row + card[at:] + s[j:]
    if 'id="matchday"' not in s:
        marker = s.find('<!-- SIDEBAR -->')
        if marker > 0:
            at = s.rfind('</div>', 0, marker)
            name = rec['name']
            addr = c.get('ground_address') or g.get('ground_name') or ''
            if c.get('postcode') and c['postcode'] not in addr:
                addr += ', ' + c['postcode']
            lis = [f'<li><strong>Ground:</strong> {esc(addr)}.</li>']
            if g.get('capacity'):
                lis.append(f'<li><strong>Capacity:</strong> {esc(g["capacity"])}.</li>')
            if er.get('er_team_id'):
                url = f'https://www.englandrugby.com/fixtures-and-results/search-results?team={er["er_team_id"]}'
                lis.append(f'<li><strong>Fixtures &amp; results:</strong> <a href="{url}" target="_blank" rel="noopener">live from England Rugby</a>.</li>')
            if c.get('website'):
                lis.append(f'<li><strong>Tickets &amp; matchday news:</strong> see the <a href="{html.escape(c["website"])}" target="_blank" rel="noopener noreferrer">club\'s official website</a>.</li>')
            if g.get('travel'):
                lis.append(f'<li><strong>Getting there:</strong> {esc(g["travel"])}</li>')
            block = (f'\n        <div class="about-divider"></div>\n        <div class="about-block" id="matchday"><div class="section-label">Matchday</div>'
                     f'<h2>Matchday &amp; getting to {esc(g.get("ground_name") or name)}</h2><div class="rich-text"><ul class="matchday-list">'
                     + ''.join(lis) + '</ul></div></div>\n      ')
            s = s[:at] + block + s[at:]
            s = s.replace('<li><a href="#contact" style="color:var(--red)">→ Contact ',
                          '<li><a href="#matchday" style="color:var(--red)">→ Matchday &amp; travel</a></li>\n            <li><a href="#contact" style="color:var(--red)">→ Contact ', 1)
            bump('matchday')
    return s


def solo_contact(s):
    m = re.search(r'<div class="join-contact-left">(.*?)</div>', s, re.S)
    if not m or 'join-solo' in s:
        return s
    body = re.sub(r'<!--.*?-->', '', m.group(1), flags=re.S).strip()
    if body.count('<p') == 1 and body.startswith('<p') and body.endswith('</p>') and len(text_of(body)) < 260:
        s = s.replace('<div class="join-contact-layout">', '<div class="join-contact-layout join-solo">', 1)
        bump('contact_solo')
    return s


def enhance_club(path, rec, contacts, grounds, ER):
    s = read(path)
    orig = s
    c = {k: v for k, v in contacts.get(rec['slug'], {}).items() if v}
    g = grounds.get(rec['slug'])
    er = ER.get(rec['slug'], {})
    is_team = rec['type'] == 'SportsTeam'
    pro = get_pro(s)
    s = strip_gallery(s)
    s = strip_history_tiles(s)
    s = merge_nearby(s, rec)
    s = add_photos(s, rec['slug'], rec.get('name') or rec['slug'])
    if is_team:
        s = add_venue(s, rec, pro)
        s = add_ground(s, rec, c, g, er)
        s = rebuild_faq(s, rec, c, g, pro)
        s = solo_contact(s)
    else:
        s, n = convert_faq_items(s)
        if n:
            bump('faq_accordion')
    s = close_faq(s)
    s = s.replace(f'&copy; 2025 UK Rugby Club Directory', f'&copy; {YEAR} UK Rugby Club Directory')
    if s != orig:
        write(path, s)
        bump('club_pages_changed')


# ───────────────────────────── other pages ─────────────────────────────

GUIDE_SEC = re.compile(r'<section class="guide-sec"( id="([^"]+)")?( aria-labelledby="([^"]+)")?>\s*(<h2 id="[^"]+">(.*?)</h2>)\s*(.*?)\s*</section>', re.S)

FOLLOW = '''<!-- FOLLOW THE GAME -->
<section class="sec sec-off" id="follow-the-game">
  <div class="con">
    <div class="sh"><span class="ey">Fixtures &amp; Tables</span><h2>Follow the Game</h2>
    <p>Looking for this weekend's matches or the league table? Every club profile links to its fixtures. These are the official competition sites.</p></div>
    <div class="follow-grid">
      <a class="follow-card" href="https://www.englandrugby.com/fixtures-and-results" target="_blank" rel="noopener"><strong>England Rugby</strong><span>Fixtures, results and tables for clubs across the English league pyramid</span></a>
      <a class="follow-card" href="https://www.champrugby.com/" target="_blank" rel="noopener"><strong>Champ Rugby</strong><span>England's second tier: fixtures, results and tables</span></a>
      <a class="follow-card" href="https://www.rugby-league.com/" target="_blank" rel="noopener"><strong>Rugby Football League</strong><span>Rugby league fixtures, results and competitions</span></a>
      <a class="follow-card" href="https://www.wru.wales/" target="_blank" rel="noopener"><strong>Welsh Rugby Union</strong><span>Community and professional rugby in Wales</span></a>
      <a class="follow-card" href="https://www.scottishrugby.org/" target="_blank" rel="noopener"><strong>Scottish Rugby</strong><span>Club fixtures and competitions in Scotland</span></a>
      <a class="follow-card" href="rugby-union-league-structure.html"><strong>How the leagues work</strong><span>Which level your local club plays at, from PREM Rugby down</span></a>
    </div>
  </div>
</section>

'''


PHOTO_DIR = 'imgs/clubs'


def add_photos(s, slug, name):
    """Two-image gallery (ground + club) straight after the About block.
    Only rendered when BOTH files exist and are different, so no empty placeholders ever ship.
    Files: imgs/clubs/<slug>-ground.(webp|jpg) and imgs/clubs/<slug>-club.(webp|jpg)
    Optional captions/credits: tools/club-photos.csv (slug,ground_alt,club_alt,credit)."""
    if 'id="club-photos"' in s:
        return s
    found = {}
    for kind in ('ground', 'club'):
        for ext in ('webp', 'jpg', 'jpeg', 'png'):
            f = os.path.join(ROOT, PHOTO_DIR, f'{slug}-{kind}.{ext}')
            if os.path.exists(f):
                found[kind] = f'../{PHOTO_DIR}/{slug}-{kind}.{ext}'
                break
    if len(found) < 2:
        return s
    import hashlib
    h = [hashlib.md5(open(os.path.join(ROOT, v[3:]), 'rb').read()).hexdigest() for v in found.values()]
    if h[0] == h[1]:
        return s
    meta = PHOTO_META.get(slug, {})
    g_alt = esc(meta.get('ground_alt') or f'{name} home ground')
    c_alt = esc(meta.get('club_alt') or f'{name} players and clubhouse')
    credit = meta.get('credit')
    cap = f'<p class="club-photos-credit">{esc(credit)}</p>' if credit else ''
    block = (f'<div class="about-block club-photos" id="club-photos"><div class="club-photos-grid">'
             f'<figure><img src="{found["ground"]}" alt="{g_alt}" width="800" height="533" loading="lazy" decoding="async"><figcaption>The ground</figcaption></figure>'
             f'<figure><img src="{found["club"]}" alt="{c_alt}" width="800" height="533" loading="lazy" decoding="async"><figcaption>The club</figcaption></figure>'
             f'</div>{cap}</div>\n        ')
    k = s.find('<!--glance-->')
    if k < 0:
        return s
    bump('photos')
    return s[:k] + block + s[k:]


HOME_REMOVE = ['union-or-league', 'areas-guide', 'areas', 'beginners', 'leagues', 'about-directory',
               'rugby-teams', 'england-teams', 'sources', 'england-rugby-league-teams',
               'gloucestershire-clubs', 'lymington-mariners']


def remove_home_sections(s):
    """Owner request: drop these guide sections (and their TOC links) from the homepage only."""
    n = 0
    for sid in HOME_REMOVE:
        m = re.search(r'<section class="guide-sec"[^>]*\bid="%s"[^>]*>' % re.escape(sid), s)
        if not m:
            continue
        end = s.find('</section>', m.end())
        if end < 0 or '<section' in s[m.end():end]:
            continue
        s = s[:m.start()] + s[end + len('</section>'):].lstrip('\n')
        s = re.sub(r'<li><a href="#%s">.*?</a></li>' % re.escape(sid), '', s, count=1)
        n += 1
    if n:
        bump('home_sections_removed', n)
    return s


def enhance_home(path):
    s = read(path)
    orig = s
    s = remove_home_sections(s)

    def fold(m):
        full, idattr, sid, aria, _, h2, title, body = (m.group(0), m.group(1), m.group(2), m.group(3), m.group(4), m.group(5), m.group(6), m.group(7))
        if 'class="guide-more"' in body:
            return full
        a = re.match(r'(<p class="guide-answer">.*?</p>)\s*', body, re.S)
        answer = a.group(1) if a else ''
        rest = body[a.end():] if a else body
        if len(text_of(rest)) < 400:        # short sections stay as they are
            return full
        is_open = ' open' if sid == 'how-to-find' else ''
        label = text_of(title)
        return (f'<section class="guide-sec"{idattr or ""}{aria or ""}>\n{h2}\n{answer}\n'
                f'<details class="guide-more"{is_open}><summary>Read more: {esc(label)}</summary><div class="guide-more-body">\n{rest}\n</div></details>\n</section>')

    s2 = GUIDE_SEC.sub(fold, s)
    if s2 != s:
        bump('home_sections_folded', len(GUIDE_SEC.findall(s)))
        s = s2
    # duplicate id="areas": the second one belongs to the guide
    if s.count('id="areas"') == 2:
        first = s.find('id="areas"')
        second = s.find('id="areas"', first + 10)
        s = s[:second] + 'id="areas-guide"' + s[second + len('id="areas"'):]
        s = re.sub(r'(<nav class="guide-toc".*?)href="#areas"', r'\1href="#areas-guide"', s, count=1, flags=re.S)
        bump('home_dup_id')
    if 'id="follow-the-game"' not in s:
        k = s.find('<!-- WHY US -->')
        if k > 0:
            s = s[:k] + FOLLOW + s[k:]
            bump('home_follow_strip')
    s, n = convert_faq_items(s)
    s = close_faq(s)
    s = s.replace('&copy; 2025 UK Rugby Club Directory', f'&copy; {YEAR} UK Rugby Club Directory')
    if s != orig:
        write(path, s)


def enhance_other(path):
    s = read(path)
    orig = s
    s, n = convert_faq_items(s)
    if n:
        bump('hub_faq_pages')
    s = close_faq(s)
    s = s.replace('&copy; 2025 UK Rugby Club Directory', f'&copy; {YEAR} UK Rugby Club Directory')
    if s != orig:
        write(path, s)


# ───────────────────────────── main ─────────────────────────────

def load_grounds():
    rows = {}
    p = os.path.join(HERE, 'club-grounds.csv')
    if os.path.exists(p):
        for r in csv.DictReader(open(p, encoding='utf-8')):
            r = {k: (v or '').strip() for k, v in r.items()}
            if r.get('slug'):
                rows[r['slug']] = r
    return rows


def load_photo_meta():
    rows = {}
    p = os.path.join(HERE, 'club-photos.csv')
    if os.path.exists(p):
        for r in csv.DictReader(open(p, encoding='utf-8')):
            r = {k: (v or '').strip() for k, v in r.items()}
            if r.get('slug'):
                rows[r['slug']] = r
    return rows


PHOTO_META = load_photo_meta()


def main():
    ER = load_er()
    contacts = load_contacts()
    grounds = load_grounds()
    redirected = set()
    for line in open(os.path.join(ROOT, '_redirects'), encoding='utf-8'):
        m = re.match(r'(/club/[^\s]+\.html)\s+/[^\s]*\s+301', line)
        if m:
            redirected.add(m.group(1)[1:])
    recs = {r['slug']: r for r in json.load(open(os.path.join(HERE, 'clubs.json')))}
    for path in sorted(glob.glob(os.path.join(ROOT, 'club', '*.html'))):
        rel = os.path.relpath(path, ROOT)
        slug = os.path.basename(path)[:-5]
        if rel in redirected or slug not in recs or not recs[slug]['type']:
            continue
        enhance_club(path, recs[slug], contacts, grounds, ER)
    root_redirected = set()
    for line in open(os.path.join(ROOT, '_redirects'), encoding='utf-8'):
        m = re.match(r'/([^/\s]+\.html)\s+\S+\s+301', line)
        if m:
            root_redirected.add(m.group(1))
    for path in sorted(glob.glob(os.path.join(ROOT, '*.html'))):
        base = os.path.basename(path)
        if base in root_redirected:
            continue
        if base == 'index.html':
            enhance_home(path)
        else:
            enhance_other(path)
    print(json.dumps(STATS, indent=1))


if __name__ == '__main__':
    main()
