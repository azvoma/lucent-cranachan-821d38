"""
Long-form guide sections for city / county hub pages (applied by tools/apply_hub_guides.py).

Facts about leagues come from England Rugby team pages checked on 31 Oct 2026
(tools/er-teams.csv); founding years and towns come from tools/clubs.json.
FAQs stay in each hub's existing FAQ section, so guides here have none.
"""

U = '2026-11-01'

HUB_GUIDES = {
    'rugby-clubs-leeds': dict(
        title='Rugby Clubs in Leeds: Union &amp; League Teams Near You',
        meta='Rugby clubs in Leeds: compare Leeds rugby union and rugby league teams, from Leeds Rhinos to East Leeds ARLFC, Otley and Morley. Find a club near you.',
        h1='Rugby Clubs in Leeds',
        takeaways=[
            '**Rugby clubs in Leeds** play both codes. Our directory lists 17 clubs in and around the city: 10 rugby league and 7 rugby union.',
            'Rugby league dominates inside the city, from [Leeds Rhinos](club/leeds-rhinos.html) in Super League to amateur clubs such as [East Leeds](club/east-leeds-arlfc.html), [West Leeds](club/west-leeds-arlfc.html) and [Stanningley](club/stanningley-arlfc.html).',
            'The strongest **Leeds rugby union** clubs are just outside the city: [Otley](club/otley-rfc.html) and [Wharfedale](club/wharfedale-rfc.html) play in National League 2 North.',
        ],
        sections=[
            dict(id='leeds-union', h2='Leeds rugby union clubs',
                 answer='Rugby union clubs in Leeds range from National League 2 North sides in Otley and Wharfedale to community clubs in Morley, Headingley and north-west Leeds. If you want competitive Saturday rugby union, look at Otley, Wharfedale, Ilkley or Morley. For a friendly first club, look at Roundhegians, Bramley Phoenix or Aireborough.',
                 md='''
| Club | Area | Founded | League 2026-27 |
|---|---|---|---|
| [Otley RFC](club/otley-rfc.html) | Otley | 1865 | National League 2 North |
| [Wharfedale RFC](club/wharfedale-rfc.html) | Upper Wharfedale | 1923 | National League 2 North |
| [Ilkley RFC](club/ilkley-rfc.html) | Ilkley | 1895 | Regional 1 North East |
| [Morley RFC](club/morley-rfc.html) | Morley | 1878 | Regional 2 North East |
| [Roundhegians RFC](club/roundhegians-rfc.html) | Leeds | 1951 | Counties 2 Yorkshire B |
| [Bramley Phoenix RUFC](club/bramley-phoenix.html) | Bramley, Leeds | 1970 | Counties 2 Yorkshire B |
| [Aireborough RFC](club/aireborough-rfc.html) | Guiseley | 1921 | Counties 4 Yorkshire B |

*Leagues confirmed from England Rugby team pages on 31 October 2026.*

**A common mix-up:** searches for "Leeds rugby union" often bring up Leeds Rhinos, who play rugby *league*. If you want the 15-a-side game, use the union clubs in the table above.
'''),
            dict(id='leeds-league', h2='Rugby league clubs in Leeds',
                 answer='Leeds is one of rugby league\'s heartlands. Leeds Rhinos play in Super League at Headingley, and Hunslet RLFC play in the RFL Championship. A strong amateur scene includes East Leeds, West Leeds, Stanningley, Bramley Buffaloes, Hunslet Warriors, Oulton Raiders and Kippax Welfare, which is where new players start.',
                 md='''
| Club | Area | Founded | Level |
|---|---|---|---|
| [Leeds Rhinos](club/leeds-rhinos.html) | Headingley | 1890 | Super League (professional) |
| [Hunslet RLFC](club/hunslet-rlfc.html) | Hunslet | 1883 | RFL Championship |
| [East Leeds ARLFC](club/east-leeds-arlfc.html) | East Leeds | 1903 | Amateur |
| [Stanningley ARLFC](club/stanningley-arlfc.html) | Stanningley | 1923 | Amateur |
| [Oulton Raiders ARLFC](club/oulton-raiders-arlfc.html) | Oulton | 1932 | Amateur |
| [Bramley Buffaloes ARLFC](club/bramley-buffaloes-arlfc.html) | Bramley | 1949 | Amateur |
| [West Leeds ARLFC](club/west-leeds-arlfc.html) | West Leeds | 1963 | Amateur |
| [Hunslet Warriors ARLFC](club/hunslet-warriors.html) | Hunslet | 1964 | Amateur |
| [Kippax Welfare ARLFC](club/kippax-welfare-arlfc.html) | Kippax | 1929 | Amateur |

**Playing tip:** Leeds Rhinos do not run open-age teams for the public. To play rugby league in Leeds, contact one of the amateur clubs above. Most also run large junior sections. The amateur open-age season runs mainly through spring and summer.
'''),
            dict(id='leeds-choose', h2='Choosing between Leeds rugby teams',
                 answer='Choose a Leeds rugby team by code first, then by distance and training night. North and west Leeds have most of the rugby union clubs. East and south Leeds are rugby league territory. Contact two clubs, go to training, and pick the one where the coaching and the people suit you.',
                 md='''
1. **North-west Leeds, Otley, Ilkley, Guiseley:** mostly rugby union.
2. **East and south Leeds, Hunslet, Kippax, Oulton:** mostly rugby league.
3. **West Leeds, Bramley, Stanningley:** both codes within a couple of miles.

For clubs across the wider county, see our [rugby league clubs](rugby-league.html) list and [Yorkshire rugby union clubs](rugby-union.html?region=yorkshire). Halifax ([Siddal](club/siddal-arlfc.html)), Castleford and Wakefield are all within half an hour.
'''),
        ]),
    'rugby-clubs-birmingham': dict(
        title='Rugby Clubs in Birmingham &amp; Solihull: Teams Near You',
        meta='Rugby clubs in Birmingham and Solihull: compare Birmingham Moseley, Bournville, Sutton Coldfield, Solihull and more. See leagues and find a rugby team near you.',
        h1='Rugby Clubs in Birmingham',
        takeaways=[
            '**Rugby clubs in Birmingham** are mostly rugby union. The highest-ranked is [Birmingham Moseley](club/birmingham-moseley.html) in National League 1, followed by [Bournville](club/bournville-rfc.html) in National League 2 West.',
            'Solihull, Sutton Coldfield, Stourbridge, Halesowen and Kingswinford all have clubs within 30 minutes of the city centre.',
            'For rugby league, the nearest club in our directory is [Midlands Hurricanes](club/midlands-hurricanes.html) in Coventry.',
        ],
        sections=[
            dict(id='bham-clubs', h2='Rugby teams in Birmingham by level',
                 answer='Birmingham\'s rugby teams cover every level of the English game. Birmingham Moseley play in National League 1 and Bournville in National League 2 West. Stourbridge are in Regional 1 Midlands and Sutton Coldfield in Regional 2 Midlands North. Community clubs such as Camp Hill, Harborne and Birmingham & Solihull play in the Counties leagues.',
                 md='''
| Club | Area | Founded | League 2026-27 |
|---|---|---|---|
| [Birmingham Moseley](club/birmingham-moseley.html) | Moseley | 1873 | National League 1 |
| [Bournville RFC](club/bournville-rfc.html) | Bournville | 1909 | National League 2 West |
| [Stourbridge RFC](club/stourbridge-rfc.html) | Stourbridge | 1876 | Regional 1 Midlands |
| [Sutton Coldfield RFC](club/sutton-coldfield-rfc.html) | Sutton Coldfield | 1921 | Regional 2 Midlands North |
| [Dudley Kingswinford RFC](club/dudley-kingswinford-rfc.html) | Kingswinford | 1887 | Regional 2 Midlands West |
| [Camp Hill RFC](club/camp-hill-rfc.html) | Shirley | 1893 | Counties 1 Midlands West (South) |
| [Old Halesonians RFC](club/old-halesonians-rfc.html) | Halesowen | 1953 | Counties 1 Midlands West (North) |
| [Birmingham & Solihull RFC](club/birmingham-solihull-rfc.html) | Birmingham | – | Counties 2 Midlands West (East) |
| [Harborne RFC](club/harborne-rfc.html) | Harborne | 1928 | Counties 3 Midlands West (South) |

*Leagues confirmed from England Rugby team pages on 31 October 2026.*
'''),
            dict(id='solihull', h2='Rugby clubs in Solihull',
                 answer='Solihull has three clubs in our directory: Solihull RFC (founded 1924), Edwardian FC (founded 1882) and Camp Hill RFC in Shirley (founded 1893). Camp Hill plays in Counties 1 Midlands West (South). All three are community clubs with adult and junior sections, and they are the closest options for south Birmingham.',
                 md='''
- [Solihull RFC](club/solihull-rfc.html): the town's rugby club, founded 1924.
- [Edwardian FC](club/edwardian-fc.html): despite the "FC", a rugby union club, founded 1882.
- [Camp Hill RFC](club/camp-hill-rfc.html): Shirley, on the Solihull–Birmingham border.

Further east, Warwickshire clubs such as [Kenilworth](club/kenilworth-rfc.html) and [Leamington](club/leamington-rfc.html) are an easy drive. See our [Warwickshire rugby clubs](rugby-clubs-warwickshire.html) page.
'''),
            dict(id='bham-start', h2='Starting rugby in Birmingham',
                 answer='Most Birmingham clubs welcome adult beginners. Start with a club that runs a 2nd or 3rd XV, because you will get regular games while you learn. Many West Midlands clubs also run touch rugby sessions in spring and summer, which is a low-risk way to try the sport.',
                 md='''
- **Getting there:** clubs in Moseley, Bournville and Harborne are reachable by train or bus from the city centre. Sutton Coldfield and Solihull are easier by car.
- **Levels:** if you have played before, the National League clubs train three or more times a week. Counties clubs usually train twice.
- **Pitfall:** "Moseley" appears in two listings in our directory, the historic Moseley club and [Birmingham Moseley](club/birmingham-moseley.html), its current senior side. Check the profile for the right contact.
'''),
        ]),
    'rugby-clubs-bristol': dict(
        title='Rugby Clubs in Bristol: Find a Rugby Team Near You',
        meta='Rugby clubs in Bristol: Bristol Bears, Dings Crusaders, Clifton, Old Redcliffians, Cleve and more. Compare Bristol rugby teams and their leagues.',
        h1='Rugby Clubs in Bristol',
        takeaways=[
            '**Rugby clubs in Bristol** are all rugby union. Our directory lists clubs from PREM side [Bristol Bears](club/bristol-bears.html) down to community sides such as [Avonmouth Old Boys](club/avonmouth-old-boys-rfc.html).',
            'Bristol is unusually strong below the professional game. [Dings Crusaders](club/dings-crusaders-rfc.html) play in National League 1, and [Clifton](club/clifton-rfc.html) and [Old Redcliffians](club/old-redcliffians-rfc.html) in National League 2 West.',
            'For women\'s rugby, [Bristol Bears Women](club/bristol-bears-women.html) play in Premiership Women\'s Rugby.',
        ],
        sections=[
            dict(id='bristol-teams', h2='Bristol rugby teams and their leagues',
                 answer='Bristol has rugby union at every level. Bristol Bears play in PREM Rugby and Dings Crusaders in National League 1. Clifton and Old Redcliffians play in National League 2 West, Cleve in Regional 2 Severn, and Avonmouth Old Boys in the Counties leagues. Bristol Harlequins complete the city\'s community club scene.',
                 md='''
| Club | Area | Founded | League 2026-27 |
|---|---|---|---|
| [Bristol Bears](club/bristol-bears.html) | Ashton Gate | 1888 | PREM Rugby |
| [Dings Crusaders RFC](club/dings-crusaders-rfc.html) | Bristol | 1897 | National League 1 |
| [Clifton RFC](club/clifton-rfc.html) | Bristol | 1872 | National League 2 West |
| [Old Redcliffians RFC](club/old-redcliffians-rfc.html) | Bristol | 1918 | National League 2 West |
| [Cleve RFC](club/cleve-rfc.html) | Mangotsfield | 1922 | Regional 2 Severn |
| [Avonmouth Old Boys RFC](club/avonmouth-old-boys-rfc.html) | Avonmouth | 1897 | Counties 3 Gloucestershire South |
| [Bristol Harlequins RFC](club/bristol-harlequins-rfc.html) | Bristol | 1946 | – |

*Leagues confirmed from England Rugby team pages on 31 October 2026. Sponsor names (Tribute Ale) omitted.*
'''),
            dict(id='bristol-choose', h2='How to pick a rugby club in Bristol',
                 answer='Pick a Bristol rugby club by how competitive you want to be and which side of the city you live on. Dings, Clifton and Old Redcliffians suit experienced players. Cleve, Avonmouth and Bristol Harlequins are good for newcomers. Clubs in north and east Bristol are easier to reach from the M32 and M4.',
                 md='''
Nearby areas worth comparing:

- **Bath and north Somerset:** see [rugby clubs in Somerset](rugby-clubs-somerset.html).
- **South Gloucestershire and Gloucester:** see [Gloucestershire rugby clubs](rugby-clubs-gloucestershire.html).
- **The wider region:** see [South West rugby clubs](south-west-rugby-clubs.html).
'''),
        ]),
    'rugby-clubs-cardiff': dict(
        title='Rugby Clubs in Cardiff: Cardiff Rugby Teams &amp; Clubs',
        meta='Rugby clubs in Cardiff: Cardiff Rugby, Cardiff RFC, Glamorgan Wanderers, Llanishen, Rumney, St Peter\'s and Cardiff Met. Find a Cardiff rugby team near you.',
        h1='Rugby Clubs in Cardiff',
        takeaways=[
            '**Rugby clubs in Cardiff** run from [Cardiff Rugby](club/cardiff-rugby.html) in the United Rugby Championship to community clubs in Llanishen, Rumney and Roath.',
            '[Cardiff RFC](club/cardiff-rfc.html), founded in 1876, now plays in Super Rygbi Cymru, the semi-professional league below the regions, as Glamorgan Cardiff.',
            'For students, [Cardiff Metropolitan University RFC](club/cardiff-met-rfc.html) is one of Welsh university rugby\'s best-known sides.',
        ],
        sections=[
            dict(id='cardiff-teams', h2='Cardiff rugby teams at a glance',
                 answer='Cardiff\'s rugby teams sit at three levels. Cardiff Rugby are the professional region in the United Rugby Championship. Cardiff RFC (Glamorgan Cardiff) play in Super Rygbi Cymru. Community clubs such as Glamorgan Wanderers, Llanishen, Rumney and St Peter\'s play in the WRU\'s community leagues, and they are where most local players start.',
                 md='''
| Club | Area | Founded | Level |
|---|---|---|---|
| [Cardiff Rugby](club/cardiff-rugby.html) | Cardiff Arms Park | 1876 | United Rugby Championship |
| [Cardiff RFC](club/cardiff-rfc.html) | Cardiff Arms Park | 1876 | Super Rygbi Cymru |
| [Glamorgan Wanderers RFC](club/glamorgan-wanderers-rfc.html) | Ely | 1893 | WRU community leagues |
| [St Peter's RFC](club/st-peters-rfc.html) | Roath | 1886 | WRU community leagues |
| [Llanishen RFC](club/llanishen-rfc.html) | Llanishen | 1962 | WRU community leagues |
| [Rumney RFC](club/rumney-rfc.html) | Rumney | – | WRU community leagues |
| [Cardiff Met RFC](club/cardiff-met-rfc.html) | Cyncoed | – | University and WRU leagues |
'''),
            dict(id='cardiff-join', h2='Joining a rugby club in Cardiff',
                 answer='To join a rugby club in Cardiff, choose a community club near where you live: Llanishen and Rumney in the north and east, St Peter\'s in Roath, or Glamorgan Wanderers in the west. Contact the club through its profile and go along to training. Welsh community clubs usually train on Tuesday and Thursday evenings.',
                 md='''
**Local insight:** Welsh club rugby is deeply tied to its communities. Clubhouses are social hubs on match days, and many clubs run large mini and junior sections from age six.

**Watch out for the name:** "Cardiff Rugby" (the region) and "Cardiff RFC" (the club) are separate teams that share Cardiff Arms Park. Check which one you mean before contacting them.

For the rest of Wales, browse [Welsh rugby clubs](rugby-union.html?region=wales) or read how the [Welsh leagues](rugby-leagues-uk.html#wales) work.
'''),
        ]),
    'rugby-clubs-hull': dict(
        title='Hull Rugby Teams &amp; Clubs: Rugby League and Union in Hull',
        meta='Hull rugby teams: Hull FC and Hull KR in Super League, amateur clubs like West Hull and East Hull, and Hull RUFC for rugby union. Compare Hull rugby clubs.',
        h1='Hull Rugby Teams &amp; Clubs',
        takeaways=[
            '**Hull rugby teams** are led by two Super League clubs: [Hull FC](club/hull-fc.html) and [Hull KR](club/hull-kingston-rovers.html), who won the 2025 Grand Final.',
            'Amateur rugby league is strong. [West Hull](club/west-hull-arlfc.html) play in the 2026 NCRL National Premier League, alongside [East Hull](club/east-hull-arlfc.html), [Hull Dockers](club/hull-dockers-arlfc.html) and [Myton Warriors](club/myton-warriors-arlfc.html).',
            'For rugby union, [Hull RUFC](club/hull-rufc.html) (founded 1865) and [Driffield](club/driffield-rfc.html) play in Regional 1 North East.',
        ],
        sections=[
            dict(id='hull-league', h2='Rugby league clubs in Hull',
                 answer='Hull is split between two professional rugby league clubs: Hull FC from the west of the city and Hull KR from the east. Below them, amateur clubs such as West Hull, East Hull, Hull Dockers, Myton Warriors and Skirlaugh run open-age and junior teams. West Hull play at the top amateur level, the NCRL National Premier League.',
                 md='''
| Club | Founded | Level (2026) |
|---|---|---|
| [Hull FC](club/hull-fc.html) | 1865 | Super League |
| [Hull Kingston Rovers](club/hull-kingston-rovers.html) | 1883 | Super League |
| [West Hull ARLFC](club/west-hull-arlfc.html) | 1949 | NCRL National Premier League |
| [East Hull ARLFC](club/east-hull-arlfc.html) | 1920 | Amateur |
| [Hull Dockers ARLFC](club/hull-dockers-arlfc.html) | 1958 | Amateur |
| [Myton Warriors ARLFC](club/myton-warriors-arlfc.html) | 1962 | Amateur |
| [Skirlaugh ARLFC](club/skirlaugh-arlfc.html) | 1948 | Amateur |
| [Beverley ARLFC](club/beverley-arlfc.html) | 1950 | Amateur |
'''),
            dict(id='hull-union', h2='Hull rugby union clubs',
                 answer='Hull RUFC is the city\'s main rugby union club, founded in 1865 and now playing in Regional 1 North East. Around the city, Hessle, Beverley, Driffield, Bridlington and Goole all have union clubs. Driffield is also in Regional 1 North East, and Bridlington and Goole are in Counties 1 Yorkshire.',
                 md='''
| Club | Town | League 2026-27 |
|---|---|---|
| [Hull RUFC](club/hull-rufc.html) | Hull | Regional 1 North East |
| [Driffield RFC](club/driffield-rfc.html) | Driffield | Regional 1 North East |
| [Bridlington RFC](club/bridlington-rfc.html) | Bridlington | Counties 1 Yorkshire |
| [Goole RFC](club/goole-rfc.html) | Goole | Counties 1 Yorkshire |
| [Beverley RUFC](club/beverley-rufc.html) | Beverley | Counties 2 Yorkshire A |
| [Hessle RFC](club/hessle-rfc.html) | Hessle | – |

*Leagues confirmed from England Rugby team pages on 31 October 2026.*
'''),
        ]),
    'rugby-clubs-surrey': dict(
        title='Rugby Clubs in Surrey: Find a Surrey Rugby Club',
        meta='Rugby clubs in Surrey: Richmond, Esher, Dorking, Farnham, Guildford, Camberley, Sutton &amp; Epsom and more, with their 2026-27 leagues. Find a club near you.',
        h1='Rugby Clubs in Surrey',
        takeaways=[
            '**Rugby clubs in Surrey** are all rugby union. Our directory lists 14, from [Richmond](club/richmond-rfc.html) in Champ Rugby to village clubs such as [Cranleigh](club/cranleigh-rfc.html) and [Haslemere](club/haslemere-rfc.html).',
            'Surrey is strong at National League level: [Esher](club/esher-rfc.html), [Dorking](club/dorking-rfc.html) and [London Welsh](club/london-welsh-rfc.html) all play in National League 2 East.',
            'Around Guildford there are two clubs: [Guildford RFC](club/guildford-rfc.html) (Regional 2 South Central) and [Guildford & Godalming RFC](club/guildford-godalming-rfc.html).',
        ],
        sections=[
            dict(id='surrey-levels', h2='Surrey rugby clubs by league',
                 answer='Surrey rugby clubs cover every level of the community game. Richmond play in Champ Rugby. Esher, Dorking and London Welsh are in National League 2 East, and Farnham in Regional 1 South Central. Guildford and Camberley are in Regional 2 South Central and Sutton & Epsom in Regional 2 South East, with village clubs in the Counties leagues.',
                 md='''
| Club | Town | Founded | League 2026-27 |
|---|---|---|---|
| [Richmond RFC](club/richmond-rfc.html) | Richmond | 1861 | Champ Rugby |
| [Esher RFC](club/esher-rfc.html) | Esher | 1923 | National League 2 East |
| [Dorking RFC](club/dorking-rfc.html) | Dorking | 1921 | National League 2 East |
| [London Welsh RFC](club/london-welsh-rfc.html) | Richmond | 1885 | National League 2 East |
| [Farnham RFC](club/farnham-rfc.html) | Farnham | 1891 | Regional 1 South Central |
| [Guildford RFC](club/guildford-rfc.html) | Guildford | 1922 | Regional 2 South Central |
| [Camberley RFC](club/camberley-rfc.html) | Camberley | 1929 | Regional 2 South Central |
| [Sutton & Epsom RFC](club/sutton-epsom-rfc.html) | Sutton | 1920 | Regional 2 South East |
| [London Cornish RFC](club/london-cornish-rfc.html) | Richmond | 1962 | Counties 1 Surrey/Sussex |
| [Cranleigh RFC](club/cranleigh-rfc.html) | Cranleigh | 1921 | Counties 3 Surrey |
| [Haslemere RFC](club/haslemere-rfc.html) | Haslemere | 1930 | Counties 3 Surrey |

*Leagues confirmed from England Rugby team pages on 31 October 2026.*

Also in Surrey: [Reigate & Redhill](club/reigate-redhill-rfc.html), [Walton on Thames](club/walton-on-thames-rfc.html) and [Guildford & Godalming](club/guildford-godalming-rfc.html).
'''),
            dict(id='surrey-near', h2='Surrey rugby near the London and Sussex borders',
                 answer='North Surrey clubs such as Richmond, London Welsh and Esher are effectively part of the London rugby scene. Clubs in the south of the county, around Reigate, Cranleigh and Haslemere, are closer to Sussex. If you live near a county border, compare our London and Sussex pages as well, because the nearest club may be over the line.',
                 md='''
- [Rugby clubs in London](rugby-clubs-london.html)
- [Rugby clubs in Sussex](rugby-clubs-sussex.html)
- [Rugby clubs in Hampshire](rugby-clubs-hampshire.html), for the Farnham and Camberley side
'''),
        ]),
    'south-west-rugby-clubs': dict(
        title='South West Rugby: Clubs in Devon, Cornwall &amp; Somerset',
        meta='South West rugby clubs: find a club in Devon, Cornwall, Somerset, Bristol, Gloucestershire, Dorset and Wiltshire, with each club\'s 2026-27 league.',
        h1='South West Rugby Clubs',
        takeaways=[
            '**South West rugby** has more clubs per head than almost anywhere in England. Our directory lists over 75 South West clubs across seven counties.',
            'The region has three PREM clubs ([Bath](club/bath-rugby.html), [Bristol Bears](club/bristol-bears.html), [Exeter Chiefs](club/exeter-chiefs.html)) plus [Gloucester](club/gloucester-rugby.html). Below them are [Cornish Pirates](club/cornish-pirates.html) and [Hartpury](club/hartpury-rfc.html) in Champ Rugby.',
            'Community leagues in the South West carry the **Tribute Ale** sponsor name. Regional 1 Tribute Ale South West is the top regional league.',
        ],
        sections=[
            dict(id='sw-counties', h2='England South West rugby by county',
                 answer='England\'s South West rugby clubs fall under the RFU\'s South West Division, which covers Cornwall, Devon, Somerset, Gloucestershire, Bristol, Dorset, Wiltshire and the Berks/Bucks & Oxon area. Devon and Cornwall have the most clubs in our directory, with strong community sides in nearly every town.',
                 md='''
| County | Clubs in our directory | Highest-ranked community clubs (2026-27) |
|---|---|---|
| Devon | 22 | [Plymouth Albion](club/plymouth-albion.html) (National League 1), [Barnstaple](club/barnstaple-rfc.html) (NL2 West) |
| Cornwall | 16 | [Camborne](club/camborne-rfc.html) (National League 1), [Redruth](club/redruth-rfc.html) (NL2 West) |
| Bristol | 11 | [Dings Crusaders](club/dings-crusaders-rfc.html) (National League 1), [Clifton](club/clifton-rfc.html) (NL2 West) |
| Somerset | 9 | [Taunton](club/taunton-rfc.html) (NL2 West) |
| Gloucestershire | 8 | [Cinderford](club/cinderford-rfc.html) (NL2 West), [Cleve](club/cleve-rfc.html) (Regional 2 Severn) |
| Dorset | 6 | [Bournemouth](club/bournemouth-rfc.html) (Regional 1 South Central) |
| Wiltshire | 5 | [Trowbridge](club/trowbridge-rfc.html) (Regional 1 South West) |
'''),
            dict(id='sw-leagues', h2='South West rugby leagues explained',
                 answer='South West clubs play in Regional 1 South West at level 5, then Regional 2 South West and Regional 2 Severn at level 6. Below that are the Counties leagues, such as Counties 1 Western West and Counties 2 Cornwall. All are sponsored by Tribute Ale. The old "South West 1" and "South West Premier" names were retired in 2022.',
                 md='''
Clubs in our directory currently in **Regional 1 Tribute Ale South West** include:

- [Brixham](club/brixham-rfc.html)
- [Exmouth](club/exmouth-rfc.html)
- [Sidmouth](club/sidmouth-rfc.html)
- [Launceston](club/launceston-rfc.html)
- [St Austell](club/st-austell-rfc.html)
- [Trowbridge](club/trowbridge-rfc.html)

For how these leagues fit the national pyramid, see the [English rugby union league structure](rugby-union-league-structure.html).

County pages for the region: [Bristol](rugby-clubs-bristol.html) · [Somerset](rugby-clubs-somerset.html) · [Gloucestershire](rugby-clubs-gloucestershire.html)
'''),
        ]),
    'rugby-clubs-kent': dict(
        takeaways=[
            '**Rugby clubs in Kent** are all rugby union. Our directory lists 11, from [Tonbridge Juddians](club/tonbridge-juddians-rfc.html) in National League 1 to town clubs along the coast.',
            '[Canterbury](club/canterbury-rfc.html) play in National League 2 East. [Sevenoaks](club/sevenoaks-rfc.html) and [Tunbridge Wells](club/tunbridge-wells-rfc.html) play in Regional 1 South Central.',
            'Most Kent clubs have big mini and junior sections, and the Counties 1 and 2 Kent leagues offer adult rugby at every standard.',
        ],
        sections=[
            dict(id='kent-levels', h2='Kent rugby clubs and their leagues',
                 answer='Kent rugby teams span five levels. Tonbridge Juddians play in National League 1 and Canterbury in National League 2 East. Sevenoaks and Tunbridge Wells are in Regional 1 South Central, and Gravesend and Medway in Regional 2 South East. Ashford, Thanet Wanderers, Maidstone and Folkestone play in the Counties Kent leagues.',
                 md='''
| Club | Town | Founded | League 2026-27 |
|---|---|---|---|
| [Tonbridge Juddians RFC](club/tonbridge-juddians-rfc.html) | Tonbridge | 1884 | National League 1 |
| [Canterbury RFC](club/canterbury-rfc.html) | Canterbury | 1930 | National League 2 East |
| [Sevenoaks RFC](club/sevenoaks-rfc.html) | Sevenoaks | 1921 | Regional 1 South Central |
| [Tunbridge Wells RFC](club/tunbridge-wells-rfc.html) | Tunbridge Wells | 1888 | Regional 1 South Central |
| [Gravesend RFC](club/gravesend-rfc.html) | Gravesend | 1920 | Regional 2 South East |
| [Medway RFC](club/medway-rfc.html) | Rochester | 1929 | Regional 2 South East |
| [Ashford RFC](club/ashford-rfc.html) | Ashford | 1920 | Counties 1 Kent |
| [Thanet Wanderers RFC](club/thanet-wanderers.html) | Broadstairs | 1927 | Counties 1 Kent |
| [Maidstone RFC](club/maidstone-rfc.html) | Maidstone | 1880 | Counties 2 Kent |
| [Folkestone RFC](club/folkestone-rfc.html) | Folkestone | 1929 | Counties 2 Kent |
| [Dartford RFC](club/dartford-rfc.html) | Dartford | 1960 | – |

*Leagues confirmed from England Rugby team pages on 31 October 2026.*
'''),
            dict(id='kent-choose', h2='Finding rugby teams in Kent near you',
                 answer='Kent is a big county, so start by area. West Kent has Tonbridge, Sevenoaks and Tunbridge Wells. North Kent has Dartford, Gravesend and Medway. East Kent has Canterbury, Thanet, Ashford and Folkestone. Choose two clubs within 20 minutes, check their training nights, and go to a session at each.',
                 md='''
**Practical tip:** north-west Kent is close to south-east London. Clubs such as [Sidcup](club/sidcup-rfc.html), [Beckenham](club/beckenham-rfc.html) and [Old Elthamians](club/old-elthamians-rfc.html) may be nearer than a Kent club. See [rugby clubs in London](rugby-clubs-london.html).

Kent's governing body is Kent County RFU, which runs county cups and representative teams alongside the RFU leagues.
'''),
        ]),
    'rugby-clubs-hampshire': dict(
        takeaways=[
            '**Rugby clubs in Hampshire** are all rugby union. Our directory lists 10 across the county and the Isle of Wight.',
            '[Havant](club/havant-rfc.html) are the highest-ranked, in National League 2 East. [Petersfield](club/petersfield-rfc.html), [Tottonians](club/tottonians-rfc.html) and [Winchester](club/winchester-rfc.html) play in Regional 2 South Central.',
            'For **rugby clubs near Southampton**, the nearest are [Trojans](club/trojans-rfc.html) and [Eastleigh](club/eastleigh-rfc.html) in Eastleigh and [Tottonians](club/tottonians-rfc.html) in Totton.',
        ],
        sections=[
            dict(id='hants-levels', h2='Hampshire rugby clubs by league',
                 answer='Hampshire rugby runs from Havant in National League 2 East down to the Counties Hampshire leagues. Petersfield, Tottonians and Winchester play in Regional 2 South Central. Trojans, Andover and Basingstoke are in Counties 1 Hampshire, Eastleigh in Counties 2, and Alton and the Isle of Wight in Counties 3.',
                 md='''
| Club | Town | Founded | League 2026-27 |
|---|---|---|---|
| [Havant RFC](club/havant-rfc.html) | Havant | 1951 | National League 2 East |
| [Petersfield RFC](club/petersfield-rfc.html) | Petersfield | 1883 | Regional 2 South Central |
| [Tottonians RFC](club/tottonians-rfc.html) | Totton | 1948 | Regional 2 South Central |
| [Winchester RFC](club/winchester-rfc.html) | Winchester | 1893 | Regional 2 South Central |
| [Trojans Rugby Club](club/trojans-rfc.html) | Eastleigh (Southampton) | 1874 | Counties 1 Hampshire |
| [Andover RFC](club/andover-rfc.html) | Andover | 1928 | Counties 1 Hampshire |
| [Basingstoke RFC](club/basingstoke-rfc.html) | Basingstoke | 1948 | Counties 1 Hampshire |
| [Eastleigh RFC](club/eastleigh-rfc.html) | Eastleigh | 1975 | Counties 2 Hampshire |
| [Alton RFC](club/alton-rfc.html) | Alton | 1928 | Counties 3 Hampshire |
| [Isle of Wight RFC](club/isle-of-wight-rfc.html) | Newport, IoW | 1924 | Counties 3 Hampshire |

*Leagues confirmed from England Rugby team pages on 31 October 2026.*
'''),
            dict(id='southampton', h2='Rugby clubs in Southampton',
                 answer='Southampton\'s rugby clubs are on the edge of the city. Trojans, founded in 1874, and Eastleigh RFC are both in Eastleigh, a few miles north. Tottonians are in Totton to the west. Trojans is a multi-sport club with a large junior section and is often searched as "Trojans Southampton".',
                 md='''
- [Trojans Rugby Club](club/trojans-rfc.html): Counties 1 Hampshire, founded 1874.
- [Eastleigh RFC](club/eastleigh-rfc.html): Counties 2 Hampshire.
- [Tottonians RFC](club/tottonians-rfc.html): Regional 2 South Central, the highest-ranked club near the city.

Further east, [Havant](club/havant-rfc.html) is the nearest National League club for Portsmouth. On the Surrey border, Farnham and Camberley are listed on our [Surrey page](rugby-clubs-surrey.html).
'''),
        ]),
    'rugby-clubs-london': dict(
        takeaways=[
            '**Rugby clubs in London** cover both codes. In union, [Saracens](club/saracens.html) and [Harlequins](club/harlequins.html) play in PREM Rugby. In league, [London Broncos](club/london-broncos.html) and [London Skolars](club/london-skolars.html) are the capital\'s clubs.',
            'Below the professional game, London has two Champ Rugby clubs ([Ealing Trailfinders](club/ealing-trailfinders.html), [Blackheath](club/blackheath-fc.html)), [Rosslyn Park](club/rosslyn-park-fc.html) in National League 1 and dozens of community clubs.',
            'For **east London**, look at [Wanstead](club/wanstead-rfc.html), [Woodford](club/woodford-rfc.html) and [Ilford Wanderers](club/ilford-wanderers-rfc.html).',
        ],
        sections=[
            dict(id='london-areas', h2='London rugby union clubs by area',
                 answer='London rugby union clubs are spread across every part of the city. South-west London has the most, around Richmond, Barnes, Wimbledon and Twickenham. Blackheath, Sidcup and Old Elthamians cover the south-east, Finchley and Barnet the north, and Wanstead and Woodford the east. Most community clubs play in Regional 2 or the Counties Middlesex and Surrey leagues.',
                 md='''
| Area | Clubs (league 2026-27) |
|---|---|
| South-west | [Rosslyn Park](club/rosslyn-park-fc.html) (NL1), [Barnes](club/barnes-rfc.html) (NL2 East), [Wimbledon](club/wimbledon-rfc.html) (Regional 1 South Central), [Twickenham](club/twickenham-rfc.html) (Regional 2 South Central) |
| West | [Ealing Trailfinders](club/ealing-trailfinders.html) (Champ), [Hammersmith & Fulham](club/hammersmith-fulham-rfc.html) (Regional 2 SE), [Chiswick](club/chiswick-rfc.html) (Counties 1 Middx) |
| South-east | [Blackheath](club/blackheath-fc.html) (Champ), [Sidcup](club/sidcup-rfc.html) (Regional 1 SE), [Beckenham](club/beckenham-rfc.html), [Old Elthamians](club/old-elthamians-rfc.html) (Regional 2 SE) |
| South | [Battersea Ironsides](club/battersea-ironsides-rfc.html) (Regional 2 SE), [Streatham-Croydon](club/streatham-croydon-rfc.html) (Counties 3 Surrey) |
| North | [Finchley](club/finchley-rfc.html) (Regional 2 Anglia), [Barnet](club/barnet-rfc.html), [Enfield Ignatians](club/enfield-ignatians-rfc.html) (Counties 2 Middx) |
| East | [Wanstead](club/wanstead-rfc.html), [Woodford](club/woodford-rfc.html) (Regional 2 Anglia), [Ilford Wanderers](club/ilford-wanderers-rfc.html) (Essex Merit League) |

*Leagues confirmed from England Rugby team pages on 31 October 2026.*
'''),
            dict(id='london-league', h2='Rugby league clubs in London',
                 answer='London has two senior rugby league clubs in our directory. London Broncos, founded in 1980, play in the RFL Championship. London Skolars, founded in 1995, are based in north London. Amateur rugby league in the capital is organised through the NCRL\'s National Conference Southern and the London & South East men\'s league.',
                 md='''
Rugby league in London is small compared with the North, but it is welcoming to newcomers. Many players come from rugby union or from overseas. Start by contacting [London Skolars](club/london-skolars.html), or ask [London Broncos](club/london-broncos.html) about their community programme.
'''),
        ]),
    'rugby-clubs-manchester': dict(
        takeaways=[
            '**Manchester rugby teams** play both codes. Our Greater Manchester page lists 28 clubs: 15 rugby league and 13 rugby union.',
            'Rugby league is led by [Wigan Warriors](club/wigan-warriors.html) and [Leigh Leopards](club/leigh-leopards.html) in Super League, with [Wigan St Judes](club/wigan-st-judes.html) in the 2026 NCRL National Premier League.',
            'Rugby union is led by [Sale Sharks](club/sale-sharks.html) in PREM Rugby, with [Rochdale](club/rochdale-rfc.html) and [Stockport](club/stockport-rfc.html) in Regional 1 North West.',
        ],
        sections=[
            dict(id='mcr-league', h2='Rugby league teams in Manchester',
                 answer='Greater Manchester has more professional rugby league clubs than anywhere outside West Yorkshire. Wigan Warriors and Leigh Leopards play in Super League, and Salford Red Devils, Oldham, Rochdale Hornets and Swinton Lions in the Championship. Amateur clubs such as Wigan St Judes, Wigan St Patricks and Leigh Miners Rangers are where new players start.',
                 md='''
| Club | Town | Founded | Level (2026) |
|---|---|---|---|
| [Wigan Warriors](club/wigan-warriors.html) | Wigan | 1872 | Super League |
| [Leigh Leopards](club/leigh-leopards.html) | Leigh | 1878 | Super League |
| [Salford Red Devils](club/salford-red-devils.html) | Salford | 1873 | RFL Championship |
| [Oldham RLFC](club/oldham-rlfc.html) | Oldham | 1876 | RFL Championship |
| [Rochdale Hornets](club/rochdale-hornets.html) | Rochdale | 1871 | RFL Championship |
| [Swinton Lions](club/swinton-lions.html) | Swinton | 1866 | RFL Championship |
| [Wigan St Judes ARLFC](club/wigan-st-judes.html) | Wigan | 1920 | NCRL National Premier League |
| [Wigan St Patricks ARLFC](club/wigan-st-patricks.html) | Wigan | 1927 | Amateur |
| [Leigh Miners Rangers](club/leigh-miners-rangers.html) | Leigh | 1919 | Amateur |
| [Eccles & Salford ARLFC](club/eccles-salford-arlfc.html) | Salford | 1921 | Amateur |
'''),
            dict(id='mcr-union', h2='Rugby union clubs in Manchester',
                 answer='Manchester\'s rugby union clubs are concentrated in the south and east of the county. Sale Sharks play in PREM Rugby. Rochdale and Stockport are in Regional 1 North West, and Altrincham Kersal, Bolton, Broughton Park, Didsbury Toc H, Eccles and Wigan RFC play in Counties 1 Lancashire & Cheshire.',
                 md='''
| Club | Town | League 2026-27 |
|---|---|---|
| [Sale Sharks](club/sale-sharks.html) | Salford | PREM Rugby |
| [Rochdale RFC](club/rochdale-rfc.html) | Rochdale | Regional 1 North West |
| [Stockport RFC](club/stockport-rfc.html) | Stockport | Regional 1 North West |
| [Broughton Park FC](club/broughton-park-fc.html) | Manchester | Counties 1 Lancashire & Cheshire |
| [Didsbury Toc H RFC](club/didsbury-toc-h-rfc.html) | Manchester | Counties 1 Lancashire & Cheshire |
| [Altrincham Kersal RFC](club/altrincham-kersal-rfc.html) | Altrincham | Counties 1 Lancashire & Cheshire |
| [Bolton RFC](club/bolton-rfc.html) | Bolton | Counties 1 Lancashire & Cheshire |
| [Eccles RFC](club/eccles-rfc.html) | Eccles | Counties 1 Lancashire & Cheshire |
| [Wigan RFC](club/wigan-rfc.html) | Wigan | Counties 1 Lancashire & Cheshire |

*Leagues confirmed from England Rugby team pages on 31 October 2026.*
'''),
        ]),
    # ── new hubs (built by build_hubs.py, guide added here) ──
    'rugby-clubs-edinburgh': dict(
        takeaways=[
            '**Rugby clubs in Edinburgh** are all rugby union. [Edinburgh Rugby](club/edinburgh-rugby.html) play in the United Rugby Championship, and the city has some of Scotland\'s oldest club sides.',
            'Club rugby in the city is led by [Watsonians](club/watsonians-rfc.html) (founded 1875), [Heriot\'s](club/heriots-fp-rfc.html), [Boroughmuir](club/boroughmuir-rfc.html) and [Currie Chieftains](club/currie-chieftains.html).',
            'East and West Lothian add [Musselburgh](club/musselburgh-rfc.html), [Haddington](club/haddington-rfc.html), [Linlithgow](club/linlithgow-rfc.html) and [Livingston](club/livingston-rfc.html).',
        ],
        sections=[
            dict(id='edi-teams', h2='Edinburgh rugby teams',
                 answer='Edinburgh\'s rugby teams range from the professional Edinburgh Rugby side, who play in the United Rugby Championship, to long-established clubs. Watsonians, Heriot\'s, Boroughmuir, Inverleith and Currie Chieftains all run adult, women\'s or junior teams. Most club sides play in the Scottish Premiership or the National Leagues.',
                 md='''
| Club | Area | Founded |
|---|---|---|
| [Edinburgh Rugby](club/edinburgh-rugby.html) | Edinburgh (professional) | 1996 as a pro team |
| [Watsonians RFC](club/watsonians-rfc.html) | Myreside | 1875 |
| [Heriot's FP RFC](club/heriots-fp-rfc.html) | Goldenacre | 1890 |
| [Inverleith RFC](club/inverleith-rfc.html) | Inverleith | 1890 |
| [Boroughmuir RFC](club/boroughmuir-rfc.html) | Meggetland | 1919 |
| [Currie Chieftains](club/currie-chieftains.html) | Currie | – |
| [Musselburgh RFC](club/musselburgh-rfc.html) | Musselburgh | 1921 |
| [Haddington RFC](club/haddington-rfc.html) | Haddington | 1911 |
| [Linlithgow RFC](club/linlithgow-rfc.html) | Linlithgow | 1920 |
| [Livingston RFC](club/livingston-rfc.html) | Livingston | 1966 |
'''),
            dict(id='edi-join', h2='Joining a rugby club in Edinburgh',
                 answer='To join a rugby club in Edinburgh, choose by area and level. The big city clubs field several adult teams, so beginners and experienced players both get games. Lothian clubs such as Musselburgh, Haddington and Linlithgow are community-focused. Scottish clubs need coaches working with children to be PVG-checked, so ask about this when joining a junior section.',
                 md='''
Scottish club rugby has its own league system: the Scottish Premiership, then National Leagues One to Four, then regional leagues. See our guide to [rugby leagues in Scotland](rugby-leagues-uk.html#scotland).

For the rest of the country, browse [Scottish rugby clubs](rugby-union.html?region=scotland).
'''),
        ]),
    'rugby-clubs-sussex': dict(
        takeaways=[
            '**Rugby clubs in Sussex** are all rugby union. Our directory lists 15 across East and West Sussex, from [Brighton](club/brighton-rfc.html) (founded 1868) to [Uckfield](club/uckfield-rfc.html) and [Worthing](club/worthing-rfc.html).',
            'Sussex clubs play in the RFU\'s London & South East Division leagues, including the Counties Surrey/Sussex leagues.',
            'Most Sussex clubs run mini and junior sections as well as adult teams.',
        ],
        sections=[
            dict(id='sussex-clubs', h2='Sussex rugby clubs by area',
                 answer='Sussex rugby clubs are spread along the coast and through the Weald. Brighton, Worthing, Eastbourne and Hastings & Bexhill cover the coast. Horsham, Crawley, Haywards Heath and Burgess Hill cover mid-Sussex. Uckfield, Crowborough and Lewes cover East Sussex, and Chichester, Bognor, Midhurst and Pulborough cover West Sussex.',
                 md='''
| Area | Clubs (founded) |
|---|---|
| Brighton and Lewes | [Brighton RFC](club/brighton-rfc.html) (1868), [Lewes RFC](club/lewes-rfc.html) (1929) |
| East Sussex Weald | [Uckfield RFC](club/uckfield-rfc.html) (1936), [Crowborough RFC](club/crowborough-rfc.html) (1927) |
| East Sussex coast | [Eastbourne RFC](club/eastbourne-rfc.html) (1878), [Hastings & Bexhill RFC](club/hastings-bexhill-rfc.html) (1926) |
| Mid Sussex | [Haywards Heath RFC](club/haywards-heath-rfc.html) (1964), [Burgess Hill RFC](club/burgess-hill-rfc.html) (1956) |
| North Sussex | [Horsham RFC](club/horsham-rfc.html) (1930), [Crawley RFC](club/crawley-rfc.html) (1962) |
| West Sussex coast | [Worthing RFC](club/worthing-rfc.html) (1921), [Chichester RFC](club/chichester-rfc.html) (1925), [Bognor RFC](club/bognor-rfc.html) (1933) |
| West Sussex rural | [Midhurst RFC](club/midhurst-rfc.html) (1921), [Pulborough RFC](club/pulborough-rfc.html) (1952) |
'''),
            dict(id='sussex-choose', h2='Choosing a rugby club in Sussex',
                 answer='Choose a Sussex rugby club by location first. The county is long and the A27 and A23 shape travel times, so a club 15 minutes away is better than a stronger one an hour away. Then check whether the club runs the team you need, whether that is men\'s, women\'s, vets or juniors.',
                 md='''
Crawley and Horsham are close to [Surrey clubs](rugby-clubs-surrey.html) such as Reigate & Redhill. Crowborough and Uckfield are near the [Kent border](rugby-clubs-kent.html), with Tunbridge Wells close by.
'''),
        ]),
    'rugby-clubs-somerset': dict(
        takeaways=[
            '**Rugby clubs in Somerset** range from [Bath Rugby](club/bath-rugby.html) in PREM Rugby to market-town clubs across the county.',
            '[Taunton](club/taunton-rfc.html) are the highest-ranked community club, in National League 2 West.',
            'Our directory lists 9 Somerset clubs, including [Bridgwater & Albion](club/bridgwater-albion-rfc.html), [Weston-super-Mare](club/weston-super-mare-rfc.html), [Clevedon](club/clevedon-rfc.html), [Nailsea & Backwell](club/nailsea-backwell-rfc.html) and [Yeovil](club/yeovil-rfc.html).',
        ],
        sections=[
            dict(id='somerset-clubs', h2='Somerset rugby clubs',
                 answer='Somerset rugby clubs include one of England\'s most famous professional clubs, Bath, founded in 1865, and a ring of community clubs in Taunton, Bridgwater, Weston-super-Mare, Clevedon, Nailsea and Yeovil. Taunton play in National League 2 West. Yeovil play in Counties 2 Dorset & Wilts South because of where the town sits.',
                 md='''
| Club | Town | Founded | League 2026-27 |
|---|---|---|---|
| [Bath Rugby](club/bath-rugby.html) | Bath | 1865 | PREM Rugby |
| [Taunton RFC](club/taunton-rfc.html) | Taunton | 1875 | National League 2 West |
| [Bridgwater & Albion RFC](club/bridgwater-albion-rfc.html) | Bridgwater | 1875 | – |
| [Weston-super-Mare RFC](club/weston-super-mare-rfc.html) | Weston-super-Mare | 1875 | – |
| [Clevedon RFC](club/clevedon-rfc.html) | Clevedon | 1921 | – |
| [Nailsea & Backwell RFC](club/nailsea-backwell-rfc.html) | Nailsea | 1920 | – |
| [Yeovil RFC](club/yeovil-rfc.html) | Yeovil | 1887 | Counties 2 Dorset & Wilts South |

*Leagues confirmed from England Rugby team pages on 31 October 2026, where available.*
'''),
            dict(id='somerset-near', h2='Rugby near Bath and north Somerset',
                 answer='For rugby near Bath, Bath Rugby\'s community programmes and the clubs in Bristol and north Somerset are the closest options. Clevedon and Nailsea & Backwell sit between Bath, Bristol and Weston. Players in east Somerset may also find Wiltshire clubs such as Trowbridge, in Regional 1 South West, within reach.',
                 md='''
- [Rugby clubs in Bristol](rugby-clubs-bristol.html)
- [South West rugby clubs](south-west-rugby-clubs.html)
- [Gloucestershire rugby clubs](rugby-clubs-gloucestershire.html)
'''),
        ]),
    'rugby-clubs-gloucestershire': dict(
        takeaways=[
            '**Rugby clubs in Gloucestershire** include two professional sides: [Gloucester Rugby](club/gloucester-rugby.html) in PREM Rugby and [Hartpury](club/hartpury-rfc.html) in Champ Rugby.',
            '[Cinderford](club/cinderford-rfc.html) play in National League 2 West, and [Cleve](club/cleve-rfc.html) in Regional 2 Severn.',
            'For women\'s rugby, [Gloucester-Hartpury Women](club/gloucester-hartpury-women.html) play in Premiership Women\'s Rugby.',
        ],
        sections=[
            dict(id='glos-clubs', h2='Gloucestershire rugby clubs by league',
                 answer='Gloucestershire rugby clubs cover every level. Gloucester play in PREM Rugby and Hartpury in Champ Rugby. Cinderford in the Forest of Dean are in National League 2 West, and Cleve in Mangotsfield in Regional 2 Severn. Cheltenham, Stroud and Cirencester play in the Tribute Ale Counties leagues.',
                 md='''
| Club | Town | Founded | League 2026-27 |
|---|---|---|---|
| [Gloucester Rugby](club/gloucester-rugby.html) | Gloucester | 1873 | PREM Rugby |
| [Hartpury RFC](club/hartpury-rfc.html) | Hartpury | 2014 | Champ Rugby |
| [Cinderford RFC](club/cinderford-rfc.html) | Cinderford | 1886 | National League 2 West |
| [Cleve RFC](club/cleve-rfc.html) | Mangotsfield | 1922 | Regional 2 Severn |
| [Cheltenham RFC](club/cheltenham-rfc.html) | Cheltenham | 1886 | Counties 1 Western North |
| [Stroud RFC](club/stroud-rfc.html) | Stroud | 1874 | Counties 2 Gloucestershire |
| [Cirencester RFC](club/cirencester-rfc.html) | Cirencester | 1878 | Counties 3 Gloucestershire North |

*Leagues confirmed from England Rugby team pages on 31 October 2026. Sponsor names omitted.*
'''),
            dict(id='gloucester', h2='Rugby clubs in Gloucester',
                 answer='In Gloucester city, our directory currently lists Gloucester Rugby, the PREM club at Kingsholm, founded in 1873, and Hartpury just outside the city. The city also has several community clubs that we have not yet listed. If you run one, you can register it free so local players can find you.',
                 md='''
Until more Gloucester city clubs are listed, the closest community options in our directory are [Cheltenham](club/cheltenham-rfc.html), [Stroud](club/stroud-rfc.html) and [Cinderford](club/cinderford-rfc.html). Each is around 20 to 30 minutes away. [Register a Gloucester club](register.html)
'''),
        ]),
    'rugby-clubs-warwickshire': dict(
        takeaways=[
            '**Rugby clubs in Warwickshire** include the town of Rugby, where the game is traditionally said to have begun, and [Rugby Football Club](club/rugby-football-club.html) itself.',
            '[Coventry](club/coventry-rfc.html) are the county\'s leading club, in Champ Rugby. [Broadstreet](club/broadstreet-rfc.html) play in Regional 1 Midlands and [Kenilworth](club/kenilworth-rfc.html) in Regional 2 Midlands West.',
            'For **Leamington Spa rugby**, there are two clubs: [Leamington RFC](club/leamington-rfc.html) and [Old Leamingtonians](club/old-leamingtonians-rfc.html), both in Counties 1 Midlands West (South).',
        ],
        sections=[
            dict(id='warks-clubs', h2='Warwickshire rugby clubs by league',
                 answer='Warwickshire rugby runs from Coventry in Champ Rugby to Broadstreet in Regional 1 Midlands and Kenilworth in Regional 2 Midlands West. Leamington and Old Leamingtonians play in Counties 1 Midlands West (South). Stratford-upon-Avon and Rugby have historic town clubs. For rugby league, Midlands Hurricanes are based in Coventry.',
                 md='''
| Club | Town | Founded | League 2026-27 |
|---|---|---|---|
| [Coventry RFC](club/coventry-rfc.html) | Coventry | 1874 | Champ Rugby |
| [Broadstreet RFC](club/broadstreet-rfc.html) | Coventry | 1956 | Regional 1 Midlands |
| [Kenilworth RFC](club/kenilworth-rfc.html) | Kenilworth | 1924 | Regional 2 Midlands West |
| [Leamington RFC](club/leamington-rfc.html) | Leamington Spa | 1875 | Counties 1 Midlands West (South) |
| [Old Leamingtonians RFC](club/old-leamingtonians-rfc.html) | Leamington Spa | 1927 | Counties 1 Midlands West (South) |
| [Stratford-upon-Avon RFC](club/stratford-upon-avon-rfc.html) | Stratford-upon-Avon | 1896 | – |
| [Rugby Football Club](club/rugby-football-club.html) | Rugby | 1873 | – |
| [Midlands Hurricanes](club/midlands-hurricanes.html) | Coventry | 2019 (rugby league) | RFL Championship |

*Union leagues confirmed from England Rugby team pages on 31 October 2026.*
'''),
            dict(id='leamington', h2='Rugby in Leamington Spa',
                 answer='Leamington Spa has two rugby union clubs, Leamington RFC (founded 1875) and Old Leamingtonians RFC (founded 1927). Both play in Counties 1 Midlands West (South), and both run senior and junior teams. Kenilworth, in Regional 2 Midlands West, is a ten-minute drive away for players wanting a higher level.',
                 md='''
Old Leamingtonians are often shortened to "OLRFC" or "Old Leams". Search either name in the directory to find them. For clubs across the county boundary, see [rugby clubs in Birmingham](rugby-clubs-birmingham.html).
'''),
        ]),
    'rugby-clubs-lancashire': dict(
        takeaways=[
            '**Rugby clubs in Lancashire** in our directory are rugby union clubs north of Greater Manchester. The leaders are [Fylde](club/fylde-rfc.html) and [Preston Grasshoppers](club/preston-grasshoppers.html) in National League 2 North.',
            '[Blackburn](club/blackburn-rfc.html) and [Vale of Lune](club/vale-of-lune-rfc.html) play in Regional 1 North West.',
            'Lancashire RFU also covers Greater Manchester and Merseyside. See our [Manchester](rugby-clubs-manchester.html) and [Merseyside](rugby-clubs-merseyside.html) pages.',
        ],
        sections=[
            dict(id='lancs-clubs', h2='Lancashire rugby clubs by league',
                 answer='Lancashire\'s leading rugby union clubs are Fylde and Preston Grasshoppers in National League 2 North, then Blackburn and Vale of Lune in Regional 1 North West. Fleetwood, Burnley and Chorley play in the Counties Lancashire & Cheshire leagues. Wigan, Leigh, St Helens and Warrington are listed under Greater Manchester, Merseyside and Cheshire.',
                 md='''
| Club | Town | Founded | League 2026-27 |
|---|---|---|---|
| [Fylde RFC](club/fylde-rfc.html) | Lytham St Annes | 1920 | National League 2 North |
| [Preston Grasshoppers](club/preston-grasshoppers.html) | Preston | 1869 | National League 2 North |
| [Blackburn RFC](club/blackburn-rfc.html) | Blackburn | 1876 | Regional 1 North West |
| [Vale of Lune RFC](club/vale-of-lune-rfc.html) | Lancaster | 1905 | Regional 1 North West |
| [Fleetwood RFC](club/fleetwood-rfc.html) | Fleetwood | 1927 | Counties 2 Lancashire & Cheshire |
| [Burnley RFC](club/burnley-rfc.html) | Burnley | 1875 | Counties 3 Lancashire & Cheshire |
| [Chorley RFC](club/chorley-rfc.html) | Chorley | 1923 | – |

*Leagues confirmed from England Rugby team pages on 31 October 2026.*
'''),
        ]),
}
