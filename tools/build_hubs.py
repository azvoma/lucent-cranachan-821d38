#!/usr/bin/env python3
"""
Build county / regional hub pages for ukrugbyclubdirectory.co.uk.

Run from the repo root:  python3 tools/extract_clubs.py && python3 tools/build_hubs.py

Each hub has a hand-written introduction (HUBS below) and a club list built from
the live club pages, so the lists stay in sync when clubs are added. The page
shell (head, header, footer) is copied from rugby-clubs-surrey.html so hubs
always match the rest of the site.
"""
import html, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://ukrugbyclubdirectory.co.uk'

P = 'style="font-size:.97rem;color:var(--text-secondary);line-height:1.75;margin-bottom:.9rem"'
H2 = 'style="font-size:1.6rem;font-weight:700;color:var(--text-primary);margin:2.25rem 0 1rem;letter-spacing:-.02em"'

HUBS = [
    dict(slug='rugby-clubs-london', place='London', counties=['Greater London'],
         title='Rugby Clubs in London | Union &amp; League Clubs by Area',
         meta='Find rugby clubs in London: {n} union and league clubs across the capital, from Harlequins and Saracens to community sides in Barnes, Wimbledon and Woodford.',
         keywords='rugby clubs in London, London rugby clubs, rugby union London, rugby league London, rugby near me London',
         intro=[
             'London has more rugby than anywhere else in the UK, from Premiership giants to Saturday-afternoon community sides. This page lists the {n} London clubs in our directory, grouped by area so you can find one you can actually get to on a weeknight.',
             'At the top of the game, <a href="club/harlequins.html">Harlequins</a> play at the Twickenham Stoop and <a href="club/saracens.html">Saracens</a> in north London, and both run women\'s sides too. Below them sit long-established clubs such as <a href="club/blackheath-fc.html">Blackheath</a> and <a href="club/rosslyn-park-fc.html">Rosslyn Park</a>, and a large network of community clubs across every borough. The capital\'s rugby league is led by <a href="club/london-broncos.html">London Broncos</a>, with <a href="club/london-skolars.html">London Skolars</a> in the north of the city.',
             'Travel matters more in London than anywhere else. Most players pick a club near home or work rather than the "best" club, so use the town list below to narrow things down first.'],
         faqs=[('Are there rugby league clubs in London?', 'Yes. <a href="club/london-broncos.html">London Broncos</a> are the capital\'s best-known rugby league club, and <a href="club/london-skolars.html">London Skolars</a> are based in north London. Most London clubs, however, play rugby union.'),
               ('Where are the professional rugby clubs in London?', '<a href="club/harlequins.html">Harlequins</a> play at the Twickenham Stoop in south-west London and <a href="club/saracens.html">Saracens</a> in north London. Both run community programmes alongside their professional teams.')]),
    dict(slug='rugby-clubs-manchester', place='Greater Manchester', counties=['Greater Manchester'],
         title='Rugby Clubs in Manchester | Union &amp; League in Greater Manchester',
         meta='Find rugby clubs in Greater Manchester: {n} rugby league and union clubs in Wigan, Leigh, Salford, Oldham, Stockport and more. Compare clubs near you.',
         keywords='rugby clubs Manchester, rugby clubs Greater Manchester, rugby league Wigan, rugby league Leigh, rugby union Manchester',
         intro=[
             'Greater Manchester is one of the few places in the UK where both codes are equally at home. This page brings together the {n} Greater Manchester clubs in our directory — {league} rugby league and {union} rugby union.',
             'Rugby league runs deep in towns such as Wigan, Leigh, Oldham, Rochdale and Swinton, where professional clubs like <a href="club/wigan-warriors.html">Wigan Warriors</a> and <a href="club/leigh-leopards.html">Leigh Leopards</a> sit above a strong amateur game. Rugby union is led by <a href="club/sale-sharks.html">Sale Sharks</a>, who play in Salford, with community clubs across Stockport, Bolton, Altrincham and south Manchester.',
             'If you are new to the area, decide on the code first: in Wigan or Leigh the nearest club is likely to be rugby league, while in the southern suburbs it is more likely to be union.'],
         faqs=[('Which code is more popular in Greater Manchester?', 'Both are well established. Rugby league is strongest in the western and northern towns such as Wigan, Leigh and Oldham, while rugby union clubs are spread more evenly, especially in the south of the county.')]),
    dict(slug='rugby-clubs-cumbria', place='Cumbria', counties=['Cumbria'],
         title='Rugby Clubs in Cumbria | Union &amp; League Clubs Near You',
         meta='Find rugby clubs in Cumbria: {n} union and league clubs from Carlisle and Kendal to Barrow, Whitehaven and Workington. Compare clubs and find one near you.',
         keywords='rugby clubs Cumbria, Cumbria rugby, rugby league Cumbria, Carlisle rugby club, Kendal rugby, Whitehaven rugby league',
         intro=[
             'Cumbria plays both codes, and which one you find depends on where you live. This page lists the {n} Cumbrian clubs in our directory — {league} rugby league and {union} rugby union.',
             'The west coast towns of Barrow, Whitehaven and Workington are rugby league country, with <a href="club/barrow-raiders.html">Barrow Raiders</a>, <a href="club/whitehaven-rlfc.html">Whitehaven</a> and <a href="club/workington-town-rlfc.html">Workington Town</a> backed by busy amateur clubs. Rugby union is strongest in Carlisle, Kendal, Penrith and the Lake District towns, where clubs such as <a href="club/kendal-rfc.html">Kendal</a> and <a href="club/keswick-rfc.html">Keswick</a> are at the heart of their communities.',
             'Distances are long in Cumbria, so many players choose a club by training night as much as by location.'],
         faqs=[('Where is rugby league played in Cumbria?', 'Mainly along the west coast: Barrow-in-Furness, Whitehaven, Workington and the surrounding towns all have professional or amateur rugby league clubs.')]),
    dict(slug='rugby-clubs-merseyside', place='Merseyside', counties=['Merseyside'],
         title='Rugby Clubs in Merseyside | St Helens, Liverpool &amp; Wirral',
         meta='Find rugby clubs in Merseyside: {n} league and union clubs in St Helens, Liverpool, Southport and the Wirral. Compare clubs and find one near you.',
         keywords='rugby clubs Merseyside, rugby clubs Liverpool, St Helens rugby league, Wirral rugby club, Southport rugby',
         intro=[
             'Merseyside is split between two rugby traditions. This page lists the {n} Merseyside clubs in our directory — {league} rugby league and {union} rugby union.',
             'St Helens is a rugby league town through and through: alongside the professional <a href="club/st-helens-rfc.html">St Helens</a> club there are amateur sides such as <a href="club/thatto-heath-crusaders.html">Thatto Heath Crusaders</a> and <a href="club/pilkington-recs.html">Pilkington Recs</a>. Rugby union is centred on Liverpool, Southport, Crosby and the Wirral, with clubs such as <a href="club/waterloo-rfc.html">Waterloo</a> and <a href="club/wirral-rfc.html">Wirral</a>.',
             'Use the town list below to see which code is closest to you.'],
         faqs=[('Is St Helens a rugby league or rugby union town?', 'Mainly rugby league. St Helens has a professional rugby league club and several amateur league sides, although there is also a rugby union club in the town.')]),
    dict(slug='rugby-clubs-kent', place='Kent', counties=['Kent'],
         title='Rugby Clubs in Kent | Find a Rugby Union Club in Kent',
         meta='Find rugby clubs in Kent: {n} rugby union clubs in Maidstone, Canterbury, Tonbridge, Sevenoaks, Ashford and more. Compare clubs and find one near you.',
         keywords='rugby clubs Kent, Kent rugby clubs, rugby union Kent, Maidstone rugby club, Canterbury rugby club, Tonbridge rugby',
         intro=[
             'Kent has a strong rugby union community, with a club in almost every large town. This page lists the {n} Kent clubs in our directory so you can compare them in one place.',
             'Clubs range from <a href="club/tonbridge-juddians-rfc.html">Tonbridge Juddians</a> and <a href="club/canterbury-rfc.html">Canterbury</a> to town sides in <a href="club/maidstone-rfc.html">Maidstone</a>, <a href="club/sevenoaks-rfc.html">Sevenoaks</a>, <a href="club/ashford-rfc.html">Ashford</a> and along the coast. Most run several senior teams plus large mini and junior sections.',
             'Clubs in north-west Kent, such as Dartford and Gravesend, are also within easy reach of south-east London clubs — see our <a href="rugby-clubs-london.html">London rugby clubs</a> page.'],
         faqs=[('Do Kent rugby clubs run junior sections?', 'Most do. Mini and junior rugby is a big part of community clubs in Kent — see our <a href="junior-youth-rugby-clubs.html">junior and youth rugby guide</a> for how the age groups work.')]),
    dict(slug='rugby-clubs-cheshire', place='Cheshire', counties=['Cheshire'],
         title='Rugby Clubs in Cheshire | Union &amp; League Clubs Near You',
         meta='Find rugby clubs in Cheshire: {n} union and league clubs in Chester, Warrington, Widnes, Macclesfield, Wilmslow and more. Compare clubs and find one near you.',
         keywords='rugby clubs Cheshire, Cheshire rugby, Chester rugby club, Warrington rugby league, Widnes rugby, Macclesfield rugby',
         intro=[
             'Cheshire offers both codes. This page lists the {n} Cheshire clubs in our directory — {league} rugby league and {union} rugby union.',
             'In the north of the county, Warrington and Widnes are rugby league strongholds, home to <a href="club/warrington-wolves.html">Warrington Wolves</a> and <a href="club/widnes-vikings.html">Widnes Vikings</a> and several amateur clubs. Elsewhere rugby union is the main game, with clubs in <a href="club/chester-rfc.html">Chester</a>, <a href="club/macclesfield-rfc.html">Macclesfield</a>, <a href="club/wilmslow-rfc.html">Wilmslow</a>, Northwich, Congleton and Crewe.',
             'Warrington also has a rugby union club, so players there can choose either code.'],
         faqs=[('Are there rugby league clubs in Cheshire?', 'Yes. Warrington and Widnes both have professional rugby league clubs, and there are amateur league clubs in Warrington and Runcorn.')]),
    dict(slug='rugby-clubs-north-yorkshire', place='North Yorkshire', counties=['North Yorkshire'],
         title='Rugby Clubs in North Yorkshire | York, Harrogate &amp; Scarborough',
         meta='Find rugby clubs in North Yorkshire: {n} union and league clubs in York, Harrogate, Scarborough, Middlesbrough, Malton and more. Compare clubs near you.',
         keywords='rugby clubs North Yorkshire, York rugby club, Harrogate rugby, Scarborough rugby, Middlesbrough rugby, York Knights',
         intro=[
             'North Yorkshire is a big county with rugby in most of its towns. This page lists the {n} North Yorkshire clubs in our directory — {union} rugby union and {league} rugby league.',
             'York is the only place in the county with both codes at a high level: <a href="club/york-knights.html">York Knights</a> play rugby league, alongside amateur league clubs and <a href="club/york-rugby-union.html">York RUFC</a>. Elsewhere rugby union dominates, with clubs in <a href="club/harrogate-rfc.html">Harrogate</a>, <a href="club/scarborough-rfc.html">Scarborough</a>, <a href="club/malton-norton-rfc.html">Malton &amp; Norton</a>, Whitby, Skipton, Selby and on Teesside.',
             'For West and South Yorkshire, see our <a href="rugby-clubs-leeds.html">Leeds</a> and <a href="rugby-clubs-hull.html">Hull</a> pages or <a href="rugby-union.html?region=yorkshire">all Yorkshire rugby</a>.'],
         faqs=[('Is there rugby league in York?', 'Yes. York Knights are the city\'s professional rugby league club, and there are amateur league clubs such as Heworth and New Earswick All Blacks.')]),
    dict(slug='north-east-rugby-clubs', place='the North East', counties=['County Durham', 'Tyne and Wear', 'Northumberland'],
         title='North East Rugby Clubs | Newcastle, Durham &amp; Northumberland',
         meta='Find rugby clubs in the North East: {n} clubs across Newcastle, Sunderland, Durham, Darlington, Hartlepool and Northumberland. Compare clubs near you.',
         keywords='North East rugby clubs, rugby clubs Newcastle, rugby clubs Durham, Northumberland rugby, Darlington rugby, Sunderland rugby',
         intro=[
             'The North East is rugby union country, with strong clubs in almost every town between the Tees and the Scottish border. This page lists the {n} clubs in our directory across County Durham, Tyne and Wear and Northumberland.',
             '<a href="club/newcastle-falcons.html">Newcastle Falcons</a> are the region\'s professional side, but the heart of North East rugby is its community clubs — from <a href="club/blaydon-rfc.html">Blaydon</a>, <a href="club/darlington-mowden-park-sharks.html">Darlington Mowden Park</a> and <a href="club/durham-city-rfc.html">Durham City</a> to market-town clubs in Northumberland such as <a href="club/tynedale-rfc.html">Tynedale</a>, <a href="club/morpeth-rfc.html">Morpeth</a> and <a href="club/alnwick-rfc.html">Alnwick</a>.',
             'Use the town list below to find clubs near you, then check each profile for where the club plays.'],
         faqs=[('Is there rugby league in the North East?', 'Rugby league is much smaller here than rugby union, but our directory lists <a href="club/newcastle-thunder.html">Newcastle Thunder</a>.')]),
    dict(slug='rugby-clubs-hertfordshire', place='Hertfordshire', counties=['Hertfordshire'],
         title='Rugby Clubs in Hertfordshire | Find a Rugby Club in Herts',
         meta='Find rugby clubs in Hertfordshire: {n} rugby union clubs in St Albans, Hitchin, Harpenden, Hertford, Stevenage, Watford and more. Compare clubs near you.',
         keywords='rugby clubs Hertfordshire, Herts rugby clubs, St Albans rugby club, Hitchin rugby, Harpenden rugby, Hertford rugby club',
         intro=[
             'Hertfordshire has a busy rugby union scene, with clubs in most of its towns and large mini and junior sections. This page lists the {n} Hertfordshire clubs in our directory.',
             'Clubs include <a href="club/st-albans-rfc.html">St Albans</a>, <a href="club/hitchin-rfc.html">Hitchin</a>, <a href="club/harpenden-rfc.html">Harpenden</a>, <a href="club/hertford-rfc.html">Hertford</a>, Stevenage, Hemel Hempstead, Cheshunt and <a href="club/fullerians-rfc.html">Fullerians</a> in Watford.',
             'South Hertfordshire is close to north London, so it is worth looking at our <a href="rugby-clubs-london.html">London rugby clubs</a> page too.'],
         faqs=[('Can adults start playing rugby in Hertfordshire?', 'Yes. Most clubs in the county run several senior teams, so beginners can start at a level that suits them. Our guide to <a href="blog/how-to-start-playing-rugby-as-an-adult-uk-guide/">starting rugby as an adult</a> explains what to expect.')]),
    dict(slug='rugby-clubs-hampshire', place='Hampshire', counties=['Hampshire'],
         title='Rugby Clubs in Hampshire | Find a Rugby Club in Hampshire',
         meta='Find rugby clubs in Hampshire: {n} rugby union clubs in Winchester, Basingstoke, Eastleigh, Andover, Havant and more. Compare clubs and find one near you.',
         keywords='rugby clubs Hampshire, Hampshire rugby, Winchester rugby club, Basingstoke rugby, Eastleigh rugby, Southampton rugby clubs',
         intro=[
             'Hampshire has rugby union clubs from the New Forest to the Surrey border. This page lists the {n} Hampshire clubs in our directory so you can compare them in one place.',
             'Around Southampton, <a href="club/trojans-rfc.html">Trojans</a> and Eastleigh are based in Eastleigh, with <a href="club/tottonians-rfc.html">Tottonians</a> in Totton. Further north and east there are clubs in <a href="club/winchester-rfc.html">Winchester</a>, <a href="club/basingstoke-rfc.html">Basingstoke</a>, <a href="club/andover-rfc.html">Andover</a>, Alton, Petersfield and Havant.',
             'Clubs near the Surrey border are also within reach of our <a href="rugby-clubs-surrey.html">Surrey rugby clubs</a>.'],
         faqs=[('Which rugby clubs are near Southampton?', 'In our directory, the nearest clubs are <a href="club/trojans-rfc.html">Trojans</a> and Eastleigh RFC in Eastleigh, and <a href="club/tottonians-rfc.html">Tottonians</a> in Totton.')]),
]


def load_cards():
    s = open(os.path.join(ROOT, 'clubs.html'), encoding='utf-8').read()
    cards = {}
    for c in re.findall(r'<div class="club-card-wrap"[^>]*>\s*<article class="club-card.*?</article>\s*</div>', s, re.S):
        m = re.search(r'club/([a-z0-9-]+)\.html', c)
        if m:
            cards[m.group(1)] = c
    return cards


def shell():
    s = open(os.path.join(ROOT, 'rugby-clubs-surrey.html'), encoding='utf-8').read()
    head_end = s.find('<link rel="icon"')
    head_tail = s[head_end:s.find('</head>')]
    head_tail = re.sub(r'<script type="application/ld\+json">.*?</script>\s*', '', head_tail, flags=re.S)
    header = s[s.find('</head>'):s.find('<main>')]
    footer = s[s.find('</main>'):]
    # drop the generic FAQ block that follows </main> on older pages
    footer = re.sub(r'<section class="faq-reference-section".*?</section>\s*', '', footer, flags=re.S)
    return head_tail, header, footer


def plural(n, one, many):
    return f'{n} {one if n == 1 else many}'


def build(hub, clubs, cards, all_hubs, shell_parts):
    head_tail, header, footer = shell_parts
    rs = sorted([c for c in clubs if c['county'] in hub['counties'] and c['slug'] in cards],
                key=lambda c: (c['town'] or 'zz', c['name']))
    n = len(rs)
    league = sum(1 for r in rs if 'league' in r['sport'].lower())
    union = n - league
    fmt = dict(n=n, league=league, union=union)
    url = f'{SITE}/{hub["slug"]}.html'
    title = hub['title']
    meta = hub['meta'].format(**fmt)
    # town index
    towns = {}
    for r in rs:
        towns.setdefault(r['town'] or 'Other', []).append(r)
    town_items = ''.join(
        f'<li><strong>{html.escape(t)}:</strong> ' + ', '.join(
            f'<a href="club/{r["slug"]}.html">{html.escape(r["name"])}</a>' for r in v) + '</li>'
        for t, v in sorted(towns.items()))
    grid = lambda sub: '<div class="grid-3" style="margin-bottom:1.5rem">' + ''.join(cards[r['slug']] for r in sub) + '</div>'
    if league and union:
        lists = (f'<h2 {H2} id="clubs">Rugby Union Clubs in {hub["place"]}</h2>' + grid([r for r in rs if 'league' not in r['sport'].lower()]) +
                 f'<h2 {H2}>Rugby League Clubs in {hub["place"]}</h2>' + grid([r for r in rs if 'league' in r['sport'].lower()]))
    else:
        lists = f'<h2 {H2} id="clubs">All Rugby Clubs in {hub["place"]}</h2>' + grid(rs)
    faqs = [(f'How many rugby clubs are there in {hub["place"]}?',
             f'Our directory currently lists {plural(n, "club", "clubs")} in {hub["place"]}'
             + (f' — {union} rugby union and {league} rugby league.' if league and union else '.')
             + ' If a club is missing, you can <a href="register.html">register it for free</a>.')] + hub['faqs'] + [
            (f'How do I join a rugby club in {hub["place"]}?',
             'Pick two or three clubs near you, check each club\'s profile for where it plays and how to get in touch, then ask about the next training session. Our <a href="blog/how-to-find-a-rugby-club-near-you/">guide to finding a rugby club</a> walks you through it.')]
    faq_html = ''.join(
        f'<div class="faq-item" style="margin-bottom:1.25rem"><h3 style="font-size:1.15rem;font-weight:700;color:var(--text-primary);margin:1.5rem 0 .6rem">{q}</h3><p {P}>{a}</p></div>'
        for q, a in faqs)
    other = ''.join(f'<a href="{h}.html">{html.escape(lbl)}</a><span class="sep">·</span>' for h, lbl in all_hubs if h != hub['slug'])
    intro = ''.join(f'<p {P}>{p.format(**fmt)}</p>' for p in hub['intro'])
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": url + '#page', "name": re.sub('<[^>]+>', '', html.unescape(title.split(' | ')[0])),
         "description": meta, "url": url, "inLanguage": "en-GB",
         "isPartOf": {"@type": "WebSite", "name": "UK Rugby Club Directory", "url": SITE + '/'}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + '/'},
            {"@type": "ListItem", "position": 2, "name": "All Clubs", "item": SITE + '/clubs.html'},
            {"@type": "ListItem", "position": 3, "name": re.sub('<[^>]+>', '', html.unescape(title.split(' | ')[0])), "item": url}]},
        {"@type": "ItemList", "numberOfItems": n, "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "url": f'{SITE}/club/{r["slug"]}.html', "name": r['name']} for i, r in enumerate(rs)]},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": re.sub('<[^>]+>', '', q),
             "acceptedAnswer": {"@type": "Answer", "text": html.unescape(re.sub('<[^>]+>', '', a))}} for q, a in faqs]}]}
    h1 = re.sub(r' \|.*$', '', title)
    page = f'''<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{html.escape(meta, quote=True)}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{html.escape(meta, quote=True)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/imgs/rugby-union-hero.jpg">
<meta property="og:site_name" content="UK Rugby Club Directory">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{html.escape(meta, quote=True)}">
<meta name="geo.region" content="GB">
<meta name="theme-color" content="#293241">
{head_tail}<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
{header}<main>
<section class="listing-hero-england" style="position:relative;min-height:220px;display:flex;align-items:stretch;overflow:hidden;border-bottom:none">
  <div class="lh-left" style="position:relative;z-index:2;flex:0 0 58%;background:var(--navy);clip-path:polygon(0 0,82% 0,100% 100%,0 100%);padding:2.25rem 5rem 2.25rem 2rem;display:flex;flex-direction:column;justify-content:center">
    <nav class="breadcrumb" style="margin-bottom:.6rem">
      <a href="index.html">Home</a><span class="bc-sep">›</span>
      <a href="clubs.html">All Clubs</a><span class="bc-sep">›</span>
      <span class="bc-cur">{html.escape(hub["place"].replace("the ", "").title() if hub["place"].startswith("the ") else hub["place"])}</span>
    </nav>
    <span class="lh-eyebrow" style="font-family:Oswald,sans-serif;font-size:.65rem;font-weight:600;letter-spacing:.14em;text-transform:uppercase;margin-bottom:.5rem;display:block">UK Rugby Club Directory</span>
    <h1 style="font-family:Oswald,sans-serif;font-size:clamp(1.6rem,3.6vw,2.5rem);font-weight:700;color:#fff;letter-spacing:.03em;text-transform:uppercase;margin:0 0 .5rem;line-height:1.05">{h1}</h1>
    <p style="font-size:.9rem;color:rgba(255,255,255,.82);line-height:1.55;margin-bottom:1rem;max-width:430px">Compare {plural(n, "rugby club", "rugby clubs")} in {html.escape(hub["place"])}, see where each one plays, and find the right club near you.</p>
    <div class="club-hero-er-btns">
      <a href="#clubs" class="btn-er-primary">Browse the Clubs ›</a>
      <a href="register.html" class="btn-er-ghost">Register Your Club ›</a>
    </div>
  </div>
  <div class="lh-right lh-pattern" aria-hidden="true" style="position:absolute;right:0;top:0;bottom:0;width:42%"></div>
</section>
<div class="seo-links-bar">
  <div class="con seo-links-inner">
    <strong>Other areas:</strong>
    {other}<a href="clubs.html">All Clubs</a>
  </div>
</div>
<section class="sec">
  <div class="con">
    <div style="max-width:880px;margin:0 auto">
      {intro}
      <h2 {H2}>Rugby Clubs by Town</h2>
      <ul style="list-style:none;padding:0;margin:0 0 1rem;line-height:1.9;font-size:.95rem">{town_items}</ul>
    </div>
    {lists}
  </div>
</section>
<section class="sec sec-off" id="faq">
  <div class="con">
    <div class="sh"><span class="ey">Quick Answers</span><h2>{html.escape(re.sub(r" \|.*$", "", html.unescape(title)))} FAQs</h2></div>
    <div style="max-width:880px;margin:0 auto">{faq_html}</div>
  </div>
</section>
<section class="sec">
  <div class="con" style="text-align:center">
    <h2 {H2}>Is Your Club Missing?</h2>
    <p {P}>We add new clubs regularly. If your club is not listed yet, register it for free so players searching near you can find it.</p>
    <a href="register.html" class="btn btn-red">Register Your Club Free</a>
  </div>
</section>
{footer}'''
    open(os.path.join(ROOT, hub['slug'] + '.html'), 'w', encoding='utf-8').write(page)
    return n


def main():
    clubs = [c for c in json.load(open(os.path.join(ROOT, 'tools', 'clubs.json'))) if c['type'] == 'SportsTeam']
    cards = load_cards()
    parts = shell()
    existing = [('rugby-clubs-surrey', 'Surrey'), ('rugby-clubs-essex', 'Essex'), ('south-west-rugby-clubs', 'South West'),
                ('rugby-clubs-bristol', 'Bristol'), ('rugby-clubs-birmingham', 'Birmingham'), ('rugby-clubs-cardiff', 'Cardiff'),
                ('rugby-clubs-leeds', 'Leeds'), ('rugby-clubs-hull', 'Hull')]
    new = [(h['slug'], h['place'].replace('the ', '').replace('Greater ', '')) for h in HUBS]
    for hub in HUBS:
        print(hub['slug'], build(hub, clubs, cards, existing + new, parts))
    print('club pages linked to their hub:', link_club_pages(clubs))


def link_club_pages(clubs):
    """Give every club page in a hub county a link to its hub (once)."""
    n = 0
    for hub in HUBS:
        label = 'the North East' if hub['slug'] == 'north-east-rugby-clubs' else hub['place']
        link = (f'<p style="margin-top:.5rem"><a href="../{hub["slug"]}.html" style="color:var(--red);font-weight:600">'
                f'Rugby clubs in {html.escape(label)} →</a></p>')
        for c in clubs:
            if c['county'] not in hub['counties']:
                continue
            path = os.path.join(ROOT, 'club', c['slug'] + '.html')
            if not os.path.exists(path):
                continue
            s = open(path, encoding='utf-8', errors='surrogateescape').read()
            if f'../{hub["slug"]}.html' in s:
                continue
            m = re.search(r'(<a href="\.\./clubs\.html\?q=[^"]*"[^>]*>Search [^<]*</a></p>)', s)
            if not m:
                continue
            s = s[:m.end()] + link + s[m.end():]
            open(path, 'w', encoding='utf-8', errors='surrogateescape').write(s)
            n += 1
    return n


if __name__ == '__main__':
    main()
