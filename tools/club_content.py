#!/usr/bin/env python3
"""
Club page content upgrade (idempotent). For every club page in club/:

- Title: adds the "<Name> Rugby Club" / "Rugby League Club" form people search for,
  keeping the official name, e.g. "Siddal Rugby League Club (Siddal ARLFC) | Halifax"
- "At a glance" block in the About column: a direct answer naming the club, its
  code, town, founding year and confirmed 2026-27 league, plus a facts table
  (also-known-as names, league and level, ground, governing body, contact, area guide)
- Extra FAQ "What league does X play in?" where the league is confirmed
- FAQPage JSON-LD built from the visible FAQs, and alternateName on SportsTeam
- Hand-written paragraphs for the highest-volume clubs (OVERRIDES)

Data: tools/clubs.json, tools/er-teams.csv (England Rugby, 31 Oct 2026),
tools/club-contacts.csv. Run from repo root: python3 tools/club_content.py
"""
import csv
import html as H
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://ukrugbyclubdirectory.co.uk'

PREM = {'bath-rugby', 'bristol-bears', 'exeter-chiefs', 'gloucester-rugby', 'harlequins', 'leicester-tigers',
        'newcastle-falcons', 'northampton-saints', 'sale-sharks', 'saracens'}
SUPER_LEAGUE = {'bradford-bulls', 'castleford-tigers', 'catalans-dragons', 'huddersfield-giants', 'hull-fc',
                'hull-kingston-rovers', 'leeds-rhinos', 'leigh-leopards', 'st-helens-rfc', 'toulouse-olympique',
                'wakefield-trinity', 'warrington-wolves', 'wigan-warriors', 'york-knights'}
NCRL_PREMIER = {'siddal-arlfc', 'heworth-arlfc', 'thatto-heath-crusaders', 'west-hull-arlfc', 'wigan-st-judes',
                'castleford-lock-lane'}

WALES = {'Ceredigion', 'South Glamorgan', 'Carmarthenshire', 'Neath Port Talbot', 'Rhondda Cynon Taf', 'Caerphilly',
         'Powys', 'Bridgend', 'Conwy', 'Blaenau Gwent', 'Gwent', 'Monmouthshire', 'Pembrokeshire', 'Swansea', 'Newport',
         'Gwynedd', 'Vale of Glamorgan', 'Torfaen', 'Merthyr Tydfil', 'Denbighshire', 'Flintshire', 'Wrexham',
         'Isle of Anglesey', 'Anglesey', 'Mid Glamorgan', 'West Glamorgan', 'Cardiff'}
SCOT = {'Midlothian', 'Lanarkshire', 'Roxburghshire', 'Aberdeenshire', 'Angus', 'Fife', 'Stirlingshire',
        'Clackmannanshire', 'Edinburgh', 'Glasgow', 'Ayrshire', 'Berwickshire', 'Selkirkshire', 'Perthshire',
        'East Lothian', 'Dunbartonshire', 'Renfrewshire', 'Dumfriesshire', 'Highland', 'Inverness-shire',
        'Peeblesshire', 'West Lothian', 'Scottish Borders', 'Morayshire', 'Moray', 'Argyll', 'Kinross-shire'}
NI = {'County Antrim', 'County Down', 'County Armagh', 'County Londonderry', 'County Tyrone', 'County Fermanagh'}

HUB = {  # county -> (hub page, label)
    'Greater London': ('rugby-clubs-london', 'London'), 'Greater Manchester': ('rugby-clubs-manchester', 'Manchester'),
    'Cumbria': ('rugby-clubs-cumbria', 'Cumbria'), 'Merseyside': ('rugby-clubs-merseyside', 'Merseyside'),
    'Kent': ('rugby-clubs-kent', 'Kent'), 'Cheshire': ('rugby-clubs-cheshire', 'Cheshire'),
    'North Yorkshire': ('rugby-clubs-north-yorkshire', 'North Yorkshire'),
    'County Durham': ('north-east-rugby-clubs', 'the North East'), 'Tyne and Wear': ('north-east-rugby-clubs', 'the North East'),
    'Northumberland': ('north-east-rugby-clubs', 'the North East'), 'Hertfordshire': ('rugby-clubs-hertfordshire', 'Hertfordshire'),
    'Hampshire': ('rugby-clubs-hampshire', 'Hampshire'), 'Isle of Wight': ('rugby-clubs-hampshire', 'Hampshire'),
    'Midlothian': ('rugby-clubs-edinburgh', 'Edinburgh'), 'East Lothian': ('rugby-clubs-edinburgh', 'Edinburgh'),
    'West Lothian': ('rugby-clubs-edinburgh', 'Edinburgh'), 'West Sussex': ('rugby-clubs-sussex', 'Sussex'),
    'East Sussex': ('rugby-clubs-sussex', 'Sussex'), 'Somerset': ('rugby-clubs-somerset', 'Somerset'),
    'Gloucestershire': ('rugby-clubs-gloucestershire', 'Gloucestershire'), 'Warwickshire': ('rugby-clubs-warwickshire', 'Warwickshire'),
    'Lancashire': ('rugby-clubs-lancashire', 'Lancashire'), 'Surrey': ('rugby-clubs-surrey', 'Surrey'),
    'Essex': ('rugby-clubs-essex', 'Essex'), 'Bristol': ('rugby-clubs-bristol', 'Bristol'),
    'West Midlands': ('rugby-clubs-birmingham', 'Birmingham'), 'South Glamorgan': ('rugby-clubs-cardiff', 'Cardiff'),
    'East Yorkshire': ('rugby-clubs-hull', 'Hull'), 'Devon': ('south-west-rugby-clubs', 'the South West'),
    'Cornwall': ('south-west-rugby-clubs', 'the South West'), 'Dorset': ('south-west-rugby-clubs', 'the South West'),
    'Wiltshire': ('south-west-rugby-clubs', 'the South West'),
}
LEEDS_TOWNS = {'Leeds', 'Otley', 'Ilkley', 'Morley', 'Guiseley', 'Kippax'}

# Extra names people search for, and hand-written context for high-volume club searches.
OVERRIDES = {
    'siddal-arlfc': dict(aka=['Siddal RL', 'Siddal RLFC', 'Siddal Rugby League Club', 'Siddal Rugby Club'],
        extra='Siddal are one of the strongest amateur rugby league clubs in the country. In 2026 they are one of the 12 clubs in the NCRL National Premier League, which replaced the National Conference League as the top level of community rugby league. The club, from the Siddal area of Halifax, also runs junior teams, and new players can contact it about open-age and youth training.'),
    'trojans-rfc': dict(aka=['Trojans RFC', 'Trojans Southampton', 'Southampton Trojans', 'Trojans Club Southampton'],
        extra='Trojans is one of Hampshire\'s oldest rugby clubs, founded in 1874. It is based in Eastleigh on the northern edge of Southampton, which is why it is often searched for as "Trojans Southampton". It is a multi-sport club, and its rugby section plays in Counties 1 Hampshire in 2026-27. The nearest alternatives are Eastleigh RFC and Tottonians in Totton.'),
    'uckfield-rfc': dict(aka=['Uckfield Rugby Football Club', 'Uckfield Rugby Club', 'Uckfield Rugby'],
        extra='Uckfield RFC is the rugby club for Uckfield and the surrounding villages of the East Sussex Weald, founded in 1936. Like most Sussex community clubs, it runs adult teams alongside a mini and junior section. Nearby clubs include Crowborough and Lewes.'),
    'old-leamingtonians-rfc': dict(aka=['OLRFC', 'Old Leams', 'Old Leamingtonians Rugby Club'],
        extra='Old Leamingtonians, usually shortened to "Old Leams" or OLRFC, is one of two rugby union clubs in Leamington Spa. It was founded in 1927 and plays in Counties 1 Midlands West (South) in 2026-27, the same league as neighbours Leamington RFC.'),
    'leigh-leopards': dict(aka=['Leigh Centurions', 'Leigh RLFC', 'Leigh Rugby League Club', 'Leigh Rugby Club'],
        extra='Leigh Leopards were known as Leigh Centurions until they rebranded in 2022, and many people still search for the old name. The club plays in Super League in 2026. For amateur rugby league in the town, see Leigh Miners Rangers and Leigh East. Leigh also has a rugby union club, Leigh RFC.'),
    'leeds-rhinos': dict(aka=['Leeds Rugby League Club', 'Leeds RLFC', 'The Rhinos'],
        ground='Headingley Stadium, St Michael\'s Lane, Leeds LS6 3BR',
        extra='Leeds Rhinos play rugby league in Super League at Headingley Stadium. The stadium shares a site with Yorkshire\'s cricket ground. If you are looking for a rugby union club in Leeds, or to play yourself, see our Leeds rugby clubs page: the Rhinos are a professional team and do not run open-age teams for the public.'),
    'warrington-wolves': dict(aka=['Warrington Rugby League Club', 'Warrington RLFC', 'The Wire', 'The Wolves'],
        ground='The Halliwell Jones Stadium, Mike Gregory Way, Warrington WA2 7NE',
        extra='Warrington Wolves play rugby league in Super League at the Halliwell Jones Stadium. The club\'s traditional nickname is "The Wire", a reference to the town\'s wire-making industry, and "the Wolves" was added in the Super League era. For tickets and contact, use the club\'s official website. For amateur rugby league in the town, see our Cheshire rugby clubs page.'),
    'irfu': dict(aka=['Irish Rugby Football Union', 'Irish Rugby', 'Ireland Rugby'],
        extra='The IRFU is the governing body for rugby union across the whole island of Ireland, including Northern Ireland. It runs the Energia All-Ireland League (AIL), the top club competition. From 2026-27 the AIL\'s lower divisions are split into regional 2B North and 2B South divisions. Professional rugby is played by the four provinces, Leinster, Munster, Ulster and Connacht, in the United Rugby Championship.'),
    'st-helens-rfc': dict(aka=['St Helens Saints', 'Saints RLFC', 'St Helens Rugby League Club'],
        extra='St Helens R.F.C., known as Saints, play rugby league in Super League. Despite the "RFC" in the name, this is the town\'s professional rugby league club. If you are looking for rugby union in St Helens, see St Helens RFC (Union), listed separately in our directory.'),
    'st-helens-rfc-union': dict(aka=['St Helens Rugby Union Club', 'St Helens RUFC']),
    'whitehaven-rfc-union': dict(aka=['Whitehaven Rugby Union Club', 'Whitehaven RUFC']),
    'bristol-bears': dict(aka=['Bristol Rugby', 'Bristol Bears Rugby', 'Bristol Rugby Club']),
    'edinburgh-rugby': dict(aka=['Edinburgh Rugby Club', 'Edinburgh Rugby Team']),
    'hull-rufc': dict(aka=['Hull Rugby Union Club', 'Hull RUFC', 'Hull Rugby Club']),
    'folkestone-rfc': dict(aka=['Folkestone Rugby Club', 'Folkestone Rugby Football Club']),
    'llanishen-rfc': dict(aka=['Llanishen Rugby Club', 'Llanishen Rugby Football Club']),
    'solihull-rfc': dict(aka=['Solihull Rugby Club', 'Solihull Rugby Football Club', 'Solihull Rugby']),
    'chiswick-rfc': dict(aka=['Chiswick Rugby Club', 'Chiswick Rugby Football Club']),
}


def norm(name):
    return re.sub(r'\s*\((?:Union|Rugby Union|League)\)', '', name).strip()


def split_name(name):
    n = norm(name)
    m = re.match(r'^(.*?)\s+(RFC|RUFC|ARLFC|RLFC|FC|Rugby Football Club|Rugby Club|Rugby Union Club|Rugby)$', n)
    return (m.group(1), m.group(2)) if m else (n, None)


def variants(name, sport, slug):
    base, suf = split_name(name)
    v = []
    if suf:
        if 'League' in sport:
            v = [f'{base} Rugby League Club'] + ([f'{base} ARLFC'] if suf == 'ARLFC' else []) + [f'{base} RLFC', f'{base} RL']
        else:
            v = [f'{base} Rugby Club', f'{base} RFC', f'{base} Rugby Football Club', f'{base} Rugby']
            if suf == 'RUFC':
                v.insert(1, f'{base} RUFC')
    v = OVERRIDES.get(slug, {}).get('aka', []) + v
    out, seen = [], {name.lower(), norm(name).lower()}
    for x in v:
        if x.lower() not in seen:
            seen.add(x.lower())
            out.append(x)
    return out[:5]


def level(league):
    if not league:
        return None
    for pat, n in (('Champ Rugby', 2), (r'National League 1\b', 3), ('National League 2', 4), ('Regional 1', 5),
                   ('Regional 2', 6), ('Counties 1', 7), ('Counties 2', 8), ('Counties 3', 9), ('Counties 4', 10)):
        if re.search(pat, league):
            return n
    return None


def clean_league(l):
    l = re.sub(r' \|.*$', '', l or '').replace('Tribute Ale ', '').replace('adm ', '').strip()
    return l.replace('Middx', 'Middlesex')


def nation(county):
    return 'Wales' if county in WALES else 'Scotland' if county in SCOT else 'Northern Ireland' if county in NI else 'England'


def gov_body(sport, nat):
    if 'League' in sport:
        return 'Rugby Football League (RFL)'
    return {'England': 'Rugby Football Union (England Rugby)', 'Wales': 'Welsh Rugby Union (WRU)',
            'Scotland': 'Scottish Rugby', 'Northern Ireland': 'IRFU (Ulster Branch)'}[nat]


def league_sentence(slug, sport, league):
    if slug in PREM:
        return 'In 2026-27 the club plays in PREM Rugby, the top tier of English rugby union.', 'PREM Rugby (level 1)'
    if slug in SUPER_LEAGUE:
        return 'In 2026 the club plays in Super League, the top tier of rugby league.', 'Super League'
    if slug in NCRL_PREMIER:
        return ('In 2026 its open-age team plays in the NCRL National Premier League, the top level of amateur rugby league.',
                'NCRL National Premier League')
    lv = level(league)
    if league and lv:
        return (f'In 2026-27 its first XV plays in {league}, level {lv} of the English rugby union league structure.',
                f'{league} (level {lv})')
    if league:
        return f'In 2026-27 its first XV plays in the {league}.', league
    return '', None


def esc(t):
    return H.escape(t, quote=False)


def hub_for(c):
    if c['county'] == 'West Yorkshire' and c['town'] in LEEDS_TOWNS:
        return ('rugby-clubs-leeds', 'Leeds')
    return HUB.get(c['county'])


def build_glance(c, ct, league):
    slug, name, sport = c['slug'], norm(c['name']), c['sport']
    code = 'rugby league' if 'League' in sport else 'rugby union'
    base, suf = split_name(c['name'])
    aka = variants(c['name'], sport, slug)
    nat = nation(c['county'])
    where = c['town'] + (f', {c["county"]}' if c['county'] and c['county'] != c['town'] else '')
    founded = c['founded'] if re.fullmatch(r'\d{4}', c['founded'] or '') else ''
    lsent, lcell = league_sentence(slug, sport, league)
    answer = f'{name} is a {code} club in {where}' + (f', founded in {founded}' if founded else '') + '. '
    answer += lsent + (' ' if lsent else '')
    if aka:
        answer += f'It is also known as {", ".join(aka[:-1]) + " or " + aka[-1] if len(aka) > 1 else aka[0]}.'
    h2_name = f'{base} Rugby League Club' if suf and 'League' in sport else f'{base} Rugby Club' if suf else name
    ov = OVERRIDES.get(slug, {})
    ground = ov.get('ground') or ' '.join(x for x in [(ct or {}).get('ground_address', ''), (ct or {}).get('postcode', '')] if x).strip()
    has = [k for k, lbl in (('phone', 'phone'), ('email', 'email'), ('website', 'website'), ('facebook', 'Facebook')) if (ct or {}).get(k)]
    if has or c.get('ld_website'):
        contact = '<a href="#contact">' + esc(', '.join(lbl for k, lbl in (('phone', 'Phone'), ('email', 'Email'), ('website', 'Website'), ('facebook', 'Facebook')) if k in has) or 'Website') + ' – see Join &amp; Contact</a>'
    else:
        contact = '<a href="#contact">See Join &amp; Contact</a>'
    rows = [('Official name', esc(name))]
    if aka:
        rows.append(('Also known as', esc(', '.join(aka))))
    rows += [('Code', 'Rugby league' if code == 'rugby league' else 'Rugby union'), ('Based in', esc(where))]
    if founded:
        rows.append(('Founded', founded))
    if lcell:
        rows.append(('League (2026-27)' if 'League' not in sport else 'Competition (2026)', esc(lcell)))
    if ground:
        rows.append(('Ground', esc(ground)))
    rows.append(('Governing body', esc(gov_body(sport, nat))))
    rows.append(('Contact', contact))
    hub = hub_for(c)
    if hub:
        rows.append(('Area guide', f'<a href="../{hub[0]}.html">Rugby clubs in {esc(hub[1])}</a>'))
    table = '<div class="guide-table-wrap"><table class="guide-table glance-table"><tbody>' + ''.join(
        f'<tr><th scope="row">{k}</th><td>{v}</td></tr>' for k, v in rows) + '</tbody></table></div>'
    extra = f'<p>{esc(ov["extra"])}</p>' if ov.get('extra') else ''
    src = ('<p class="glance-src">League confirmed from England Rugby, 31 October 2026.</p>'
           if league and slug not in PREM else '')
    block = (f'<!--glance--><div class="about-divider"></div><div class="about-block club-glance" id="at-a-glance"><div class="section-label">At a Glance</div>'
             f'<h2>{esc(h2_name)} at a glance</h2><div class="rich-text"><p class="guide-answer"><strong>{esc(answer.strip())}</strong></p>'
             f'{extra}{table}{src}</div></div><!--/glance-->')
    return block, aka, lcell


def new_title(c, old):
    name, sport = norm(c['name']), c['sport']
    base, suf = split_name(c['name'])
    if not suf or suf in ('Rugby', 'Rugby Club', 'Rugby Football Club', 'Rugby Union Club'):
        return None
    lead = f'{base} Rugby League Club' if 'League' in sport else f'{base} Rugby Club'
    t = f'{lead} ({name})'
    place = c['town'] if c['town'] and c['town'].lower() not in base.lower() else (c['county'] or '')
    if place and place.lower() not in base.lower() and len(t) + len(place) + 3 <= 60:
        t += f' | {place}'
    return t if len(t) <= 65 else lead + f' | {place}' if place else lead


def main():
    clubs = {c['slug']: c for c in json.load(open(os.path.join(ROOT, 'tools', 'clubs.json'))) if c['type'] == 'SportsTeam'}
    er = {r['slug']: clean_league(r['league']) for r in csv.DictReader(open(os.path.join(ROOT, 'tools', 'er-teams.csv')))}
    contacts = {r['slug']: r for r in csv.DictReader(open(os.path.join(ROOT, 'tools', 'club-contacts.csv')))}
    n = 0
    for slug, c in sorted(clubs.items()):
        path = os.path.join(ROOT, 'club', slug + '.html')
        if not os.path.exists(path):
            continue
        s = open(path, encoding='utf-8', errors='surrogateescape').read()
        if 'class="about-divider"' not in s:
            continue
        league = er.get(slug) or ''
        block, aka, lcell = build_glance(c, contacts.get(slug), league)
        if '<!--glance-->' in s:
            s = re.sub(r'<!--glance-->.*?<!--/glance-->', lambda m: block, s, count=1, flags=re.S)
        else:
            i = s.find('<div class="about-divider"></div>')
            s = s[:i] + block + '\n        ' + s[i:]
        # title
        t = new_title(c, None)
        try:  # hand-written titles (tools/content/club_guides.py) win over the generated form
            from club_guides import CLUBS as _CG
            t = _CG[slug]['title'] if slug in _CG else t
        except ImportError:
            pass
        if t:
            from guide_render import set_head
            s = set_head(s, t)
        # stale NCL wording
        if slug in NCRL_PREMIER:
            s = s.replace('competing strongly in the National Conference League', 'playing in the NCRL National Premier League, the top amateur division')
            s = s.replace('competing in the National Conference League', 'playing in the NCRL National Premier League, the top amateur division')
        s = re.sub(r'competing in (?:county and )?National Conference League rugby', 'competing in the National Community Rugby League (formerly the National Conference League)', s)
        s = re.sub(r'competing (strongly )?in the National Conference League(?! \()', r'competing \1in the National Community Rugby League (formerly the National Conference League)', s)
        # league FAQ
        name = norm(c['name'])
        if lcell and 'data-faq="league"' not in s:
            q = f'What league does {name} play in?'
            a = league_sentence(slug, c['sport'], league)[0].replace('the club', name).replace('its first XV', f'{name}\'s first XV').replace('its open-age team', f'{name}\'s open-age team')
            item = (f'<div class="faq-item" data-faq="league" style="margin-bottom:1.25rem"><h3 style="font-size:1.05rem;margin-bottom:.35rem">{esc(q)}</h3>'
                    f'<p>{esc(a)} See <a href="../rugby-union-league-structure.html">how the leagues work</a>.</p></div>'
                    if 'League' not in c['sport'] else
                    f'<div class="faq-item" data-faq="league" style="margin-bottom:1.25rem"><h3 style="font-size:1.05rem;margin-bottom:.35rem">{esc(q)}</h3>'
                    f'<p>{esc(a)} See <a href="../rugby-leagues-uk.html#rugby-league-england">how the rugby league competitions work</a>.</p></div>')
            m = re.search(r'(<section class="sec" id="faq">.*?<div style="max-width:860px;margin:0 auto">)', s, re.S)
            if m:
                s = s[:m.end()] + item + s[m.end():]
        # JSON-LD: alternateName + FAQPage
        if aka:
            s = re.sub(r'("@type": "SportsTeam", "@id": "[^"]+", "name": "[^"]+")(, "alternateName": \[[^\]]*\])?',
                       lambda m: m.group(1) + ', "alternateName": ' + json.dumps(aka, ensure_ascii=False), s, count=1)
        sec = re.search(r'<section class="sec" id="faq">(.*?)</section>', s, re.S)
        if sec:
            qa = re.findall(r'<h3[^>]*>(.*?)</h3>\s*<p[^>]*>(.*?)</p>', sec.group(1), re.S)
            cl = lambda t: H.unescape(re.sub(r'<[^>]+>', '', t)).strip()
            ld = ('<script type="application/ld+json" id="guide-ld">' + json.dumps({
                "@context": "https://schema.org", "@type": "FAQPage", "@id": f'{SITE}/club/{slug}.html#faq',
                "mainEntity": [{"@type": "Question", "name": cl(q), "acceptedAnswer": {"@type": "Answer", "text": cl(a)}} for q, a in qa]},
                ensure_ascii=False) + '</script>')
            if 'id="guide-ld"' in s:
                s = re.sub(r'<script type="application/ld\+json" id="guide-ld">.*?</script>', lambda m: ld, s, count=1, flags=re.S)
            else:
                s = s.replace('</head>', ld + '\n</head>', 1)
        open(path, 'w', encoding='utf-8', errors='surrogateescape').write(s)
        n += 1
    print('club pages updated:', n)


if __name__ == '__main__':
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'content'))
    main()
