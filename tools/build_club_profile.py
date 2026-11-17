#!/usr/bin/env python3
"""
build_club_profile.py - UK Rugby Club Profile page template (11 sections).

Usage:
  python3 tools/build_club_profile.py                       # builds both sample pages into preview/
  python3 tools/build_club_profile.py record.json out.html  # builds one page from any club record

The site is plain static HTML (no framework), so the template is a Python
renderer in the same style as the other tools/*.py scripts. Each of the 11
sections is its own function and returns a smart fallback block when its data
is missing, so a sparse record never produces a broken layout or empty box.

Header, navigation and footer are lifted from an existing club page so the
profile always matches the live site chrome.
"""
import datetime
import html
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CFG = json.loads((ROOT / "tools/club-profile-config.json").read_text(encoding="utf-8"))
SHELL_SRC = ROOT / "tools/club-page-shell.html"   # frozen copy of an original club page: header/footer source
TODAY = datetime.date.today()

# ---------------------------------------------------------------- helpers
def esc(v):
    return html.escape(str(v if v is not None else ""), quote=True)

def fill(url, c):
    g = c.get("ground") or {}
    return (url.replace("{slug}", c["slug"]).replace("{lat}", str(g.get("lat") or ""))
            .replace("{lng}", str(g.get("lng") or "")).replace("{postcode}", (g.get("postcode") or "").replace(" ", "+")))

def monogram(c):
    words = [w for w in re.split(r"[\s&-]+", c["name"]) if w and w.upper() not in
             {"RFC", "RUFC", "RLFC", "ARLFC", "RFU", "FC", "CLUB", "RUGBY", "THE"}]
    return "".join(w[0] for w in words[:3]).upper() or c["name"][:2].upper()

def pretty_date(iso):
    d = datetime.date.fromisoformat(iso)
    return d.strftime("%a %-d %b")

def missing(label="Not yet provided"):
    return f'<span class="cp-missing">{esc(label)}</span>'

AD = '<span class="cp-ad">Affiliate link</span>'
SPONSORED = 'rel="sponsored nofollow noopener" target="_blank"'

ICONS = {
    "pin": '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/>',
    "grass": '<path d="M3 20c2-5 3-9 3-14M9 20c1-4 2-8 1-13M15 20c0-5 1-9 4-13M21 20H3"/>',
    "car": '<path d="M5 17h14M6 17l1.5-6h9L18 17M4 17v2h3v-2M17 17v2h3v-2"/><circle cx="8.5" cy="14" r=".6"/><circle cx="15.5" cy="14" r=".6"/>',
    "cup": '<path d="M5 8h12v6a5 5 0 01-5 5h-2a5 5 0 01-5-5V8zM17 9h2a2 2 0 010 4h-2M7 3v2M11 3v2M15 3v2"/>',
    "seat": '<path d="M3 20h18M5 20V9l7-5 7 5v11M9 20v-6h6v6"/>',
    "paw": '<circle cx="6.5" cy="10" r="1.8"/><circle cx="10" cy="6.5" r="1.8"/><circle cx="14.5" cy="6.5" r="1.8"/><circle cx="18" cy="10" r="1.8"/><path d="M12 12c3 0 5 3 5 5.5 0 1.5-1.2 2.5-2.8 2.5-1 0-1.4-.5-2.2-.5s-1.2.5-2.2.5C8.2 20 7 19 7 17.5 7 15 9 12 12 12z"/>',
    "train": '<rect x="5" y="3" width="14" height="14" rx="3"/><path d="M5 11h14M9 21l2-4M15 21l-2-4"/><circle cx="9" cy="14" r=".6"/><circle cx="15" cy="14" r=".6"/>',
    "check": '<path d="M5 12l5 5L20 7"/>',
    "trophy": '<path d="M8 21h8M12 17v4M7 4h10v5a5 5 0 01-10 0V4zM17 5h3v2a3 3 0 01-3 3M7 5H4v2a3 3 0 003 3"/>',
    "star": '<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/>',
    "ball": '<ellipse cx="12" cy="12" rx="9.5" ry="6" transform="rotate(-30 12 12)"/><path d="M8 14l6-4M10 10l4 4"/>',
}

def icon(name, size=20):
    return (f'<svg class="cp-ico" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" '
            f'aria-hidden="true" focusable="false">{ICONS[name]}</svg>')

def prompt_card(title, text, cta, href="#", attrs=""):
    """Reusable fallback block used wherever data is missing."""
    return (f'<div class="cp-empty"><div><strong>{esc(title)}</strong><p>{esc(text)}</p></div>'
            f'<a class="btn cp-btn-ghost cp-btn-sm" href="{esc(href)}" {attrs}>{esc(cta)}</a></div>')

def haversine_mi(a, b):
    """Helper for build pipelines: distance in miles between (lat,lng) pairs."""
    r = 3958.8
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    dp, dl = p2 - p1, math.radians(b[1] - a[1])
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(h))

# ------------------------------------------------------------ section 1
def s1_hero(c):
    crest = (f'<img src="{esc(c["crest"])}" alt="{esc(c["name"])} club crest" width="96" height="96" fetchpriority="high">'
             if c.get("crest") else f'<span class="cp-monogram" role="img" aria-label="{esc(c["name"])} monogram">{esc(monogram(c))}</span>')
    div = f'<span class="cp-badge cp-badge-div">{esc(c["division"])}</span>' if c.get("division") else ""
    loc = ", ".join(x for x in (c.get("town"), c.get("county")) if x)
    meta = loc + (f' <span aria-hidden="true">·</span> Founded {esc(c["founded"])}' if c.get("founded") else "")
    if c.get("claimed"):
        claim = '<span class="cp-verified">' + icon("check", 16) + 'Verified club profile</span>'
    else:
        claim = '<button type="button" class="btn cp-btn-ghost" data-open-dialog="claim-dialog">Claim This Club</button>'
    return f'''<section class="cp-hero" aria-labelledby="club-h1">
  <div class="con cp-hero-in">
    <nav class="breadcrumb cp-crumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a><span class="bc-sep">›</span><a href="{esc(c.get("region_url","../clubs.html"))}">{esc(c["code"])}</a><span class="bc-sep">›</span><span class="bc-cur">{esc(c["name"])}</span></nav>
    <div class="cp-hero-row">
      <div class="cp-crest">{crest}</div>
      <div class="cp-hero-id">
        <div class="cp-badges"><span class="cp-badge cp-badge-code">{esc(c["code"])}</span>{div}</div>
        <h1 id="club-h1">{esc(c["name"])}</h1>
        <p class="cp-hero-meta">{meta}</p>
      </div>
      <div class="cp-hero-cta">
        <a class="btn cp-btn-primary" href="#enquire" data-open-enquire data-role="Prospective Player">Join / Trial Session</a>
        {claim}
      </div>
    </div>
  </div>
  <div class="cp-hoops" aria-hidden="true"></div>
</section>
<nav class="cp-subnav" aria-label="Page sections"><div class="con"><ul>
  <li><a href="#overview">Overview</a></li><li><a href="#teams">Teams &amp; Training</a></li><li><a href="#fixtures">Fixtures</a></li>
  <li><a href="#matchday">Matchday Guide</a></li><li><a href="#location">Location</a></li><li><a href="#history">History</a></li><li><a href="#reviews">Reviews</a></li>
</ul></div></nav>'''

# ------------------------------------------------------------ section 2
def s2_facts(c):
    g = c.get("ground") or {}
    lead = c.get("leadership") or []
    lead_html = "<br>".join(f'<span class="cp-lead">{esc(x["name"])}</span> <small>{esc(x["role"])}</small>' for x in lead) if lead else missing()
    links = []
    if c.get("website"):
        links.append(f'<a href="{esc(c["website"])}" target="_blank" rel="noopener noreferrer">Website ↗</a>')
    for k, label in (("facebook", "Facebook"), ("instagram", "Instagram"), ("x", "X")):
        u = (c.get("socials") or {}).get(k)
        if u:
            links.append(f'<a href="{esc(u)}" target="_blank" rel="noopener noreferrer">{label} ↗</a>')
    items = [
        ("Ground", esc(g.get("name")) if g.get("name") else missing()),
        ("Postcode", esc(g.get("postcode")) if g.get("postcode") else missing()),
        ("Governing body", esc(c.get("governing_body")) if c.get("governing_body") else missing()),
        ("League / division", esc(c.get("division")) if c.get("division") else missing()),
        ("Club colours", esc(c.get("colours")) if c.get("colours") else missing()),
        ("Nickname", esc(c.get("nickname")) if c.get("nickname") else missing()),
        ("Director of Rugby / Captain", lead_html),
        ("Website &amp; social", " · ".join(links) if links else missing()),
    ]
    cells = "".join(f'<div class="cp-fact"><dt>{k}</dt><dd>{v}</dd></div>' for k, v in items)
    gaps = sum(1 for _, v in items if "cp-missing" in v)
    nudge = (f'<p class="cp-nudge">{gaps} detail{"s" if gaps != 1 else ""} missing. '
             f'<a href="../claim.html">Club official? Add them</a>.</p>') if gaps else ""
    return f'''<section class="cp-sec" id="overview" aria-labelledby="h-overview">
  <h2 id="h-overview" class="cp-h2">At a glance</h2>
  <dl class="cp-facts">{cells}</dl>{nudge}
</section>'''

# ------------------------------------------------------------ section 3
def gear_strip(c):
    m = CFG["monetisation"]
    if not (m.get("enabled") and m["gear_strip"].get("enabled")):
        return ""
    surf = ((c.get("ground") or {}).get("surface") or "").upper()
    if "3G" in surf or "4G" in surf:
        text, url = "Training on 3G artificial turf? Shop RFU-approved moulded boots &amp; protection", m["gear_strip"]["url_3g"]
    elif surf in ("GRASS", "NATURAL GRASS"):
        text, url = "Playing on heavy winter grass? Shop soft-ground studs, scrum caps &amp; gumshields", m["gear_strip"]["url_grass"]
    else:
        return ""
    return (f'<aside class="cp-gear" aria-label="Kit suggestion">{icon("ball", 22)}<p>{text}</p>'
            f'<a class="cp-gear-link" href="{esc(fill(url, c))}" {SPONSORED}>Shop kit →</a>{AD}</aside>')

def s3_teams(c):
    teams = c.get("teams") or []
    if not teams:
        body = prompt_card("Training times not added yet", "Tell us when and where this club trains so new players know when to turn up.",
                           "Submit training times", "../claim.html")
        return f'<section class="cp-sec" id="teams" aria-labelledby="h-teams"><h2 id="h-teams" class="cp-h2">Teams, age groups &amp; training</h2>{body}</section>'
    tabs, panels = [], []
    for i, t in enumerate(teams):
        sel = "true" if i == 0 else "false"
        tabs.append(f'<button role="tab" id="tab-{t["key"]}" aria-controls="panel-{t["key"]}" aria-selected="{sel}" tabindex="{0 if i == 0 else -1}">{esc(t["label"])}</button>')
        sess = "".join(
            f'<li><span class="cp-when">{esc(s["days"])}, {esc(s["time"])}</span>' + (f'<span class="cp-sess-note">{esc(s["note"])}</span>' if s.get("note") else "") + "</li>"
            for s in t.get("sessions", [])) or '<li>' + missing("Times to be confirmed") + "</li>"
        pol = f'<p class="cp-policy">{icon("check", 18)}<span>{esc(t["beginner_policy"])}</span></p>' if t.get("beginner_policy") else ""
        contact = f'<p class="cp-contact">Contact: {esc(t["contact"])}</p>' if t.get("contact") else ""
        panels.append(f'''<div role="tabpanel" id="panel-{t["key"]}" aria-labelledby="tab-{t["key"]}" class="cp-panel"{"" if i == 0 else " hidden"} tabindex="0">
  <p class="cp-summary">{esc(t.get("summary",""))}</p><ul class="cp-sessions">{sess}</ul>{pol}{contact}</div>''')
    return f'''<section class="cp-sec" id="teams" aria-labelledby="h-teams">
  <h2 id="h-teams" class="cp-h2">Teams, age groups &amp; training</h2>
  <div class="cp-tabs" data-tabs><div class="cp-tablist" role="tablist" aria-label="Teams and age groups">{"".join(tabs)}</div>{"".join(panels)}</div>
  {gear_strip(c)}
</section>'''

# ------------------------------------------------------------ section 4
def s4_sidebar(c):
    m = CFG["monetisation"]
    form = f'''<div class="cp-card cp-enquire-card" id="enquire" data-enquire-card>
  <h2 class="cp-card-h">Enquire with {esc(c["name"])}</h2>
  <form class="cp-form" name="club-enquiry" method="POST" action="/" data-netlify="true" netlify-honeypot="bot-field" data-validate data-demo="{str(CFG["demo_forms"]).lower()}" novalidate>
    <input type="hidden" name="form-name" value="club-enquiry"><input type="hidden" name="club" value="{esc(c["slug"])}">
    <p class="cp-hp" aria-hidden="true"><label>Leave blank <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
    <div class="cp-field"><label for="enq-role">I am a…</label>
      <select id="enq-role" name="role" required>
        <option value="Prospective Player">Prospective Player</option><option value="Parent (Minis/Juniors)">Parent (Minis/Juniors)</option>
        <option value="Visiting Fixture Secretary">Visiting Fixture Secretary</option><option value="Potential Sponsor">Potential Sponsor</option></select></div>
    <div class="cp-field"><label for="enq-name">Full name</label><input id="enq-name" name="name" type="text" autocomplete="name" required minlength="2"><span class="cp-err" id="enq-name-err" role="alert"></span></div>
    <div class="cp-field"><label for="enq-email">Email address</label><input id="enq-email" name="email" type="email" autocomplete="email" required><span class="cp-err" id="enq-email-err" role="alert"></span></div>
    <div class="cp-field"><label for="enq-msg">Message / experience level</label><textarea id="enq-msg" name="message" rows="4" required minlength="10" placeholder="e.g. Played at school, looking for a Tuesday trial session"></textarea><span class="cp-err" id="enq-msg-err" role="alert"></span></div>
    <button class="btn cp-btn-primary cp-submit" type="submit"><span class="cp-btn-label">Send enquiry</span><span class="cp-spin" aria-hidden="true"></span></button>
    <p class="cp-form-status" role="status" aria-live="polite"></p>
    <p class="cp-fine">We pass your details to the club only. <a href="../privacy-policy.html">Privacy policy</a>.</p>
  </form>
</div>'''
    slot = ""
    if m.get("enabled") and m.get("sidebar_slot") in ("travel", "injury_cover"):
        g = c.get("ground") or {}
        kind = m["sidebar_slot"]
        if kind == "travel" and (g.get("lat") is None or g.get("lng") is None):
            kind = "injury_cover"      # hotel search needs coordinates: fall back rather than ship a broken link
        if kind == "travel":
            ground = g.get("name") or c["name"]
            slot = f'''<aside class="cp-card cp-partner" aria-label="Travel partner" data-slot-a>
  {AD}<h3 class="cp-card-h">Away fans &amp; travel</h3>
  <p>Travelling to {esc(c.get("town") or c["name"])} for matchday? Compare hotels within 3 miles of {esc(ground)}.</p>
  <a class="btn cp-btn-ghost cp-btn-block" href="{esc(fill(m["travel"]["url"], c))}" {SPONSORED}>Compare hotels →</a></aside>'''
        else:
            slot = f'''<aside class="cp-card cp-partner" aria-label="Insurance partner" data-slot-a>
  {AD}<h3 class="cp-card-h">Player protection</h3>
  <p>Playing for {esc(c["name"])}? Compare sports injury cover built for amateur rugby players.</p>
  <a class="btn cp-btn-ghost cp-btn-block" href="{esc(fill(m["injury_cover"]["url"], c))}" {SPONSORED}>Compare cover →</a></aside>'''
    return f'<aside class="cp-aside" aria-label="Contact the club"><div class="cp-aside-in">{form}{slot}</div></aside>'

# ------------------------------------------------------------ section 5
def s5_fixtures(c):
    st, fx = c.get("standing"), [f for f in (c.get("fixtures") or []) if f["date"] >= TODAY.isoformat()][:3]
    town = c.get("town") or "your area"
    if st:
        pills = "".join(f'<span class="cp-pill cp-pill-{r}" title="{ {"W":"Win","L":"Loss","D":"Draw"}.get(r, r) }">{r}<span class="sr-only"> ({ {"W":"win","L":"loss","D":"draw"}.get(r, r) })</span></span>' for r in st.get("form", [])[:5])
        bar = f'''<div class="cp-standing"><div><span class="cp-big">{esc(st["position"])}<sup>{_ord(st["position"])}</sup></span><span class="cp-small">of {esc(st["of"])}</span></div>
  <div><span class="cp-big">{esc(st["played"])}</span><span class="cp-small">Played</span></div><div><span class="cp-big">{esc(st["points"])}</span><span class="cp-small">Points</span></div>
  <div class="cp-form-wrap"><span class="cp-pills" aria-label="Last five results">{pills}</span><span class="cp-small">Last 5</span></div></div>'''
    else:
        bar = prompt_card("League position not available", "Standings appear once the club's league and results are linked.", "Add league details", "../claim.html")
    if fx:
        rows = "".join(f'''<li class="cp-fix" data-date="{f["date"]}"><time datetime="{f["date"]}T{esc(f.get("ko","00:00"))}"><span class="cp-fix-d">{pretty_date(f["date"])}</span><span class="cp-fix-k">{esc(f.get("ko","TBC"))}</span></time>
  <span class="cp-fix-o">{esc(f["opponent"])}</span><span class="cp-ha cp-ha-{f["venue"].lower()}">{"Home" if f["venue"] == "H" else "Away"}</span></li>''' for f in fx)
        fixtures = f'<ol class="cp-fixtures" aria-label="Next fixtures">{rows}</ol>'
    else:
        fixtures = prompt_card("No upcoming fixtures listed", "Is this your club? Add the fixture list so players, parents and away fans can plan.", "Add fixtures", "../claim.html")
    strip = ""
    m = CFG["monetisation"]
    if m.get("enabled"):
        pubs = f"https://www.google.com/maps/search/?api=1&query={esc('rugby pubs near ' + town).replace(' ', '+')}"
        strip = f'''<div class="cp-strip"><p>Watch Premiership, URC &amp; Six Nations live — <a href="{pubs}" target="_blank" rel="noopener nofollow">find rugby pubs in {esc(town)}</a> or <a href="{esc(fill(m["streaming"]["url"], c))}" {SPONSORED}>stream fixtures</a>.</p>{AD}</div>'''
    return f'''<section class="cp-sec" id="fixtures" aria-labelledby="h-fixtures">
  <h2 id="h-fixtures" class="cp-h2">League standing, form &amp; fixtures</h2>
  <div class="cp-card cp-fx-card">{bar}{fixtures}{strip}</div>
</section>'''

def _ord(n):
    n = int(n)
    return "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")

# ------------------------------------------------------------ section 6
def s6_matchday(c):
    g, md = c.get("ground") or {}, c.get("matchday") or {}
    surf = g.get("surface")
    surf_label = {"3G": "3G artificial", "4G": "4G artificial", "GRASS": "Natural grass"}.get((surf or "").upper(), surf)
    rows = [("grass", "Pitch surface", surf_label), ("car", "Parking &amp; overflow", md.get("parking")),
            ("cup", "Clubhouse bar &amp; food", md.get("bar_food")), ("seat", "Spectator comfort", md.get("comfort")),
            ("paw", "Dog policy", md.get("dogs"))]
    lis = "".join(f'<li>{icon(i, 22)}<div><strong>{k}</strong><span>{esc(v) if v else missing("Not yet provided")}</span></div></li>' for i, k, v in rows)
    gaps = sum(1 for *_, v in rows if not v)
    note = ""
    if md.get("notes"):
        note = f'<div class="cp-readmore" data-readmore><div class="cp-rm-body"><p>{esc(md["notes"])}</p></div><button type="button" class="cp-rm-btn" aria-expanded="false">Read more</button></div>'
    elif gaps >= 3:
        note = prompt_card("Matchday details needed", "Parking, food and facilities help away supporters plan their day.", "Add matchday info", "../claim.html")
    partner = ""
    m = CFG["monetisation"]
    if m.get("enabled") and (g.get("postcode")):
        partner = f'''<aside class="cp-partner-inline" aria-label="Local matchday partner">{AD}
  <div><strong>Visiting {esc(c["name"])}?</strong><p>Top-rated pubs, restaurants &amp; stays near {esc(g["postcode"])}.</p></div>
  <a class="btn cp-btn-ghost cp-btn-sm" href="{esc(fill(m["local_partner"]["url"], c))}" {SPONSORED}>See nearby →</a></aside>'''
    return f'''<section class="cp-sec" id="matchday" aria-labelledby="h-matchday">
  <h2 id="h-matchday" class="cp-h2">Away fan &amp; matchday guide</h2>
  <ul class="cp-specs">{lis}</ul>{note}{partner}
</section>'''

# ------------------------------------------------------------ section 7
def s7_location(c):
    g = c.get("ground") or {}
    lat, lng = g.get("lat"), g.get("lng")
    addr = ", ".join(x for x in (g.get("address"), g.get("postcode")) if x)
    if lat is None or lng is None:
        q = esc("+".join(x for x in (c["name"], g.get("postcode") or c.get("town") or "") if x)).replace(" ", "+")
        return f'''<section class="cp-sec" id="location" aria-labelledby="h-location"><h2 id="h-location" class="cp-h2">Location &amp; directions</h2>
  {prompt_card("Exact ground location not pinned yet", "Add the clubhouse gate coordinates so visitors can navigate straight to the entrance.", "Add location", "../claim.html")}
  <p class="cp-fallback-link"><a href="https://www.google.com/maps/search/?api=1&query={q}" target="_blank" rel="noopener">Search {esc(c["name"])} on Google Maps ↗</a></p></section>'''
    d = 0.004
    osm = f"https://www.openstreetmap.org/export/embed.html?bbox={lng-d*1.6:.5f}%2C{lat-d:.5f}%2C{lng+d*1.6:.5f}%2C{lat+d:.5f}&layer=mapnik&marker={lat}%2C{lng}"
    st = g.get("station")
    station = f'<p class="cp-station">{icon("train", 20)}<span>Nearest station: <strong>{esc(st["name"])}</strong>, about {esc(st["walk_mins"])} min walk</span></p>' if st else ""
    return f'''<section class="cp-sec" id="location" aria-labelledby="h-location">
  <h2 id="h-location" class="cp-h2">Location, clubhouse gate &amp; directions</h2>
  <p class="cp-addr">{icon("pin", 20)}<span>{esc(addr) or esc(g.get("name"))}</span></p>
  <div class="cp-map" data-map data-src="{osm}" data-title="Map showing the {esc(c["name"])} clubhouse entrance">
    <button type="button" class="cp-map-load">Load interactive map</button>
  </div>
  <div class="cp-mapbtns" role="group" aria-label="Open in a maps app">
    <a class="btn cp-btn-ghost cp-btn-sm" href="https://www.google.com/maps/search/?api=1&query={lat},{lng}" target="_blank" rel="noopener">Google Maps</a>
    <a class="btn cp-btn-ghost cp-btn-sm" href="https://maps.apple.com/?ll={lat},{lng}&q={esc(g.get("name") or c["name"]).replace(" ", "%20")}" target="_blank" rel="noopener">Apple Maps</a>
    <a class="btn cp-btn-ghost cp-btn-sm" href="https://waze.com/ul?ll={lat},{lng}&navigate=yes" target="_blank" rel="noopener">Waze</a>
  </div>{station}
</section>'''

# ------------------------------------------------------------ section 8
def s8_history(c):
    h = c.get("history") or {}
    text = (h.get("text") or "").strip()
    paras = "".join(f"<p>{esc(p)}</p>" for p in text.split("\n\n") if p.strip())
    narrative = (f'<div class="cp-readmore" data-readmore><div class="cp-rm-body cp-serif">{paras}</div><button type="button" class="cp-rm-btn" aria-expanded="false">Read more</button></div>'
                 if text else prompt_card("Club history not added yet", "Share the story of the club: when it started, where it has played and who has pulled on the shirt.",
                                          "Submit club history", "../claim.html"))
    hon = h.get("honours") or []
    honours = (f'<div class="cp-hon"><h3 class="cp-h3">Club honours</h3><ul class="cp-honours">' + "".join(f"<li>{icon('trophy', 18)}<span>{esc(x)}</span></li>" for x in hon) + "</ul></div>") if hon else ""
    al = h.get("alumni") or []
    alumni = (f'<div class="cp-alu"><h3 class="cp-h3">Notable alumni &amp; internationals</h3><ul class="cp-alumni">' +
              "".join(f'<li><span class="cp-cap">{icon("star", 16)}</span><div><strong>{esc(a["name"])}</strong><small>{esc(a.get("note",""))}</small></div></li>' for a in al) + "</ul></div>") if al else ""
    extra = "" if (hon or al) else prompt_card("No honours or alumni listed", "Know of a title, cup win or international? Tell us and we'll add it.", "Submit club history", "../claim.html")
    return f'''<section class="cp-sec" id="history" aria-labelledby="h-history">
  <h2 id="h-history" class="cp-h2">Club heritage, honours &amp; alumni</h2>
  {narrative}<div class="cp-two">{honours}{alumni}</div>{extra}
</section>'''

# ------------------------------------------------------------ section 9
BARS = (("atmosphere", "Clubhouse atmosphere"), ("pitch", "Pitch quality"), ("welcome", "Welcome for newcomers"), ("food", "Matchday food &amp; pint"))

def s9_ratings(c):
    r = c.get("ratings") or {}
    if r.get("count"):
        bars = "".join(f'''<li><span class="cp-bar-l">{lab}</span><div class="cp-bar" role="meter" aria-valuemin="0" aria-valuemax="5" aria-valuenow="{r["bars"].get(k, 0)}" aria-label="{lab.replace("&amp;", "and")}: {r["bars"].get(k, 0)} out of 5"><i style="width:{r["bars"].get(k, 0) / 5 * 100:.0f}%"></i></div><span class="cp-bar-v">{r["bars"].get(k, 0):.1f}</span></li>''' for k, lab in BARS)
        body = f'''<div class="cp-score"><span class="cp-big cp-score-n">{r["overall"]:.1f}</span><span class="cp-small">out of 5</span><span class="cp-small">{esc(r["count"])} rating{"s" if r["count"] != 1 else ""}</span></div><ul class="cp-bars">{bars}</ul>'''
    else:
        body = prompt_card("No ratings yet", "Be the first to rate this ground and help other players and fans know what to expect.", "Rate this ground", "#", 'data-open-dialog="rate-dialog"')
    btn = '<button type="button" class="btn cp-btn-primary" data-open-dialog="rate-dialog">Rate This Ground</button>' if r.get("count") else ""
    return f'''<section class="cp-sec" id="reviews" aria-labelledby="h-reviews">
  <h2 id="h-reviews" class="cp-h2">Verified fan &amp; player ground ratings</h2>
  <div class="cp-card cp-rate-card">{body}</div>
  <div class="cp-rate-foot">{btn}<p class="cp-fine">Ratings are moderated before they appear.</p></div>
</section>'''

# ----------------------------------------------------------- section 10
def s10_sponsors(c):
    sp = c.get("sponsors") or []
    if c.get("claimed") and sp:
        grid = "".join(f'<li class="cp-sponsor"><span class="cp-sp-t">{esc(s["tier"])}</span><strong>{esc(s["name"])}</strong></li>' for s in sp)
        grid_html = f'<ul class="cp-sponsors">{grid}</ul>'
    elif sp:
        grid = "".join(f'<li class="cp-sponsor"><span class="cp-sp-t">{esc(s["tier"])}</span><strong>{esc(s["name"])}</strong></li>' for s in sp)
        grid_html = f'<ul class="cp-sponsors">{grid}</ul><p class="cp-fine">Unverified: shown from public club information until the profile is claimed.</p>'
    else:
        slots = "".join('<li class="cp-sponsor cp-sponsor-empty"><span class="cp-sp-t">Available</span><strong>Your business here</strong></li>' for _ in range(4))
        grid_html = f'<ul class="cp-sponsors">{slots}</ul>'
    return f'''<section class="cp-band" id="sponsors" aria-labelledby="h-sponsors"><div class="con">
  <h2 id="h-sponsors" class="cp-h2">Club sponsors</h2>{grid_html}
  <div class="cp-b2b">
    <div class="cp-b2b-card"><h3 class="cp-h3">Club committee</h3><p>Are you on the {esc(c["name"])} committee? Upgrade to a Verified Pro Profile to showcase your sponsors, remove third-party ads, and receive direct player enquiries.</p>
      <a class="btn cp-btn-primary" href="{esc(CFG["b2b"]["upgrade_url"])}">Upgrade to Verified Pro</a></div>
    <div class="cp-b2b-card"><h3 class="cp-h3">Local business</h3><p>Sponsor {esc(c["name"])}'s page — reach local players, parents and away supporters every week.</p>
      <a class="btn cp-btn-ghost" href="{esc(CFG["b2b"]["sponsor_url"])}">Become a sponsor</a></div>
  </div>
</div></section>'''

# ----------------------------------------------------------- section 11
def _cards(items):
    out = []
    for n in items[:4]:
        href = f'../club/{n["slug"]}.html' if n.get("slug") else "#"
        out.append(f'''<li><a class="cp-ncard" href="{esc(href)}"{"" if n.get("slug") else ' aria-disabled="true"'}><strong>{esc(n["name"])}</strong>
  <span class="cp-ncard-m"><span class="cp-badge cp-badge-code cp-badge-sm">{esc(n["code"])}</span><span>{(f'{n["distance_mi"]:.1f} mi' if n.get("distance_mi") is not None else esc(n.get("town", "")))}</span></span><small>{esc(n.get("division",""))}</small></a></li>''')
    return "".join(out)

def s11_nearby(c):
    def block(title, items, empty_t):
        if items:
            return f'<div><h3 class="cp-h3">{title}</h3><ul class="cp-ngrid">{_cards(items)}</ul></div>'
        return f'<div><h3 class="cp-h3">{title}</h3>{prompt_card(empty_t, "We are still mapping nearby clubs.", "Browse all clubs", "../clubs.html")}</div>'
    div = c.get("division") or "this division"
    return f'''<section class="cp-sec cp-sec-wide" id="nearby" aria-labelledby="h-nearby"><div class="con">
  <h2 id="h-nearby" class="cp-h2">Nearby clubs &amp; league rivals</h2>
  {block("Other rugby clubs within 10 miles", c.get("nearby_10mi") or [], "No nearby clubs found yet")}
  {block(f"More clubs in {esc(div)}", c.get("same_division") or [], "No other clubs in this division yet")}
</div></section>'''

# ------------------------------------------------------------- dialogs
def dialogs(c):
    claim = f'''<dialog class="cp-dialog" id="claim-dialog" aria-labelledby="claim-h"><div class="cp-dlg-in">
  <button type="button" class="cp-x" data-close-dialog aria-label="Close">×</button>
  <h2 id="claim-h" class="cp-h2">Claim {esc(c["name"])}</h2>
  <ol class="cp-steps"><li>Tell us your role and official club email</li><li>We check it against the club website or RFU/RFL/WRU records</li><li>Within 2 working days you can edit your profile, add sponsors and see enquiries</li></ol>
  <form class="cp-form" name="club-claim" method="POST" action="/" data-netlify="true" netlify-honeypot="bot-field" data-validate data-demo="{str(CFG["demo_forms"]).lower()}" novalidate>
    <input type="hidden" name="form-name" value="club-claim"><input type="hidden" name="club" value="{esc(c["slug"])}">
    <p class="cp-hp" aria-hidden="true"><label>Leave blank <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
    <div class="cp-field"><label for="cl-name">Your name</label><input id="cl-name" name="name" required minlength="2" autocomplete="name"><span class="cp-err" role="alert"></span></div>
    <div class="cp-field"><label for="cl-role">Your role</label><select id="cl-role" name="role" required><option value="">Choose…</option><option>Club secretary</option><option>Chair / President</option><option>Membership secretary</option><option>Other committee member</option></select><span class="cp-err" role="alert"></span></div>
    <div class="cp-field"><label for="cl-email">Official club email</label><input id="cl-email" name="email" type="email" required autocomplete="email"><span class="cp-err" role="alert"></span></div>
    <div class="cp-field"><label for="cl-proof">How can we verify you?</label><textarea id="cl-proof" name="proof" rows="3" required minlength="10" placeholder="e.g. Listed as secretary on the club website, or send from the club's own domain"></textarea><span class="cp-err" role="alert"></span></div>
    <button class="btn cp-btn-primary cp-submit" type="submit"><span class="cp-btn-label">Request verification</span><span class="cp-spin" aria-hidden="true"></span></button>
    <p class="cp-form-status" role="status" aria-live="polite"></p>
  </form></div></dialog>'''
    stars = "".join(f'''<fieldset class="cp-rate-set"><legend>{lab}</legend><div class="cp-stars">''' + "".join(
        f'<input type="radio" id="r-{k}-{n}" name="{k}" value="{n}" required><label for="r-{k}-{n}" title="{n} out of 5"><span class="sr-only">{n}</span>★</label>' for n in range(5, 0, -1)) + '</div><span class="cp-err" role="alert"></span></fieldset>' for k, lab in BARS)
    rate = f'''<dialog class="cp-dialog" id="rate-dialog" aria-labelledby="rate-h"><div class="cp-dlg-in">
  <button type="button" class="cp-x" data-close-dialog aria-label="Close">×</button>
  <h2 id="rate-h" class="cp-h2">Rate {esc((c.get("ground") or {}).get("name") or c["name"])}</h2>
  <form class="cp-form" name="ground-rating" method="POST" action="/" data-netlify="true" netlify-honeypot="bot-field" data-validate data-demo="{str(CFG["demo_forms"]).lower()}" novalidate>
    <input type="hidden" name="form-name" value="ground-rating"><input type="hidden" name="club" value="{esc(c["slug"])}">
    <p class="cp-hp" aria-hidden="true"><label>Leave blank <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
    {stars}
    <div class="cp-field"><label for="rt-who">I am a…</label><select id="rt-who" name="who" required><option value="">Choose…</option><option>Player</option><option>Parent</option><option>Home supporter</option><option>Away supporter</option></select><span class="cp-err" role="alert"></span></div>
    <div class="cp-field"><label for="rt-c">Comment (optional)</label><textarea id="rt-c" name="comment" rows="3" maxlength="500"></textarea></div>
    <button class="btn cp-btn-primary cp-submit" type="submit"><span class="cp-btn-label">Submit rating</span><span class="cp-spin" aria-hidden="true"></span></button>
    <p class="cp-form-status" role="status" aria-live="polite"></p>
  </form></div></dialog>'''
    drawer = '''<dialog class="cp-dialog cp-drawer" id="enquire-drawer" aria-label="Enquire with the club"><div class="cp-dlg-in">
  <button type="button" class="cp-x" data-close-dialog aria-label="Close">×</button><div class="cp-drawer-body" data-drawer-body></div></div></dialog>'''
    mbar = f'''<div class="cp-mbar" role="region" aria-label="Quick actions"><a class="btn cp-btn-primary" href="#enquire" data-open-enquire data-role="Prospective Player">Enquire / Join</a>
  <a class="btn cp-btn-ghost" href="{_directions_url(c)}" target="_blank" rel="noopener">Directions</a></div>'''
    return claim + rate + drawer + mbar

def _directions_url(c):
    g = c.get("ground") or {}
    if g.get("lat") is not None and g.get("lng") is not None:
        return f'https://www.google.com/maps/dir/?api=1&destination={g["lat"]},{g["lng"]}'
    q = "+".join(x for x in (c["name"], g.get("postcode") or c.get("town") or "") if x).replace(" ", "+")
    return f"https://www.google.com/maps/search/?api=1&query={esc(q)}"

# ------------------------------------------------------------ JSON-LD
def jsonld(c, canonical):
    g = c.get("ground") or {}
    place_id = canonical + "#ground"
    sport = c["code"]
    addr = {"@type": "PostalAddress", "addressLocality": c.get("town"), "addressRegion": c.get("county"), "addressCountry": "GB"}
    if g.get("postcode"):
        addr["postalCode"] = g["postcode"]
    if g.get("address"):
        addr["streetAddress"] = g["address"]
    place = {"@type": "Place", "@id": place_id, "name": g.get("name") or f'{c["name"]} ground', "address": addr}
    if g.get("lat") is not None and g.get("lng") is not None:
        place["geo"] = {"@type": "GeoCoordinates", "latitude": g["lat"], "longitude": g["lng"]}
    club = {"@type": "SportsClub", "@id": canonical + "#club", "name": c["name"], "url": canonical, "sport": sport,
            "location": {"@id": place_id}, "address": addr}
    if c.get("founded"):
        club["foundingDate"] = str(c["founded"])
    if c.get("governing_body"):
        club["memberOf"] = {"@type": "SportsOrganization", "name": c["governing_body"]}
    same = [u for u in [c.get("website")] + list((c.get("socials") or {}).values()) if u]
    if same:
        club["sameAs"] = same
    r = c.get("ratings") or {}
    if r.get("count"):
        club["aggregateRating"] = {"@type": "AggregateRating", "ratingValue": r["overall"], "ratingCount": r["count"], "bestRating": 5, "worstRating": 1}
    crumbs = {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": CFG["site_url"] + "/"},
        {"@type": "ListItem", "position": 2, "name": c["code"], "item": CFG["site_url"] + "/" + c.get("region_url", "clubs.html").lstrip("./")},
        {"@type": "ListItem", "position": 3, "name": c["name"]}]}
    doc = {"@context": "https://schema.org", "@graph": [club, place, crumbs]}
    return json.dumps(doc, ensure_ascii=False).replace("</", "<\\/")

# ---------------------------------------------------------------- page
def head(c, canonical, sample):
    title = f'{c["name"]} | {c["code"]} Club in {c.get("town") or c.get("county")} | UK Rugby Club Directory'
    div = f' in {c["division"]}' if c.get("division") else ""
    desc = (f'{c["name"]} is a {c["code"].lower()} club in {c.get("town")}, {c.get("county")}{div}. '
            f'Training times, fixtures, matchday guide, directions and how to join.')[:158]
    robots = "noindex,nofollow" if sample else "index,follow,max-image-preview:large,max-snippet:-1"
    return f'''<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{esc(canonical)}">
<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{esc(canonical)}">
<meta property="og:site_name" content="UK Rugby Club Directory"><meta name="theme-color" content="#293241">
<link rel="icon" href="../favicon.ico" sizes="48x48"><link rel="icon" href="../favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="../apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;600;700&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../css/style.css">
<link rel="stylesheet" href="../css/club-profile.css">
<script type="application/ld+json">{jsonld(c, canonical)}</script>
</head>
'''

def shell():
    t = SHELL_SRC.read_text(encoding="utf-8")
    top = t[t.index("<body"): t.index('<main id="main">') + len('<main id="main">')]
    top = top.replace("<body>", '<body class="cp-page">', 1)
    bottom = t[t.index("</main>"):]
    bottom = bottom.replace('<script src="../js/main.js"></script></body></html>', "")
    return top, bottom

def sample_banner(sample):
    return ('<div class="cp-sample-banner" role="note">SAMPLE DATA: fictional club used to test the profile template. Not indexed.</div>' if sample else "")

def build(c, sample=True):
    canonical = f'{CFG["site_url"]}/club/{c["slug"]}.html'
    top, bottom = shell()
    main = (f'{sample_banner(sample)}{s1_hero(c)}\n<div class="con cp-layout"><div class="cp-main">\n'
            f'{s2_facts(c)}\n{s3_teams(c)}\n{s5_fixtures(c)}\n{s6_matchday(c)}\n{s7_location(c)}\n{s8_history(c)}\n{s9_ratings(c)}\n</div>\n'
            f'{s4_sidebar(c)}\n</div>\n{s10_sponsors(c)}\n{s11_nearby(c)}\n')
    page = (head(c, canonical, sample) + top + main + bottom + dialogs(c)
            + '\n<script src="../js/main.js"></script>\n<script src="../js/club-profile.js" defer></script>\n</body></html>\n')
    return page

def word_count(c):
    return len(((c.get("history") or {}).get("text") or "").split())

if __name__ == "__main__":
    if len(sys.argv) == 3:
        rec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        Path(sys.argv[2]).write_text(build(rec, sample=False), encoding="utf-8")
        print("wrote", sys.argv[2])
    else:
        out = ROOT / "preview"
        out.mkdir(exist_ok=True)
        for name, rec_file in (("club-profile-sample.html", "club-profile-sample.json"), ("club-profile-sample-sparse.html", "club-profile-sample-sparse.json")):
            rec = json.loads((ROOT / "tools" / rec_file).read_text(encoding="utf-8"))
            (out / name).write_text(build(rec, sample=True), encoding="utf-8")
            print("wrote preview/" + name, "| history words:", word_count(rec))
