#!/usr/bin/env python3
"""
Build the assets that make the directory easy to link to (backlink readiness).

Additive only: writes NEW files and never regenerates existing hubs or pages.
  - 9 new area hubs (built with the same renderer as tools/build_hubs.py)
  - rugby-clubs-by-area.html   index of every area hub
  - link-to-us.html            link snippets + badges for clubs, councils, schools, bloggers
  - rugby-club-statistics.html counts from the directory data
  - press.html                 media / citation page
  - school-university-rugby.html
  - badges/ukrcd-badge-light.svg, badges/ukrcd-badge-dark.svg
  - appends new URLs to sitemap.xml and _redirects (idempotent)
  - links each club page to its new hub (idempotent, one line)

Run from the repo root:  python3 tools/build_backlink_assets.py
"""
import collections, datetime, html, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_hubs as bh

ROOT, SITE = bh.ROOT, bh.SITE
TODAY = '2026-11-19'
P, H2 = bh.P, bh.H2
H3 = 'style="font-size:1.15rem;font-weight:700;color:var(--text-primary);margin:1.5rem 0 .6rem"'
TD = 'style="padding:.55rem .75rem;border-bottom:1px solid #e3e8ef;vertical-align:top;font-size:.92rem"'
TH = 'style="padding:.55rem .75rem;text-align:left;border-bottom:2px solid #293241;font-size:.85rem;text-transform:uppercase;letter-spacing:.04em"'
CODE = 'style="display:block;background:#f4f6f9;border:1px solid #e3e8ef;border-radius:8px;padding:.6rem .75rem;font-size:.82rem;line-height:1.5;user-select:all;overflow-wrap:anywhere;font-family:ui-monospace,Menlo,Consolas,monospace"'

# --------------------------------------------------------------------------- new hubs
def L(slug, name):
    return f'<a href="club/{slug}.html">{name}</a>'

NEW_HUBS = [
 dict(slug='rugby-clubs-west-yorkshire', place='West Yorkshire', counties=['West Yorkshire'],
  title='Rugby Clubs in West Yorkshire | League &amp; Union Clubs by Town',
  meta='Find rugby clubs in West Yorkshire: {n} league and union clubs in Leeds, Bradford, Wakefield, Castleford, Halifax, Huddersfield and more. Compare clubs near you.',
  keywords='rugby clubs West Yorkshire, rugby league West Yorkshire, rugby union West Yorkshire, Leeds rugby, Wakefield rugby league, Bradford rugby',
  intro=['West Yorkshire is one of the strongest rugby league areas in the world, with rugby union clubs in many of the same towns. This page lists the {n} West Yorkshire clubs in our directory — {league} rugby league and {union} rugby union.',
         'Professional rugby league is represented by ' + ', '.join([L('leeds-rhinos','Leeds Rhinos'),L('wakefield-trinity','Wakefield Trinity'),L('castleford-tigers','Castleford Tigers'),L('bradford-bulls','Bradford Bulls'),L('huddersfield-giants','Huddersfield Giants'),L('featherstone-rovers','Featherstone Rovers'),L('halifax-panthers','Halifax Panthers')]) + ' and others, with a large amateur network beneath them. Rugby union clubs include ' + ', '.join([L('headingley-rfc','Headingley'),L('otley-rfc','Otley'),L('wharfedale-rfc','Wharfedale'),L('ilkley-rfc','Ilkley'),L('morley-rfc','Morley'),L('bradford-bingley-rfc','Bradford &amp; Bingley')]) + '.',
         'For the city on its own see our <a href="rugby-clubs-leeds.html">Leeds rugby clubs</a> page; for the wider region, the <a href="rugby-union.html?region=yorkshire">Yorkshire rugby union listings</a>.'],
  faqs=[('Which code is bigger in West Yorkshire?', 'Rugby league is the traditional game in towns such as Wakefield, Castleford, Dewsbury, Batley and Featherstone, while rugby union is strong in Leeds, Otley, Ilkley and the Aire and Wharfe valleys. Many towns have clubs of both codes.')]),
 dict(slug='rugby-clubs-south-yorkshire', place='South Yorkshire', counties=['South Yorkshire'],
  title='Rugby Clubs in South Yorkshire | Sheffield, Doncaster &amp; Rotherham',
  meta='Find rugby clubs in South Yorkshire: {n} league and union clubs in Sheffield, Doncaster, Rotherham, Barnsley and more. Compare clubs and find one near you.',
  keywords='rugby clubs South Yorkshire, Sheffield rugby club, Doncaster rugby, Rotherham rugby, Barnsley rugby',
  intro=['This page lists the {n} South Yorkshire clubs in our directory — {union} rugby union and {league} rugby league — across Sheffield, Doncaster, Rotherham and Barnsley.',
         'Clubs include ' + ', '.join([L('doncaster-knights','Doncaster Knights'),L('rotherham-titans','Rotherham Titans'),L('sheffield-tigers-rfc','Sheffield Tigers'),L('barnsley-rfc','Barnsley'),L('penistone-rfc','Penistone'),L('thornensians-rfc','Thornensians')]) + ' in rugby union, and ' + L('sheffield-eagles','Sheffield Eagles') + ' and ' + L('doncaster-rlfc','Doncaster') + ' in rugby league.'],
  faqs=[('Is there rugby league in South Yorkshire?', 'Yes. <a href="club/sheffield-eagles.html">Sheffield Eagles</a> and <a href="club/doncaster-rlfc.html">Doncaster</a> play rugby league, and the neighbouring West Yorkshire towns are close by — see our <a href="rugby-clubs-west-yorkshire.html">West Yorkshire rugby clubs</a> page.')]),
 dict(slug='rugby-clubs-devon', place='Devon', counties=['Devon'],
  title='Rugby Clubs in Devon | Exeter, Plymouth, Torbay &amp; North Devon',
  meta='Find rugby clubs in Devon: {n} clubs including Exeter Chiefs, Plymouth Albion, Barnstaple, Torquay and Newton Abbot. Compare clubs and find one near you.',
  keywords='rugby clubs Devon, Devon rugby clubs, Exeter rugby, Plymouth rugby, Torquay rugby club, Barnstaple rugby',
  intro=['Devon has a rugby union club in almost every town. This page lists the {n} Devon clubs in our directory so you can compare them in one place.',
         'At the top are ' + L('exeter-chiefs','Exeter Chiefs') + ' (with ' + L('exeter-chiefs-women','Exeter Chiefs Women') + ') and ' + L('plymouth-albion','Plymouth Albion') + '. Community clubs include ' + ', '.join([L('exeter-rfc','Exeter'),L('barnstaple-rfc','Barnstaple'),L('bideford-rfc','Bideford'),L('torquay-athletic-rfc','Torquay Athletic'),L('newton-abbot-rfc','Newton Abbot'),L('tavistock-rfc','Tavistock'),L('exmouth-rfc','Exmouth')]) + '.',
         'See also the wider <a href="south-west-rugby-clubs.html">South West rugby clubs</a> page, and <a href="rugby-clubs-cornwall.html">rugby clubs in Cornwall</a> next door.'],
  faqs=[('Are there professional rugby clubs in Devon?', '<a href="club/exeter-chiefs.html">Exeter Chiefs</a> and <a href="club/plymouth-albion.html">Plymouth Albion</a> are the best-known senior clubs in the county.')]),
 dict(slug='rugby-clubs-cornwall', place='Cornwall', counties=['Cornwall'],
  title='Rugby Clubs in Cornwall | Redruth, Camborne, Truro &amp; More',
  meta='Find rugby clubs in Cornwall: {n} clubs including Cornish Pirates, Redruth, Camborne, Truro, Launceston and St Austell. Compare clubs and find one near you.',
  keywords='rugby clubs Cornwall, Cornwall rugby, Cornish Pirates, Redruth rugby, Camborne rugby, Truro rugby club',
  intro=['Rugby is a big part of community life in Cornwall. This page lists the {n} Cornish clubs in our directory — {union} rugby union and {league} rugby league.',
         L('cornish-pirates','Cornish Pirates') + ' are the best-known senior club. Community clubs include ' + ', '.join([L('redruth-rfc','Redruth'),L('camborne-rfc','Camborne'),L('truro-rfc','Truro'),L('launceston-rfc','Launceston'),L('st-austell-rfc','St Austell'),L('falmouth-rfc','Falmouth'),L('newquay-hornets-rfc','Newquay Hornets')]) + ', with ' + L('cornwall-rlfc','Cornwall RLFC') + ' flying the flag for rugby league.',
         'Next door, see <a href="rugby-clubs-devon.html">rugby clubs in Devon</a>, or the <a href="south-west-rugby-clubs.html">South West overview</a>.'],
  faqs=[('Is there rugby league in Cornwall?', 'Yes, <a href="club/cornwall-rlfc.html">Cornwall RLFC</a> is listed in our directory, although most Cornish clubs play rugby union.')]),
 dict(slug='rugby-clubs-west-midlands', place='the West Midlands', counties=['West Midlands'],
  title='Rugby Clubs in the West Midlands | Birmingham, Coventry &amp; Solihull',
  meta='Find rugby clubs in the West Midlands: {n} clubs in Birmingham, Coventry, Solihull, Wolverhampton, Stourbridge and Sutton Coldfield. Find one near you.',
  keywords='rugby clubs West Midlands, Birmingham rugby, Coventry rugby, Solihull rugby, Wolverhampton rugby, Sutton Coldfield rugby',
  intro=['This page lists the {n} clubs in our directory across the West Midlands county — Birmingham, Coventry, Solihull, Wolverhampton and the Black Country.',
         'Clubs include ' + ', '.join([L('coventry-rfc','Coventry'),L('moseley-rugby-club','Moseley'),L('birmingham-solihull-rfc','Birmingham &amp; Solihull'),L('broadstreet-rfc','Broadstreet'),L('sutton-coldfield-rfc','Sutton Coldfield'),L('stourbridge-rfc','Stourbridge'),L('wolverhampton-rfc','Wolverhampton')]) + '. ' + L('midlands-hurricanes','Midlands Hurricanes') + ' play rugby league.',
         'For the city alone see <a href="rugby-clubs-birmingham.html">Birmingham rugby clubs</a>, and for the surrounding county <a href="rugby-clubs-warwickshire.html">Warwickshire</a>.'],
  faqs=[('Which rugby clubs are in Coventry?', 'Our directory lists <a href="club/coventry-rfc.html">Coventry RFC</a>, <a href="club/broadstreet-rfc.html">Broadstreet RFC</a> and <a href="club/midlands-hurricanes.html">Midlands Hurricanes</a> (rugby league) among others.')]),
 dict(slug='rugby-clubs-leicestershire', place='Leicestershire', counties=['Leicestershire'],
  title='Rugby Clubs in Leicestershire | Leicester, Loughborough &amp; Hinckley',
  meta='Find rugby clubs in Leicestershire: {n} clubs including Leicester Tigers, Loughborough, Hinckley, Market Harborough and Melton Mowbray. Find one near you.',
  keywords='rugby clubs Leicestershire, Leicester rugby, Leicester Tigers, Loughborough rugby, Hinckley rugby, Market Harborough rugby',
  intro=['Leicestershire is one of English rugby union\'s heartlands. This page lists the {n} Leicestershire clubs in our directory.',
         L('leicester-tigers','Leicester Tigers') + ' (and ' + L('leicester-tigers-women','Leicester Tigers Women') + ') are the best-known club, alongside ' + L('loughborough-lightning','Loughborough Lightning') + '. Community clubs include ' + ', '.join([L('hinckley-rfc','Hinckley'),L('loughborough-rfc','Loughborough'),L('lutterworth-rfc','Lutterworth'),L('market-harborough-rfc','Market Harborough'),L('melton-mowbray-rfc','Melton Mowbray'),L('wigston-rfc','Wigston')]) + '.'],
  faqs=[('Where do Leicester Tigers play?', 'See the <a href="club/leicester-tigers.html">Leicester Tigers club page</a> for ground and contact details.')]),
 dict(slug='rugby-clubs-oxfordshire', place='Oxfordshire', counties=['Oxfordshire'],
  title='Rugby Clubs in Oxfordshire | Oxford, Banbury, Henley &amp; Chinnor',
  meta='Find rugby clubs in Oxfordshire: {n} clubs in Oxford, Banbury, Bicester, Chinnor, Henley and Chipping Norton. Compare clubs and find one near you.',
  keywords='rugby clubs Oxfordshire, Oxford rugby club, Banbury rugby, Chinnor rugby, Henley rugby, Bicester rugby',
  intro=['This page lists the {n} Oxfordshire clubs in our directory — rugby union and rugby league — across Oxford, Banbury, Bicester, Chinnor, Henley and Chipping Norton.',
         'Clubs include ' + ', '.join([L('oxford-quins','Oxford Quins'),L('oxford-rfc','Oxford'),L('banbury-rfc','Banbury'),L('bicester-rfc','Bicester'),L('chinnor-rfc','Chinnor'),L('henley-rfc','Henley'),L('chipping-norton-rfc','Chipping Norton')]) + ', plus ' + L('oxford-rlfc','Oxford RLFC') + ' for rugby league.'],
  faqs=[('Is there rugby league in Oxfordshire?', 'Yes, <a href="club/oxford-rlfc.html">Oxford RLFC</a> is listed in our directory, alongside several rugby union clubs.')]),
 dict(slug='rugby-clubs-scottish-borders', place='the Scottish Borders', counties=['Roxburghshire', 'Berwickshire', 'Selkirkshire'],
  title='Rugby Clubs in the Scottish Borders | Hawick, Melrose, Gala &amp; Kelso',
  meta='Find rugby clubs in the Scottish Borders: {n} clubs including Hawick, Melrose, Gala, Kelso, Selkirk, Jed-Forest and Jedburgh. Find one near you.',
  keywords='rugby clubs Scottish Borders, Borders rugby, Hawick rugby, Melrose rugby, Gala rugby, Kelso rugby, Selkirk rugby',
  intro=['The Scottish Borders is one of the best-known rugby areas in Britain. This page lists the {n} Borders clubs in our directory.',
         'Clubs include ' + ', '.join([L('hawick-rfc','Hawick'),L('melrose-rfc','Melrose'),L('gala-rfc','Gala'),L('kelso-rfc','Kelso'),L('selkirk-rfc','Selkirk'),L('jed-forest-rfc','Jed-Forest'),L('jedburgh-rfc','Jedburgh'),L('coldstream-rfc','Coldstream'),L('eyemouth-rfc','Eyemouth')]) + '. Melrose is also the home of the sevens game, first played there in 1883.',
         'For the capital, see <a href="rugby-clubs-edinburgh.html">rugby clubs in Edinburgh</a>, or browse <a href="rugby-union.html?region=scotland">all Scottish clubs</a>.'],
  faqs=[('Where was rugby sevens invented?', 'Rugby sevens began in Melrose in 1883, and the <a href="club/melrose-rfc.html">Melrose club</a> is still based there.')]),
 dict(slug='rugby-clubs-carmarthenshire', place='Carmarthenshire', counties=['Carmarthenshire'],
  title='Rugby Clubs in Carmarthenshire | Llanelli, Carmarthen &amp; Llandovery',
  meta='Find rugby clubs in Carmarthenshire: {n} clubs including Scarlets, Llanelli, Carmarthen Quins, Llandovery and Ammanford. Find one near you.',
  keywords='rugby clubs Carmarthenshire, Llanelli rugby, Scarlets, Carmarthen Quins, Llandovery rugby, Ammanford rugby',
  intro=['Carmarthenshire is a West Wales rugby heartland. This page lists the {n} clubs in our directory across Llanelli, Carmarthen, Llandovery and Ammanford.',
         L('scarlets','Scarlets') + ' are the region\'s professional side, with community clubs such as ' + ', '.join([L('llanelli-rfc','Llanelli'),L('carmarthen-quins-rfc','Carmarthen Quins'),L('llandovery-rfc','Llandovery'),L('amman-united-rfc','Amman United'),L('tycroes-rfc','Tycroes'),L('tumble-rfc','Tumble'),L('brynamman-rfc','Brynamman')]) + ', and ' + L('west-wales-raiders','West Wales Raiders') + ' for rugby league.',
         'For the capital see <a href="rugby-clubs-cardiff.html">Cardiff rugby clubs</a>, or browse <a href="rugby-union.html?region=wales">all Welsh clubs</a>.'],
  faqs=[('Is there rugby league in West Wales?', 'Yes, <a href="club/west-wales-raiders.html">West Wales Raiders</a> are listed in our directory, though most local clubs play rugby union.')]),
]

def build_new_hubs():
    clubs = [c for c in json.load(open(os.path.join(ROOT, 'tools', 'clubs.json'))) if c['type'] == 'SportsTeam']
    cards = bh.load_cards()
    parts = bh.shell()
    existing = [('rugby-clubs-surrey', 'Surrey'), ('rugby-clubs-essex', 'Essex'), ('south-west-rugby-clubs', 'South West'),
                ('rugby-clubs-bristol', 'Bristol'), ('rugby-clubs-birmingham', 'Birmingham'), ('rugby-clubs-cardiff', 'Cardiff'),
                ('rugby-clubs-leeds', 'Leeds'), ('rugby-clubs-hull', 'Hull')]
    new = [(h['slug'], h['place'].replace('the ', '')) for h in NEW_HUBS]
    for hub in NEW_HUBS:
        # fail loudly if a hand-linked club page does not exist
        for slug in re.findall(r'club/([a-z0-9-]+)\.html', ' '.join(hub['intro'] + [a for _, a in hub['faqs']])):
            assert os.path.exists(os.path.join(ROOT, 'club', slug + '.html')), (hub['slug'], slug)
        print(hub['slug'], bh.build(hub, clubs, cards, existing + new, parts))
    # one internal link from each club page to its new hub (idempotent)
    linked = 0
    for hub in NEW_HUBS:
        label = hub['place']
        link = (f'<p style="margin-top:.5rem"><a href="../{hub["slug"]}.html" style="color:var(--red);font-weight:600">'
                f'Rugby clubs in {html.escape(label)} →</a></p>')
        for c in clubs:
            if c['county'] not in hub['counties']:
                continue
            path = os.path.join(ROOT, 'club', c['slug'] + '.html')
            s = open(path, encoding='utf-8', errors='surrogateescape').read()
            if f'../{hub["slug"]}.html' in s:
                continue
            m = re.search(r'(<a href="\.\./clubs\.html\?q=[^"]*"[^>]*>Search [^<]*</a></p>)', s)
            if not m:
                continue
            s = s[:m.end()] + link + s[m.end():]
            open(path, 'w', encoding='utf-8', errors='surrogateescape').write(s)
            linked += 1
    print('club pages linked to a new hub:', linked)

# --------------------------------------------------------------------------- generic page
def page(slug, title, meta, h1, lede, body, crumb, ld_type='WebPage', extra_ld=None):
    head_tail, header, footer = bh.shell()
    url = f'{SITE}/{slug}.html'
    graph = [{"@type": ld_type, "@id": url + '#page', "name": h1, "description": meta, "url": url, "inLanguage": "en-GB",
              "isPartOf": {"@type": "WebSite", "name": "UK Rugby Club Directory", "url": SITE + '/'}},
             {"@type": "BreadcrumbList", "itemListElement": [
                 {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + '/'},
                 {"@type": "ListItem", "position": 2, "name": crumb, "item": url}]}] + (extra_ld or [])
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    m = html.escape(meta, quote=True)
    return f'''<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{m}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{m}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/imgs/home-hero.jpg">
<meta property="og:site_name" content="UK Rugby Club Directory">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{m}">
<meta name="theme-color" content="#293241">
{head_tail}<script type="application/ld+json">{ld}</script>
{header}<main id="main">
<section class="listing-hero-england" style="position:relative;min-height:200px;display:flex;align-items:stretch;overflow:hidden;border-bottom:none">
  <div class="lh-left" style="position:relative;z-index:2;flex:0 0 62%;background:var(--navy);clip-path:polygon(0 0,82% 0,100% 100%,0 100%);padding:2.25rem 5rem 2.25rem 2rem;display:flex;flex-direction:column;justify-content:center">
    <nav class="breadcrumb" style="margin-bottom:.6rem"><a href="index.html">Home</a><span class="bc-sep">›</span><span class="bc-cur">{html.escape(crumb)}</span></nav>
    <span class="lh-eyebrow" style="font-family:Oswald,sans-serif;font-size:.65rem;font-weight:600;letter-spacing:.14em;text-transform:uppercase;margin-bottom:.5rem;display:block">UK Rugby Club Directory</span>
    <h1 style="font-family:Oswald,sans-serif;font-size:clamp(1.6rem,3.6vw,2.4rem);font-weight:700;color:#fff;letter-spacing:.03em;text-transform:uppercase;margin:0 0 .5rem;line-height:1.05">{h1}</h1>
    <p style="font-size:.9rem;color:rgba(255,255,255,.82);line-height:1.55;max-width:460px;margin:0">{lede}</p>
  </div>
  <div class="lh-right lh-pattern" aria-hidden="true" style="position:absolute;right:0;top:0;bottom:0;width:38%"></div>
</section>
<section class="sec"><div class="con"><div style="max-width:880px;margin:0 auto">
{body}
</div></div></section>
{footer}'''

def write(slug, s):
    open(os.path.join(ROOT, slug + '.html'), 'w', encoding='utf-8').write(s)

# --------------------------------------------------------------------------- data
def hub_list():
    out = []
    seen = {}
    for slug, label in ([(h['slug'], h['place']) for h in bh.HUBS] + [(h['slug'], h['place']) for h in NEW_HUBS] +
            [('rugby-clubs-surrey', 'Surrey'), ('rugby-clubs-essex', 'Essex'), ('south-west-rugby-clubs', 'the South West'),
             ('rugby-clubs-bristol', 'Bristol'), ('rugby-clubs-birmingham', 'Birmingham'), ('rugby-clubs-cardiff', 'Cardiff'),
             ('rugby-clubs-leeds', 'Leeds'), ('rugby-clubs-hull', 'Hull')]):
        if slug in seen:
            continue
        seen[slug] = 1
        p = os.path.join(ROOT, slug + '.html')
        n = None
        if os.path.exists(p):
            m = re.search(r'"numberOfItems":\s*(\d+)', open(p, encoding='utf-8').read())
            n = int(m.group(1)) if m else None
        out.append((slug, label, n))
    return sorted(out, key=lambda x: x[1].replace('the ', ''))

WALES = {'Anglesey','Blaenau Gwent','Bridgend','Caerphilly','Carmarthenshire','Ceredigion','Conwy','Denbighshire','Gwynedd','Merthyr Tydfil','Monmouthshire','Neath Port Talbot','Pembrokeshire','Powys','Rhondda Cynon Taf','Swansea','Torfaen','South Glamorgan','West Glamorgan','Wrexham'}
SCOT = {'Aberdeenshire','Angus','Ayrshire','Berwickshire','Clackmannanshire','Dumfriesshire','East Lothian','Fife','Inverness-shire','Lanarkshire','Midlothian','Morayshire','Peeblesshire','Perthshire','Roxburghshire','Selkirkshire','Stirlingshire','West Lothian'}
NI = {'County Antrim','County Armagh','County Tyrone','County Down'}
OTHER = {'Haute-Garonne','Pyrénées-Orientales','Jersey',''}

def nation(c):
    if c in WALES: return 'Wales'
    if c in SCOT: return 'Scotland'
    if c in NI: return 'Northern Ireland'
    if c in OTHER: return 'Elsewhere (France, Jersey)'
    return 'England'

def stats():
    d = [c for c in json.load(open(os.path.join(ROOT, 'tools', 'clubs.json'))) if c['type'] == 'SportsTeam']
    tot = len(d)
    league = sum('league' in c['sport'].lower() for c in d)
    union = sum('union' in c['sport'].lower() for c in d)
    nat = collections.Counter(nation(c['county']) for c in d)
    natcode = collections.defaultdict(lambda: [0, 0])
    for c in d:
        natcode[nation(c['county'])][0 if 'union' in c['sport'].lower() else 1] += 1
    counties = collections.Counter(c['county'] for c in d if c['county'] and c['county'] not in OTHER)
    return dict(total=tot, league=league, union=union, nat=nat, natcode=natcode, counties=counties,
                tel=sum(c['has_tel'] for c in d), mail=sum(c['has_mail'] for c in d))

# --------------------------------------------------------------------------- badges
def badges():
    for name, bg, fg, uk, sub in [('light', '#ffffff', '#293241', '#ee6c4d', '#3d5a80'), ('dark', '#293241', '#ffffff', '#ee6c4d', '#98c1d9')]:
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 56" width="200" height="56" role="img" aria-label="Listed on the UK Rugby Club Directory">
<title>Listed on the UK Rugby Club Directory</title>
<rect x="1" y="1" width="198" height="54" rx="8" fill="{bg}" stroke="#293241" stroke-width="2"/>
<text x="14" y="22" font-family="Arial,Helvetica,sans-serif" font-size="9" font-weight="700" fill="{sub}" letter-spacing="1.5">LISTED ON THE</text>
<text x="14" y="44" font-family="Arial,Helvetica,sans-serif" font-size="12" font-weight="700" fill="{uk}" letter-spacing="1.5">UK</text>
<rect x="36" y="29" width="1.5" height="19" rx=".75" fill="{fg}"/>
<text x="44" y="39" font-family="Arial,Helvetica,sans-serif" font-size="12.5" font-weight="700" fill="{fg}">Rugby Club Directory</text>
</svg>
'''
        open(os.path.join(ROOT, 'badges', f'ukrcd-badge-{name}.svg'), 'w', encoding='utf-8').write(svg)

# --------------------------------------------------------------------------- pages
def by_area():
    hubs = hub_list()
    rows = ''.join(f'<li style="padding:.45rem 0;border-bottom:1px solid #e3e8ef"><a href="{s}.html" style="font-weight:600">Rugby clubs in {html.escape(l)}</a>'
                   + (f' <span style="color:var(--text-secondary);font-size:.88rem">— {n} clubs</span>' if n else '') + '</li>' for s, l, n in hubs)
    body = f'''<p {P}>Every area guide in the directory in one place. Each guide lists the clubs in that area by town, with both rugby union and rugby league where both are played.</p>
<h2 {H2} id="areas">Area guides</h2>
<ul style="list-style:none;padding:0;margin:0 0 1.5rem">{rows}</ul>
<h2 {H2}>Browse by region</h2>
<p {P}>For areas without their own guide yet, use the regional listings: <a href="rugby-union.html?region=wales">Wales</a>, <a href="rugby-union.html?region=scotland">Scotland</a>, <a href="rugby-union.html?region=northern-ireland">Northern Ireland</a>, <a href="rugby-union.html?region=midlands">the Midlands</a>, <a href="rugby-union.html?region=north-east">the North East</a>, <a href="rugby-union.html?region=yorkshire">Yorkshire</a> and <a href="rugby-league.html">all rugby league clubs</a>.</p>
<p {P}>Also see our guides to <a href="womens-rugby-clubs.html">women's rugby</a>, <a href="junior-youth-rugby-clubs.html">junior and youth rugby</a>, <a href="school-university-rugby.html">school and university rugby</a> and <a href="rugby-leagues-uk.html">the UK rugby leagues</a>.</p>
<p {P}>Running a club, council or community website? See <a href="link-to-us.html">how to link to the directory</a>.</p>'''
    write('rugby-clubs-by-area', page('rugby-clubs-by-area', 'Rugby Clubs by Area | County &amp; City Guides | UK Rugby Club Directory',
        f'Browse rugby clubs by area: {len(hubs)} county, city and regional guides covering union and league clubs across England, Scotland and Wales.',
        'Rugby Clubs by Area', 'Every county, city and regional rugby guide in one place.', body, 'Rugby Clubs by Area', 'CollectionPage'))

def link_to_us():
    hubs = hub_list()
    hub_rows = ''.join(f'<tr><td {TD}>{html.escape(l.replace("the ", "").title() if l.startswith("the ") else l)}</td><td {TD}><code {CODE}>&lt;a href="{SITE}/{s}.html"&gt;Rugby clubs in {html.escape(l)}&lt;/a&gt;</code></td></tr>' for s, l, n in hubs)
    snippet_text = f'<a href="{SITE}/">UK Rugby Club Directory</a>'
    snippet_badge = f'<a href="{SITE}/" rel="noopener"><img src="{SITE}/badges/ukrcd-badge-light.svg" alt="Listed on the UK Rugby Club Directory" width="200" height="56"></a>'
    snippet_club = f'<a href="{SITE}/club/YOUR-CLUB-SLUG.html" rel="noopener"><img src="{SITE}/badges/ukrcd-badge-dark.svg" alt="Listed on the UK Rugby Club Directory" width="200" height="56"></a>'
    e = html.escape
    body = f'''<p {P}>The UK Rugby Club Directory is a free listing of rugby union and rugby league clubs across the UK. If you run a club, a county body, a council or community website, a school or university, or a rugby blog, you are welcome to link to it. This page has ready-to-use links and badges.</p>
<h2 {H2}>Which page should I link to?</h2>
<table style="width:100%;border-collapse:collapse;margin-bottom:1.5rem"><thead><tr><th {TH}>If you are…</th><th {TH}>Link to…</th></tr></thead><tbody>
<tr><td {TD}>A rugby club</td><td {TD}>Your own club page (find it via <a href="clubs.html">All Clubs</a>) — not listed yet? <a href="register.html">Register free</a>, or <a href="claim.html">claim and update</a> your listing.</td></tr>
<tr><td {TD}>A county or regional rugby body, or a local authority</td><td {TD}>The <a href="rugby-clubs-by-area.html">area guide</a> for your county or city (table below).</td></tr>
<tr><td {TD}>A school, college or university</td><td {TD}><a href="school-university-rugby.html">School and university rugby</a>, <a href="junior-youth-rugby-clubs.html">junior and youth clubs</a> or <a href="womens-rugby-clubs.html">women's clubs</a>.</td></tr>
<tr><td {TD}>A blogger, journalist or forum moderator</td><td {TD}><a href="rugby-leagues-uk.html">UK rugby leagues</a>, <a href="rugby-union-league-structure.html">union league structure</a> or <a href="rugby-club-statistics.html">club statistics</a>.</td></tr>
<tr><td {TD}>Replacing a dead link to a club website</td><td {TD}>The club's page here, which links onward to its official website and England Rugby (or the national body) where we hold the details.</td></tr>
</tbody></table>
<h2 {H2}>Simple text link</h2>
<p {P}>Click the box to select it, then copy and paste.</p>
<code {CODE}>{e(snippet_text)}</code>
<h2 {H2}>Badge for your website</h2>
<p {P}><img src="badges/ukrcd-badge-light.svg" alt="Listed on the UK Rugby Club Directory" width="200" height="56" style="margin-right:1rem;vertical-align:middle"> <span style="display:inline-block;background:#293241;padding:.3rem;border-radius:10px;vertical-align:middle"><img src="badges/ukrcd-badge-dark.svg" alt="Listed on the UK Rugby Club Directory (dark version)" width="200" height="56"></span></p>
<h3 {H3}>Link to the directory</h3>
<code {CODE}>{e(snippet_badge)}</code>
<h3 {H3}>Link to your club's own page</h3>
<p {P}>Replace <strong>YOUR-CLUB-SLUG</strong> with the end of your club page address, for example <code>harlequins</code> for <code>{SITE}/club/harlequins.html</code>. Use the dark badge on dark backgrounds.</p>
<code {CODE}>{e(snippet_club)}</code>
<h2 {H2}>Links to area guides</h2>
<table style="width:100%;border-collapse:collapse;margin-bottom:1.5rem"><thead><tr><th {TH}>Area</th><th {TH}>HTML</th></tr></thead><tbody>{hub_rows}</tbody></table>
<h2 {H2}>Quoting or citing us</h2>
<p {P}>Please link to the page you used. Our <a href="about.html">editorial standards</a> explain where club details come from and how we check them, and our <a href="press.html">media page</a> has key figures and a suggested citation.</p>
<h2 {H2}>Spotted a mistake?</h2>
<p {P}>Tell us through <a href="contact-us.html">the contact page</a> and we will correct it. Club officials can also <a href="claim.html">claim their listing</a> to keep details up to date.</p>'''
    write('link-to-us', page('link-to-us', 'Link to Us | Badges &amp; Link Snippets | UK Rugby Club Directory',
        'Link to the UK Rugby Club Directory: copy-and-paste links, badges for club websites and ready-made links to every county and city rugby guide.',
        'Link to the Directory', 'Copy-and-paste links and badges for clubs, councils, schools and rugby websites.', body, 'Link to Us'))

def statistics():
    s = stats()
    nat_rows = ''.join(f'<tr><td {TD}>{n}</td><td {TD}>{s["natcode"][n][0]}</td><td {TD}>{s["natcode"][n][1]}</td><td {TD}><strong>{s["nat"][n]}</strong></td></tr>'
                       for n in ['England', 'Wales', 'Scotland', 'Northern Ireland', 'Elsewhere (France, Jersey)'] if s['nat'][n])
    county_rows = ''.join(f'<tr><td {TD}>{i}</td><td {TD}>{html.escape(c)}</td><td {TD}><strong>{n}</strong></td></tr>' for i, (c, n) in enumerate(s['counties'].most_common(15), 1))
    t, u, l = s['total'], s['union'], s['league']
    body = f'''<p {P}>These figures are counted from the club profiles in the UK Rugby Club Directory as of {datetime.date.fromisoformat(TODAY).strftime("%-d %B %Y")}. They describe <strong>our listings</strong>, not every rugby club in the UK: some clubs are not listed yet.</p>
<h2 {H2}>Key figures</h2>
<ul style="line-height:1.9;font-size:.97rem;margin:0 0 1rem 1.2rem">
<li><strong>{t}</strong> rugby club and team profiles</li>
<li><strong>{u}</strong> rugby union and <strong>{l}</strong> rugby league profiles</li>
<li><strong>{len(s["counties"])}</strong> counties and areas represented across England, Wales, Scotland and Northern Ireland</li>
</ul>
<h2 {H2}>Club profiles by nation and code</h2>
<table style="width:100%;border-collapse:collapse;margin-bottom:1.5rem"><thead><tr><th {TH}>Nation</th><th {TH}>Union</th><th {TH}>League</th><th {TH}>Total</th></tr></thead><tbody>{nat_rows}</tbody></table>
<h2 {H2}>Counties with the most listed clubs</h2>
<table style="width:100%;border-collapse:collapse;margin-bottom:1.5rem"><thead><tr><th {TH}>#</th><th {TH}>County</th><th {TH}>Listed clubs</th></tr></thead><tbody>{county_rows}</tbody></table>
<p {P}>West Yorkshire stands out because of its dense rugby league network; see the <a href="rugby-clubs-west-yorkshire.html">West Yorkshire guide</a>. Every area has its own guide in our <a href="rugby-clubs-by-area.html">area index</a>.</p>
<h2 {H2}>Method and caveats</h2>
<ul style="line-height:1.8;font-size:.95rem;margin:0 0 1rem 1.2rem">
<li>Counts come from the county, town and code recorded on each club profile. County is the county recorded on the profile, which may differ from historic or governing-body areas.</li>
<li>Rugby businesses, media and equipment suppliers are excluded.</li>
<li>Figures change as clubs are added or corrected. Check the date above before quoting them.</li>
</ul>
<p {P}>Quoting these figures? See the <a href="press.html">media page</a> for a suggested citation, or <a href="link-to-us.html">how to link to us</a>.</p>'''
    write('rugby-club-statistics', page('rugby-club-statistics', 'UK Rugby Club Statistics | Clubs by Nation, Code &amp; County',
        f'UK rugby club statistics from the directory: {t} club profiles ({u} union, {l} league) by nation, code and county, with method notes.',
        'UK Rugby Club Statistics', 'How many rugby clubs are listed, by nation, code and county.', body, 'Rugby Club Statistics'))
    return s

def press(s):
    cite = f'UK Rugby Club Directory, "Rugby Club Statistics", {SITE}/rugby-club-statistics.html (accessed [date]).'
    body = f'''<p {P}>For journalists, bloggers, researchers and organisations writing about grassroots rugby in the UK.</p>
<h2 {H2}>About the directory</h2>
<p {P}>The UK Rugby Club Directory is a free online directory of rugby union and rugby league clubs across England, Scotland, Wales and Northern Ireland. It currently holds {s["total"]} club profiles ({s["union"]} union, {s["league"]} league), each with its own page, plus area guides, league guides and advice for people looking for a club to join.</p>
<h2 {H2}>Useful pages</h2>
<ul style="line-height:1.9;font-size:.97rem;margin:0 0 1rem 1.2rem">
<li><a href="rugby-club-statistics.html">Rugby club statistics</a> — clubs by nation, code and county</li>
<li><a href="rugby-leagues-uk.html">UK rugby leagues guide</a> and <a href="rugby-union-league-structure.html">union league structure</a></li>
<li><a href="rugby-clubs-by-area.html">Area guides</a> for counties and cities</li>
<li><a href="womens-rugby-clubs.html">Women's rugby clubs</a>, <a href="junior-youth-rugby-clubs.html">junior and youth rugby</a> and <a href="school-university-rugby.html">school and university rugby</a></li>
<li><a href="blog/how-to-find-a-rugby-club-near-you/">How to find a rugby club near you</a> and <a href="blog/how-to-start-playing-rugby-as-an-adult-uk-guide/">how to start playing rugby as an adult</a></li>
<li><a href="about.html">Editorial standards</a> — where our information comes from and how it is checked</li>
</ul>
<h2 {H2}>Suggested citation</h2>
<code {CODE}>{html.escape(cite)}</code>
<h2 {H2}>Contact</h2>
<p {P}>Questions, corrections or requests for comment: <a href="mailto:hello@ukrugbyclubdirectory.co.uk">hello@ukrugbyclubdirectory.co.uk</a> or the <a href="contact-us.html">contact page</a>. If you quote our figures, please link to the page you used — see <a href="link-to-us.html">how to link to us</a>.</p>'''
    write('press', page('press', 'Media &amp; Data | Quoting the UK Rugby Club Directory',
        'Media information for the UK Rugby Club Directory: about the directory, key figures, useful pages, a suggested citation and how to get in touch.',
        'Media &amp; Data', 'About the directory, key figures and how to cite us.', body, 'Media &amp; Data'))

def schools():
    body = f'''<p {P}>Rugby is often a player's first contact with the game at school or university, and a local club is where most people carry on afterwards. This page explains how to connect the three and where to find official information for each nation.</p>
<h2 {H2}>From school to club</h2>
<p {P}>Many clubs run mini and junior sections that players move through before reaching senior rugby, and some have links with local schools. Our <a href="junior-youth-rugby-clubs.html">junior and youth rugby guide</a> explains age groups and how to find a club with a youth section. Girls and women can also look at our <a href="womens-rugby-clubs.html">women's rugby guide</a>.</p>
<h2 {H2}>University rugby</h2>
<p {P}>Most universities run their own rugby clubs, and university sport in the UK is organised through <a href="https://www.bucs.org.uk" target="_blank" rel="noopener">BUCS</a>. Playing at university does not stop you joining a town club in the same city, and many players do both. Browse clubs in university cities through our guides to <a href="rugby-clubs-leeds.html">Leeds</a>, <a href="rugby-clubs-bristol.html">Bristol</a>, <a href="rugby-clubs-birmingham.html">Birmingham</a>, <a href="rugby-clubs-cardiff.html">Cardiff</a>, <a href="rugby-clubs-edinburgh.html">Edinburgh</a>, <a href="rugby-clubs-leicestershire.html">Leicestershire</a> (including Loughborough) and <a href="rugby-clubs-oxfordshire.html">Oxfordshire</a>.</p>
<h2 {H2}>After university</h2>
<p {P}>Moving to a new town for work is the most common time people look for a club. Use the <a href="rugby-clubs-by-area.html">area guides</a> to see what is near you, then contact two or three clubs and ask about the next training session. Our <a href="blog/how-to-find-a-rugby-club-near-you/">guide to finding a club</a> covers what to ask.</p>
<h2 {H2}>Official information</h2>
<ul style="line-height:1.9;font-size:.97rem;margin:0 0 1rem 1.2rem">
<li><a href="https://www.englandrugby.com" target="_blank" rel="noopener">England Rugby</a> — rugby union in England</li>
<li><a href="https://www.wru.wales" target="_blank" rel="noopener">Welsh Rugby Union</a></li>
<li><a href="https://www.scottishrugby.org" target="_blank" rel="noopener">Scottish Rugby</a></li>
<li><a href="https://www.irfu.ie" target="_blank" rel="noopener">IRFU</a> — Ireland, including Ulster</li>
<li><a href="https://www.rugby-league.com" target="_blank" rel="noopener">Rugby Football League</a> — rugby league in England</li>
<li><a href="https://www.bucs.org.uk" target="_blank" rel="noopener">BUCS</a> — university sport</li>
</ul>
<h2 {H2}>Teachers and student unions</h2>
<p {P}>You are welcome to link to this page or to your local <a href="rugby-clubs-by-area.html">area guide</a> from school or students' union pages. See <a href="link-to-us.html">how to link to us</a>.</p>'''
    write('school-university-rugby', page('school-university-rugby', 'School &amp; University Rugby | From Pitch to Club | UK Rugby Club Directory',
        'How to move from school and university rugby into a local club: junior sections, university cities, and official links for England, Wales, Scotland and Ireland.',
        'School &amp; University Rugby', 'How to go from school and university rugby to a local club.', body, 'School &amp; University Rugby'))

# --------------------------------------------------------------------------- sitemap / redirects
def sitemap_and_redirects():
    new = [h['slug'] for h in NEW_HUBS] + ['rugby-clubs-by-area', 'link-to-us', 'rugby-club-statistics', 'press', 'school-university-rugby']
    sm = open(os.path.join(ROOT, 'sitemap.xml'), encoding='utf-8').read()
    add = ''
    for slug in new:
        if f'/{slug}.html</loc>' not in sm:
            pr = '0.8' if slug.startswith('rugby-clubs-') or slug == 'rugby-club-statistics' else '0.6'
            add += f'  <url><loc>{SITE}/{slug}.html</loc><lastmod>{TODAY}</lastmod><changefreq>weekly</changefreq><priority>{pr}</priority></url>\n'
    if add:
        sm = sm.replace('</urlset>', add + '</urlset>')
        open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8').write(sm)
    rd = open(os.path.join(ROOT, '_redirects'), encoding='utf-8').read()
    radd = ''
    for slug in new:
        if f'/{slug} ' not in rd:
            radd += f'/{slug}            /{slug}.html   301!\n/{slug}/           /{slug}.html   301!\n'
    for h in NEW_HUBS:
        key = '/county/' + h['slug'].replace('rugby-clubs-', '')
        if key + ' ' not in rd:
            radd += f'{key}  /{h["slug"]}.html  301!\n'
    if radd:
        open(os.path.join(ROOT, '_redirects'), 'w', encoding='utf-8').write(rd.rstrip('\n') + '\n\n# ─── Backlink-readiness pages (Nov 2026) ───\n' + radd)
    print('sitemap/_redirects updated:', bool(add), bool(radd))

def main():
    build_new_hubs()
    badges()
    by_area()
    link_to_us()
    press(statistics())
    schools()
    sitemap_and_redirects()

if __name__ == '__main__':
    main()
