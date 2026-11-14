"""
Hand-written, source-checked guide content for the 14 club pages flagged "poor quality" in the
SE Ranking content-score export of 14 Nov 2026. Applied by tools/apply_club_guides.py.

Every fact below was checked against the club's own website, its governing body, Companies House /
the Charity Commission, or Wikipedia (named in `sources`). Where sources disagree, the copy says so
rather than picking one silently. League names come from England Rugby (tools/er-teams.csv,
31 Oct 2026). Nothing here is copied from a source: all wording is our own.

Fields per club
  title, meta      <title> (50-60 chars) and meta description (140-155 chars)
  about            replaces the thin "About the Club" paragraphs (list of HTML paragraphs)
  history          replaces the one-line history paragraph (list of HTML paragraphs)
  answer           40-60 word direct answer (shown under the guide H2)
  sections         [dict(id, h2, answer, md)]  -- md is markdown; links are site-relative
  faqs             [(question, answer)] added to the page's FAQ section (and its FAQPage JSON-LD)
  sources          [(label, url)] shown in "How we checked this page"
  table            optional dict(h2, id, answer, slugs, intro) -> data-driven nearby-clubs table
"""
UPDATED = '2026-11-14'

CLUBS = {}

# ---------------------------------------------------------------------------------------------
CLUBS['rosslyn-park-fc'] = dict(
    title='Rosslyn Park FC: Rugby Club in Roehampton, SW London',
    meta='Rosslyn Park FC is a rugby union club at The Rock, Roehampton, founded in 1879 and playing in National League 1. See the ground, travel and how to join.',
    about=[
        'Rosslyn Park FC is a rugby union club in Roehampton, south-west London, founded in 1879. Its first XV plays at The Rock on Priory Lane, off Upper Richmond Road, beside Barnes Common.',
        'The club is correctly Rosslyn Park FC, not RFC: it kept "Football Club" without adding the word rugby. Alongside the senior men\'s sides it runs women\'s, junior, youth and mini rugby.',
    ],
    history=[
        'Rosslyn Park began in 1879 as a group of cricketing friends from Hampstead who wanted to keep playing through the winter. The cricket club took its name from the grounds of Rosslyn House, and its red-and-white hoops arrived in 1881. The club moved around north and west London before settling at Old Deer Park, Richmond, and then bought its own ground in Roehampton in 1956.',
    ],
    answer='Rosslyn Park FC is a rugby union club founded in 1879 and based at The Rock, Priory Lane, in Roehampton, south-west London. Its first team plays in National League 1, the third tier of English rugby union, and the club also runs women\'s, junior, youth and mini sections.',
    sections=[
        dict(id='park-history', h2='What is the history of Rosslyn Park FC?',
             answer='Rosslyn Park was formed in 1879 by cricketing friends in Hampstead, north London. At the end of the first season, Charles Hoyer Millar proposed a football club to keep the players together over winter. The club has played at Roehampton since 1956.',
             md='''
- **1879:** founded from a cricket club that played in the grounds of Rosslyn House, Hampstead.
- **1881:** the club adopts its red-and-white hoops, after starting in blue with a white Maltese cross.
- **Before 1956:** home grounds at South End Green, Gospel Oak, Acton and, for a long spell, Old Deer Park in Richmond.
- **1912:** exhibition matches in Prague, Budapest and Vienna, reported as the first rugby matches played in those cities.
- **1939:** the club starts the Rosslyn Park National Schools Sevens, which has grown into one of the largest school rugby tournaments in the world.
- **1987:** placed in Division Two when national league rugby began, and won it.

Rosslyn Park has stayed in the top three tiers or just below for most of the league era. The club now sits in National League 1, level 3 of the English structure. Our [guide to the English league structure](rugby-union-league-structure.html) explains what the levels mean.
'''),
        dict(id='park-ground', h2='Where do Rosslyn Park play and how do you get there?',
             answer='Rosslyn Park play at The Rock, Priory Lane, Upper Richmond Road, London SW15 5JH, on land leased from the neighbouring Roehampton Club. The nearest station is Barnes, a short walk away. Buses 337 and 493 stop on Upper Richmond Road near Rocks Lane.',
             md='''
| Detail | Information |
|---|---|
| Ground | The Rock, Priory Lane, Roehampton |
| Address | Rosslyn Park FC, Priory Lane, Upper Richmond Road, London SW15 5JH |
| Phone | 020 8876 1879 (from the club's contact page) |
| Capacity | About 2,000, of which 630 are seated |
| Station | Barnes, a short walk away |
| Buses | 337 or 493 along Upper Richmond Road; 265 from Putney Bridge to Roehampton Lane |
| Youth and mini sections | Some junior games are played on separate pitches, so check the club's fixture list before you travel |

The Rock sits next to the Roehampton Club on the edge of Richmond Park, so there is little street parking. Plan to use public transport on busy match days.
'''),
        dict(id='london-league', h2='Are there rugby league clubs in London?',
             answer='Yes, but far fewer than rugby union clubs. Our directory lists two rugby league clubs in London: London Broncos and London Skolars. Rosslyn Park is a rugby union club, so for rugby league clubs in London use the pages below.',
             md='''
People searching for rugby league clubs in London sometimes land on union club pages like this one, so here is the quick route:

- [London Broncos](club/london-broncos.html), the professional club.
- [London Skolars](club/london-skolars.html), the community club.
- [All rugby clubs in London](rugby-clubs-london.html), covering both codes.
- [All UK rugby league clubs](rugby-league.html), if you are open to travelling.
'''),
    ],
    faqs=[
        ('What league do Rosslyn Park play in?', 'In 2026-27 Rosslyn Park\'s first XV plays in National League 1, according to England Rugby. That is the third tier of English rugby union.'),
        ('Is it Rosslyn Park FC or Rosslyn Park RFC?', 'The club\'s correct name is Rosslyn Park FC. It has always kept "Football Club" without adding "Rugby" to the name.'),
        ('Can I join Rosslyn Park as a beginner or a junior?', 'Yes. Rosslyn Park runs women\'s, junior, youth and mini sections as well as the senior men\'s sides, and its mini and youth set-up starts from under-6s. Contact the club for session times.'),
        ('How do I get to Rosslyn Park\'s ground?', 'The ground is on Priory Lane off Upper Richmond Road, SW15 5JH. Barnes station is a short walk away, and buses 337 and 493 stop near the junction with Rocks Lane.'),
    ],
    sources=[
        ('Rosslyn Park FC: history', 'https://rosslynpark.co.uk/about/history/'),
        ('Rosslyn Park FC: contact and getting here', 'https://rosslynpark.co.uk/contact'),
        ('Wikipedia: Rosslyn Park F.C.', 'https://en.wikipedia.org/wiki/Rosslyn_Park_F.C.'),
        ('England Rugby: league (via tools/er-teams.csv)', 'https://www.englandrugby.com/'),
    ],
)

# ---------------------------------------------------------------------------------------------
CLUBS['blackheath-fc'] = dict(
    title='Blackheath FC: The World\'s Oldest Open Rugby Club, 1858',
    meta='Blackheath FC, founded 1858, is the oldest open rugby club in the world. Read its history, see where it plays in Eltham, and find out how to join.',
    about=[
        'Blackheath FC was founded in 1858 and is recognised as the oldest open rugby club in the world. Members simply call it "the Club".',
        'The first team plays at Well Hall, Eltham, in south-east London, after leaving the famous Rectory Field in 2016. Other Blackheath teams still use Rectory Field.',
    ],
    history=[
        'Blackheath FC was founded in 1858 by former pupils of the Blackheath Proprietary School, and it became the first open rugby club without restricted membership. It was a founder member of the Rugby Football Union in 1871, and the first rugby international that year was played by teams led by Blackheath\'s captain. The Rectory Field was the club\'s home from 1883 to 2016.',
    ],
    answer='Blackheath FC is a rugby union club founded in 1858 and widely recognised as the oldest open rugby club in the world. Its first team now plays at Well Hall, Eltham, south-east London, having left the Rectory Field in 2016. The club fields many teams from juniors upwards.',
    sections=[
        dict(id='oldest-club', h2='Why is Blackheath called the oldest open rugby club?',
             answer='Blackheath was founded in 1858 by old boys of a local school and opened its membership to anyone in 1862. Other clubs, such as Dublin University and Edinburgh Academicals, are older but began as institutional clubs. Blackheath describes itself as the oldest independent rugby club.',
             md='''
"Oldest" depends on what you count, so here is how the claim breaks down:

| Claim | Detail |
|---|---|
| Founded | 1858, by old boys of the Blackheath Proprietary School |
| "Open" club | Membership opened to all in 1862, so the club was not tied to a school, college or military unit |
| Nickname | "The Club" or "Club", still heard at matches |
| Rugby Football Union | Founder member in 1871 |
| First international | England's captain in the 1871 match against Scotland at Raeburn Place, Edinburgh, was from Blackheath |
| Oldest fixture | Blackheath v Richmond, first played on 2 January 1864, described as the oldest continuing fixture between two rugby clubs |

The same history explains the club's FC name. It dates from before the RFU existed in 1871, so it kept "Football Club".
'''),
        dict(id='blackheath-grounds', h2='Where does Blackheath FC play?',
             answer='Blackheath\'s first team plays at Well Hall, Kidbrooke Lane, Eltham, London SE9 6TE, which was its training ground before it became the match-day home in 2016. The club\'s other teams still use the historic Rectory Field on Charlton Road.',
             md='''
- **Well Hall, Eltham:** first-team home since the end of the 2015-16 season. The move was made for financial stability and a better match-day experience.
- **Rectory Field:** the club played here from 1883 until 30 April 2016, when it beat Blaydon 45-17 in the last first-team game. It is shared with cricket, tennis and squash, and other Blackheath teams still play there.
- **League:** England Rugby lists the first team in Champ Rugby for 2026-27. Check the club's fixture list for the current season.
- **Contact:** 020 8850 0210 or info@blackheathrugby.co.uk (from the club's England Rugby listing).
'''),
        dict(id='east-london', h2='Which rugby clubs are in east London?',
             answer='Blackheath is in south-east London, not east London. For rugby clubs in east London, Ilford Wanderers, Wanstead and Woodford are the closest listed in our directory, and the Essex hub covers clubs further out along the Central line and the A12.',
             md='''
| Club | Area | Profile |
|---|---|---|
| Ilford Wanderers RFC | Ilford | [Ilford Wanderers](club/ilford-wanderers-rfc.html) |
| Wanstead RFC | Wanstead | [Wanstead](club/wanstead-rfc.html) |
| Woodford RFC | Woodford Green | [Woodford](club/woodford-rfc.html) |
| Greenwich RFC | Greenwich, south-east | [Greenwich](club/greenwich-rfc.html) |

For the full list see [rugby clubs in London](rugby-clubs-london.html) and [rugby clubs in Essex](rugby-clubs-essex.html).
'''),
    ],
    faqs=[
        ('When was Blackheath FC founded?', 'Blackheath FC was founded in 1858 by old boys of the Blackheath Proprietary School. It is widely described as the oldest open rugby club in the world.'),
        ('Where does Blackheath FC play its home games?', 'The first team plays at Well Hall in Eltham, SE9 6TE, having moved from the Rectory Field in 2016. Some other Blackheath sides still play at the Rectory Field.'),
        ('Why is it called "the Club"?', 'Blackheath was the first open club, and its members came to call it simply "the Club". The nickname survives at the ground and in the club shop.'),
        ('How do I join Blackheath FC?', 'Contact the club by email or phone, using the details on this page. Blackheath runs sides from juniors to veterans, so there is usually a team for new players.'),
    ],
    sources=[
        ('Blackheath FC: our history', 'https://blackheathrugby.co.uk/our-history/'),
        ('Wikipedia: Blackheath F.C.', 'https://en.wikipedia.org/wiki/Blackheath_F.C.'),
        ('British & Irish Lions: Your Club Your Lions, Blackheath', 'https://www.lionsrugby.com/en/news/your-club-your-lions-blackheath-fc'),
        ('The Rugby Journal: Rectory Field', 'https://www.therugbyjournal.com/ghost-grounds/rectory-field-blackheath-fc'),
    ],
)

# ---------------------------------------------------------------------------------------------
CLUBS['coventry-rfc'] = dict(
    title='Coventry RFC: Rugby Club, History & Warwickshire Guide',
    meta='Coventry RFC, founded 1874, plays in Champ Rugby at the Nick Newbold Stadium. Read its history and see other Warwickshire rugby clubs near Coventry.',
    about=[
        'Coventry RFC is a rugby union club in Coventry, West Midlands, founded in 1874. The first team plays in Champ Rugby, the second tier of English rugby union.',
        'The club\'s home is the Nick Newbold Stadium, known until March 2026 as the Butts Park Arena, in Spon End close to the city centre.',
    ],
    history=[
        'Coventry traces its origins to a match in 1874 between members of Stoke Cricket Club and students of Allesley Park College, played half under rugby rules and half under association rules. The club won the RFU Knockout Cup in 1973, beating Bristol 27-15, and retained it in 1974 with a 26-6 win over London Scottish. It played at Coundon Road from 1921 until 2004, then returned to the Butts.',
    ],
    answer='Coventry RFC is a rugby union club founded in 1874 that plays in Champ Rugby, the second tier of English rugby. Its home is the Nick Newbold Stadium, formerly Butts Park Arena, in Coventry. It is the best-known club in Warwickshire\'s rugby area after Rugby and Leamington.',
    sections=[
        dict(id='coventry-ground', h2='Where does Coventry RFC play?',
             answer='Coventry RFC play at the Nick Newbold Stadium, formerly Butts Park Arena, Butts Road, Coventry CV1 3GE. It opened in 2004 and was renamed on 21 March 2026 in honour of Nick Newbold, who worked at the club for 17 years. Capacity is about 5,250.',
             md='''
| Detail | Information |
|---|---|
| Stadium | Nick Newbold Stadium (Butts Park Arena until 21 March 2026) |
| Address | Butts Road, Coventry CV1 3GE |
| Capacity | About 5,250, with 3,000 seats |
| Opened | 2004, after 83 years at Coundon Road |
| Record league crowd | 5,047 against Nottingham in an RFU Championship game, 26 December 2023 |
| Club phone | 024 7623 1001 |

The stadium also hosts conferences and events, and it has been used for rugby league and American football as well as rugby union.
'''),
        dict(id='warwickshire', h2='What are the rugby clubs in Warwickshire?',
             answer='Warwickshire has five rugby union clubs in our directory: Kenilworth, Leamington, Old Leamingtonians, Rugby Football Club and Stratford-upon-Avon. Coventry RFC is in the West Midlands county but is the area\'s highest-level club, so it is often searched for alongside them.',
             md='''
| Club | Town | Profile |
|---|---|---|
| Kenilworth RFC | Kenilworth | [Kenilworth](club/kenilworth-rfc.html) |
| Leamington RFC | Leamington Spa | [Leamington](club/leamington-rfc.html) |
| Old Leamingtonians RFC | Leamington Spa | [Old Leamingtonians](club/old-leamingtonians-rfc.html) |
| Rugby Football Club | Rugby | [Rugby FC](club/rugby-football-club.html) |
| Stratford-upon-Avon RFC | Stratford-upon-Avon | [Stratford](club/stratford-upon-avon-rfc.html) |

Compare them all on our [Warwickshire rugby clubs page](rugby-clubs-warwickshire.html), and see [Birmingham and West Midlands clubs](rugby-clubs-birmingham.html) for clubs such as Moseley and Birmingham & Solihull.
'''),
    ],
    faqs=[
        ('What league does Coventry RFC play in?', 'In 2026-27 Coventry plays in Champ Rugby, according to England Rugby. That is the second tier of the English rugby union league system.'),
        ('Is Butts Park Arena still called that?', 'Butts Park Arena was renamed the Nick Newbold Stadium from 21 March 2026. Some maps and older web pages still use the old name.'),
        ('How old is Coventry RFC?', 'The club dates its origins to an 1874 match, so it is more than 150 years old. It won the RFU Knockout Cup in 1973 and 1974.'),
        ('Which rugby clubs are near Coventry?', 'In Warwickshire, Kenilworth, Leamington and Rugby Football Club are all within about 15 miles. Our Warwickshire and Birmingham pages list them with their towns.'),
    ],
    sources=[
        ('Coventry Rugby: our heritage', 'https://coventryrugby.co.uk/our-heritage'),
        ('Coventry Rugby: Nick Newbold Stadium announcement', 'https://www.coventryrugby.co.uk/butts-park-arena-to-be-known-as-the-nick-newbold-stadium'),
        ('Wikipedia: Coventry R.F.C.', 'https://en.wikipedia.org/wiki/Coventry_R.F.C.'),
        ('Wikipedia: Nick Newbold Stadium', 'https://en.wikipedia.org/wiki/Nick_Newbold_Stadium'),
    ],
)

# ---------------------------------------------------------------------------------------------
CLUBS['edwardian-fc'] = dict(
    title='Edwardian FC: Rugby Club in Solihull, West Midlands (1882)',
    meta='Edwardian FC is a rugby union club in Solihull, formed in 1882 by King Edward\'s School old boys. See its history, ground and other Solihull rugby clubs.',
    about=[
        'Edwardian FC is a rugby union club in Solihull, West Midlands. It began in 1882 as the Old Edwardians, a club for former pupils of King Edward\'s School in Birmingham.',
        'The club has played at Streetsbrook Road in Solihull since 1959 and has been Edwardian FC since May 1977.',
    ],
    history=[
        'A meeting on 26 June 1882 in the old King Edward\'s School building in New Street, Birmingham, set up an Old Edwardian Football Club. The club moved around south Birmingham for decades, including Wake Green Road in Moseley and Wheelers Lane in Kings Heath, until it bought its own ground at Streetsbrook Road, Solihull, in 1959. It dropped the "Old" and became Edwardian FC in May 1977, as fewer players came from the school.',
    ],
    answer='Edwardian FC is a rugby union club in Solihull, West Midlands, formed in 1882 by old boys of King Edward\'s School, Birmingham. It has played at its own ground on Streetsbrook Road since 1959. It is one of two rugby clubs with Solihull links in our directory.',
    sections=[
        dict(id='edwardian-story', h2='How did Edwardian FC start?',
             answer='Edwardian FC began with a meeting on 26 June 1882 at King Edward\'s School in New Street, Birmingham, to set up an Old Edwardian Football Club. It opened its membership beyond former pupils and changed its name to Edwardian FC in May 1977.',
             md='''
- **1882:** first meeting at the old school building in New Street, Birmingham. Early matches were at Bristol Road and the Warwickshire County Cricket Ground, Edgbaston.
- **Early 1900s:** home games at Wake Green Road, Moseley, then Vicarage Road, Kings Heath from 1911.
- **Until the Second World War:** home matches at Wheelers Lane, Kings Heath.
- **1959:** the club gets its own ground, with two pitches, at Streetsbrook Road, Solihull.
- **1977:** the club becomes Edwardian FC.

The club still carries its roots in its full name, "Edwardian Football Club (Rugby Union)", which separates it from other sports clubs with similar names.
'''),
        dict(id='solihull-clubs', h2='Which rugby clubs are in Solihull?',
             answer='In and around Solihull our directory lists Edwardian FC at Streetsbrook Road, Birmingham & Solihull RFC at Portway, and the former Solihull RFC, which merged into Birmingham & Solihull in 1989. For more clubs in the wider area, see our Birmingham rugby clubs guide.',
             md='''
| Club | Where | Notes |
|---|---|---|
| [Edwardian FC](club/edwardian-fc.html) | Streetsbrook Road, Solihull | Old Edwardians since 1882, own ground since 1959 |
| [Birmingham & Solihull RFC](club/birmingham-solihull-rfc.html) | Portway, on the Birmingham and Solihull border | Known as "the Bees" |
| [Solihull RFC](club/solihull-rfc.html) | Sharmans Cross Road (historic) | Merged with Birmingham RFC in 1989 |
| [Camp Hill RFC](club/camp-hill-rfc.html) | Shirley | Nearest other club in our directory |

Compare all of them in our guide to [rugby clubs in Birmingham](rugby-clubs-birmingham.html).
'''),
    ],
    faqs=[
        ('Where does Edwardian FC play?', 'Edwardian FC plays at Streetsbrook Road in Solihull, where the club has had its own ground since 1959. Check the club\'s Pitchero site for fixtures and directions.'),
        ('Is Edwardian FC the same as Old Edwardians?', 'The club began in 1882 as the Old Edwardians, for old boys of King Edward\'s School in Birmingham. It changed its name to Edwardian FC in May 1977.'),
        ('How do I join Edwardian FC?', 'Use the club website linked on this page, which hosts team pages and contact details. Most clubs are happy for beginners to come to a training session first.'),
        ('Are there other rugby clubs in Solihull?', 'Birmingham & Solihull RFC is close by at Portway, and Camp Hill RFC is in nearby Shirley. See our Birmingham rugby clubs page for the full list.'),
    ],
    sources=[
        ('Edwardian FC (Pitchero): club history', 'https://pitchero.com/clubs/edsrugby/a/history-8449.html'),
        ('Birmingham & Solihull RFC: club history', 'https://www.beesrugby.com/a/club-history-39250.html'),
    ],
)

# ---------------------------------------------------------------------------------------------
CLUBS['solihull-rfc'] = dict(
    title='Solihull Rugby Club: History and Where to Play in Solihull',
    meta='Solihull RFC was founded in 1933 and merged into Birmingham & Solihull in 1989. Read the story and find rugby clubs in Birmingham and Solihull to join now.',
    about=[
        'Solihull RFC was a rugby union club in Solihull, West Midlands, founded in 1933 and based at Sharmans Cross Road. In 1989 it merged with Birmingham RFC to form Birmingham & Solihull RFC, the club known as "the Bees".',
        'We keep this page because people still search for Solihull rugby. We have not found a separate club currently playing under the Solihull RFC name. If yours does, please tell us and we will update the listing.',
    ],
    history=[
        'Solihull RFC was founded in 1933 and played at Sharmans Cross Road, Solihull. Birmingham & Solihull RFC says on its own site that Solihull, like its neighbour Birmingham RFC (founded in 1909 and based at Portway), found it hard to adjust to league rugby. The two clubs merged in 1989. Our directory previously gave a founding year of 1924, which we have corrected to match the Bees\' club history.',
    ],
    answer='Solihull RFC was a rugby union club founded in 1933 at Sharmans Cross Road, Solihull. It merged with Birmingham RFC in 1989 to form Birmingham & Solihull RFC, the "Bees". To play rugby near Birmingham or Solihull today, use the clubs listed below.',
    sections=[
        dict(id='solihull-story', h2='What happened to Solihull RFC?',
             answer='Solihull RFC merged with Birmingham RFC in 1989 to create Birmingham & Solihull RFC. That club played at Sharmans Cross Road until 2010, then moved to Portway. A third club using the Birmingham & Solihull name now plays community rugby at Portway.',
             md='''
The Birmingham & Solihull name has been used by three separate rugby clubs, which is why searches for it can be confusing:

1. **Birmingham & Solihull RFC (1989):** formed from the merger of Birmingham RFC (1909) and Solihull RFC (1933). It grew into a Championship club and was nicknamed the Bees.
2. **A second club (2009):** a private company that took over the senior playing side and ran it semi-professionally.
3. **The present club:** a community club at Portway that restarted in the Greater Birmingham Merit League in 2019-20 and kept the Bees name.

The old ground at Sharmans Cross Road was left in 2010 after relegation from the Championship, and the site has stood unused since. The former clubhouse was damaged by fire in 2014.
'''),
        dict(id='where-to-play', h2='Which rugby clubs are in and near Birmingham?',
             answer='Birmingham has more than a dozen rugby union clubs in our directory, from Moseley and Birmingham & Solihull to Bournville, Camp Hill and Sutton Coldfield. If you want rugby near Birmingham, start with the table below and then check training nights with the club.',
             md='''
| Club | Town |
|---|---|
| [Birmingham & Solihull RFC](club/birmingham-solihull-rfc.html) | Birmingham |
| [Birmingham Moseley](club/birmingham-moseley.html) and [Moseley Rugby Club](club/moseley-rugby-club.html) | Birmingham |
| [Bournville RFC](club/bournville-rfc.html) | Birmingham |
| [Camp Hill RFC](club/camp-hill-rfc.html) | Shirley |
| [Edwardian FC](club/edwardian-fc.html) | Solihull |
| [Harborne RFC](club/harborne-rfc.html) | Birmingham |
| [Sutton Coldfield RFC](club/sutton-coldfield-rfc.html) | Sutton Coldfield |
| [Yardley & District RFC](club/yardley-district-rfc.html) | Birmingham |

Our [Birmingham rugby clubs page](rugby-clubs-birmingham.html) compares them all, including women's and junior sections.
'''),
    ],
    faqs=[
        ('When was Solihull RFC founded?', 'Birmingham & Solihull RFC\'s own history says Solihull RFC was founded in 1933. Our directory previously showed 1924, which we have corrected.'),
        ('Does Solihull RFC still exist?', 'The original Solihull RFC merged with Birmingham RFC in 1989 to form Birmingham & Solihull RFC. We have not found a separate Solihull RFC playing today, so we point readers to current clubs.'),
        ('Where is the old Solihull RFC ground?', 'It was at Sharmans Cross Road in Solihull. Birmingham & Solihull RFC left it in 2010, and the ground has been unused since.'),
        ('Which rugby club should I join in Solihull?', 'Edwardian FC at Streetsbrook Road is the closest club with its own ground in Solihull. Birmingham & Solihull RFC at Portway and Camp Hill RFC in Shirley are also nearby.'),
    ],
    sources=[
        ('Birmingham & Solihull RFC: club history', 'https://www.beesrugby.com/a/club-history-39250.html'),
        ('Wikipedia: Birmingham & Solihull R.F.C.', 'https://en.wikipedia.org/wiki/Birmingham_%26_Solihull_R.F.C.'),
        ('The Rugby Journal: Sharmans Cross Road', 'https://www.therugbyjournal.com/ghost-grounds/sharmans-cross-road-birmingham-solihull-rfc'),
    ],
)

# ---------------------------------------------------------------------------------------------
CLUBS['folkestone-rfc'] = dict(
    title='Folkestone RFC: Rugby Club in Kent | Training & Joining',
    meta='Folkestone RFC is a Kent rugby union club in Newington, formed in 1973. See the ground, training nights, league and how to join senior and junior teams.',
    about=[
        'Folkestone RFC is a rugby union club in Folkestone, Kent, started by a group of enthusiasts in the 1973-74 season. It is a registered charity and plays at New Burlington Field, Newington, close to the Channel Tunnel terminal.',
        'The club runs senior men\'s sides, a women\'s team and junior rugby from under-6s upwards.',
    ],
    history=[
        'Folkestone Rugby Football Club was started by a few enthusiasts in the 1973-74 season. Its first match was against Snowdown Colliery, and trials at Hillside School attracted more than 40 players. In its early years the club worked from the Folkestone Sports Centre and played on the Polo Field, now the Three Hills sports park, and at Morehall Recreation Ground, before moving to its present ground at Newington. Our directory previously gave 1929 as the founding year, which does not match the club\'s own history, so we have corrected it.',
    ],
    answer='Folkestone RFC is a Kent rugby union club formed in the 1973-74 season and based at New Burlington Field, Newington, Folkestone CT18 8BH. Its first XV plays in Counties 2 Kent, and the club runs senior, women\'s and junior teams, with new players welcome at training on Tuesday and Thursday evenings.',
    sections=[
        dict(id='folkestone-join', h2='How do I join Folkestone RFC?',
             answer='Folkestone RFC welcomes new players to all its senior squads. The first, second and third teams train together on Tuesday and Thursday evenings, with players arriving from 6:30pm for a 7pm start. Juniors can start from under-6s. Contact the club to confirm times before your first visit.',
             md='''
- **Seniors:** all senior teams welcome new players; the first, second and third squads train together on Tuesday and Thursday evenings.
- **Juniors:** the club takes both new and experienced players from the under-6 age group upwards. Children under 14 cannot create their own account on the club's Pitchero site, so a parent or guardian signs up.
- **Kit:** boots with studs are preferred, but short-studded moulded football-style boots or trainers can be worn when the weather is dry and the ground is hard.
- **Contact:** 01303 266887 or frfcmembership@gmail.com, from the club's England Rugby listing.
'''),
        dict(id='folkestone-ground', h2='Where is Folkestone RFC\'s ground?',
             answer='The ground is New Burlington Field, Bargrove, Newington, Folkestone, Kent CT18 8BH, a few miles west of the town centre near the Channel Tunnel terminal. The club is a registered charity and the clubhouse is available for private hire.',
             md='''
| Detail | Information |
|---|---|
| Ground | New Burlington Field, Newington |
| Postcode | CT18 8BH |
| League (2026-27) | Counties 2 Kent (England Rugby) |
| Earlier grounds | The Polo Field (now Three Hills sports park) and Morehall Recreation Ground |
| Clubhouse | Available for private hire |

Folkestone is not to be confused with Cheriton Road, the town's football and cricket ground, which is a different site.
'''),
        dict(id='kent-clubs', h2='Which other rugby clubs are near Folkestone?',
             answer='Within Kent the nearest clubs in our directory are Ashford, Canterbury and Thanet Wanderers. All three have senior sides and junior sections. Our Kent rugby clubs page compares all 11 Kent clubs we list, with their towns and what league they play in.',
             md='''
| Club | Town | Profile |
|---|---|---|
| Ashford RFC | Ashford | [Ashford](club/ashford-rfc.html) |
| Canterbury RFC | Canterbury | [Canterbury](club/canterbury-rfc.html) |
| Thanet Wanderers RFC | Broadstairs | [Thanet Wanderers](club/thanet-wanderers.html) |

See all [rugby clubs in Kent](rugby-clubs-kent.html).
'''),
    ],
    faqs=[
        ('When was Folkestone RFC founded?', 'The club\'s own history says it started in the 1973-74 season, when a few enthusiasts organised the first match against Snowdown Colliery.'),
        ('What league does Folkestone RFC play in?', 'In 2026-27 the first XV plays in Counties 2 Kent, according to England Rugby. That is level 8 of the English structure.'),
        ('When does Folkestone RFC train?', 'The first, second and third senior squads train together on Tuesday and Thursday evenings, arriving from 6:30pm for a 7pm start. Check the club website for junior times.'),
        ('Can children play rugby at Folkestone RFC?', 'Yes. The club takes new and experienced players from the under-6 age group upwards.'),
    ],
    sources=[
        ('Folkestone RFC: club history (Pitchero)', 'https://www.folkestonerugbyclub.co.uk/a/about-us-23073.html?page=3'),
        ('Folkestone RFC: first XV team page', 'https://www.folkestonerugbyclub.co.uk/teams/28907'),
        ('Folkestone RFC: under-13s team page', 'https://folkestonerugbyclub.co.uk/teams/29242'),
        ('Charity Commission register: Folkestone Rugby Football Club', 'https://opencharities.uk/ew/1171276'),
    ],
)

# ---------------------------------------------------------------------------------------------
CLUBS['windsor-rfc'] = dict(
    title='Windsor RFC: Rugby Club at Home Park, Windsor, Berkshire',
    meta='Windsor RFC is a rugby union club at Home Park beside Windsor Castle, Berkshire. See its league, ground, travel tips and how to join. Not Windsor, Ontario.',
    about=[
        'Windsor RFC is a rugby union club in Windsor, Berkshire. It plays at Home Park, on Datchet Road beside Windsor Castle, and shares the site with the town\'s cricket club.',
        'This is Windsor in Berkshire, England, not Windsor, Ontario, which has a rugby club of its own.',
    ],
    history=[
        'Windsor Rugby Football Club has been based in Home Park for generations. The Duke of Edinburgh opened its sports pavilion, shared with Windsor and Eton Cricket Club, on 23 April 1962. The club today is run through a company, Windsor Rugby Football Club Limited, incorporated in December 2010 and registered at Home Park.',
    ],
    answer='Windsor RFC is a rugby union club in Windsor, Berkshire, based at Home Park, Datchet Road, SL4 6HX, next to Windsor Castle. Its first XV plays in Counties 1 Southern North in 2026-27, according to England Rugby, and the club is a community amateur rugby club.',
    sections=[
        dict(id='windsor-ground', h2='Where does Windsor RFC play?',
             answer='Windsor RFC plays at Home Park, Datchet Road, Windsor SL4 6HX, a public park on the Windsor Estate that sits within the setting of Windsor Castle. The park is the main sports venue in Windsor and is shared with cricket, tennis, archery and angling clubs.',
             md='''
| Detail | Information |
|---|---|
| Ground | Home Park, Datchet Road, Windsor |
| Postcode | SL4 6HX |
| Setting | Public park beside Windsor Castle, 31 hectares |
| Sharing | Cricket, tennis, archery, hockey and angling clubs also use the park |
| Station | Windsor & Eton Riverside is close to the Home Park entrance |
| League (2026-27) | Counties 1 Southern North (England Rugby) |

Parking inside Home Park is tightly restricted by the Windsor Estate, so travel by train or use town-centre car parks where possible.
'''),
        dict(id='windsor-disambiguation', h2='Windsor rugby: Berkshire or Ontario?',
             answer='This page covers Windsor RFC in Berkshire, England. Windsor, Ontario, in Canada, has a separate club, Windsor Rugby, which began in the 1960s. If you searched for "windsor rugby" from the UK, the club listed here is the one beside Windsor Castle.',
             md='''
To avoid confusion:

- **Windsor RFC (this page):** Home Park, Windsor, Berkshire, SL4 6HX, in the English league system.
- **Nearby English clubs:** [Maidenhead RFC](club/maidenhead-rfc.html) and [Bracknell RFC](club/bracknell-rfc.html) are both within about 10 miles. Our [Berkshire and south clubs](rugby-union.html) list the rest.
'''),
    ],
    faqs=[
        ('What league does Windsor RFC play in?', 'In 2026-27 the first XV plays in Counties 1 Southern North, according to England Rugby.'),
        ('Where is Windsor RFC\'s ground?', 'The ground is Home Park, Datchet Road, Windsor SL4 6HX, in a public park next to Windsor Castle.'),
        ('Is Windsor RFC a community club?', 'Yes. Windsor Rugby Football Club Limited was incorporated in December 2010 and describes itself as a community amateur rugby club at Home Park.'),
        ('How do I join Windsor RFC?', 'Contact the club using the details on this page and ask about the next training session. New players are normally invited to try a session before committing.'),
    ],
    sources=[
        ('Companies House: Windsor Rugby Football Club Limited (07465574)', 'https://find-and-update.company-information.service.gov.uk/company/07465574'),
        ('Windsor Great Park: Home Park Public', 'https://windsorgreatpark.co.uk/explore/home-park-public/the-park/'),
        ('Royal Borough of Windsor and Maidenhead: Home Park', 'https://rbwm.gov.uk/leisure-and-culture/parks-and-open-spaces/home-park'),
        ('England Rugby: league (via tools/er-teams.csv)', 'https://www.englandrugby.com/'),
    ],
)

# ---------------------------------------------------------------------------------------------
CLUBS['tynedale-rfc'] = dict(
    title='Tynedale RFC: Rugby Club in Corbridge, Northumberland',
    meta='Tynedale RFC, founded in 1876, plays in National League 2 North at Tynedale Park, Corbridge. See its history, ground, directions and how to join.',
    about=[
        'Tynedale RFC is a rugby union club in Corbridge, Northumberland, founded in 1876. The first XV plays in National League 2 North, the fourth tier of English rugby union.',
        'The club\'s ground, Tynedale Park, is a 35-acre site on Station Road in the Tyne valley, about three miles east of Hexham.',
    ],
    history=[
        'Tynedale was founded in Hexham Town Hall in 1876, after a letter was addressed to the "Captain of Hexham Rugby Club", which did not exist. The club helped to found the Northumberland Rugby Union with five others, and in 1885 it won the first sevens tournament it entered, at Hawick. It left its Dene Park ground in Hexham for Tynedale Park, Corbridge, in the mid-1970s. In January 2005 the River Tyne flooded the ground and clubhouse.',
    ],
    answer='Tynedale RFC is a rugby union club in Corbridge, Northumberland, founded in 1876. Its first XV plays in National League 2 North at Tynedale Park, Station Road, NE45 5AY. The club runs senior, women\'s and junior rugby for the Tyne valley, three miles east of Hexham.',
    sections=[
        dict(id='tynedale-history', h2='What is the history of Tynedale Rugby Club?',
             answer='Tynedale was founded in 1876 in Hexham Town Hall and played at Dene Park in Hexham for roughly 75 years before moving to Corbridge. It was a founder of the Northumberland Rugby Union and, in 1885, won the first sevens tournament it entered, at Hawick.',
             md='''
- **1876:** founded in Hexham Town Hall; first match against Elswick.
- **1883:** three Tynedale men played for Northumberland in a 3-3 draw with the first New Zealand touring side.
- **1905:** the club changes its name from "Tynedale Football Club" to "Tynedale Rugby Football Club".
- **1914:** wins the last Northumberland Cup final before the First World War, beating Percy Park 9-6.
- **1926:** buys Dene Park for £1,550 in its Jubilee year, funded by donations, special efforts and an RFU loan.
- **Mid-1970s:** moves to Tynedale Park, Corbridge.
- **January 2005:** the River Tyne floods the ground and clubhouse.

The club has played in the national leagues for much of the league era. It is now in National League 2 North, level 4 of the English structure, and in 2024-25 it finished second.
'''),
        dict(id='tynedale-getting-there', h2='How do I get to Tynedale Park?',
             answer='Tynedale Park is on Station Road, Corbridge NE45 5AY, on the south side of the River Tyne, 17 miles west of Newcastle and 40 miles east of Carlisle. Corbridge railway station is the nearest, and the ground is about three miles east of Hexham.',
             md='''
| Detail | Information |
|---|---|
| Address | Tynedale Park, Station Road, Corbridge, Northumberland NE45 5AY |
| Site | 35 acres |
| Distance | 17 miles west of Newcastle, 40 miles east of Carlisle, 3 miles east of Hexham |
| Directions | From the north, cross the Tyne bridge and bear left onto the B6529 |
| Station | Corbridge |
| League (2026-27) | National League 2 North (England Rugby) |
'''),
        dict(id='northumberland-clubs', h2='What other rugby clubs are in Northumberland?',
             answer='Other Northumberland clubs in our directory include Alnwick, Ashington, Blyth, Hexham and Morpeth. Our North East rugby clubs guide compares them with Durham and Tyne and Wear clubs, so you can choose a club by distance and level.',
             md='''
Nearby clubs in our directory:

- [Hexham RFC](club/hexham-rfc.html), three miles west
- [Morpeth RFC](club/morpeth-rfc.html)
- [Blyth RFC](club/blyth-rfc.html)
- [Alnwick RFC](club/alnwick-rfc.html)
- [Ashington RFC](club/ashington-rfc.html)

See all clubs in our [North East rugby clubs guide](north-east-rugby-clubs.html).
'''),
    ],
    faqs=[
        ('When was Tynedale RFC founded?', 'Tynedale RFC was founded in 1876 at Hexham Town Hall, and its first match was against Elswick.'),
        ('What league does Tynedale play in?', 'In 2026-27 Tynedale plays in National League 2 North, according to England Rugby. That is the fourth tier of English rugby union.'),
        ('Where is Tynedale RFC\'s ground?', 'The ground is Tynedale Park, Station Road, Corbridge NE45 5AY, on the south side of the River Tyne.'),
        ('Is Tynedale Rugby Club in Hexham or Corbridge?', 'It was founded in Hexham and played there until the mid-1970s, but it now plays at Corbridge. Hexham RFC is a separate club.'),
    ],
    sources=[
        ('Tynedale RFC: club history (Pitchero)', 'https://www.tynedalerfc.co.uk/a/club-history-53816.html?page=3'),
        ('Tynedale RFC: historical articles', 'https://www.tynedalerfc.co.uk/a/interesting-historical-articles-61219.html?page=11'),
        ('Tynedale RFC 7s: how to find us', 'https://events.liveit.io/tynedale-rugby-club/tynedale-rfc-7s-2/'),
        ('Wikipedia: Tynedale RFC', 'https://en.wikipedia.org/wiki/Tynedale_RFC'),
    ],
)

# ---------------------------------------------------------------------------------------------
CLUBS['brighton-rfc'] = dict(
    title='Brighton RFC: Rugby Club in Sussex | Brighton Blues',
    meta='Brighton Football Club (RFU), the Brighton Blues, was founded in 1868 and plays at Waterhall. Read its history and find other rugby clubs in Sussex.',
    about=[
        'Brighton FC (RFU), known as the Brighton Blues, is a rugby union club in Brighton, East Sussex, founded in 1868. It plays at Waterhall Playing Fields on the northern edge of the city.',
        'The club was formed before the RFU itself, so it is one of the few clubs designated FC rather than RFC.',
    ],
    history=[
        'Brighton Football Club was founded in 1868, three years before the RFU existed, which is why it is "FC" rather than "RFC". Its own history traces earlier football played under modified rugby rules in Brighton from 1852. In December 1902 it became the first English club to tour France under union regulations. The club later moved from Horsdean to Waterhall, and it celebrated its 150th season in 2018-19.',
    ],
    answer='Brighton Football Club (RFU), the Brighton Blues, is a rugby union club in Brighton, East Sussex, founded in 1868 and based at Waterhall Playing Fields, Waterhall Road. It is one of the oldest clubs in England and one of two rugby clubs on playing fields in Brighton and Hove.',
    sections=[
        dict(id='brighton-history', h2='How old is Brighton Rugby Club?',
             answer='Brighton Football Club was founded in 1868, making 2018-19 its 150th season. Club historian John Honeysett has argued that earlier Brighton matches played under rugby rules in 1865-66 could make it even older, though Blackheath and other clubs are normally cited as the oldest.',
             md='''
- **1868:** the founding date used by the club. It predates the RFU (1871), so the club kept the "FC" designation.
- **1902:** first English club to tour France under rugby union regulations.
- **Later:** the club moved from Horsdean to Waterhall, after the Brighton bypass changed the land around the old ground.
- **Club alumni:** Harlequins fly-half Marcus Smith played junior rugby at Brighton, where his father Jeremy was club captain.

The 150th-season research is in John Honeysett's book *The History of Brighton Football Club (Rugby Union)*.
'''),
        dict(id='brighton-ground', h2='Where does Brighton RFC play?',
             answer='Brighton RFC plays at Waterhall Playing Fields, Waterhall Road, Brighton BN1 8YR (the England Rugby listing gives BN1 8YN), on the northern edge of the city. The club holds a lease of more than 90 years on its clubhouse and hires the pitches from Brighton & Hove City Council.',
             md='''
| Detail | Information |
|---|---|
| Ground | Waterhall Playing Fields, Waterhall Road, Brighton |
| Clubhouse | Club room with lift access, outside bar and accessible toilets |
| Phone | 01273 562729 (England Rugby listing) |
| Neighbours | Hove RFC, whose first match as a club was against Brighton on 20 September 1952 |
| Inclusive option | Brighton & Hove Sea Serpents RFC, founded in 2015, is a gay and inclusive club in the city |

The Waterhall site is also used by walkers and dog owners, so arrive in good time on match days.
'''),
        dict(id='sussex-clubs', h2='Which are the main rugby clubs in Sussex?',
             answer='Our directory lists 15 rugby union clubs across East and West Sussex, from Brighton and Eastbourne to Chichester, Horsham and Worthing. Most also run mini and junior sections, so you can usually find a Sussex club within a short drive of home.',
             md='''
| Area | Clubs |
|---|---|
| Brighton and Mid Sussex | [Brighton](club/brighton-rfc.html), [Burgess Hill](club/burgess-hill-rfc.html), [Haywards Heath](club/haywards-heath-rfc.html), [Lewes](club/lewes-rfc.html), [Uckfield](club/uckfield-rfc.html) |
| East Sussex coast | [Eastbourne](club/eastbourne-rfc.html), [Hastings & Bexhill](club/hastings-bexhill-rfc.html), [Crowborough](club/crowborough-rfc.html) |
| West Sussex | [Chichester](club/chichester-rfc.html), [Bognor](club/bognor-rfc.html), [Horsham](club/horsham-rfc.html), [Crawley](club/crawley-rfc.html), [Midhurst](club/midhurst-rfc.html), [Pulborough](club/pulborough-rfc.html), [Worthing](club/worthing-rfc.html) |

Compare all of them on our [Sussex rugby clubs page](rugby-clubs-sussex.html).
'''),
    ],
    faqs=[
        ('When was Brighton RFC founded?', 'Brighton Football Club (RFU) was founded in 1868. Because that was before the RFU was formed in 1871, it keeps the "FC" name.'),
        ('Where does Brighton RFC play?', 'The club plays at Waterhall Playing Fields, Waterhall Road, on the northern edge of Brighton.'),
        ('What are the Brighton Blues?', 'Brighton Blues is the nickname of Brighton Football Club (RFU), the rugby union club based at Waterhall.'),
        ('Are there other rugby clubs in Brighton and Hove?', 'Yes. Hove RFC plays at Hove Recreation Ground, and Brighton & Hove Sea Serpents RFC is a gay and inclusive club. Lewes, Burgess Hill and Haywards Heath are nearby.'),
    ],
    sources=[
        ('Brighton Blues: club history (Pitchero)', 'https://www.brightonblues.co.uk/a/club-history-36020.html'),
        ('The Rugby Paper: Brighton lay claim to being rugby\'s oldest', 'https://therugbypaper.co.uk/?p=313861'),
        ('World Rugby Museum: Kent v Sussex 1866', 'https://worldrugbymuseum.com/from-the-vaults/club-rugby/kent-v-sussex-1866-the-worlds-first-representative-match'),
        ('Brighton & Hove City Council: playing pitch strategy, rugby', 'https://design.brighton-hove.gov.uk/playing-pitch-strategy-appendix-d-assessment-need-report-rugby'),
    ],
)

# ---------------------------------------------------------------------------------------------
CLUBS['eccles-salford-arlfc'] = dict(
    title='Eccles & Salford ARLFC: Salford City Roosters Rugby League',
    meta='Eccles & Salford ARLFC is now Salford City Roosters, an amateur rugby league club in Greater Manchester with men\'s and junior teams. See how to join.',
    about=[
        'Eccles & Salford ARLFC is an amateur rugby league club in Salford, Greater Manchester. It is now known as Salford City Roosters and began as G.E.C. in the late 1970s before becoming Eccles ARLFC and, for a time, Eccles Roosters.',
        'The club runs a men\'s team in the North West Men\'s League and junior boys\' and girls\' teams.',
    ],
    history=[
        'Salford City Roosters began in the late 1970s as G.E.C. in the Manchester league system; Wikipedia gives 1977 and the club\'s own fundraising page says 1980. It became Eccles ARLFC, won its first league title in 1980-81, and was renamed Eccles Roosters after linking up with the Sydney Roosters. It later became Salford City Roosters and left the National Conference League in 2019. Our directory previously gave 1921 as the founding year, which we could not match to any source.',
    ],
    answer='Eccles & Salford ARLFC is an amateur rugby league club in Eccles, Salford, Greater Manchester, now called Salford City Roosters. Its men\'s team plays in the North West Men\'s League, and the club runs 11 boys\' and girls\' teams from under-6s upwards. It left the National Conference League in 2019.',
    sections=[
        dict(id='roosters-name', h2='Is Eccles & Salford ARLFC the same as Salford City Roosters?',
             answer='Yes. The club that our directory lists as Eccles & Salford ARLFC now plays as Salford City Roosters. It started as G.E.C., became Eccles ARLFC, then Eccles Roosters after a link-up with the Sydney Roosters, and finally Salford City Roosters. Search for any of those names to find it.',
             md='''
| Era | Name |
|---|---|
| Late 1970s | G.E.C. |
| By 1980-81 | Eccles ARLFC, which won its first league title that season |
| Roosters link-up | Eccles Roosters, after a partnership with the Sydney Roosters (NRL) |
| Now | Salford City Roosters |

Alfrieda Kindon, who gave four decades to the club, was awarded the Silver Boot Award. Wikipedia lists the ground as the Moat Hall Sports Centre in Eccles; confirm training venues with the club before you travel.
'''),
        dict(id='north-west-clubs', h2='Which rugby clubs are in the North West?',
             answer='The North West has more rugby clubs than any other region in our directory, with rugby league concentrated around Wigan, Leigh, Salford, St Helens and Warrington. For the nearest clubs to Salford, start with the Greater Manchester list below, then try our Lancashire and Cheshire pages.',
             md='''
Amateur and professional rugby league clubs near Salford:

| Club | Town | Profile |
|---|---|---|
| Irlam Hornets ARLFC | Irlam | [Irlam Hornets](club/irlam-hornets-arlfc.html) |
| Swinton Lions | Swinton | [Swinton Lions](club/swinton-lions.html) |
| Salford Red Devils | Salford | [Salford Red Devils](club/salford-red-devils.html) |
| Wigan St Judes ARLFC | Wigan | [Wigan St Judes](club/wigan-st-judes.html) |
| Leigh Miners Rangers | Leigh | [Leigh Miners Rangers](club/leigh-miners-rangers.html) |

Area guides: [Manchester](rugby-clubs-manchester.html), [Lancashire](rugby-clubs-lancashire.html), [Cheshire](rugby-clubs-cheshire.html), [Merseyside](rugby-clubs-merseyside.html) and [Cumbria](rugby-clubs-cumbria.html).
'''),
    ],
    faqs=[
        ('What league does Salford City Roosters play in?', 'Its men\'s team plays in the North West Men\'s League. The club previously competed in the National Conference League and left in 2019.'),
        ('Does the club run junior teams?', 'Yes. The club says it fields 11 boys\' and girls\' teams from under-6s up to its men\'s team.'),
        ('Where is Eccles ARLFC?', 'The club is in Eccles in the City of Salford, Greater Manchester. Wikipedia lists the Moat Hall Sports Centre as its ground, so confirm with the club before visiting.'),
        ('Why is it listed as Eccles & Salford ARLFC?', 'That was the name used in our directory. The club now trades as Salford City Roosters, so we show both names.'),
    ],
    sources=[
        ('Salford City Roosters: about us', 'https://www.salfordcityroosters.com/about'),
        ('Wikipedia: Salford City Roosters', 'https://en.wikipedia.org/wiki/Salford_City_Roosters'),
        ('Total Rugby League: Salford pull out of NCL (2019)', 'https://www.totalrl.com/salford-pull-out/'),
    ],
)

# ---------------------------------------------------------------------------------------------
CLUBS['leeds-rhinos'] = dict(
    title='Leeds Rhinos: Address, History & Leeds Rugby Union Clubs',
    meta='Leeds Rhinos, founded 1870, play Super League at Headingley Stadium, LS6 3BR. Get the address, club facts and details of Leeds rugby union side Tykes.',
    about=[
        'Leeds Rhinos are a professional rugby league club in Leeds, West Yorkshire, founded in 1870 as Leeds St John\'s. They play in Super League at Headingley Stadium, St Michael\'s Lane, Leeds LS6 3BR.',
        'The Rhinos are a rugby league club. The city\'s rugby union club is Leeds Tykes, which plays in National League 1.',
    ],
    history=[
        'Leeds Rhinos began in 1870 as Leeds St John\'s, a church club known as the "Old Blue and Ambers", which played at the Militia Barracks before moving to Cardigan Fields near Headingley. The club has played at Headingley since 1890, and it dropped "St John\'s" that year. It was a founder member of the Northern Union in 1895, and the "Rhinos" name arrived in 1997 as Super League began. Our directory previously gave 1890 as the founding year, which is the year the club moved to Headingley, so we have corrected it to 1870.',
    ],
    answer='Leeds Rhinos are a professional rugby league club founded in 1870 as Leeds St John\'s. They play in Super League at Headingley Stadium, St Michael\'s Lane, Leeds LS6 3BR. Leeds also has a separate rugby union club, Leeds Tykes, which plays in National League 1.',
    sections=[
        dict(id='rhinos-facts', h2='What are the key facts about Leeds Rhinos?',
             answer='Leeds Rhinos are nicknamed the Rhinos and the Loiners, play in blue and amber, and have won the League Championship 11 times, the Challenge Cup 14 times and the World Club Challenge three times, according to Wikipedia. Their home is Headingley Stadium in north-west Leeds.',
             md='''
| Fact | Detail |
|---|---|
| Founded | 1870, as Leeds St John's |
| Nicknames | The Rhinos, the Loiners |
| Colours | Blue and amber |
| Competition | Super League (2026) |
| Ground | Headingley Stadium, St Michael's Lane, Leeds LS6 3BR |
| Honours (Wikipedia) | 11 League Championships, 14 Challenge Cups, 3 World Club Challenges |
| Same-site sports | Yorkshire County Cricket Club plays at the adjoining ground |
| Tickets and contact | Use the official club website; we do not hold a verified public phone number |

The Rhinos are a professional club and do not run open-age teams for beginners. For amateur rugby league in Leeds, see East Leeds, West Leeds, Hunslet Warriors and Bramley Buffaloes on our [Leeds rugby clubs page](rugby-clubs-leeds.html).
'''),
        dict(id='leeds-union', h2='Is there a Leeds rugby union team?',
             answer='Yes. Leeds Tykes is Leeds\' rugby union club and plays in National League 1, the third tier of English rugby, at The Sycamores in Bramhope. It was formed in 1991 as Leeds RUFC from the merger of Roundhay and Headingley, and its history is closely tied to the Rhinos.',
             md='''
| Detail | Leeds Rhinos | Leeds Tykes |
|---|---|---|
| Code | Rugby league | Rugby union |
| Competition | Super League | National League 1 (2026-27) |
| Ground | Headingley Stadium | The Sycamores, Bramhope |
| Founded | 1870 | 1991 (as Leeds RUFC) |
| Link | Both clubs came together under Leeds Rugby Limited in 1998 | Played at Headingley from 1996 and later moved to The Sycamores |

For union clubs at every level in the city, including Roundhay and Otley, use our [Leeds rugby clubs page](rugby-clubs-leeds.html) and the [rugby union directory](rugby-union.html).
'''),
        dict(id='rhinos-address', h2='What is the Leeds Rhinos address?',
             answer='The address is Headingley Stadium, St Michael\'s Lane, Leeds LS6 3BR. The ground is in Headingley, about two miles north-west of Leeds city centre, and shares its site with the cricket ground. For ticket office hours and match-day travel, check the official club website before you go.',
             md='''
- **Address:** Headingley Stadium, St Michael's Lane, Leeds LS6 3BR
- **Area:** Headingley, north-west Leeds
- **Official site:** [leedsrhinos.com](https://www.leedsrhinos.com)
- **Visitors from other clubs:** the Rhinos publish away-fan guides, so supporters from other clubs can usually find match-day information on their own club's site as well.
'''),
    ],
    faqs=[
        ('Where do Leeds Rhinos play?', 'Leeds Rhinos play at Headingley Stadium, St Michael\'s Lane, Leeds LS6 3BR. They have played at Headingley since 1890.'),
        ('When were Leeds Rhinos founded?', 'The club was founded in 1870 as Leeds St John\'s. The "Rhinos" name was adopted in 1997, at the start of Super League.'),
        ('Do Leeds Rhinos play rugby union?', 'No. Leeds Rhinos are a rugby league club. Leeds Tykes is the city\'s rugby union club, and it plays in National League 1.'),
        ('Can I join Leeds Rhinos as a player?', 'The Rhinos are a professional club, so beginners cannot simply join. Local amateur rugby league clubs such as East Leeds and West Leeds welcome new players.'),
    ],
    sources=[
        ('Wikipedia: Leeds Rhinos', 'https://en.wikipedia.org/wiki/Leeds_Rhinos'),
        ('Wikipedia: Leeds Tykes', 'https://en.wikipedia.org/wiki/Leeds_Tykes'),
        ('Leeds Tykes: matchday and fixtures', 'https://www.leeds-tykes.com/home/matchday/'),
        ('Leeds Rhinos: official site', 'https://www.leedsrhinos.com'),
    ],
)

# ---------------------------------------------------------------------------------------------
CLUBS['st-helens-rfc'] = dict(
    title='St Helens RFC (Saints): Rugby League Club, Address & History',
    meta='St Helens RFC, the Saints, are a Super League rugby league club founded in 1873. Get the BrewDog Stadium address and find St Helens union clubs.',
    about=[
        'St Helens R.F.C., known as Saints, is a professional rugby league club in St Helens, Merseyside, founded in 1873. They play in Super League at the BrewDog Stadium, formerly the Totally Wicked Stadium, in the Peasley Cross area of the town.',
        'Despite "RFC" in the name, this is not a rugby union club. St Helens RFC (Union) is listed separately.',
    ],
    history=[
        'St Helens was founded in 1873 and was a founder member of the Northern Union in 1895. The club left Knowsley Road in 2011 for a new stadium, which opened in 2012 as Langtree Park. The ground was called the Totally Wicked Stadium from 2017 to 2025. In October 2025 the club agreed a ten-year partnership with BrewDog, and the home of the Saints became the BrewDog Stadium.',
    ],
    answer='St Helens RFC, known as the Saints, is a professional rugby league club founded in 1873 that plays in Super League. The club\'s address is the BrewDog Stadium, McManus Drive, St Helens WA9 3AL. The town\'s rugby union club, St Helens RFC (Union), is a separate listing.',
    sections=[
        dict(id='saints-address', h2='What is the St Helens rugby club address?',
             answer='The Saints\' address is the BrewDog Stadium, McManus Drive, Peasley Cross, St Helens WA9 3AL. By car, leave the M62 at junction 7, follow the A570 James Roby Way to Sherdley Road, then bear left onto Peasley Cross Lane.',
             md='''
| Detail | Information |
|---|---|
| Stadium | BrewDog Stadium (Totally Wicked Stadium 2017-2025; Langtree Park 2012-2016) |
| Address | McManus Drive, Peasley Cross, St Helens WA9 3AL |
| Capacity | About 18,000 |
| By car | M62 junction 7, A570 (James Roby Way / St Helens Linkway), Sherdley Road, Peasley Cross Lane |
| Parking | The neighbouring retail park and Tesco Extra warn that people who are not using their stores may receive a fixed penalty charge |
| Walking | The stadium is reached via the Steve Prescott Bridge over James Roby Way |
| Ticket and club enquiries | Official site: [saintsrlfc.com](https://www.saintsrlfc.com) |
'''),
        dict(id='st-helens-union', h2='Is there a St Helens rugby union club?',
             answer='Yes. St Helens RFC (Union) is the town\'s rugby union club and is listed separately from the Saints. People searching for St Helens rugby union are usually looking for that club or for others on Merseyside, which our Merseyside guide covers.',
             md='''
- **Saints (this page):** rugby league, Super League, BrewDog Stadium.
- **St Helens RFC (Union):** [rugby union profile](club/st-helens-rfc-union.html).
- **Amateur rugby league nearby:** [Thatto Heath Crusaders](club/thatto-heath-crusaders.html), who play in the NCRL National Premier League in 2026.
- **More clubs:** [rugby clubs in Merseyside](rugby-clubs-merseyside.html).
'''),
    ],
    faqs=[
        ('Where do St Helens rugby league club play?', 'St Helens play at the BrewDog Stadium, McManus Drive, St Helens WA9 3AL. The ground opened in 2012 as Langtree Park and was the Totally Wicked Stadium from 2017 to 2025.'),
        ('When was St Helens RFC founded?', 'The Saints were founded in 1873 and were one of the founder clubs of the Northern Union in 1895.'),
        ('Is St Helens RFC a rugby union or rugby league club?', 'This profile is for the Saints, a rugby league club. St Helens RFC (Union) is a separate rugby union club in the town.'),
        ('Can I park near the stadium?', 'Do not park at the neighbouring retail park or Tesco Extra unless you are visiting those stores, because you may be charged a fixed penalty. Check the club\'s match-day guide for official parking.'),
    ],
    sources=[
        ('St Helens R.F.C.: match days at the stadium (February 2025)', 'https://www.saintsrlfc.com/2025/02/12/match-days-at-the-totally-wicked-stadium/'),
        ('St Helens R.F.C.: BrewDog partnership and stadium rename (October 2025)', 'https://www.saintsrlfc.com/2025/10/20/st-helens-r-f-c-announces-landmark-partnership-with-brewdog-welcome-to-the-brewdog-stadium/'),
        ('St Helens R.F.C.: Challenge Cup semi-final fan guide (directions)', 'https://www.saintsrlfc.com/?p=92578'),
                ('Charity Commission: Saints Community Development Foundation (address)', 'https://register-of-charities.charitycommission.gov.uk/en/charity-search/-/charity-details/5114650/contact-information'),
    ],
)

# ---------------------------------------------------------------------------------------------
CLUBS['warrington-wolves'] = dict(
    title='Warrington Wolves: Contact Number, Address & Club Guide',
    meta='Warrington Wolves, founded 1876, play Super League at the Halliwell Jones Stadium, WA2 7NE. Find the contact number, address and Warrington amateur clubs.',
    about=[
        'Warrington Wolves are a professional rugby league club in Warrington, Cheshire, founded in 1876 as Warrington Zingari. They play in Super League at the Halliwell Jones Stadium, Mike Gregory Way, Warrington WA2 7NE.',
        'The club is also known as "the Wire", a reference to the town\'s wire-making industry.',
    ],
    history=[
        'Warrington Wolves were founded in 1876 as Warrington Zingari Football Club by seven young local men. "Zingari" was a common name for clubs without a permanent home. The club took the Warrington name from 1877, was one of the founders of the Northern Union in 1895 and added "Wolves" officially in 1997. Our directory previously gave 1879, but the club\'s heritage research and Wikipedia both give 1876. The Wolves moved from Wilderspool Stadium to the Halliwell Jones Stadium in the early 2000s.',
    ],
    answer='Warrington Wolves are a professional rugby league club founded in 1876 that plays in Super League at the Halliwell Jones Stadium, Warrington WA2 7NE. The club\'s main enquiry number published by other clubs is 01925 248888, open Monday to Friday, 10am to 4pm. Confirm it on the official website before ringing.',
    sections=[
        dict(id='wolves-contact', h2='What is the Warrington Wolves contact number?',
             answer='The Warrington Wolves enquiry line published by visiting clubs is 01925 248888, staffed Monday to Friday, 10am to 4pm. The ticket office is at the Halliwell Jones Stadium, and the club email listed on other clubs\' away-day pages is info@warringtonwolves.com. Use the club website to confirm before you call.',
             md='''
| Contact route | Detail | How we checked |
|---|---|---|
| Phone | 01925 248888, Monday to Friday, 10am to 4pm | Printed on a Leeds Rhinos away-fans page (2018) and not yet re-checked against the Wolves' own site |
| Email | info@warringtonwolves.com | Listed on Huddersfield Giants' away-day page |
| Post and visits | The Halliwell Jones Stadium, Mike Gregory Way, Warrington WA2 7NE | Warrington Wolves ticket information page |
| Foundation | Warrington Wolves Community Foundation, 01925 248884 | Charity Commission register |
| Official site | [warringtonwolves.com](https://www.warringtonwolves.com) | Use it for the current numbers |

We checked these on 14 November 2026 only against third-party pages. Club numbers change, so please confirm on the official website. If you find one that is out of date, tell us and we will fix it.
'''),
        dict(id='wolves-club', h2='What are the key facts about Warrington Wolves?',
             answer='Warrington Wolves were founded in 1876 as Warrington Zingari and are nicknamed the Wire. The club says it is the only British club to have played every season in the top flight. Its stadium holds about 15,000 and it plays in Super League in 2026.',
             md='''
- **Founded:** 1876, as Warrington Zingari Football Club; became simply Warrington in 1877 and Warrington Wolves in 1997.
- **Name:** "the Wire" refers to the town's wire-making industry.
- **Ground:** Halliwell Jones Stadium, replacing Wilderspool Stadium, the club's home for around 100 years.
- **Honours:** Wikipedia lists the League Championship three times and the Challenge Cup nine times.
- **Rivals:** Widnes Vikings, St Helens, Wigan Warriors and Leigh Leopards.
'''),
        dict(id='warrington-amateur', h2='Are there amateur rugby league clubs in Warrington?',
             answer='Yes. Our directory lists Crosfields ARLFC, Latchford ARLFC and Woolston Rovers ARLFC in Warrington, plus Warrington RFC for rugby union. The Wolves are professional, so new players should contact a local amateur club or the club\'s foundation for community sessions.',
             md='''
| Club | Code | Profile |
|---|---|---|
| Crosfields ARLFC | Rugby league | [Crosfields](club/crosfields-arlfc.html) |
| Latchford ARLFC | Rugby league | [Latchford](club/latchford-arlfc.html) |
| Woolston Rovers ARLFC | Rugby league | [Woolston Rovers](club/woolston-rovers-arlfc.html) |
| Warrington RFC | Rugby union | [Warrington RFC](club/warrington-rfc.html) |

More clubs in the area are on our [Cheshire rugby clubs page](rugby-clubs-cheshire.html).
'''),
    ],
    faqs=[
        ('What is the Warrington Wolves phone number?', 'Visiting clubs publish 01925 248888 as the Wolves\' enquiry line, answered Monday to Friday, 10am to 4pm. Check warringtonwolves.com before calling, as numbers can change.'),
        ('Where do Warrington Wolves play?', 'They play at the Halliwell Jones Stadium, Mike Gregory Way, Warrington WA2 7NE.'),
        ('When were Warrington Wolves founded?', 'The club was founded in 1876 as Warrington Zingari. It became Warrington in 1877 and added "Wolves" in 1997.'),
        ('Why are Warrington Wolves called the Wire?', 'The nickname refers to Warrington\'s historic wire-making industry.'),
    ],
    sources=[
        ('Warrington Wolves: ticket information', 'https://warringtonwolves.com/tickets-and-hospitality/ticket-information'),
        ('Leeds Rhinos: fan information, Warrington Wolves (away)', 'https://therhinos.co.uk/article/23514/fan-information-|-warrington-wolves-(away)'),
        ('Huddersfield Giants: Warrington away-day information', 'https://giantsrl.com/the-club/away-day-information/warrington-wolves'),
        ('Warrington Rugby Heritage: history', 'https://www.warringtonrugbyheritage.com/history'),
        ('Wikipedia: Warrington Wolves', 'https://en.wikipedia.org/wiki/Warrington_Wolves'),
    ],
)

# ---------------------------------------------------------------------------------------------
CLUBS['irfu'] = dict(
    title='IRFU: Irish Rugby Football Union and Irish Club Rugby',
    meta='The IRFU runs rugby union across Ireland, including the Energia All-Ireland League. See how Irish club rugby works and the Northern Ireland clubs.',
    about=[
        'The Irish Rugby Football Union (IRFU) is the governing body for rugby union across the island of Ireland, in both the Republic of Ireland and Northern Ireland. It is based in Dublin and was founded in 1879.',
        'This is a governing-body listing, not a playing club. To find an Irish club, use the Energia All-Ireland League and Northern Ireland club information below.',
    ],
    history=[
        'The IRFU was formed in 1879 and organises the game through four provincial branches: Leinster, Munster, Ulster and Connacht. Ulster covers Northern Ireland. The IRFU runs the Energia All-Ireland League for men and women, the top level of club rugby on the island.',
    ],
    answer='The Irish Rugby Football Union (IRFU) governs rugby union across the island of Ireland through four provinces: Leinster, Munster, Ulster and Connacht. It runs the Energia All-Ireland League, the top tier of Irish club rugby, which has five men\'s divisions and, from 2026-27, restructured lower divisions.',
    sections=[
        dict(id='irish-club-structure', h2='How does Irish club rugby work?',
             answer='Irish club rugby is organised through the IRFU and its four provincial branches. The Energia All-Ireland League sits at the top, with five men\'s divisions of 10 teams in 2025-26. Below it, provincial leagues in Leinster, Munster, Ulster and Connacht feed promotion into the AIL.',
             md='''
| Level | Competition | Notes |
|---|---|---|
| Professional | United Rugby Championship | Leinster, Munster, Ulster and Connacht |
| Top club level | Energia All-Ireland League (AIL) | Five men's divisions in 2025-26: 1A, 1B, 2A, 2B and 2C |
| Provincial leagues | Leinster, Munster, Ulster and Connacht leagues | Winners play off for AIL places |
| Community | Local club leagues and junior rugby | Run by each province |

**2025-26:** St Mary's College won their third AIL title, with Clontarf runners-up.

**2026-27:** the IRFU is merging Divisions 2B and 2C and splitting them geographically into 2BN (North) and 2BS (South). Clubs placed in the new divisions include Banbridge, Malone, Rainey Old Boys, Ballyclare, Bective Rangers, Clonmel, Enniscorthy and Skerries.

The women's AIL is also being restructured for 2026-27, so check [irishrugby.ie](https://www.irishrugby.ie) for the current format.
'''),
        dict(id='northern-ireland-clubs', h2='What Irish rugby clubs are in Northern Ireland?',
             answer='Our directory lists Armagh, Ballymena, Dungannon, Instonians and Malone, plus Ulster Rugby, for Northern Ireland. They fall under the IRFU\'s Ulster branch, and several play in the Energia All-Ireland League, so they are the best starting point for club rugby in the UK part of Ireland.',
             md='''
| Club | Town | Profile |
|---|---|---|
| Armagh RFC | Armagh | [Armagh](club/armagh-rfc.html) |
| Ballymena RFC | Ballymena | [Ballymena](club/ballymena-rfc.html) |
| Dungannon RFC | Dungannon | [Dungannon](club/dungannon-rfc.html) |
| Instonians RFC | Belfast | [Instonians](club/instonians-rfc.html) |
| Malone RFC | Belfast | [Malone](club/malone-rfc.html) |
| Ulster Rugby | Belfast | [Ulster Rugby](club/ulster-rugby.html) |

For clubs in the Republic of Ireland, use the IRFU's own club finder. Our [UK rugby leagues guide](rugby-leagues-uk.html) explains how the Irish pyramid compares with the English, Scottish and Welsh ones.
'''),
    ],
    faqs=[
        ('What is the IRFU?', 'The IRFU is the Irish Rugby Football Union, the governing body for rugby union across the whole island of Ireland. It was founded in 1879 and is based in Dublin.'),
        ('What is the Energia All-Ireland League?', 'It is the top level of club rugby in Ireland, run by the IRFU. In 2025-26 it had five men\'s divisions of 10 teams, and St Mary\'s College won the title.'),
        ('Does the IRFU cover Northern Ireland?', 'Yes. Rugby union in Northern Ireland is run through the IRFU\'s Ulster branch, and Northern Ireland clubs compete in the same league system as clubs in the Republic.'),
        ('How do I find an Irish rugby club to join?', 'Start with the IRFU\'s club information or the Ulster Rugby site for clubs in Northern Ireland. Our directory also lists Northern Ireland clubs with their towns.'),
    ],
    sources=[
        ('IRFU: Energia men\'s All-Ireland League', 'https://www.irishrugby.ie/energia-all-ireland-league/energia-mens-ail'),
        ('IRFU: changes to the men\'s AIL for 2026/27', 'https://www.irishrugby.ie/2025/10/30/irfu-confirms-changes-to-mens-energia-all-ireland-league-structure-for-26-27-season/'),
        ('IRFU: AIL divisional rundown, April 2026', 'https://www.irishrugby.ie/2026/04/04/energiaail-mens-divisions-play-off-details-ups-downs/'),
        ('Wikipedia: 2025-26 All-Ireland League', 'https://en.wikipedia.org/wiki/2025%E2%80%9326_All-Ireland_League_(rugby_union)'),
    ],
)
