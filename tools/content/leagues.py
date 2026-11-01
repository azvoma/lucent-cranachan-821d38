"""Long-form content for the two league guide pages (rendered by tools/build_guides.py)."""

UPDATED = '2026-11-01'

RUGBY_LEAGUES_UK = dict(
    slug='rugby-leagues-uk',
    title='Rugby Leagues in the UK: Every League Explained (2026-27)',
    meta='Rugby leagues in the UK explained: PREM Rugby, Super League, Super Rygbi Cymru, the Scottish Premiership and every level below. See where your club plays.',
    h1='Rugby Leagues in the UK: Every League Explained',
    hero_sub='Every men\'s rugby union and rugby league competition across England, Wales, Scotland and Northern Ireland, from the professional game to your local club.',
    crumb='UK Rugby Leagues',
    image='imgs/rugby-union-hero.jpg',
    updated=UPDATED, published='2026-09-23',
    about=['Rugby union', 'Rugby league', 'Premiership Rugby', 'Super League', 'Rugby Football Union', 'Rugby Football League'],
    takeaways=[
        'There are two sets of **rugby leagues in the UK**: rugby union leagues (run by the RFU, WRU, Scottish Rugby and IRFU) and rugby league competitions (run by the RFL). They are different sports with different rules.',
        'The top men\'s rugby union league in England is **PREM Rugby** (10 clubs). Automatic promotion and relegation with Champ Rugby ended in 2026-27, and new clubs now join by meeting set criteria.',
        'Rugby league\'s **Super League** has 14 clubs in 2026. In 2026 the Championship and League One merged into one 20-club second tier, and a new National Community Rugby League now tops the amateur game.',
        'Most rugby is played well below the professional leagues. Of the 267 English clubs in our directory with a confirmed 2026-27 league, 118 (44%) play in the Counties leagues at level 7 and below.',
    ],
    sections=[
        dict(id='overview', h2='What are the rugby leagues in the UK?',
             answer='The UK has separate rugby union and rugby league pyramids. Each union nation runs its own leagues: England, Wales, Scotland, and Ireland (which includes Northern Ireland). The professional Welsh, Scottish and Irish teams also play in the cross-border United Rugby Championship. Rugby league is run by the RFL, with Super League at the top.',
             img=('imgs/rugby-union-hero.webp', 'Rugby union ball carrier in a blue and white kit driving into a tackle during a top-flight UK rugby league match', 1600, 1066),
             md='''
The quickest way to understand **UK rugby leagues** is to start with who runs them. Each governing body runs its own pyramid. Clubs move up or down that pyramid through promotion and relegation, or, at the top of English rugby union and in Super League, by meeting entry criteria.

| Nation / code | Governing body | Top men's competition | Next level down |
|---|---|---|---|
| England – rugby union | Rugby Football Union (RFU) | PREM Rugby (10 clubs) | Champ Rugby |
| England – rugby league | Rugby Football League (RFL) | Super League (14 clubs in 2026) | RFL Championship (20 clubs) |
| Wales – rugby union | Welsh Rugby Union (WRU) | United Rugby Championship (Welsh regions) | Super Rygbi Cymru (10 clubs) |
| Scotland – rugby union | Scottish Rugby | United Rugby Championship (Edinburgh, Glasgow Warriors) | Scottish Premiership (10 clubs) |
| Northern Ireland – rugby union | Irish Rugby Football Union (IRFU) | United Rugby Championship (Ulster) | Energia All-Ireland League |

When people search for "rugby leagues", they usually mean one of three things:

1. **A list of the competitions**, such as the table above.
2. **How the levels fit together**, covered section by section below.
3. **Which league a particular club plays in.** Every club in [our directory](clubs.html) has a profile, and English union clubs show their current league where we could confirm it.
'''),
        dict(id='union-vs-league', h2='Rugby union leagues vs rugby league: what is the difference?',
             answer='Rugby union and rugby league are two different sports that split in 1895. Union is played 15-a-side with contested rucks, lineouts and scrums. League is 13-a-side with a six-tackle limit. Each code has its own clubs, competitions and governing body, so a "rugby union league" and "rugby league" mean different things.',
             md='''
The naming causes real confusion. "Rugby league" is the name of a sport. A "rugby union league" is simply a division in the other sport.

| | Rugby union | Rugby league |
|---|---|---|
| Players per side | 15 | 13 |
| Possession | Contested at rucks and mauls | Six tackles, then a turnover |
| Set pieces | Scrums and lineouts | Scrums (uncontested) and play-the-ball |
| England's governing body | RFU | RFL |
| Heartland | Everywhere, especially the South, Midlands, Wales and Scotland | Yorkshire, Lancashire, Greater Manchester, Cumbria |
| Clubs in our directory | 470 | 101 |

Many towns in the North of England have clubs of both codes. Wigan, Warrington, Leeds and Hull, for example, all have rugby union clubs as well as famous rugby league teams. If you want to play, check the club's profile before you go: the *Sport* field at the top of every directory listing tells you which code it plays.
'''),
        dict(id='england-union', h2='English rugby union leagues (RFU)',
             answer='English men\'s rugby union runs from PREM Rugby at level 1 through Champ Rugby, National League 1 and the three National League 2 divisions. Below those come six Regional 1 leagues, twelve Regional 2 leagues, and county-based Counties leagues from level 7 down. Most community clubs play in Regional or Counties leagues.',
             md='''
| Level | League(s) | Leagues at this level |
|---|---|---|
| 1 | PREM Rugby | 1 |
| 2 | Champ Rugby | 1 |
| 3 | National League 1 | 1 |
| 4 | National League 2 East, North, West | 3 |
| 5 | Regional 1 | 6 |
| 6 | Regional 2 | 12 |
| 7+ | Counties 1, 2, 3 and below | Many, run by the RFU's four divisions |

### What changed in 2026-27

The biggest change is at the top. The RFU Council voted in February 2026 to end automatic promotion and relegation between PREM Rugby and Champ Rugby from the 2026-27 season. A Champ club can now join the top flight only through a criteria-based process. That process looks at:

- on-field performance
- finances
- commercial strength
- stadium
- geographical reach

Below the PREM, promotion and relegation still work in the usual way, with automatic places and play-offs.

For a full level-by-level breakdown with promotion rules and old league names, read our [English rugby union league structure guide](rugby-union-league-structure.html).
'''),
        dict(id='rugby-league-england', h2='Rugby league competitions in England',
             answer='In 2026, men\'s professional rugby league in England has two tiers. Super League has 14 clubs, and the RFL Championship has 20 after it merged with League One. Below them, the National Community Rugby League (NCRL) replaced the National Conference League as the top of the amateur game, with regional men\'s leagues underneath.',
             img=('imgs/rugby-league-hero.webp', 'Rugby league players in action during a Super League match, with a ball carrier in teal breaking between two defenders', 1600, 1060),
             md='''
### Super League

The 14 Super League clubs in 2026 are:

- [Bradford Bulls](club/bradford-bulls.html)
- [Castleford Tigers](club/castleford-tigers.html)
- [Catalans Dragons](club/catalans-dragons.html)
- [Huddersfield Giants](club/huddersfield-giants.html)
- [Hull FC](club/hull-fc.html)
- [Hull KR](club/hull-kingston-rovers.html)
- [Leeds Rhinos](club/leeds-rhinos.html)
- [Leigh Leopards](club/leigh-leopards.html)
- [St Helens](club/st-helens-rfc.html)
- [Toulouse Olympique](club/toulouse-olympique.html)
- [Wakefield Trinity](club/wakefield-trinity.html)
- [Warrington Wolves](club/warrington-wolves.html)
- [Wigan Warriors](club/wigan-warriors.html)
- [York Knights](club/york-knights.html)

The league grew from 12 clubs to 14 for 2026. Places are decided by the RFL's club grading system rather than purely by results. For 2026, Bradford, Toulouse and York joined, and Salford dropped into the Championship.

### Championship

For 2026 the RFL combined the Championship and League One into a single 20-club second tier. It includes former Super League sides such as [Salford Red Devils](club/salford-red-devils.html) and [London Broncos](club/london-broncos.html).

### Community game

In 2026 the National Conference League was dissolved and replaced by the **National Community Rugby League**:

- **National Premier League:** 12 clubs, including [Siddal](club/siddal-arlfc.html), [Heworth](club/heworth-arlfc.html), [Thatto Heath Crusaders](club/thatto-heath-crusaders.html), [West Hull](club/west-hull-arlfc.html), [Wigan St Judes](club/wigan-st-judes.html) and [Castleford Lock Lane](club/castleford-lock-lane.html).
- **National League One** sits below it.
- **Five National Conferences:** Cumbria, North West, Southern, and two Yorkshire divisions.
- **Regional men's leagues** sit below the National Conferences.

In practice, the amateur clubs are where most people play rugby league. Professional clubs rarely run open-age teams for beginners, so if you want to play, start with your nearest amateur (ARLFC) club. Our [rugby league clubs page](rugby-league.html) lists 101 of them.
'''),
        dict(id='wales', h2='Rugby leagues in Wales',
             answer='Welsh rugby union has the professional regions in the United Rugby Championship at the top. Below them is Super Rygbi Cymru, a 10-team semi-professional league that replaced the Welsh Premiership in 2024. Community clubs then play in the Admiral Championship (East and West) and the regional divisions below.',
             md='''
The 10 Super Rygbi Cymru clubs, most now carrying a regional prefix, are:

- Glamorgan Aberavon
- Glamorgan Bridgend Ravens
- Glamorgan Cardiff
- Carmarthen Quins
- Monmouthshire Ebbw Vale
- Llandovery
- Monmouthshire Newport
- Monmouthshire Pontypool
- RGC 1404
- Glamorgan Swansea

Below Super Rygbi Cymru, the Admiral Championship is split into East and West conferences. Under that is Division One, which is split by area: North, East, East Central, West Central and West.

Wales is where our directory is most club-dense outside England. See our [Cardiff rugby clubs](rugby-clubs-cardiff.html) page, or browse [all Welsh clubs](rugby-union.html?region=wales).

**One thing to know:** Welsh club names changed a lot with the creation of Super Rygbi Cymru. Searching for the old name, such as "Cardiff RFC", usually still finds the club.
'''),
        dict(id='scotland', h2='Rugby leagues in Scotland',
             answer='Scotland\'s professional teams, Edinburgh and Glasgow Warriors, play in the United Rugby Championship. The club game is led by the 10-team Scottish Premiership, then National Leagues One to Four (40 clubs). Below those, regional leagues are run by the Caledonia, East and West regions. The semi-professional Super Series ended in 2024.',
             md='''
| Level | Competition | Clubs |
|---|---|---|
| Professional | United Rugby Championship: [Edinburgh Rugby](club/edinburgh-rugby.html), [Glasgow Warriors](club/glasgow-warriors.html) | 2 |
| 1 | Scottish Premiership | 10 |
| 2–5 | National League One to Four | 40 (10 each) |
| 6+ | Regional leagues: Caledonia, East, West | Varies |

The top four in the Premiership play off for the Scottish title. Clubs such as [Boroughmuir](club/boroughmuir-rfc.html) in Edinburgh and the Borders clubs have long been at this level.
'''),
        dict(id='ireland', h2='Rugby leagues in Northern Ireland and Ireland',
             answer='Rugby union in Northern Ireland is run by the IRFU on an all-Ireland basis. Ulster represents the province in the United Rugby Championship. Clubs play in the Energia All-Ireland League. From 2026-27 the lower AIL divisions are reorganised into regional 2B North and 2B South divisions to cut travel.',
             md='''
The men's All-Ireland League runs Division 1A, 1B and 2A. Below those, from 2026-27, come the new regional divisions:

- **2BN (North):** clubs north of a line from Dublin to Galway
- **2BS (South):** clubs south of that line

Below the AIL, clubs play in provincial leagues. For Northern Ireland, that means the Ulster leagues. See our [Ulster Rugby](club/ulster-rugby.html) and [IRFU](club/irfu.html) profiles for more.
'''),
        dict(id='womens', h2='Women\'s rugby leagues in the UK',
             answer='Women\'s rugby has its own pyramid in both codes. In England, Premiership Women\'s Rugby (PWR) is the top union league, with national and regional women\'s leagues below it. In rugby league, the RFL runs the Women\'s Super League. Many community clubs now run a women\'s team as well as men\'s and junior sides.',
             md='''
If you are looking for a women's team, the women's league structure matters less than finding a club with a squad near you. Start with our [women's rugby clubs guide](womens-rugby-clubs.html). It lists clubs with women's sides and explains how to get started.
'''),
        dict(id='find-league', h2='How to find out which league a rugby club plays in',
             answer='Look the club up on its governing body\'s competition site: England Rugby for English union, the WRU, Scottish Rugby or IRFU elsewhere, and the RFL for rugby league. League tables there are official and current. Our directory shows the confirmed league on English union club profiles, with the date we last checked it.',
             md='''
This is the method we used to confirm leagues for our directory. In late October 2026 we checked 321 English club teams this way.

1. **Find the club's profile** in the [UK rugby club directory](clubs.html) and note its exact name and town.
2. **Open the governing body's club finder.** For English union clubs, our profiles link to the club's England Rugby fixtures page.
3. **Check the first XV, not the 2nd or 3rd XV.** Lower teams often play in separate merit or reserve leagues, which can make a club look lower than it is.
4. **Check the season.** Leagues are reorganised every summer, so a table from last season can be wrong by September.
5. **Ignore sponsor names when comparing.** "Regional 1 Tribute Ale South West" and "Regional 1 South West" are the same league.

### Common pitfalls

- **Merit leagues are not part of the pyramid.** The Essex Merit League and Kent Metropolitan League are separate competitions, often for lower teams. There is no promotion from them into the RFU leagues.
- **Old league names still appear online.** "South West 1", "London 1" and "Midlands 1" were replaced in 2022. Our [league structure guide](rugby-union-league-structure.html#old-names) has a conversion table.
- **"Rugby league" in a club name can mislead.** Some union clubs sit in towns famous for rugby league, and the other way round. Always check the code.
'''),
        dict(id='our-data', h2='Where UK clubs actually play: what our directory data shows',
             answer='Most rugby clubs are community clubs, not professional teams. Of the 267 English union clubs in our directory with a confirmed 2026-27 league, only 11 play in Champ Rugby and 8 in National League 1. The rest play at levels 4 to 7 and below, and 118 of them (44%) are in the Counties leagues.',
             md='''
| Level | Clubs in our directory | Share |
|---|---|---|
| Champ Rugby (level 2) | 11 | 4% |
| National League 1 (level 3) | 8 | 3% |
| National League 2 (level 4) | 25 | 9% |
| Regional 1 (level 5) | 42 | 16% |
| Regional 2 (level 6) | 60 | 22% |
| Counties (level 7 and below) | 118 | 44% |
| Merit or other leagues | 3 | 1% |

This matters if you are choosing a club. A Counties or Regional 2 club usually trains twice a week, runs several adult teams and welcomes beginners. A National League club trains more often and recruits more selectively. Neither is better; they suit different players.

*Source: UK Rugby Club Directory. Leagues confirmed from England Rugby team pages on 31 October 2026. Professional PREM clubs are excluded.*
'''),
    ],
    faqs=[
        ('How many rugby leagues are there in the UK?',
         'There is no single number, because each nation and each code runs its own pyramid. English men\'s rugby union alone has 24 leagues across levels 1 to 6: one each at levels 1 to 3, three at level 4, six at level 5 and twelve at level 6. Below that are many more Counties leagues. Rugby league adds Super League, the Championship and the community leagues.'),
        ('What is the top rugby league in England?',
         'For rugby union it is **PREM Rugby**, with 10 clubs. For rugby league it is **Super League**, with 14 clubs in 2026.'),
        ('Is there still promotion and relegation in English rugby?',
         'Yes, below the top flight. From 2026-27 there is no automatic promotion from Champ Rugby to PREM Rugby; clubs must meet entry criteria instead. Every level from Champ Rugby downwards still has promotion and relegation, including play-offs.'),
        ('What happened to League One in rugby league?',
         'It merged with the Championship for the 2026 season, creating a single 20-club second tier below Super League.'),
        ('Which rugby league should a beginner join?',
         'Not a league as such, but a club. Look for a community club at Counties level (union) or an amateur ARLFC (league) near you. Our [find a club](clubs.html) page lists 637 clubs.'),
    ],
    related=[('rugby-union-league-structure.html', 'English rugby union league structure'), ('rugby-union.html', 'Rugby union clubs'),
             ('rugby-league.html', 'Rugby league clubs'), ('clubs.html', 'All UK rugby clubs')],
)


UNION_STRUCTURE = dict(
    slug='rugby-union-league-structure',
    title='English Rugby Union Leagues: RFU Structure 2026-27',
    meta='The English rugby union league structure explained: PREM, Champ, National Leagues, Regional 1 & 2 and Counties leagues, with promotion rules and old names.',
    h1='English Rugby Union League Structure (RFU Leagues 2026-27)',
    hero_sub='Every level of the RFU league pyramid explained, from PREM Rugby to Counties 3, with the promotion rules and the old league names.',
    crumb='Rugby Union League Structure',
    image='imgs/rugby-union-banner.jpg',
    updated=UPDATED, published='2026-09-23',
    about=['Rugby union', 'Rugby Football Union', 'English rugby union system', 'Premiership Rugby', 'National League 1'],
    takeaways=[
        'The **English rugby union league structure** has seven named levels: PREM Rugby, Champ Rugby, National League 1, National League 2 (East, North, West), Regional 1 (6 leagues), Regional 2 (12 leagues) and the Counties leagues.',
        'From **2026-27** there is no automatic promotion into PREM Rugby. Champ clubs must meet entry criteria. Everywhere below, promotion and relegation still apply.',
        'The current names date from the RFU\'s **2022 Adult Competition Review**. Old names such as *South West 1*, *London 1* and *Midlands 1* no longer exist.',
        'Most English clubs play below the national leagues. In our directory, 66% of clubs with a confirmed league play in Regional 2 or the Counties leagues.',
    ],
    sections=[
        dict(id='levels', h2='How the English rugby union league structure works',
             answer='English rugby union is a pyramid of leagues run by the Rugby Football Union (RFU). Each level has more leagues than the one above it, organised by geography. Winners move up and bottom clubs drop down, with play-offs at several levels. The one exception is the top flight, where entry is now based on criteria.',
             img=('imgs/rugby-union-banner.webp', 'Forwards locking together in a rugby union scrum at a community club in the English league structure', 1600, 926),
             md='''
| Level | League | Leagues | Teams per league | Example clubs in our directory |
|---|---|---|---|---|
| 1 | PREM Rugby | 1 | 10 | [Bath](club/bath-rugby.html), [Saracens](club/saracens.html), [Leicester Tigers](club/leicester-tigers.html) |
| 2 | Champ Rugby | 1 | 14 | [Ealing Trailfinders](club/ealing-trailfinders.html), [Bedford Blues](club/bedford-blues.html), [Coventry](club/coventry-rfc.html) |
| 3 | National League 1 | 1 | 14 | [Rosslyn Park](club/rosslyn-park-fc.html), [Plymouth Albion](club/plymouth-albion.html), [Birmingham Moseley](club/birmingham-moseley.html) |
| 4 | National League 2 East / North / West | 3 | 14 | [Barnes](club/barnes-rfc.html), [Fylde](club/fylde-rfc.html), [Clifton](club/clifton-rfc.html) |
| 5 | Regional 1 | 6 | 12 | [Blaydon](club/blaydon-rfc.html), [Hull](club/hull-rufc.html), [Farnham](club/farnham-rfc.html) |
| 6 | Regional 2 | 12 | about 12 | [Cleckheaton](club/cleckheaton-rfc.html), [Durham City](club/durham-city-rfc.html), [Chelmsford](club/chelmsford-rfc.html) |
| 7+ | Counties 1, 2, 3… | Many | Varies | [Ashington](club/ashington-rfc.html), [Basingstoke](club/basingstoke-rfc.html), [Andover](club/andover-rfc.html) |

Levels 1 to 4 are national. From level 5 down, leagues are grouped into the RFU's four geographical divisions:

- Northern
- Midlands
- London & South East
- South West

The lower a league sits, the smaller its area. This keeps travel manageable for amateur players.
'''),
        dict(id='prem', h2='Level 1: PREM Rugby (Premiership Rugby)',
             answer='PREM Rugby, sponsored as Gallagher PREM Rugby, is the top professional league in English rugby union. Its 10 clubs play a regular season followed by play-offs, with the final in June. From 2026-27, relegation is no longer automatic, and new clubs join through a criteria-based expansion process rather than by winning Champ Rugby.',
             md='''
The 10 clubs for 2026-27 are the same as in 2025-26:

- [Bath](club/bath-rugby.html)
- [Bristol Bears](club/bristol-bears.html)
- [Exeter Chiefs](club/exeter-chiefs.html)
- [Gloucester](club/gloucester-rugby.html)
- [Harlequins](club/harlequins.html)
- [Leicester Tigers](club/leicester-tigers.html)
- Newcastle Red Bulls (formerly [Newcastle Falcons](club/newcastle-falcons.html))
- [Northampton Saints](club/northampton-saints.html)
- [Sale Sharks](club/sale-sharks.html)
- [Saracens](club/saracens.html)

The 2026-27 season starts on 25 September 2026, and the final is on 19 June 2027.

**Nuance worth knowing:** the end of automatic promotion does not completely close the league. A club can still be removed if a stronger, financially viable replacement exists. Any Champ club applying must have played at least one season in Champ Rugby.
'''),
        dict(id='champ', h2='Level 2: Champ Rugby',
             answer='Champ Rugby, formerly the RFU Championship, is the second tier. It has 14 professional and semi-professional clubs. The bottom club is relegated to National League 1 and replaced by that league\'s champion. The 12th and 13th-placed clubs face a relegation play-off. Promotion upwards is now by criteria only.',
             md='''
Champ Rugby clubs in our directory include:

- [Ampthill](club/ampthill-rfc.html)
- [Bedford Blues](club/bedford-blues.html)
- [Blackheath](club/blackheath-fc.html)
- [Chinnor](club/chinnor-rfc.html)
- [Cornish Pirates](club/cornish-pirates.html)
- [Coventry](club/coventry-rfc.html)
- [Doncaster Knights](club/doncaster-knights.html)
- [Ealing Trailfinders](club/ealing-trailfinders.html)
- [Hartpury](club/hartpury-rfc.html)
- [Nottingham](club/nottingham-rfc.html)
- [Richmond](club/richmond-rfc.html)

Champ squads are mostly full-time or part-time professionals, so these clubs are rarely where a new adult player starts. Most do run thriving community and junior sections alongside the first team.
'''),
        dict(id='national-leagues', h2='Levels 3 and 4: National League 1 and National League 2',
             answer='National League 1 is a single 14-team league at level 3. The champion goes straight up to Champ Rugby, and the 2nd and 3rd-placed clubs play off for a second chance. Level 4 has three 14-team leagues: National League 2 East, North and West. Clubs are placed in one by location.',
             md='''
### National League 1 promotion and relegation (2026-27)

- **1st:** promoted to Champ Rugby.
- **2nd v 3rd:** play-off. The winner meets the 13th-placed Champ club for a place in Champ Rugby.
- **11th:** enters a four-team play-off with the runners-up of the three National League 2 divisions.
- **12th, 13th, 14th:** relegated to National League 2 East, North or West, depending on location.

### National League 2

The three level-4 leagues replaced National League 2 North and South in 2022. Each club plays 26 league games, home and away.

Clubs in our directory at this level include:

- [Barnes](club/barnes-rfc.html)
- [Chester](club/chester-rfc.html)
- [Cinderford](club/cinderford-rfc.html)
- [Clifton](club/clifton-rfc.html)
- [Esher](club/esher-rfc.html)
- [Harrogate](club/harrogate-rfc.html)
- [Havant](club/havant-rfc.html)
'''),
        dict(id='regional', h2='Levels 5 and 6: Regional 1 and Regional 2 leagues',
             answer='Regional 1 is level 5, with six leagues of 12 teams: Midlands, North East, North West, South Central, South East and South West. Regional 2 is level 6, with twelve leagues. This is where many large community clubs play: amateur, well organised, and usually with several senior teams.',
             md='''
**Regional 1 (level 5), six leagues:**

- Regional 1 Midlands
- Regional 1 North East
- Regional 1 North West
- Regional 1 South Central
- Regional 1 South East
- Regional 1 South West

**Regional 2 (level 6), twelve leagues:**

- Anglia
- Midlands East
- Midlands North
- Midlands West
- North
- North East
- North West
- Severn
- South Central
- South East
- South West
- Thames

In the South West, these leagues carry the *Tribute Ale* sponsor name, for example "Regional 1 Tribute Ale South West". It is the same league.

The number of level-5 leagues went up from four to six in 2022. The leagues also got smaller: Regional 1 Midlands, for example, went from 14 teams to 12. The aim was shorter journeys and fewer mismatched games.
'''),
        dict(id='counties', h2='Level 7 and below: the Counties leagues',
             answer='Below Regional 2, the Counties leagues run from Counties 1 at level 7 downwards. They are organised by county or group of counties, for example Counties 1 Kent or Counties 2 Yorkshire. This is where most English clubs play. In our directory, 118 of 267 clubs with a confirmed league play in a Counties league.',
             md='''
Examples of the Counties leagues our directory clubs play in this season:

- **Northern Division:** Counties 1 Yorkshire, Counties 1 North East, Counties 1 Cumbria, Counties 1 Lancashire & Cheshire
- **Midlands Division:** Counties 1 Midlands East (North/South), Counties 1 Midlands West (North/South)
- **London & SE Division:** Counties 1 Kent, Counties 1 Hampshire, Counties 1 Herts, Counties 1 Middlesex, Counties 1 Surrey/Sussex, Counties 1 Eastern Counties
- **South West Division:** Counties 1 Southern North and South, Counties 1 Western North and West

Counties 2 and 3 split the same areas more finely. For example, Counties 2 Berks/Bucks & Oxon has East and West leagues.

**Practical tip:** if you are new to rugby, a Counties club is usually the friendliest place to start. The standard varies widely, but most clubs at this level field a 2nd or 3rd XV where beginners get regular games.
'''),
        dict(id='old-names', h2='Old rugby union league names vs new (2022 changes)',
             answer='The RFU renamed and reshaped levels 4 to 7 in the 2022 Adult Competition Review. National League 2 North and South became three leagues (East, North, West). The old level-5 "Premier" leagues became Regional 1, the level-6 "1" leagues became Regional 2, and county leagues became Counties 1, 2 and 3.',
             md='''
| Level | Before 2022-23 | From 2022-23 |
|---|---|---|
| 4 | National League 2 North, National League 2 South | National League 2 East, North, West |
| 5 | Four leagues, e.g. South West Premier, Midlands Premier, London & SE Premier, North Premier | Six Regional 1 leagues |
| 6 | e.g. South West 1 East/West, Midlands 1 East/West, London 1 North/South, North 1 East/West | Twelve Regional 2 leagues |
| 7+ | e.g. South West 2, Midlands 2, London 2, Yorkshire 1, county leagues | Counties 1, 2, 3… |

Clubs were reallocated on geography as well as level, so a club from the old "South West 1 East" did not necessarily go into a league with the same name. To see where a club plays today, check its profile in our [directory](clubs.html).
'''),
        dict(id='promotion', h2='How promotion and relegation work in practice',
             answer='Promotion and relegation are decided on league points. In most RFU leagues that means 4 for a win and 2 for a draw, plus bonus points for four or more tries or losing by seven or fewer. Champions usually go up automatically, with play-offs at several levels.',
             md='''
In practice, these are the things that catch clubs and supporters out:

1. **Bonus points matter.** A losing bonus point in March can decide a title in April.
2. **Geography can move you sideways.** A promoted club may join a league with a different regional name from the one it expected.
3. **Restructures override results.** When the RFU changes the number of leagues, as in 2022, some clubs move without being promoted or relegated.
4. **Ring-fencing at the top.** From 2026-27 the step from Champ Rugby to PREM Rugby is by application, not by finishing first.
5. **Lower teams play elsewhere.** 2nd and 3rd XVs usually play in merit or reserve leagues that sit outside the pyramid.
'''),
        dict(id='find', h2='How to find a club at the right level for you',
             answer='Pick a level that matches how often you can train and how competitive you want to be. Then shortlist clubs near you in our directory and check each club\'s confirmed league on its profile. Contact two or three of them before you choose, and ask how many adult teams they run.',
             md='''
- **Up to 2 sessions a week, social or new to rugby:** look for a Counties club, especially one with a 2nd or 3rd XV.
- **Experienced, want competitive Saturday rugby:** look at Regional 1 and 2 clubs.
- **Ex-academy or university first-team player:** National League clubs are the likeliest fit.

Browse by area on our county pages, for example [Kent](rugby-clubs-kent.html), [Hampshire](rugby-clubs-hampshire.html) or [Surrey](rugby-clubs-surrey.html). You can also see every [rugby union club in the UK](rugby-union.html).
'''),
    ],
    faqs=[
        ('What are the levels of English rugby union?',
         'Level 1 is PREM Rugby, level 2 is Champ Rugby, level 3 is National League 1 and level 4 is National League 2 (East, North and West). Level 5 is Regional 1 (six leagues), level 6 is Regional 2 (twelve leagues), and Counties 1, 2 and 3 run from level 7 downwards.'),
        ('How many RFU leagues are there?',
         'There are 24 leagues at levels 1 to 6: one each at levels 1 to 3, three at level 4, six at level 5 and twelve at level 6. There are dozens more Counties leagues below that, run by the RFU\'s four geographical divisions.'),
        ('Is there relegation from the Premiership?',
         'Not automatically. From 2026-27 the RFU ended automatic promotion and relegation between PREM Rugby and Champ Rugby. A club could still be replaced if a stronger, financially viable candidate meets the entry criteria.'),
        ('What league is South West 1 now?',
         'South West 1 East and West were level-6 leagues. Since the 2022 restructure, level 6 in the South West is covered by Regional 2 South West and Regional 2 Severn (sponsored as Tribute Ale). Individual clubs were reallocated by location, so check a club\'s profile for its current league.'),
        ('What does "Counties 1" mean in rugby?',
         'Counties 1 is level 7 of the English rugby union pyramid, the highest of the county-based leagues. Examples include Counties 1 Kent, Counties 1 Yorkshire and Counties 1 Surrey/Sussex.'),
    ],
    related=[('rugby-leagues-uk.html', 'All UK rugby leagues'), ('rugby-union.html', 'Rugby union clubs UK'),
             ('clubs.html', 'Find a rugby club'), ('junior-youth-rugby-clubs.html', 'Junior and youth rugby')],
)
