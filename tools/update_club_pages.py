#!/usr/bin/env python3
"""
Club page updater for ukrugbyclubdirectory.co.uk
================================================

Run from the repo root:   python3 tools/update_club_pages.py

What it does (safe to re-run — every step is idempotent):

  1. Replaces generated "fake" badge images (SVG placeholders saved as .png)
     with the honest initials fallback.
  2. Removes the empty "Club Gallery" placeholder boxes.
  3. Replaces the shared stock hero photo (professional players) with a
     neutral pattern panel.
  4. Removes the unverified "All Welcome / Membership" stat.
  5. Deletes templated filler sentences that repeat across hundreds of pages.
  6. Rewrites the generic "Join" copy and FAQ answers so they say something
     true and useful for that club (incl. the right governing body).
  7. Injects contact details from tools/club-contacts.csv (website, phone,
     email, Facebook, ground address, postcode) into the page, the contact
     button and the JSON-LD.  Blank cells are ignored, so you can fill the
     CSV in gradually and re-run.

Only pages in /club/ that are live (not 301'd) are touched.
"""
import csv, glob, html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(ROOT, 'tools', 'club-contacts.csv')

WALES = {'South Glamorgan', 'Carmarthenshire', 'Neath Port Talbot', 'Rhondda Cynon Taf', 'Ceredigion',
         'Caerphilly', 'Powys', 'Bridgend', 'Conwy', 'Blaenau Gwent', 'Monmouthshire', 'Pembrokeshire',
         'Denbighshire', 'West Glamorgan', 'Gwynedd', 'Anglesey', 'Merthyr Tydfil', 'Wrexham',
         'Mid Glamorgan', 'Gwent', 'Flintshire', 'Torfaen', 'Newport', 'Swansea', 'Vale of Glamorgan', 'Cardiff'}
SCOTLAND = {'Midlothian', 'Lanarkshire', 'Roxburghshire', 'Aberdeenshire', 'Angus', 'Fife', 'Stirlingshire',
            'Clackmannanshire', 'Berwickshire', 'Perthshire', 'Selkirkshire', 'East Lothian', 'West Lothian',
            'Ayrshire', 'Morayshire', 'Inverness-shire', 'Dumfriesshire', 'Peeblesshire', 'Renfrewshire',
            'Dunbartonshire', 'City of Edinburgh', 'Glasgow', 'Scottish Borders', 'Highland'}
N_IRELAND = {'County Antrim', 'County Armagh', 'County Tyrone', 'County Down', 'County Londonderry',
             'County Fermanagh'}

FAKE_BADGES = ('tigers.png', 'bristolbears.png', 'harlequin_fc_logo.svg.png')
STOCK_HEROES = ('rugby-union-hero.jpg', 'rugby-league-hero.jpg')

# Sentences that repeat on 100+ pages and carry no club-specific information.
FILLER = [
    r"For anyone searching for an? [^.<]{2,60}? rugby club, [^.<]{2,80}? is a natural place to start\.",
    r"(?:Rugby )?[Uu]nion only turned professional in August 1995, so the club grew up playing for the love of the game\.",
    r"That gives the club more than \d+ years of rugby in [^.<]+?\.",
    r"In addition, generations of local players, coaches and volunteers have shaped its story\.",
    r"In total, the club has more than \d+ years behind it\.",
    r"[A-Z][a-z]+, the club carries more than \d+ years of history into every season\.",
    r"Whether you are new to the sport or an experienced player, this page shows you where the club plays and how to get involved\.",
    r"[A-Z][a-z]+ every club has its own character, this profile helps you see what makes this one different before you visit\.",
    r"In addition, it gives supporters in [^.<]+? a team to follow and new players a clear route into the game\.",
    r"For players in [^.<]+?, that heritage adds real meaning to pulling on the shirt\.",
    r"As a result, it holds a special place for supporters across [^.<]+?\.",
    r"Since then, the club has carried amateur rugby through almost a century of change\.",
    r"Since then, like many clubs of that era, it has seen the game change almost beyond recognition\.",
    r"The [^.<]{2,40}? had formed in \d{4}, and clubs were springing up in towns across [^.<]+?\.",
    r"For decades, clubs like this one have kept rugby league at the heart of their communities\.",
    r"[A-Z][a-z]+ use the links below to compare nearby clubs, grounds and playing levels before you decide\.",
    r"[A-Z][a-z]+ places it among the pioneering clubs of [^.<]+? rugby\.",
]
FILLER_RE = [re.compile(p) for p in FILLER]

# Generic "how to join" sentences found in the Join panel.
JOIN_FILLER = [
    r"New players, returning players and volunteers are the lifeblood of every rugby club\.",
    r"So if you want to play, coach or help out, get in touch today\.",
    r"Ask about training nights, membership and junior sections\.",
    r"In most cases, you can try a session before you commit\.",
    r"Getting started at the club is simple\.",
    r"First, get in touch to check the next training session and which teams have space\.",
    r"Then come along, meet the coaches and try a session\.",
    r"Once you are happy, simply register with the club and start playing\.",
    r"(?:Check with|Contact) the club first, because training times and age groups change from year to year\.",
    r"After that, simply turn up with boots, a gum shield and water\.",
    r"(?:Clubs|Coaches) usually offer newcomers a taster session before you register as a member\.",
    r"In fact, most rugby clubs welcome new players at any point in the season\.",
]
JOIN_RE = [re.compile(p) for p in JOIN_FILLER]

STATS = {k: 0 for k in ['pages', 'badges', 'gallery', 'hero', 'membership', 'filler', 'join', 'faq',
                        'meta', 'contacts']}


def nation(county):
    if county in WALES: return 'Wales'
    if county in SCOTLAND: return 'Scotland'
    if county in N_IRELAND: return 'Northern Ireland'
    return 'England'


def governing_body(sport, county):
    if 'league' in sport.lower():
        return 'the Rugby Football League', 'https://www.rugby-league.com/'
    return {
        'Wales': ('the Welsh Rugby Union', 'https://www.wru.wales/'),
        'Scotland': ('Scottish Rugby', 'https://scottishrugby.org/'),
        'Northern Ireland': ('the IRFU', 'https://www.irishrugby.ie/'),
    }.get(nation(county), ('England Rugby', 'https://www.englandrugby.com/'))


def gb_link(sport, county):
    name, url = governing_body(sport, county)
    return f'<a href="{url}" target="_blank" rel="noopener" style="color:var(--violet-lt)">{name}</a>'


def find_div_block(s, start):
    """Return end index of the <div> that opens at `start` (balanced)."""
    depth, i = 0, start
    tag = re.compile(r'<(/?)div\b', re.I)
    for m in tag.finditer(s, start):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return s.find('>', m.end()) + 1
    return -1


def strip_filler_sentences(s):
    """Remove filler sentences from <p> text inside <main>, outside the FAQ."""
    main_a, main_b = s.find('<main'), s.find('</main>')
    if main_a < 0: return s
    body = s[main_a:main_b]
    faq_a = body.find('id="faq"')
    head, faq = (body[:faq_a], body[faq_a:]) if faq_a > 0 else (body, '')

    def fix_p(m):
        inner = m.group(2)
        new = inner
        new = re.sub(r"It is also (one of [^.<]+?), so you can easily compare nearby options below\.",
                     r"It is \1.", new)
        new = re.sub(r"(In total, [^.<]+? in our directory)\. So use the links below[^.<]*\.", r"\1.", new)
        for rx in FILLER_RE:
            new = rx.sub('', new)
        new = re.sub(r'\s{2,}', ' ', new).strip()
        if new != inner.strip():
            STATS['filler'] += 1
        if not new:
            return ''
        return f'{m.group(1)}{new}</p>'

    head = re.sub(r'(<p(?: [^>]*)?>)(.*?)</p>', fix_p, head, flags=re.S)
    return s[:main_a] + head + faq + s[main_b:]


def load_contacts():
    rows = {}
    if os.path.exists(CSV_PATH):
        for r in csv.DictReader(open(CSV_PATH, encoding='utf-8')):
            slug = (r.get('slug') or '').strip()
            if slug:
                rows[slug] = {k: (v or '').strip() for k, v in r.items()}
    return rows


def pretty_url(u):
    return re.sub(r'^https?://(www\.)?', '', u).rstrip('/')


def tel_href(p):
    d = re.sub(r'[^\d+]', '', p)
    if d.startswith('0'): d = '+44' + d[1:]
    return d


def build_contact(rec, c):
    """Return (address_html, button_html, footnote_html) for the contact panel."""
    gold = 'style="color:var(--gold)"'
    lines = [f'<strong style="color:#fff">{html.escape(rec["name"])}</strong>']
    where = c.get('ground_address') or ', '.join(x for x in [rec['town'], rec['county']] if x)
    if c.get('postcode'): where = f'{where}, {c["postcode"]}' if c['postcode'] not in where else where
    lines.append(html.escape(where))
    if c.get('phone'):
        lines.append(f'Phone: <a href="tel:{tel_href(c["phone"])}" {gold}>{html.escape(c["phone"])}</a>')
    if c.get('email'):
        lines.append(f'Email: <a href="mailto:{html.escape(c["email"])}" {gold}>{html.escape(c["email"])}</a>')
    if c.get('website'):
        lines.append(f'Website: <a href="{html.escape(c["website"])}" target="_blank" rel="noopener noreferrer" {gold}>{html.escape(pretty_url(c["website"]))}</a>')
    if c.get('facebook'):
        lines.append(f'Facebook: <a href="{html.escape(c["facebook"])}" target="_blank" rel="noopener noreferrer" {gold}>{html.escape(pretty_url(c["facebook"]))}</a>')
    q = '+'.join((rec['name'] + ' ' + (c.get('postcode') or rec['town'])).split())
    lines.append(f'<a href="https://www.google.com/maps/search/?api=1&query={html.escape(q)}" target="_blank" rel="noopener noreferrer" {gold}>Open in Google Maps</a>')
    address = ('<address style="font-style:normal;line-height:1.9;color:rgba(255,255,255,.85)">'
               + '<br>'.join(lines) + '</address>')
    btn = 'class="btn btn-gold btn-sm" style="width:100%;justify-content:center;margin-top:1.25rem;display:inline-flex"'
    if c.get('phone'):
        button = f'<a href="tel:{tel_href(c["phone"])}" {btn}>Call the Club</a>'
    elif c.get('email'):
        button = f'<a href="mailto:{html.escape(c["email"])}" {btn}>Email the Club</a>'
    elif c.get('website'):
        button = f'<a href="{html.escape(c["website"])}" target="_blank" rel="noopener noreferrer" {btn}>Visit Club Website</a>'
    elif c.get('facebook'):
        button = f'<a href="{html.escape(c["facebook"])}" target="_blank" rel="noopener noreferrer" {btn}>Message on Facebook</a>'
    else:
        button = f'<a href="../claim.html" {btn}>Claim &amp; Add Contact Details</a>'
    missing = [x for x, k in [('a phone number', 'phone'), ('an email address', 'email'), ('training times', '_')] if not c.get(k)]
    foot = ('<p style="font-size:.8rem;color:rgba(255,255,255,.6);margin-top:.75rem">Club official? '
            '<a href="../claim.html" style="color:inherit;text-decoration:underline">Claim this listing</a> to add '
            + (', '.join(missing[:-1]) + ' and ' + missing[-1] if len(missing) > 1 else missing[0]) + '.</p>')
    if c.get('source_url'):
        foot += (f'<p style="font-size:.75rem;color:rgba(255,255,255,.5);margin-top:.35rem">Details checked '
                 f'{html.escape(c.get("checked_date", ""))} from <a href="{html.escape(c["source_url"])}" target="_blank" '
                 f'rel="noopener nofollow" style="color:inherit;text-decoration:underline">{html.escape(pretty_url(c["source_url"]).split("/")[0])}</a>.</p>')
    return address, button, foot


CURRENT_YEAR = 2026


def fix_founded(s, old, new):
    """Swap a wrong founding year for the corrected one in every place the template uses it."""
    years = CURRENT_YEAR - int(new)
    plus = f'{(years // 10) * 10}+' if years >= 10 else str(years)
    reps = [
        (rf'Est\. {old}\b', f'Est. {new}'),
        (rf'"foundingDate": "{old}"', f'"foundingDate": "{new}"'),
        (rf'([Ff]ounded in) {old}\b', rf'\1 {new}'),
        (rf'\bsince {old}\b', f'since {new}'),
        (rf'(<strong>){old}(</strong><span>Founded)', rf'\g<1>{new}\2'),
        (rf'(<dt>Founded</dt><dd>){old}(</dd>)', rf'\g<1>{new}\2'),
        (rf'(>){old}(</div><div[^>]*>Founded<)', rf'\g<1>{new}\2'),
        # history sentences carry an era clause tied to the old year — drop the clause
        (rf'(formed in|dates from|was founded in) {old}(?:, [^.<]*)?\.', rf'\1 {new}.'),
        (rf'(Founded in) {old}, ', rf'\1 {new}, '),
        (r'>\d+\+(</div><div[^>]*>Years of History<)', rf'>{plus}\1'),
        (r'more than \d+ years', f'more than {(years // 10) * 10 if years >= 10 else years} years'),
    ]
    for a, b in reps:
        s = re.sub(a, b, s)
    return s


def fix_cards_elsewhere(root, corrections, files):
    """Update 'Est. YYYY' on club cards that link to a corrected club from other pages."""
    n = 0
    for f in files:
        s = open(f, encoding='utf-8', errors='surrogateescape').read()
        o = s
        for slug, (old, new) in corrections.items():
            def card(m):
                return re.sub(rf'Est\. {old}\b', f'Est. {new}', m.group(0))
            s = re.sub(rf'club/{re.escape(slug)}\.html".{{0,1500}}?</article>', card, s, flags=re.S)
        if s != o:
            open(f, 'w', encoding='utf-8', errors='surrogateescape').write(s); n += 1
    return n


def has_contact(c):
    return any(c.get(k) for k in ('phone', 'email', 'website', 'facebook'))


def existing_contact(s):
    """Pull contact data already present in the page (from earlier work)."""
    c = {}
    m = re.search(r'Website: <a href="([^"]+)"', s)
    if m: c['website'] = html.unescape(m.group(1))
    m = re.search(r'Phone: <a href="tel:[^"]*"[^>]*>([^<]+)</a>', s)
    if m: c['phone'] = html.unescape(m.group(1))
    m = re.search(r'Email: <a href="mailto:([^"]+)"', s)
    if m: c['email'] = html.unescape(m.group(1))
    m = re.search(r'Facebook: <a href="([^"]+)"', s)
    if m: c['facebook'] = html.unescape(m.group(1))
    return c


def update_jsonld(s, c):
    def fix(m):
        try:
            j = json.loads(m.group(1))
        except Exception:
            return m.group(0)
        changed = False
        for node in j.get('@graph', [j]):
            if node.get('@type') not in ('SportsTeam', 'LocalBusiness'):
                continue
            if c.get('phone'): node['telephone'] = tel_href(c['phone']); changed = True
            if c.get('email'): node['email'] = c['email']; changed = True
            same = [u for u in [c.get('website'), c.get('facebook')] if u]
            if same: node['sameAs'] = same; changed = True
            addr = ((node.get('location') or {}).get('address')) or node.get('address')
            if isinstance(addr, dict):
                if c.get('ground_address'): addr['streetAddress'] = c['ground_address']; changed = True
                if c.get('postcode'): addr['postalCode'] = c['postcode']; changed = True
        if not changed:
            return m.group(0)
        return '<script type="application/ld+json">' + json.dumps(j, ensure_ascii=False) + '</script>'
    return re.sub(r'<script type="application/ld\+json">(.*?)</script>', fix, s, flags=re.S)


def rebuild_faqpage(s):
    """Keep FAQPage JSON-LD in step with the visible FAQ answers."""
    if 'FAQPage' not in s: return s
    sec = re.search(r'id="faq".*?</section>', s, re.S)
    if not sec: return s
    pairs = re.findall(r'<h3[^>]*>(.*?)</h3>\s*<p>(.*?)</p>', sec.group(0), re.S)
    if not pairs: return s
    ents = [{"@type": "Question", "name": html.unescape(re.sub('<[^>]+>', '', q)),
             "acceptedAnswer": {"@type": "Answer", "text": html.unescape(re.sub('<[^>]+>', '', a))}} for q, a in pairs]

    def fix(m):
        try:
            j = json.loads(m.group(1))
        except Exception:
            return m.group(0)
        nodes = j.get('@graph', [j])
        for n in nodes:
            if n.get('@type') == 'FAQPage':
                n['mainEntity'] = ents
                return '<script type="application/ld+json">' + json.dumps(j, ensure_ascii=False) + '</script>'
        return m.group(0)
    return re.sub(r'<script type="application/ld\+json">(.*?)</script>', fix, s, flags=re.S)


def process(path, rec, contacts):
    s = open(path, encoding='utf-8', errors='surrogateescape').read()
    orig = s
    name, sport, town, county = rec['name'], rec['sport'], rec['town'], rec['county']
    is_team = rec['type'] == 'SportsTeam'

    # 1. fake badges -> initials
    def badge(m):
        tag = m.group(0)
        alt = re.search(r"alt=['\"]([^'\"]*)", tag)
        initial = (alt.group(1)[:1] if alt else '?').upper()
        STATS['badges'] += 1
        cls = 'hero-badge-fallback' if 'hero-badge' in tag else 'badge-fallback'
        return f'<div class="{cls}">{initial}</div>'
    fake_rx = r"<img[^>]*src=['\"][^'\"]*(?:%s)['\"][^>]*>(\s*<div class=['\"](?:hero-)?badge-fallback['\"] style=['\"]display:none['\"]>[^<]*</div>)?" % '|'.join(re.escape(b) for b in FAKE_BADGES)
    s = re.sub(fake_rx, badge, s)

    # 2. gallery placeholders
    i = s.find('<div class="gallery-inline"')
    if i >= 0:
        j = find_div_block(s, i)
        if j > 0 and '<img' not in s[i:j]:
            k = s.rfind('<!-- ★ GALLERY', 0, i)
            start = k if k >= 0 and i - k < 120 else i
            s = s[:start] + s[j:]
            STATS['gallery'] += 1

    # 3. stock hero photo
    i = s.find('<div class="lh-right"')
    if i >= 0:
        j = find_div_block(s, i)
        block = s[i:j]
        if any(h in block for h in STOCK_HEROES):
            s = s[:i] + ('<div class="lh-right lh-pattern" aria-hidden="true" '
                         'style="position:absolute;right:0;top:0;bottom:0;width:42%"></div>') + s[j:]
            STATS['hero'] += 1

    # 4. unverified membership stat
    s2 = re.sub(r'\s*<div class="stat-div"></div>\s*<div class="stat-item">(?:(?!<div class="stat-item">).)*?'
                r'<strong>All Welcome</strong><span>Membership</span></div></div>', '', s, flags=re.S)
    if s2 != s: STATS['membership'] += 1; s = s2

    # 5. filler sentences
    s = strip_filler_sentences(s)

    # contact data: CSV overrides what is already on the page
    c = existing_contact(s)
    c.update({k: v for k, v in contacts.get(rec['slug'], {}).items() if v})
    contactable = has_contact(c)

    # 4b. corrected founding year from the CSV
    new_year = c.get('founded', '')
    old_year = rec['founded']
    if re.fullmatch(r'\d{4}', new_year or '') and old_year and new_year != old_year:
        s = fix_founded(s, old_year, new_year)
        rec = dict(rec, founded=new_year)
        STATS.setdefault('founded', 0); STATS['founded'] += 1

    # 6a. join panel
    if is_team:
        m = re.search(r'(<div class="join-contact-left">)(.*?)(</div>)', s, re.S)
        if m:
            text = html.unescape(re.sub('<[^>]+>', ' ', m.group(2)))
            sentences = [x for x in re.split(r'(?<=[.?!])\s+', ' '.join(text.split())) if x.strip()]
            generic = all(any(rx.fullmatch(x.strip()) for rx in JOIN_RE) for x in sentences) if sentences else True
            if generic or '<!--join-->' in m.group(2):
                p = 'class="text-light" style="margin-bottom:1rem"'
                if contactable:
                    body = (f'<p {p}>To ask about training, junior sections or volunteering, contact {html.escape(name)} '
                            f'directly using the details on this page.</p>')
                else:
                    body = (f'<p {p}>We don\'t hold direct contact details for {html.escape(name)} yet. You can find the club '
                            f'through {gb_link(sport, county)} or by searching for its name on social media.</p>')
                body = '<!--join-->' + body
                if body != m.group(2).strip():
                    s = s[:m.start(2)] + body + s[m.end(2):]
                    STATS['join'] += 1

    # 7. contact panel (generated pages only: they have the "Contact Details" heading)
    m = re.search(r'(<div class="join-contact-right">\s*<h3>Contact Details</h3>\s*)(<address.*?</address>)\s*(<a [^>]*class="btn btn-gold btn-sm"[^>]*>.*?</a>)\s*(<p style="font-size:\.8rem.*?</p>(?:\s*<p style="font-size:\.75rem.*?</p>)?)', s, re.S)
    if m:
        address, button, foot = build_contact(rec, c)
        new = m.group(1) + address + '\n        ' + button + '\n        ' + foot
        if new != m.group(0):
            s = s[:m.start()] + new + s[m.end():]
            if rec['slug'] in contacts: STATS['contacts'] += 1
        s = update_jsonld(s, c)

    # 6b. FAQ answers
    if is_team:
        nearby = re.findall(r'<h3 class="club-name">([^<]+)</h3>', s[s.find('id="nearby"'):] if 'id="nearby"' in s else '')
        def faq(m):
            q, a = m.group(2), m.group(4)
            qt = html.unescape(q)
            new = a
            if qt.startswith('When was') and rec['founded']:
                new = f'{html.escape(name)} was founded in {rec["founded"]}.'
            elif qt.startswith('How can I join'):
                new = (f'Contact the club using the details on this page and ask about the next training session.'
                       if contactable else
                       f'Ask the club about its next training session. The Join &amp; Contact section on this page '
                       f'shows the best way to reach {html.escape(name)}.')
            elif qt.startswith('Which other') and nearby:
                names = [html.unescape(n) for n in nearby[:3] if html.unescape(n) != name]
                if names:
                    lst = names[0] if len(names) == 1 else ', '.join(names[:-1]) + ' and ' + names[-1]
                    new = f'Nearby clubs in our directory include {html.escape(lst)}. Each has its own profile below.'
            elif qt.startswith('Where does'):
                new = re.sub(r'\s*For directions, use the Google Maps link on this page to find the ground and plan your journey\.',
                             ' Use the Google Maps link on this page for directions.', a)
            if new != a:
                STATS['faq'] += 1
            return m.group(1) + m.group(2) + m.group(3) + new + m.group(5)
        sec = re.search(r'id="faq".*?</section>', s, re.S)
        if sec:
            fixed = re.sub(r'(<h3[^>]*>)(.*?)(</h3>\s*<p>)(.*?)(</p>)', faq, sec.group(0), flags=re.S)
            s = s[:sec.start()] + fixed + s[sec.end():]
        s = rebuild_faqpage(s)

    # 8. meta descriptions: no promises the page can't keep
    def meta(mm):
        d = mm.group(2)
        nd = d.replace('Book a taster session today.', 'Plan your first visit today.')
        if not contactable:
            nd = nd.replace('club history and contact details.', 'club history and nearby clubs.')
            nd = nd.replace('history and contact details.', 'history and nearby clubs.')
        if nd != d: STATS['meta'] += 1
        return mm.group(1) + nd + mm.group(3)
    s = re.sub(r'(<meta (?:name|property)="(?:description|og:description|twitter:description)" content=")([^"]*)(")', meta, s)

    if s != orig:
        open(path, 'w', encoding='utf-8', errors='surrogateescape').write(s)
        STATS['pages'] += 1


def main():
    redirected = set()
    for line in open(os.path.join(ROOT, '_redirects'), encoding='utf-8'):
        m = re.match(r'(/club/[^\s]+\.html)\s+/[^\s]*\s+301', line)
        if m: redirected.add(m.group(1)[1:])
    recs = {r['slug']: r for r in json.load(open(os.path.join(ROOT, 'tools', 'clubs.json')))}
    contacts = load_contacts()
    for path in sorted(glob.glob(os.path.join(ROOT, 'club', '*.html'))):
        rel = os.path.relpath(path, ROOT)
        slug = os.path.basename(path)[:-5]
        if rel in redirected or slug not in recs or not recs[slug]['type']:
            continue
        process(path, recs[slug], contacts)
    corrections = {slug: (recs[slug]['founded'], c['founded']) for slug, c in contacts.items()
                   if slug in recs and re.fullmatch(r'\d{4}', c.get('founded', '') or '')
                   and recs[slug]['founded'] and c['founded'] != recs[slug]['founded']}
    if corrections:
        pages = glob.glob(os.path.join(ROOT, '*.html')) + glob.glob(os.path.join(ROOT, 'club', '*.html'))
        STATS['cards_fixed_on_pages'] = fix_cards_elsewhere(ROOT, corrections, pages)
    print(json.dumps(STATS, indent=1))


if __name__ == '__main__':
    main()
