#!/usr/bin/env python3
"""
add_joint_profiles.py - give the 22 Rugby Joints listings added on 26 Nov 2026 their own profile pages.

Builds club/<slug>.html with tools/add_business_listings.page(), then enriches each page so it is not a bare
template: what the business is and who it suits, how to use it, a tailored contact paragraph, four FAQs, and
links to three listings from the same section. Also points the cards on rugby-joints.html and clubs.html at the
new pages and updates clubs.json, clubs-index.json, the sitemap, the JSON-LD list and the "alongside N" counts.
Run from the repo root. Safe to re-run: pages that exist are skipped.
"""
import importlib.util, json, re, html, sys, zlib
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://ukrugbyclubdirectory.co.uk"
sys.path.insert(0, str(ROOT / "tools"))
spec = importlib.util.spec_from_file_location("abl", ROOT / "tools/add_business_listings.py")
abl = importlib.util.module_from_spec(spec); spec.loader.exec_module(abl)
E = lambda s: html.escape(s, quote=True)

# slug, name, website, kind, place, county, description (two sentences: what it is, who it suits), section
JOINTS = [
 ("rugbypass","RugbyPass","https://rugbypass.com","global rugby news and video site",None,None,"Global rugby news site with UK match coverage, tactical analysis, documentaries and live streaming. Useful when you want video and tactical breakdowns alongside the headlines.","news"),
 ("talking-rugby-union","Talking Rugby Union","https://www.talkingrugbyunion.co.uk","rugby union news site",None,None,"Coverage that runs from international tests down to National League rugby, BUCS university rugby and grassroots. A good fit for lower-league and student club stories.","news"),
 ("bbc-sport-rugby-union","BBC Sport: Rugby Union","https://www.bbc.co.uk/sport/rugby-union","national broadcaster's rugby union hub",None,None,"The national broadcaster's rugby union hub, with live commentary, match reports, Six Nations coverage, podcasts and video highlights. Best for major fixtures and national results.","news"),
 ("the-guardian-rugby-union","The Guardian: Rugby Union","https://www.theguardian.com/sport/rugby-union","national newspaper rugby union section",None,None,"Broadsheet match reports, columns and investigative sports journalism on rugby union. Best for analysis and longer reads on the issues facing the game.","news"),
 ("the-independent-rugby-union","The Independent: Rugby Union","https://www.independent.co.uk/topic/rugby-union","national news rugby union section",None,None,"Rugby news, opinion, match previews and analysis covering the Six Nations, the Premiership and the British & Irish Lions. Best for quick previews and commentary around big fixtures.","news"),
 ("dave-sport-premiership-rugby","Dave Sport: Premiership Rugby","https://dave.sport/rugby/premiership-rugby","fan-focused Premiership Rugby news page","England",None,"Fan-focused Premiership Rugby page with news, transfer talk, match centres and team schedules. Best for following a club's season week by week.","news"),
 ("love-rugby-league","Love Rugby League","https://loverugbyleague.com","rugby league news site",None,None,"Rugby league news covering Super League, the Championship, League 1, the NRL and transfers. A strong first stop for league supporters and clubs.","news"),
 ("serious-about-rugby-league","Serious About Rugby League","https://seriousaboutrl.com","rugby league news and opinion site",None,None,"Breaking news, transfer reports, match reaction and opinion columns on Super League and Championship clubs. Best for fast-moving league stories.","news"),
 ("forty20","Forty20","https://forty-20.com","independent rugby league magazine",None,None,"Independent rugby league magazine, in print and online, with long-form features, history and cultural analysis. Best for readers who want depth rather than match-day news.","news"),
 ("newsnow-rugby-league","NewsNow: Rugby League","https://newsnow.co.uk/h/Sport/Rugby+League","rugby league news aggregator",None,None,"Live aggregator that gathers rugby league articles and blog posts from across the web into one feed. Best for catching every story on a team or topic.","news"),
 ("the-east-terrace","The East Terrace","https://theeastterrace.com","independent rugby history and commentary blog","Wales",None,"Independent blog on rugby history, Welsh rugby commentary and satire, statistical deep dives and sports essays. Best for heritage stories and Welsh viewpoints.","blogs"),
 ("blood-and-mud","Blood & Mud","https://bloodandmud.com","humour-led rugby blog and podcast",None,None,"Humour-led rugby blog with a weekly podcast and satirical match reviews. Best for light-hearted fan commentary.","blogs"),
 ("eggchasers","EggChasers","https://eggchasers.com","independent rugby podcast and media hub",None,None,"Long-running independent rugby podcast and media hub covering the Premiership, the Six Nations and grassroots rugby. Best for listeners who want opinion and debate.","blogs"),
 ("the-rugby-blog","The Rugby Blog","https://therugbyblog.com","independent rugby news and opinion blog",None,None,"Independent blog with European and international rugby news, opinion, match previews, fantasy leagues and guest columns. Best for fans who like previews and fantasy rugby.","blogs"),
 ("musings-of-a-travelling-rugbyman","Musings of a Travelling Rugbyman","https://chrislethou.substack.com","rugby newsletter on Substack","Wales",None,"Substack newsletter on Welsh rugby governance, historic retrospectives, community rugby and travel essays. Best for thoughtful long reads on the Welsh game.","blogs"),
 ("365-sporting-days","365 Sporting Days","https://debssport.uk","rugby supporter diary blog","England",None,"Personal match-day diaries, fan essays and photo blogs covering Premiership Rugby and Saracens. Best for a supporter's view from the stands.","blogs"),
 ("scottish-rugby-fans","Scottish Rugby Fans","https://scottishrugbyfans.com","Scottish rugby supporter community","Scotland",None,"Supporter community with head-to-head records, Six Nations predictions and fan discussion. Best for Scotland fans who enjoy stats and debate.","blogs"),
 ("edinburgh-rugby-fans-group","Edinburgh Rugby Fans Group","https://edinburghrugbyfans.co.uk","Edinburgh Rugby supporter group","Edinburgh",None,"Supporter collective for Edinburgh Rugby with fixtures, away-travel information and news. Best for fans planning match days and away trips.","blogs"),
 ("black-and-ambers","Black and Ambers","https://blackandambers.co.uk","Newport RFC supporter site","Newport",None,"Supporter site and match-reporting portal for Newport RFC, covering Super Rygbi Cymru fixtures. Best for Newport match reports and club heritage.","blogs"),
 ("widnes-rugby","Widnes Rugby","https://widnesrugby.com","Widnes Vikings supporter community","Widnes",None,"Independent supporter community and forum for Widnes Vikings, with news, match commentary and club history. Best for Vikings fans who want to talk rugby league.","blogs"),
 ("the-rugby-site","The Rugby Site","https://therugbysite.com/blog","rugby tactics and coaching blog",None,None,"Tactical blog and coaching library with video analysis from international coaches and players. Best for coaches studying systems and match tactics.","coaching"),
 ("gainline-rugby","Gainline Rugby","https://gainline.app","rugby fixture and match-guide app",None,None,"Fixture schedule and match-guide app with broadcast and streaming information, automated stats and editorial previews. Best for working out where and when to watch.","software"),
]
SECNAME = {"blogs":"Blogs, Podcasts & Fan Communities","news":"News, Magazines & Media","coaching":"Coaching, Training & Performance","software":"Club Software, Data & Club Finders"}
USE = {
 "blogs":"Use {n} for independent opinion, match-day colour and club stories that the national press often skips. Follow its latest posts or episodes before you pitch an idea or ask about a collaboration.",
 "news":"Use {n} for results, previews, analysis and news across the game. Check its recent coverage to see whether your club's story fits before you get in touch.",
 "coaching":"Use {n} to find drills, tactics and training ideas for your squad. Compare what it publishes with your age group and playing level before you rely on it.",
 "software":"Use {n} to see where and when games are on and to follow fixtures and stats. Check its coverage of your league before you depend on it.",
}
CONTACT = {  # four sentences, two variants each, as on the existing business pages
 'blogs':[["{n} is one of the blogs, podcasts and fan communities listed in Rugby Joints.","Rugby Joints lists {n} among its blogs, podcasts and fan communities."],
  ["If you would like to guest on a show, write a piece or share a club story, start with the contact route on their website.","Writers, clubs and sponsors can use their official channels to ask about guest features, interviews or collaborations."],
  ["A short message that names your club or project and links to your own site makes it easier for them to reply.","Mention who you are and what you would like to share, so they can see quickly whether it fits."],
  ["Listing here is not an endorsement, so read their latest posts before you get in touch.","We list the site for reference only and are not affiliated with it."]],
 'news':[["{n} is one of the news sites, magazines and media outlets listed in Rugby Joints.","Rugby Joints lists {n} among its rugby news, magazine and media outlets."],
  ["If your club has a story, result or event worth covering, use their official channels to ask who handles submissions.","Clubs, coaches and organisers can use their official channels to ask how to send in news or match reports."],
  ["Keep your message short, add the date and place, and link to a page with the full details.","Include the key facts up front and a link to your club page, so an editor can judge the story quickly."],
  ["Listing here is not an endorsement, and coverage is always the outlet's own decision.","We are not affiliated with the outlet, so check its current submission guidance first."]],
 'coaching':[["{n} is one of the coaching, training and performance providers listed in Rugby Joints.","Rugby Joints lists {n} among its coaching, training and performance providers."],
  ["Coaches and clubs can use their official channels to ask what is on offer and how it fits their squad.","If you are planning a season, ask which courses, resources or sessions suit your age groups and playing level."],
  ["Say how many players you work with and what you want to improve, so they can point you to the right option.","Share your squad size, level and goals up front to make the conversation more useful."],
  ["Listing here is not an endorsement, so check qualifications and current details before you book or buy.","We are not affiliated with the provider, so confirm what is included on their website."]],
 'software':[["{n} is one of the club software, data and club-finder tools listed in Rugby Joints.","Rugby Joints lists {n} among its club software, data and finder tools."],
  ["Club secretaries and volunteers can use their official channels to ask how the tool works for a rugby club.","If you are comparing tools for your club, ask what is included and how it handles members, fixtures or bookings."],
  ["Note how many members and teams you have, and which job you want it to do, before you make contact.","Have your main needs written down first, so you can judge the answers against them."],
  ["Listing here is not an endorsement, so test the free options or demos where they exist.","We are not affiliated with the provider, so check current features and pricing on their website."]],
}
art = lambda w: "an" if w[:1].lower() in "aeiou" else "a"

def load_cards():
    s = (ROOT / "rugby-joints.html").read_text(encoding="utf-8")
    d = BeautifulSoup(s, "html.parser"); out = {}
    for w in d.select(".club-card-wrap"):
        slug = w["id"]; a = w.select_one("a.card-link"); img = w.select_one("img.club-badge")
        out[slug] = dict(slug=slug, name=html.unescape(w.select_one(".club-name").get_text()), sec=w["data-section"],
                         desc=w.select_one(".club-desc").get_text(), img=(img["src"] if img else None), href=a["href"])
    return s, out

def enrich(L, sec, cards):
    slug, name, site, kind, place, county, desc, _ = L
    p = ROOT / "club" / f"{slug}.html"
    d = BeautifulSoup(p.read_text(encoding="utf-8"), "html.parser")
    first, _, rest = desc.partition(". ")
    first += "." if not first.endswith(".") else ""
    # siblings: next three in the same section (alphabetical ring)
    pool = sorted([c for c in cards.values() if c["sec"] == sec], key=lambda c: re.sub(r"^the\s+", "", c["name"].lower()))
    i = next(k for k, c in enumerate(pool) if c["slug"] == slug)
    sib = [pool[(i + k) % len(pool)] for k in (1, 2, 3)]
    # about
    rt = d.select("#about .rich-text")
    rt[0].clear()
    rt[0].append(BeautifulSoup(f"<p>{E(name)} is {art(kind)} {E(kind)}. {E(first)}</p><p>{E(rest)} Rugby Joints lists it in the {E(SECNAME[sec])} section.</p>", "html.parser"))
    rt[1].clear()
    rt[1].append(BeautifulSoup(f"<p>{E(USE[sec].format(n=name))}</p><p>Related listings: " + ", ".join(f'<a href="{c["slug"]}.html">{E(c["name"])}</a>' for c in sib) + ".</p>", "html.parser"))
    d.select("#services h2")[0].string = f"How to use {name}"
    # contact paragraphs
    left = d.select_one(".join-contact-left")
    h = zlib.crc32(slug.encode())
    sents = [CONTACT[sec][k][(h >> k) & 1].replace("{n}", name) for k in range(4)]
    left.clear()
    left.append(BeautifulSoup(
        f'<p class="text-light" style="margin-bottom:1rem">Want to work with {E(name)}? The quickest route is through their official channels, where you can ask about their content, services or collaborations.</p>'
        f'<p class="text-light" style="margin-bottom:1rem">If you run {E(name)}, you can also claim this listing. That way you can add your phone number, email address and logo for free.</p>'
        f'<p class="text-light" style="margin-bottom:1rem">{E(" ".join(sents))}</p>', "html.parser"))
    # faq
    faq = d.select_one("#faq div[style*=max-width]"); faq.clear()
    qa = [(f"What is {name}?", f"{name} is {art(kind)} {kind}. {first}"),
          (f"Who is {name} best for?", f"{rest} It sits in the {SECNAME[sec]} section of Rugby Joints."),
          (f"How do I contact {name}?", "Visit their official website using the link on this page. If you run this listing, claim it to add direct contact details."),
          (f"Where else can I find similar rugby sites?", f"Rugby Joints also lists {sib[0]['name']}, {sib[1]['name']} and {sib[2]['name']} in the same section. Browse the full {SECNAME[sec]} section on the Rugby Joints page.")]
    faq.append(BeautifulSoup("".join(f'<details class="faq-item"><summary><h3>{E(q)}</h3></summary><div class="faq-a"><p>{E(a)}</p></div></details>' for q, a in qa), "html.parser"))
    # nearby = same-section siblings
    grid = d.select_one("#nearby .grid-3"); grid.clear()
    def card(c):
        img = c["img"] and (("../" + c["img"]) if not c["img"].startswith(("http", "/")) else c["img"])
        dd = c["desc"] if len(c["desc"]) <= 100 else c["desc"][:97].rsplit(" ", 1)[0] + "…"
        badge = (f'<img alt="{E(c["name"])} badge" class="club-badge" height="80" loading="lazy" src="{E(img)}" width="80"/>' if img else f'<div class="badge-fallback">{E(c["name"][:1])}</div>')
        return (f'<div><article class="club-card card"><a class="card-link" href="../club/{c["slug"]}.html"><div class="badge-area">{badge}</div>'
                f'<div class="card-content"><div class="card-meta"><span class="pill pill-business">Rugby Business</span></div><h3 class="club-name">{E(c["name"])}</h3><p class="club-desc">{E(dd)}</p>'
                f'<div class="card-cta"><span class="view-link">View Profile →</span></div></div></a></article></div>')
    grid.append(BeautifulSoup("".join(card(c) for c in sib), "html.parser"))
    d.select_one("#nearby h2").string = f"More in {SECNAME[sec]}"
    d.select_one("#nearby .sh p").string = "Other listings from the same Rugby Joints section."
    out = str(d).replace("Visit Club Website", "Visit Website")
    p.write_text(out, encoding="utf-8")

if __name__ == "__main__":
    pj, cards = load_cards()
    clubs = json.loads((ROOT / "tools/clubs.json").read_text(encoding="utf-8"))
    idx = json.loads((ROOT / "js/clubs-index.json").read_text(encoding="utf-8"))
    have = {c["slug"] for c in clubs}
    total = len(cards)
    sm = ""
    for J in JOINTS:
        slug, name, site, kind, place, county, desc, sec = J
        if (ROOT / "club" / f"{slug}.html").exists() or slug in have: print("skip", slug); continue
        abl.badge(slug, name)
        abl.page((slug, name, site, kind, place, county, desc), total)
        enrich(J, sec, cards)
        clubs.append({"slug": slug, "name": name, "type": "LocalBusiness", "sport": "", "town": place or "Online", "county": county or "UK", "founded": "", "ld_website": "", "has_tel": False, "has_mail": False,
                      "meta": f"{name}: {desc}", "canonical": f"{SITE}/club/{slug}.html"})
        idx.append({"n": name, "s": slug, "c": place or "Online", "t": "business", "b": f"/badges/{slug}.png"})
        sm += f'  <url><loc>{SITE}/club/{slug}.html</loc><lastmod>2026-11-26</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>\n'
    new = {J[0] for J in JOINTS}
    # cards: point the 22 external-link cards at their profile pages
    ARROW = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>'
    def relink(s, is_joints):
        for slug in new:
            st = s.index('<div class="club-card-wrap" id="%s"' % slug)
            en = s.index('</article></div>', st)
            blk = s[st:en]
            b2 = re.sub(r'<a href="[^"]*" class="card-link"[^>]*>', f'<a href="club/{slug}.html" class="card-link">', blk, count=1)
            b2 = re.sub(r'<span class="view-link">Visit website <svg.*?</svg></span>', '<span class="view-link">View Profile ' + ARROW + '</span>', b2, count=1, flags=re.S)
            assert b2 != blk and "_blank" not in b2, slug
            s = s[:st] + b2 + s[en:]
        return s
    for f in ("rugby-joints.html", "clubs.html"):
        s = (ROOT / f).read_text(encoding="utf-8"); s = relink(s, f == "rugby-joints.html")
        if f == "rugby-joints.html":
            s = s.replace("every listing links to the organisation's own website so you can confirm current details", "every listing has its own profile page that links to the organisation's own website so you can confirm current details")
            def fixld(m):
                j = json.loads(m.group(1))
                for it in j["@graph"][0]["mainEntity"]["itemListElement"]:
                    sl = it["url"].rsplit("#", 1)[-1]
                    if sl in new: it["url"] = f"{SITE}/club/{sl}.html"
                return '<script type="application/ld+json">' + json.dumps(j, ensure_ascii=False).replace("</", "<\\/") + "</script>"
            s = re.sub(r'<script type="application/ld\+json">(.*?)</script>', fixld, s, count=1, flags=re.S)
        (ROOT / f).write_text(s, encoding="utf-8")
    for f in (ROOT / "club").glob("*.html"):
        s = f.read_text(encoding="utf-8")
        if "pill-business" in s and "alongside 83 other listings" in s:
            f.write_text(s.replace("alongside 83 other listings", f"alongside {total - 1} other listings"), encoding="utf-8")
    p = ROOT / "sitemap.xml"; s = p.read_text(encoding="utf-8"); p.write_text(s.replace("</urlset>", sm + "</urlset>"), encoding="utf-8")
    (ROOT / "tools/clubs.json").write_text(json.dumps(clubs, ensure_ascii=False, indent=1), encoding="utf-8")
    (ROOT / "js/clubs-index.json").write_text(json.dumps(idx, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print("done", len(JOINTS), "profiles")

def fix_meta(J):
    """Title 50-60 chars and meta description 140-155 chars, mirrored into OG/Twitter/JSON-LD."""
    slug, name, site, kind, place, county, desc, sec = J
    p = ROOT / "club" / f"{slug}.html"; t = p.read_text(encoding="utf-8")
    m = re.search(r"<title>(.*?)</title>", t); old_t = m.group(1)
    cands = [f"{name} | Rugby Joints Profile | UKRCD", f"{name} | Rugby Business Profile | UKRCD", f"{name} | UK Rugby Club Directory",
             f"{name} | Rugby Joints | UKRCD", f"{name} Profile | UK Rugby Club Directory", f"{name} – Rugby Joints, UK Rugby Club Directory",
             f"{name} | Rugby Joints Listing | UKRCD", f"{name} Profile | UKRCD"]
    ok = [c for c in cands if 50 <= len(c) <= 60]
    new_t = ok[0] if ok else min(cands, key=lambda c: min(abs(len(c) - 50), abs(len(c) - 60)))
    first, _, rest = desc.partition(". ")
    first = first.rstrip(".") + "."
    tails = ["Read the full profile and find the website link.", "See the profile and official website link.", "View the profile and website link on UKRCD.",
             "See the full profile and website link.", "Profile and website link."]
    combos = [first + " " + x for x in tails] + [desc, desc + " " + tails[4], desc + " " + tails[3]] + [first + " " + rest.rstrip(".") + "." + " " + x for x in tails]
    ok = [c for c in combos if 140 <= len(c) <= 155]
    if ok: new_d = ok[0]
    else:
        c = min(combos, key=lambda c: abs(len(c) - 148)); new_d = c
        if len(c) > 155:
            c = c[:155].rsplit(" ", 1)[0].rstrip(",;:") ; new_d = c if c.endswith(".") else c + "."
    mo = re.search(r'<meta content="([^"]*)" name="description"/>', t); old_d = mo.group(1)
    t = t.replace(old_t, E(new_t).replace("&#x27;", "'") if False else html.escape(new_t, quote=False))
    t = t.replace(old_d, html.escape(new_d, quote=False))
    jd = old_d.replace("&amp;", "&")
    t = t.replace(json.dumps(jd, ensure_ascii=False)[1:-1], json.dumps(new_d, ensure_ascii=False)[1:-1])
    p.write_text(t, encoding="utf-8")
    return len(new_t), len(new_d)

if __name__ == "__main__" and "--meta" in sys.argv:
    for J in JOINTS: print(J[0], fix_meta(J))
