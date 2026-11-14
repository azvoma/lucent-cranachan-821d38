"""Long-form guide content for the four main directory pages (applied by tools/apply_main_guides.py)."""

UPDATED = '2026-11-01'

HOME = dict(
    file='index.html',
    title='Rugby Near Me: Find a Rugby Club in the UK (637 Clubs)',
    meta='Find rugby near you. Search 637 rugby union and rugby league clubs across the UK by town or county, compare local teams and see how to join. Free to use.',
    h1_html='Rugby Near Me: Find a<br><span>Rugby Club in the UK</span>',
    updated=UPDATED,
    about=['Rugby union', 'Rugby league', 'Rugby club'],
    intro='',
    takeaways=[
        'Searching for **rugby near me**? Type your town or county into the search box above. Every result opens a club profile showing where the club plays and how to get in touch.',
        'The directory lists **637 rugby clubs**: 470 rugby union and 101 rugby league clubs, plus rugby businesses, across England, Wales, Scotland and Northern Ireland.',
        'Most rugby clubs welcome beginners of any age. Look for a community club with several adult teams; in England that usually means a Regional or Counties league club.',
        'Half the clubs in our directory with a known founding date were formed before 1912, so most local rugby clubs have deep roots in their town.',
    ],
    sections=[
        dict(id='how-to-find', h2='How to find a rugby club near you',
             answer='To find a rugby club near you, search the directory by town, postcode area or county. Shortlist two or three clubs within easy reach of home or work, and check each club\'s profile for its ground and contact details. Then ask about the next training session. Most clubs let you try a session before joining.',
             img=('imgs/home-hero-2.webp', 'Community rugby union players forming a ruck during a match at a local rugby club near me', 1600, 1067),
             md='''
In practice, the club you end up at is decided by three things: distance, training night and the level the club plays at. Use this checklist:

1. **Search by town first.** Use the search box at the top of this page. If your town has no club, search the county instead or open an [area page](#areas).
2. **Check the code.** Every rugby club profile shows whether the club plays rugby union or rugby league. They are different sports with different rules.
3. **Check the training night.** Most amateur clubs train on two weeknights, often Tuesday and Thursday, and play on Saturdays (union) or Saturdays and Sundays (league).
4. **Contact the club.** 249 club pages in our directory have a direct phone number, email or website. For the rest, we link to the governing body's club finder.
5. **Go to a session.** Turn up in training kit and boots, with a gum shield. Nobody expects a beginner to know the laws.
'''),
        dict(id='union-or-league', h2='Rugby union club or rugby league club?',
             answer='A rugby union club plays the 15-a-side game, which is found in almost every UK town. A rugby league club plays the 13-a-side game, which is concentrated in Yorkshire, Lancashire, Greater Manchester and Cumbria. If you live in the North of England you may have both nearby, so check the code before you go.',
             md='''
| | Rugby union | Rugby league |
|---|---|---|
| Players per team | 15 | 13 |
| Clubs in our directory | 470 | 101 |
| Where it is strongest | Everywhere: the South, Midlands, Wales and Scotland especially | Northern England heartlands |
| Typical match day | Saturday afternoon | Saturday or Sunday |
| Browse | [Rugby union clubs](rugby-union.html) | [Rugby league clubs](rugby-league.html) |

Both codes run men's, women's and junior sections at many clubs. If you are unsure, go with the club that is easiest to reach. You are far more likely to keep playing if training is 10 minutes away.
'''),
        dict(id='areas', h2='Rugby clubs by area',
             answer='Our area pages group rugby clubs by city and county, so you can compare local rugby teams side by side. Each page lists every club we hold for that area, with the code it plays and a link to its profile. Pick the area nearest to you below, or search by town at the top.',
             md='''
| England: South | England: Midlands and North | Wales and Scotland |
|---|---|---|
| [London](rugby-clubs-london.html) | [Birmingham](rugby-clubs-birmingham.html) | [Cardiff](rugby-clubs-cardiff.html) |
| [Surrey](rugby-clubs-surrey.html) | [Manchester](rugby-clubs-manchester.html) | [Edinburgh](rugby-clubs-edinburgh.html) |
| [Kent](rugby-clubs-kent.html) | [Leeds](rugby-clubs-leeds.html) | [All Welsh clubs](rugby-union.html?region=wales) |
| [Sussex](rugby-clubs-sussex.html) | [Hull](rugby-clubs-hull.html) | [All Scottish clubs](rugby-union.html?region=scotland) |
| [Hampshire](rugby-clubs-hampshire.html) | [Merseyside](rugby-clubs-merseyside.html) | |
| [Essex](rugby-clubs-essex.html) | [Cheshire](rugby-clubs-cheshire.html) | |
| [Hertfordshire](rugby-clubs-hertfordshire.html) | [Lancashire](rugby-clubs-lancashire.html) | |
| [Bristol](rugby-clubs-bristol.html) | [Cumbria](rugby-clubs-cumbria.html) | |
| [Gloucestershire](rugby-clubs-gloucestershire.html) | [North Yorkshire](rugby-clubs-north-yorkshire.html) | |
| [Somerset](rugby-clubs-somerset.html) | [North East](north-east-rugby-clubs.html) | |
| [South West](south-west-rugby-clubs.html) | [Warwickshire](rugby-clubs-warwickshire.html) | |
'''),
        dict(id='beginners', h2='Joining a rugby club as a beginner',
             answer='You do not need any experience to join a rugby club. Community clubs run several adult teams so that new players get games at the right level. Many also run touch or walking rugby sessions. Bring boots, a gum shield and training kit, and tell the coach you are new.',
             md='''
What to expect in your first month:

- **Week 1:** Fitness, handling and basic tackle technique. Contact is introduced gradually.
- **Weeks 2–4:** You train with the squad and may be picked for a lower team such as a 3rd XV or development side.
- **Fees:** Most clubs ask for an annual subscription once you start playing regularly. Ask about student, unemployed and family rates.

**Be aware:** rugby is a contact sport. Good clubs coach safe tackling and follow the governing body's concussion protocols. Ask a club how it manages head injuries before you start.

Looking for something specific? See our guides to [women's rugby clubs](womens-rugby-clubs.html) and [junior and youth rugby](junior-youth-rugby-clubs.html).
'''),
        dict(id='leagues', h2='Local rugby leagues: what level do local clubs play at?',
             answer='Local rugby clubs in England mostly play in the Regional and Counties leagues, levels 5 to 7 and below of the RFU pyramid. Professional clubs play in PREM Rugby and Super League. Rugby league\'s amateur clubs play in the new National Community Rugby League and regional men\'s leagues.',
             md='''
Of the 267 English union clubs in our directory with a confirmed 2026-27 league:

- 118 play in the Counties leagues
- 60 play in Regional 2
- 42 play in Regional 1

That is the level of rugby most people mean when they search for a "local rugby team".

See how every competition fits together in our guide to [rugby leagues in the UK](rugby-leagues-uk.html), or read the [English rugby union league structure](rugby-union-league-structure.html).
'''),
        dict(id='about-directory', h2='About the UK Rugby Club Directory',
             answer='The UK Rugby Club Directory is a free, independent list of rugby clubs and rugby businesses in England, Wales, Scotland and Northern Ireland. We check club details against official sources, including England Rugby\'s club pages, and update profiles when clubs tell us about changes.',
             md='''
How we keep listings accurate:

- **Source checks:** in October 2026 we matched 321 English clubs to their England Rugby team pages, confirming their league, ground address and published club contact details.
- **Club-claimed profiles:** club officials can [claim a listing](claim.html) to add training times and contacts.
- **What we don't publish:** personal mobile numbers or personal email addresses, even when they appear elsewhere online.

Spotted something wrong, or is your club missing? [Register your club free](register.html) or [contact us](contact-us.html).
'''),
    ],
    faqs=[
        ('How do I find rugby near me?',
         'Type your town or county into the search box at the top of this page, or open your area page. Each result links to a club profile showing where the club plays and how to contact it.'),
        ('How many rugby clubs are there in England?',
         'England Rugby counts well over a thousand affiliated rugby union clubs, and there are hundreds of amateur rugby league clubs as well. Our directory currently lists 454 English clubs: 355 union and 99 league. We add more each month.'),
        ('Can adults start playing rugby with no experience?',
         'Yes. Most community clubs welcome adult beginners and field several teams, so new players get games at a suitable level. Touch rugby is a good low-contact way to start.'),
        ('Are there rugby clubs for women and girls near me?',
         'Many clubs now run women\'s and girls\' sections. See our [women\'s rugby clubs guide](womens-rugby-clubs.html) to find one.'),
        ('Is the directory free to use?',
         'Yes. Searching the directory is free, and clubs can register a basic listing free of charge.'),
    ],
    related=[('clubs.html', 'All rugby clubs'), ('rugby-leagues-uk.html', 'Rugby leagues in the UK'), ('register.html', 'Register your club')],
)

CLUBS = dict(
    file='clubs.html',
    title='Rugby Teams & Clubs in the UK: Full List of 637 Clubs',
    meta='The full list of UK rugby teams and clubs: 637 rugby union and rugby league clubs in England, Wales, Scotland and N. Ireland. Find a local rugby club today.',
    h1='Rugby Teams &amp; Clubs in the UK: All 637 Clubs',
    updated=UPDATED,
    about=['Rugby union', 'Rugby league', 'Rugby club'],
    intro='Browse the full list of UK rugby teams below, or search by club name, town or county. Every club has its own profile with its ground, history and contact details. Want to understand the levels first? Read our guide to <a href="rugby-leagues-uk.html">rugby leagues in the UK</a>.',
    takeaways=[
        'This is the full list of **rugby teams and clubs** in our directory: 637 clubs across the four home nations, including 470 rugby union and 101 rugby league clubs.',
        'England has the most clubs (454 in our directory), followed by Wales (66) and Scotland (44). Yorkshire and Greater London are the busiest areas.',
        'Use the filters above to switch between union, league and businesses, or jump to an **area page** to compare local rugby clubs side by side.',
    ],
    sections=[
        dict(id='list', h2='The full list of rugby clubs in the UK',
             answer='Our list of rugby clubs covers every level, from PREM Rugby and Super League to amateur community teams. Each listing shows the club\'s code, town and county and the year it was founded. Clubs are sorted so the best-known appear first. Use search or the area pages to narrow the list down to local rugby clubs.',
             md='''
| Nation | Rugby union clubs | Rugby league clubs |
|---|---|---|
| England | 355 | 99 |
| Wales | 64 | 2 |
| Scotland | 44 | – |
| Northern Ireland | 6 | – |

*Directory counts on 1 November 2026, excluding rugby businesses and a small number of clubs based overseas or in the Channel Islands.*

The busiest counties in our directory are:

- West Yorkshire: 61 clubs, mostly rugby league
- Greater London: 55
- Greater Manchester: 32
- Devon: 22
- West Midlands: 21
'''),
        dict(id='choose', h2='How to choose a local rugby club',
             answer='Choose a local rugby club by distance first, then training nights, then playing level. A club you can reach in 15 minutes is one you will keep going to. Check that it plays the code you want and runs a team at your level. Clubs with three or more adult teams suit beginners best.',
             md='''
Questions worth asking a club before you join:

1. How many adult teams do you run, and which one would I start in?
2. When are training nights, and is there a coach for newcomers?
3. What does membership cost, and is there a trial period?
4. Do you have a women's, veterans or touch rugby section?
5. For parents: which age groups do you run, and are coaches DBS-checked? (In Scotland, PVG-checked.)
'''),
        dict(id='rugby-teams-england', h2='Rugby teams in England, Wales, Scotland and Northern Ireland',
             answer='Rugby teams in England play in RFU leagues (union) or RFL competitions (league). Welsh, Scottish and Irish clubs play in their own union\'s leagues. Each nation also has professional teams in the United Rugby Championship. Every club on this page links to a profile, and English union clubs show their confirmed league.',
             md='''
- **England:** [rugby union clubs](rugby-union.html), [rugby league clubs](rugby-league.html) and the [RFU league structure](rugby-union-league-structure.html)
- **Wales:** [Cardiff rugby clubs](rugby-clubs-cardiff.html) and [all Welsh clubs](rugby-union.html?region=wales)
- **Scotland:** [Edinburgh rugby clubs](rugby-clubs-edinburgh.html) and [all Scottish clubs](rugby-union.html?region=scotland)
- **Northern Ireland:** [Ulster Rugby](club/ulster-rugby.html) and [IRFU](club/irfu.html)
'''),
        dict(id='finder', h2='Rugby club finder: other ways to search',
             answer='Besides this directory, each governing body runs an official club finder. England Rugby\'s covers RFU-affiliated union clubs, and the RFL, WRU, Scottish Rugby and IRFU each list their own clubs. Our directory brings both codes and all four nations together in one place, with area pages and full club profiles.',
             md='''
When to use which:

- **Want official fixtures and league tables?** Use the governing body's site. Our English club profiles link straight to each club's England Rugby fixtures page.
- **Want to compare clubs in one area, across both codes?** Use our [area pages](index.html#areas) or the search above.
- **Want contact details?** Check the club profile. If we don't hold any, the profile links to the best official source.
'''),
    ],
    faqs=[
        ('How many rugby clubs are there in the UK?',
         'Across both codes and all four nations there are well over 2,000 rugby clubs. Our directory lists 637 of them and grows every month. Clubs can [register for free](register.html).'),
        ('What is the difference between a rugby team and a rugby club?',
         'A club is the organisation; a team is one side it fields. A typical community club runs several adult teams (1st XV, 2nd XV and so on), a women\'s team and mini and junior age-group teams.'),
        ('How do I find a local rugby club?',
         'Search by town at the top of this page, or open your area page. Shortlist the clubs closest to you and contact them about the next training session.'),
        ('What leagues do English rugby clubs play in?',
         'English rugby union clubs play in the RFU pyramid: PREM Rugby, Champ Rugby, the National Leagues, Regional 1 and 2, and the Counties leagues. See our [league structure guide](rugby-union-league-structure.html).'),
    ],
    related=[('rugby-union.html', 'Rugby union clubs'), ('rugby-league.html', 'Rugby league clubs'), ('rugby-leagues-uk.html', 'Rugby leagues in the UK')],
)

UNION = dict(
    file='rugby-union.html',
    title='Rugby Union Teams & Clubs in the UK: All 470 Clubs',
    meta='Find rugby union teams near you: all 470 rugby union clubs in England, Wales, Scotland and N. Ireland, from PREM Rugby to grassroots. Search by area.',
    h1='Rugby Union Clubs &amp; Teams UK',
    updated=UPDATED,
    about=['Rugby union', 'Rugby Football Union', 'Rugby union club'],
    intro='Search all 470 rugby union clubs below by name or town, or filter by region. English clubs show their confirmed 2026-27 league on their profile. For how the leagues fit together, see our <a href="rugby-union-league-structure.html">English rugby union league structure guide</a>.',
    takeaways=[
        'This page lists all **470 rugby union teams and clubs** in our directory: 355 in England, 64 in Wales, 44 in Scotland and 6 in Northern Ireland.',
        'Rugby union in the UK runs from professional leagues (PREM Rugby, the United Rugby Championship) down to amateur community leagues, where most clubs play.',
        'In England, 66% of the clubs in our directory with a confirmed league play in Regional 2 or the Counties leagues. These are the clubs most likely to welcome new players.',
    ],
    sections=[
        dict(id='uk-union', h2='Rugby union in the UK',
             answer='Rugby union is the 15-a-side code of rugby and the most widely played form of the game in the UK. Each home nation has its own governing body: the RFU, the WRU, Scottish Rugby, and the IRFU for Northern Ireland. Each runs its own league pyramid, from professional teams to village clubs.',
             img=('imgs/rugby-union-hero.webp', 'Rugby union team in a blue and white kit carrying the ball into contact during a professional rugby union match in England', 1600, 1066),
             md='''
| Nation | Governing body | Top domestic league | Clubs in our directory |
|---|---|---|---|
| England | RFU | PREM Rugby | 355 |
| Wales | WRU | Super Rygbi Cymru (below the URC regions) | 64 |
| Scotland | Scottish Rugby | Scottish Premiership (below the URC sides) | 44 |
| Northern Ireland | IRFU (Ulster Branch) | Energia All-Ireland League | 6 |

Rugby union clubs in the UK are often among the oldest sports clubs in their town. [Blackheath](club/blackheath-fc.html) was founded in 1858, [Liverpool](club/liverpool-rfc.html) in 1857 and [Richmond](club/richmond-rfc.html) in 1861. Hundreds more date from the 1870s to the 1920s.
'''),
        dict(id='english-teams', h2='English rugby union teams by level',
             answer='English rugby union teams are split into professional clubs (10 in PREM Rugby), semi-professional clubs (Champ Rugby and the National Leagues) and amateur community clubs (Regional and Counties leagues). The level a club plays at tells you how competitive it is and how often it trains, which matters when choosing one.',
             md='''
| Level | League | Clubs in our directory with this league confirmed |
|---|---|---|
| 1 | PREM Rugby | 10 professional clubs (not part of the check) |
| 2 | Champ Rugby | 11 |
| 3 | National League 1 | 8 |
| 4 | National League 2 | 25 |
| 5 | Regional 1 | 42 |
| 6 | Regional 2 | 60 |
| 7+ | Counties | 118 |

The full English rugby teams list is in the directory below. For the rules on promotion, relegation and the 2022 league renaming, read the [RFU league structure guide](rugby-union-league-structure.html).
'''),
        dict(id='join', h2='How to join a rugby union club',
             answer='To join a rugby union club, find one near you in this directory, contact it through the details on its profile, and go along to a training session. Most clubs offer a free trial period before asking for membership fees. Adult beginners are welcome at almost every community club.',
             md='''
1. **Shortlist** two or three clubs near home or work.
2. **Check training nights.** Most community union clubs train on two weeknights.
3. **Turn up prepared** with boots, a gum shield and kit you don't mind getting muddy.
4. **Ask about teams.** A club with a 2nd or 3rd XV can give you games while you learn.
5. **Register.** Clubs register players with the governing body (in England, through the RFU's Game Management System) before you play competitive matches.
'''),
        dict(id='regions', h2='Rugby union clubs by region',
             answer='Use the region filter above, or open one of our area pages. These group rugby union clubs by city and county so you can compare nearby teams. Our largest union areas are Greater London, Devon, Cornwall, Surrey and the Welsh valleys.',
             md='''
Popular area pages:

- **England:** [London](rugby-clubs-london.html), [Surrey](rugby-clubs-surrey.html), [Kent](rugby-clubs-kent.html), [Sussex](rugby-clubs-sussex.html), [Hampshire](rugby-clubs-hampshire.html), [South West](south-west-rugby-clubs.html), [Gloucestershire](rugby-clubs-gloucestershire.html), [Somerset](rugby-clubs-somerset.html), [Warwickshire](rugby-clubs-warwickshire.html), [Birmingham](rugby-clubs-birmingham.html)
- **North of England:** [Leeds](rugby-clubs-leeds.html), [North East](north-east-rugby-clubs.html)
- **Wales and Scotland:** [Cardiff](rugby-clubs-cardiff.html), [Edinburgh](rugby-clubs-edinburgh.html)
'''),
    ],
    faqs=[
        ('How many rugby union teams are there in England?',
         'England Rugby has well over a thousand affiliated clubs, many running several teams each. Our directory lists 355 English rugby union clubs, from PREM Rugby to the Counties leagues.'),
        ('What is the best rugby union team in England?',
         'The top tier is PREM Rugby, with 10 professional clubs including Bath, Bristol Bears, Leicester Tigers, Northampton Saints and Saracens. Which is "best" changes season to season; the league table and play-offs decide the champion.'),
        ('Can I find rugby union clubs near me for men\'s, women\'s and junior rugby?',
         'Yes. Search by town above. Many clubs run all three. See our [women\'s rugby](womens-rugby-clubs.html) and [junior rugby](junior-youth-rugby-clubs.html) guides for specific sections.'),
        ('What is the difference between rugby union and rugby league?',
         'Union is 15-a-side with contested rucks, mauls and lineouts. League is 13-a-side, with six tackles per possession. They have separate clubs and governing bodies. See our [rugby league clubs](rugby-league.html).'),
    ],
    related=[('rugby-union-league-structure.html', 'RFU league structure'), ('rugby-leagues-uk.html', 'Rugby leagues in the UK'), ('clubs.html', 'All rugby clubs')],
)

LEAGUE = dict(
    file='rugby-league.html',
    title='UK Rugby League Clubs & Teams Near Me: All 101 Clubs',
    meta='Find rugby league clubs near you: 101 UK rugby league teams, from the 14 Super League clubs to amateur ARLFC sides in Yorkshire, Lancashire and Cumbria.',
    h1='Rugby League Clubs &amp; Teams UK',
    updated=UPDATED,
    about=['Rugby league', 'Rugby Football League', 'Super League'],
    intro='Search all 101 rugby league clubs below by name or town. Most of the amateur clubs, where new players start, are in the North of England. Looking for how the competitions work? Read our guide to <a href="rugby-leagues-uk.html">rugby leagues in the UK</a>.',
    takeaways=[
        'Our directory lists **101 rugby league clubs and teams**, from all 14 Super League clubs to amateur ARLFC sides.',
        'In 2026, **Super League** grew to 14 clubs, the Championship merged with League One into a single 20-club tier, and the new **National Community Rugby League** replaced the National Conference League.',
        'To play, join an **amateur (ARLFC) club**. Professional clubs rarely run open-age teams for beginners.',
    ],
    sections=[
        dict(id='near-me', h2='How to find rugby league clubs near me',
             answer='Rugby league clubs are concentrated in West Yorkshire, Greater Manchester, Merseyside, Cheshire, Hull and west Cumbria. Search this page by your town, or open the area page for your city. Pick an amateur club (usually named ARLFC), contact it through its profile and ask about the next training night.',
             img=('imgs/rugby-league-banner.webp', 'Rugby league players running with the ball during a Super League match between teams in teal and white kits', 1600, 1060),
             md='''
| Area | Example clubs in our directory | Area page |
|---|---|---|
| Leeds and West Yorkshire | [Leeds Rhinos](club/leeds-rhinos.html), [Siddal](club/siddal-arlfc.html), [East Leeds](club/east-leeds-arlfc.html) | [Leeds rugby clubs](rugby-clubs-leeds.html) |
| Hull | [Hull FC](club/hull-fc.html), [Hull KR](club/hull-kingston-rovers.html), [West Hull](club/west-hull-arlfc.html) | [Hull rugby teams](rugby-clubs-hull.html) |
| Wigan, Leigh and Salford | [Wigan Warriors](club/wigan-warriors.html), [Leigh Leopards](club/leigh-leopards.html), [Wigan St Judes](club/wigan-st-judes.html) | [Manchester rugby clubs](rugby-clubs-manchester.html) |
| St Helens | [St Helens](club/st-helens-rfc.html), [Thatto Heath Crusaders](club/thatto-heath-crusaders.html) | [Merseyside](rugby-clubs-merseyside.html) |
| Warrington and Widnes | [Warrington Wolves](club/warrington-wolves.html), [Widnes Vikings](club/widnes-vikings.html) | [Cheshire](rugby-clubs-cheshire.html) |
| West Cumbria | [Whitehaven](club/whitehaven-rlfc.html), [Workington Town](club/workington-town-rlfc.html) | [Cumbria](rugby-clubs-cumbria.html) |
| London | [London Broncos](club/london-broncos.html), [London Skolars](club/london-skolars.html) | [London](rugby-clubs-london.html) |
'''),
        dict(id='structure', h2='Rugby league in England: how the competitions work',
             answer='English rugby league has three main layers. Super League has 14 professional clubs in 2026, and the 20-club Championship sits below it. Under those is the community game, led by the National Community Rugby League and regional men\'s leagues. Entry to Super League is decided by club grading and an independent panel, not results alone.',
             md='''
| Level | Competition (2026) | Clubs |
|---|---|---|
| 1 | Super League | 14 |
| 2 | RFL Championship (merged with League One) | 20 |
| 3 | NCRL National Premier League | 12 |
| 4 | NCRL National League One | 12 |
| 5+ | NCRL National Conferences and regional men's leagues | Many |

The 2026 Super League clubs are:

- Bradford Bulls
- Castleford Tigers
- Catalans Dragons
- Huddersfield Giants
- Hull FC
- Hull KR
- Leeds Rhinos
- Leigh Leopards
- St Helens
- Toulouse Olympique
- Wakefield Trinity
- Warrington Wolves
- Wigan Warriors
- York Knights

Hull KR won the 2025 Grand Final, their first Super League title.

For both codes side by side, including rugby union's leagues, see [rugby leagues in the UK](rugby-leagues-uk.html).
'''),
        dict(id='play', h2='Playing amateur rugby league',
             answer='Amateur rugby league clubs, often called ARLFCs, run open-age men\'s teams, women\'s teams and junior teams from under-7s upwards. The open-age season runs mainly from spring to autumn, the opposite of rugby union. That means some players play both codes in the same year.',
             md='''
- **Season:** the main community open-age season runs through the spring and summer. Junior rugby league often runs through the winter as well.
- **Teams:** many ARLFCs field an open-age first team, an "A" team and women's sides.
- **Contact level:** full contact, with six tackles per set. Tag and touch versions are a gentler way to start.
- **Pitfall to avoid:** don't try to join a professional club's first team. Ask its community foundation about local amateur clubs instead.
'''),
    ],
    faqs=[
        ('How many rugby league clubs are there in England?',
         'There are hundreds of amateur rugby league clubs in England, plus the 14 Super League and 20 Championship clubs. Our directory currently lists 101 rugby league clubs.'),
        ('What are the 14 Super League teams in 2026?',
         'Bradford Bulls, Castleford Tigers, Catalans Dragons, Huddersfield Giants, Hull FC, Hull KR, Leeds Rhinos, Leigh Leopards, St Helens, Toulouse Olympique, Wakefield Trinity, Warrington Wolves, Wigan Warriors and York Knights.'),
        ('What happened to the National Conference League?',
         'Its clubs voted in January 2026 to dissolve it. Its divisions became the National Community Rugby League (NCRL) National Leagues, led by a 12-club National Premier League.'),
        ('Can beginners join a rugby league club?',
         'Yes. Amateur clubs welcome newcomers, and tag or touch rugby league is a low-contact way to start. Search this page for a club near you.'),
        ('Are there rugby league clubs in the south of England?',
         'Yes, though fewer. London Broncos and London Skolars are in London, and the NCRL runs a National Conference Southern for amateur clubs.'),
    ],
    related=[('rugby-leagues-uk.html', 'Rugby leagues in the UK'), ('rugby-union.html', 'Rugby union clubs'), ('clubs.html', 'All rugby clubs')],
)

from content import extras as _x  # noqa: E402  (keyword-gap sections added 14 Nov 2026)
for _g, _e in ((HOME, _x.HOME_EXTRA), (CLUBS, _x.CLUBS_EXTRA), (UNION, _x.UNION_EXTRA), (LEAGUE, _x.LEAGUE_EXTRA)):
    _g['sections'] = list(_g['sections']) + _e
    _g['updated'] = _x.UPDATED

PAGES = [HOME, CLUBS, UNION, LEAGUE]
