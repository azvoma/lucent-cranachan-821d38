"""
Keyword-gap sections for the main pages, the South West hub and the Register page, added after the
SE Ranking content-score audit of 14 Nov 2026. Tables are generated from our own data
(tools/clubs.json and tools/er-teams.csv, England Rugby, 31 Oct 2026) so every row is checkable.
"""
import csv
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UPDATED = '2026-11-14'

CLUBS = [c for c in json.load(open(os.path.join(ROOT, 'tools', 'clubs.json'))) if c.get('type') == 'SportsTeam']
ER = {r['slug']: r['league'] for r in csv.DictReader(open(os.path.join(ROOT, 'tools', 'er-teams.csv')))}
PREM = {'bath-rugby', 'bristol-bears', 'exeter-chiefs', 'gloucester-rugby', 'harlequins', 'leicester-tigers',
        'newcastle-falcons', 'northampton-saints', 'sale-sharks', 'saracens'}
SUPER = ['bradford-bulls', 'castleford-tigers', 'catalans-dragons', 'huddersfield-giants', 'hull-fc', 'hull-kingston-rovers',
         'leeds-rhinos', 'leigh-leopards', 'st-helens-rfc', 'toulouse-olympique', 'wakefield-trinity', 'warrington-wolves',
         'wigan-warriors', 'york-knights']  # same set as tools/club_content.SUPER_LEAGUE
BY = {c['slug']: c for c in CLUBS}


def lg(slug):
    if slug in PREM:
        return 'PREM Rugby'
    l = ER.get(slug, '')
    l = re.sub(r' \|.*$', '', l).replace('Tribute Ale ', '').replace('adm ', '').strip()
    return l or 'Not confirmed'


def table(slugs, league_col=True, prefix=''):
    head = '| Club | Town |' + (' League (2026-27) |' if league_col else '')
    rows = [head, '|---|---|' + ('---|' if league_col else '')]
    for s in slugs:
        c = BY[s]
        rows.append(f'| [{c["name"]}]({prefix}club/{s}.html) | {c["town"]} |' + (f' {lg(s)} |' if league_col else ''))
    return '\n'.join(rows)


def by_county(county, sport):
    return sorted((c['slug'] for c in CLUBS if c['county'] == county and c['sport'] == sport), key=lambda s: BY[s]['name'])


def n(county, sport):
    return len(by_county(county, sport))


# ------------------------------------------------------------------ clubs.html
lancs, cheshire_u, cheshire_l = by_county('Lancashire', 'Rugby Union'), by_county('Cheshire', 'Rugby Union'), by_county('Cheshire', 'Rugby League')

CLUBS_EXTRA = [
    dict(id='lancashire-cheshire', h2='Lancashire and Cheshire rugby clubs',
         answer=f'Our directory lists {len(lancs)} Lancashire rugby union clubs and {len(cheshire_u) + len(cheshire_l)} Cheshire clubs ({len(cheshire_u)} union, {len(cheshire_l)} league). Lancashire is mostly union, while Cheshire\'s Warrington and Widnes clubs make it a rugby league county too.',
         md=f'''
**Lancashire rugby clubs (union)**

{table(lancs)}

**Cheshire rugby clubs (union)**

{table(cheshire_u)}

**Cheshire rugby league clubs:** {', '.join(f'[{BY[s]["name"]}](club/{s}.html)' for s in cheshire_l)}.

Compare these clubs by town on our [Lancashire rugby clubs page](rugby-clubs-lancashire.html) and our [Cheshire rugby clubs page](rugby-clubs-cheshire.html). Greater Manchester and Merseyside clubs, which many people count as part of the North West, are on the [Manchester](rugby-clubs-manchester.html) and [Merseyside](rugby-clubs-merseyside.html) pages.
'''),
    dict(id='rugby-divisions', h2='Rugby divisions: where to see every league',
         answer='Every club profile shows the division the club plays in for 2026-27. For how the divisions connect, use our guide to rugby leagues in the UK for both codes, or the RFU league structure page for English rugby union.',
         md='''
- [Rugby leagues in the UK](rugby-leagues-uk.html): union and league, every level.
- [English RFU league structure](rugby-union-league-structure.html): PREM Rugby down to Counties 4.
'''),
]

# ------------------------------------------------------------------ index.html
leeds_l = sorted((c['slug'] for c in CLUBS if c['sport'] == 'Rugby League' and c['town'] == 'Leeds'), key=lambda s: BY[s]['name'])
glos = by_county('Gloucestershire', 'Rugby Union')
hants = by_county('Hampshire', 'Rugby Union')
supers = [s for s in SUPER if s in BY]

HOME_EXTRA = [
    dict(id='england-rugby-league-teams', h2='England rugby league teams and London rugby league clubs',
         answer=f'Our directory lists {len(supers)} Super League and top-flight rugby league clubs, mostly in Yorkshire and the North West, plus two London rugby league clubs: London Broncos and London Skolars. Amateur rugby league clubs, such as those in Leeds, Warrington and St Helens, sit below them.',
         md=f'''
**Super League and professional clubs:** {', '.join(f'[{BY[s]["name"]}](club/{s}.html)' for s in supers)}.

**London rugby league clubs:** [London Broncos](club/london-broncos.html) and [London Skolars](club/london-skolars.html). Rugby league is a northern game, so London has far fewer clubs than union. For union, see [rugby clubs in London](rugby-clubs-london.html).

Browse the whole list on our [rugby league clubs page](rugby-league.html), or read how the competitions fit together in [rugby leagues in the UK](rugby-leagues-uk.html).
'''),
    dict(id='gloucestershire-clubs', h2='Gloucestershire rugby clubs',
         answer=f'Gloucestershire has {len(glos)} rugby clubs in our directory, led by Gloucester Rugby in PREM Rugby. The county is a union stronghold, with clubs in Gloucester, Cheltenham, Stroud, Cirencester, Cinderford and Hartpury.',
         md=f'''
{table(glos)}

See the county page for more detail: [rugby clubs in Gloucestershire](rugby-clubs-gloucestershire.html).
'''),
    dict(id='lymington-mariners', h2='Looking for Lymington Mariners RFC?',
         answer='Lymington Mariners RFC is not listed in our directory yet. Lymington is in Hampshire, so the nearest clubs we do list are the Hampshire clubs below. If you run or play for Lymington Mariners, you can add the club for free on our register page.',
         md=f'''
{table(hants)}

More on the [Hampshire rugby clubs page](rugby-clubs-hampshire.html). Club officials can [register a club](register.html) to be added to the list.
'''),
]

# ------------------------------------------------------------------ rugby-union.html
UNION_EXTRA = [
    dict(id='rfu-leagues', h2='The rugby teams list and RFU leagues',
         answer='Every club in this rugby teams list shows the RFU league it plays in for 2026-27 where England Rugby has confirmed it. For how those leagues fit together, see our English RFU league structure guide.',
         md='''
Clubs in the same league are usually within reasonable travelling distance, so the league also tells you who your fixtures will be against. Full detail on levels, promotion and relegation: [English rugby union league structure](rugby-union-league-structure.html).
'''),
    dict(id='first-session', h2='Join a rugby club: what happens at your first session',
         answer='When you join a rugby club, you normally turn up to a training session, meet the coach and play non-contact drills first. The club then registers you with the RFU, which you do through the club, so contact the club first to confirm the training night.',
         md='''
- **Before you go:** message the club using the details on its profile and ask which squad suits a beginner.
- **Bring:** boots, a gumshield and a water bottle. Most clubs lend a shirt for the first session.
- **Registration:** English clubs register their players with the RFU. The club handles this, and you may be asked for ID and an emergency contact.
- **Younger players:** juniors normally start at under-6 or under-7 level in a mini section.

Not sure which club? Start with our guide to [how to join a rugby union club](#join).
'''),
]

# ------------------------------------------------------------------ rugby-league.html
LEAGUE_EXTRA = [
    dict(id='leeds-league-clubs', h2='Rugby league clubs in Leeds',
         answer=f'Leeds has {len(leeds_l)} rugby league clubs in our directory: Leeds Rhinos in Super League, plus Hunslet RLFC and the amateur clubs East Leeds, West Leeds, Bramley Buffaloes, Hunslet Warriors, Oulton Raiders and Stanningley.',
         md=f'''
{table(leeds_l, league_col=False)}

Leeds Rhinos are a professional club. Beginners should look at the amateur clubs. More on the [Leeds rugby clubs page](rugby-clubs-leeds.html), which covers rugby union in the city as well.
'''),
    dict(id='rfu-affiliated', h2='RFU affiliated clubs are rugby union clubs',
         answer='RFU affiliated clubs are rugby union clubs registered with the Rugby Football Union. Rugby league clubs are governed by the RFL, so use our rugby union page for RFU affiliated clubs. For how both codes\' leagues fit together, read rugby leagues in the UK.',
         md='''
- [UK rugby union clubs](rugby-union.html), each with its RFU league.
- [Rugby leagues in the UK](rugby-leagues-uk.html), both codes.
'''),
]

# ------------------------------------------------------------------ south-west-rugby-clubs.html
som = by_county('Somerset', 'Rugby Union')
SW_EXTRA = [
    dict(id='somerset-clubs', h2='Somerset rugby clubs and rugby clubs near Bath',
         answer=f'Somerset has {len(som)} rugby clubs in our directory. Bath Rugby, in PREM Rugby, is the only Bath club we list, and the others run from Weston-super-Mare and Clevedon to Taunton, Bridgwater and Yeovil. Bristol clubs are the closest alternatives to Bath.',
         md=f'''
{table(som)}

Bath Rugby play in the city centre at The Recreation Ground, a major PREM Rugby venue. If you want to play rather than watch, look at the community clubs above and the [Bristol rugby clubs](rugby-clubs-bristol.html) page. The county has its own page: [Somerset rugby clubs](rugby-clubs-somerset.html).
'''),
    dict(id='sw-rugby-league', h2='South West rugby league: where to play',
         answer='Rugby league is thin in the South West. Our directory lists one club in the region, Cornwall RLFC in Truro, and the nearest others are in London and the Midlands. Rugby union dominates, so check the RFL website if you want a closer league club.',
         md='''
- [Cornwall RLFC](club/cornwall-rlfc.html), Truro.
- [London Broncos](club/london-broncos.html) and [London Skolars](club/london-skolars.html), for the south-east.
- [All UK rugby league clubs](rugby-league.html).

Tag and touch rugby league sessions run in some towns without a full club, so ask the RFL or your county sports partnership. We only list clubs we can confirm.
'''),
]

# ------------------------------------------------------------------ register.html
REGISTER = dict(
    updated=UPDATED, byline=True, toc=False,
    sections=[
        dict(id='find-a-club', h2='RFU find a club: how this directory fits in',
             answer='The RFU find a club tool lists clubs registered with England Rugby, while this directory lists union and league clubs from across the UK, with each club\'s league and ground. Registering with us is free, takes two minutes and does not replace your RFU or RFL registration.',
             md='''
- **England Rugby:** the RFU\'s own find-a-club search covers English union clubs that are affiliated to the RFU.
- **This directory:** one UK-wide list of rugby union and rugby league clubs, with a profile page for each club.
- **Registering here:** adds your club to the list. It does not change your RFU affiliation, league entry or fixtures.

To check how your club is shown today, search for it on the [rugby union](rugby-union.html) or [rugby league](rugby-league.html) pages.
'''),
        dict(id='what-we-list', h2='What does a club listing include?',
             answer='A listing includes the club\'s name, town, sport, founding year, league, ground address, website and a contact route. We verify league and founding details against England Rugby and the club\'s own site, and we correct errors when the club tells us.',
             md='''
- Name, town and county, so people searching "rugby near me" can find you.
- Sport: rugby union or rugby league.
- League and level for 2026-27, where confirmed by England Rugby.
- Ground address and map link, and club contact details you choose to publish.

See how a finished listing looks on a club page such as [Tynedale RFC](club/tynedale-rfc.html). To fix a listing, use our [contact page](contact-us.html).
'''),
    ],
    faqs=[
        ('Does listing my club replace RFU registration?', 'No. This directory is independent. Your RFU or RFL affiliation, league entry and fixtures are managed through the governing body.'),
        ('How much does a listing cost?', 'A basic listing is free. A Pro listing is £9.99 a month and adds photos and a verified badge.'),
        ('How long before my club appears?', 'Listings are normally live within 24 hours of approval.'),
    ],
)
