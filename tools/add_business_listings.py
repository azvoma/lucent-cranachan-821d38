#!/usr/bin/env python3
"""
add_business_listings.py - add new listings to the Rugby Joints (business) directory.

For every entry in LISTINGS it writes club/<slug>.html (from tools/business-page-template.html, a frozen copy
of an existing business page), a monogram badge, a card on rugby-joints.html and clubs.html, and entries in
tools/clubs.json, js/clubs-index.json and sitemap.xml, then refreshes the "66 businesses" counts.
Safe to re-run: anything already present is skipped.
"""
import json, re, html
from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://ukrugbyclubdirectory.co.uk"
# slug, name, website, kind, place (None = online), county, short description
LISTINGS = [
 ("fill-your-boots","Fill Your Boots (FYB Rugby)","https://www.fybrugby.com","grassroots rugby community hub",None,None,"Grassroots rugby hub with a club finder, resources and a blog for players, coaches and volunteers."),
 ("roots-ruck-riot","Roots Ruck Riot","https://linktr.ee/rootsruckriot","grassroots rugby podcast",None,None,"Grassroots rugby podcast spotlighting community clubs, with show notes linking out to each club."),
 ("bottom-of-the-ruck","Bottom of the Ruck","https://bottomoftheruck.com","grassroots rugby newsletter",None,None,"Grassroots rugby newsletter with storytelling and club admin tips."),
 ("grassroots-womens-rugby-podcast","Grassroots Women's Rugby Podcast","https://podcasts.apple.com/podcast/id1581395903","women's grassroots rugby podcast",None,None,"Podcast about women's grassroots rugby."),
 ("our-rugby-club-podcast","Our Rugby Club Podcast","https://podcasts.apple.com/podcast/id1878628301","community rugby podcast",None,None,"Community rugby podcast featuring interviews with people from across grassroots rugby."),
 ("rugby-through-the-leagues","Rugby Through The Leagues","https://rugbyttlpod.buzzsprout.com","grassroots rugby podcast",None,None,"Podcast covering grassroots rugby outside the mainstream media."),
 ("spond-grassroots-rugby-blog","Spond Grassroots Rugby Blog","https://www.spond.com/news-and-blog/grassroots-rugby-in-the-uk/","club app blog",None,None,"Blog from the Spond club app with a piece on grassroots rugby in the UK."),
 ("club-hub-uk","Club Hub UK","https://clubhubuk.co.uk","kids activity directory",None,None,"Kids activity directory that lists junior rugby clubs, aimed at parents."),
 ("scotland-rugby-news","Scotland Rugby News","https://www.scotlandrugbynews.com","Scottish rugby news site","Scotland",None,"Independent Scottish rugby news."),
 ("durham-county-rfu","Durham County RFU","https://www.durhamcountyrfu.com/blog","county rugby union","County Durham","County Durham","County rugby union with a blog carrying local club news."),
 ("devon-rfu","Devon RFU","https://devonrfu.co.uk/useful-info/rfu-regs-and-links/","county rugby union","Devon","Devon","County rugby union with a useful links page that lists Devon clubs."),
 ("sussex-rugby","Sussex Rugby","https://sussexrugby.co.uk","county rugby union","Sussex","Sussex","Club information hub for Sussex rugby."),
 ("oxfordshire-rfu","Oxfordshire RFU","https://www.oxfordshirerfu.com","county rugby union","Oxfordshire","Oxfordshire","County rugby union with club contact lists and volunteering pages."),
 ("yorkshire-rfu","Yorkshire RFU","https://yorkshirerfu.pitchero.com","county rugby union","Yorkshire","Yorkshire","County rugby union that publishes curated helpful-links lists for clubs."),
 ("kent-sportsuite-rugby-union","Kent Sportsuite: Rugby Union","https://kent.sportsuite.co.uk/a-z/rugby-union","local sport listing","Kent","Kent","Kent sport listing page for rugby union."),
 ("medway-council-rugby","Medway Council: Rugby","https://www.medway.gov.uk/directory/30/find_a_sport/category/66","council sport directory","Medway","Kent","Medway Council's find-a-sport directory list of rugby clubs."),
 ("bristol-city-council-rugby","Bristol City Council: Rugby","https://www.bristol.gov.uk/residents/museums-parks-sports-and-culture/sports-and-fitness/rugby","council rugby page","Bristol","Bristol","Bristol City Council page pointing residents to the RFU club finder."),
 ("ig-rugby","IG Rugby","https://igrugby.org/find-a-club","inclusive rugby club finder",None,None,"Inclusive rugby clubs finder."),
]
E = lambda s: html.escape(s, quote=True)

def badge(slug, name):
    p = ROOT / "badges" / f"{slug}.png"
    if p.exists(): return
    words = [w for w in re.findall(r"[A-Za-z]+", name) if w.lower() not in ("of","the","and","rugby")] or re.findall(r"[A-Za-z]+", name)
    ini = "".join(w[0] for w in words[:2]).upper()
    im = Image.new("RGBA", (200, 200), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((0, 0, 199, 199), fill=(41, 50, 65, 255))
    f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 84)
    w, h = d.textbbox((0, 0), ini, font=f)[2:]
    d.text(((200 - w) / 2, (200 - h) / 2 - 8), ini, font=f, fill=(238, 108, 77, 255))
    im.save(p)

def page(L, total):
    slug, name, site, kind, place, county, desc = L
    loc = f"{place}, {county}" if county and place != county else (place or "Online, UK")
    dom = re.sub(r"^https?://(www\.)?", "", site).split("/")[0]
    t = (ROOT / "tools/business-page-template.html").read_text(encoding="utf-8")
    meta = f"{name}: {desc} Read the full profile and find contact details."
    t = t.replace("Planet Rugby serves rugby clubs, coaches and players from London, Greater London. Read the full profile and find contact details. Find out more today.", E(meta))
    t = t.replace('content="Planet Rugby, London rugby business, rugby services in Greater London, Planet Rugby contact, rugby businesses UK"',
                  f'content="{E(name)}, {E(name)} contact, rugby {E(kind)}, rugby businesses UK"')
    t = t.replace("Planet Rugby is a rugby business in London, Greater London. It is one of the world&#x27;s leading rugby news websites covering union, league, sevens and international fixtures.",
                  f"{E(name)} is a {E(kind)} listed in the UK Rugby Club Directory. {E(desc)}")
    t = t.replace("Planet Rugby works with rugby clubs, coaches and players across Greater London. Contact the business directly for current products, services and prices.",
                  f"Visit the {E(name)} website for current information, content and ways to get in touch.")
    t = t.replace("alongside 66 other listings", f"alongside {total - 1} other listings")
    t = t.replace("London, Greater London", E(loc))
    t = t.replace("https://www.planetrugby.com", E(site)).replace("planetrugby.com", E(dom))
    t = t.replace("planet-rugby", slug).replace("Planet Rugby", E(name))
    t = t.replace("https://ukrugbyclubdirectory.co.uk/planet%20rugby.jpg", f"{SITE}/badges/{slug}.png")
    t = t.replace("Planet+Rugby+London", "").replace("<title>"+E(name)+" |", "<title>"+E(name)+" |")
    soup = BeautifulSoup(t, "html.parser")
    for sel in (".ground-mini-card", "#county"):
        for el in soup.select(sel): el.decompose()
    for a in soup.select(".club-hero-er-btns a.btn-er-ghost"): a.decompose()
    for a in soup.select(".seo-links-inner a"):
        if a.get_text(strip=True).startswith(("Rugby in ",)):
            nxt = a.find_next_sibling()
            if nxt is not None and "sep" in (nxt.get("class") or []): nxt.decompose()
            a.decompose()
    faq = soup.select_one("#faq div[style*=max-width]")
    qa = [(f"What is {name}?", f"{name} is a {kind}. {desc}"),
          (f"How do I contact {name}?", "Visit their official website using the link above. If you run this listing, claim it to add direct contact details.")]
    faq.clear()
    faq.append(BeautifulSoup("".join(f'<details class="faq-item"><summary><h3>{E(q)}</h3></summary><div class="faq-a"><p>{E(a)}</p></div></details>' for q, a in qa), "html.parser"))
    out = str(soup)
    # schema: organisation, online ones have no postal address
    def fix(m):
        j = json.loads(m.group(1)); g = j["@graph"][0]; g["@type"] = "Organization"; g["description"] = meta
        g.pop("address", None)
        if place:
            g["address"] = {"@type": "PostalAddress", "addressLocality": place, "addressCountry": "GB", **({"addressRegion": county} if county else {})}
        j["@graph"][1]["itemListElement"][1]["name"] = "Rugby Joints"
        return '<script type="application/ld+json">' + json.dumps(j, ensure_ascii=False).replace("</", "<\\/") + "</script>"
    out = re.sub(r'<script type="application/ld\+json">(.*?)</script>', fix, out, count=1, flags=re.S)
    (ROOT / "club" / f"{slug}.html").write_text(out, encoding="utf-8")
    return loc

def card(L, loc, wrap=True):
    slug, name, site, kind, place, county, desc = L
    city = (place or "online").lower()
    return (f'<div class="club-card-wrap" data-category="business" data-name="{E(name.lower())}" data-city="{E(city)}"><article class="club-card card">\n'
            f'  <a href="club/{slug}.html" class="card-link">\n'
            f'    <div class="badge-area"><img src="badges/{slug}.png" alt="{E(name)} club badge" class="club-badge" loading="lazy" width="100" height="100"></div>\n'
            f'    <div class="card-content">\n      <div class="card-meta"><span class="pill pill-business">Rugby Business</span></div>\n'
            f'      <h3 class="club-name">{E(name)}</h3>\n'
            f'      <p class="club-loc"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>{E(loc)}</p>\n'
            f'      <p class="club-desc">{E(desc)}</p>\n'
            f'      <div class="card-cta"><span class="view-link">View Profile <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg></span></div>\n'
            f'    </div>\n  </a>\n</article></div>\n')

def insert_after_last_business_card(s, cards):
    last = [m.start() for m in re.finditer(r'<div class="club-card-wrap" data-category="business"', s)][-1]
    end = s.index("</article></div>", last) + len("</article></div>")
    return s[:end] + "\n" + cards + s[end:]

if __name__ == "__main__":
    clubs = json.loads((ROOT / "tools/clubs.json").read_text(encoding="utf-8"))
    idx = json.loads((ROOT / "js/clubs-index.json").read_text(encoding="utf-8"))
    have = {c["slug"] for c in clubs}
    new = [L for L in LISTINGS if L[0] not in have]
    old_total = sum(1 for c in clubs if not c.get("sport") and (ROOT / "club" / f'{c["slug"]}.html').exists() and "pill-business" in (ROOT / "club" / f'{c["slug"]}.html').read_text(encoding="utf-8"))
    total = old_total + len(new)
    print("existing businesses", old_total, "adding", len(new), "-> total", total)
    if not new: raise SystemExit
    cards, sm = "", ""
    for L in new:
        assert not (ROOT / "club" / f"{L[0]}.html").exists(), L[0]
        badge(L[0], L[1]); loc = page(L, total); cards += card(L, loc)
        clubs.append({"slug": L[0], "name": L[1], "type": "LocalBusiness", "sport": "", "town": L[4] or "Online", "county": L[5] or "UK", "founded": "", "ld_website": "", "has_tel": False, "has_mail": False,
                      "meta": f"{L[1]}: {L[6]}", "canonical": f"{SITE}/club/{L[0]}.html"})
        idx.append({"n": L[1], "s": L[0], "c": L[4] or "Online", "t": "business", "b": f"/badges/{L[0]}.png"})
        sm += f'  <url><loc>{SITE}/club/{L[0]}.html</loc><lastmod>2026-11-17</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>\n'
    for f in ("rugby-joints.html", "clubs.html"):
        p = ROOT / f; s = insert_after_last_business_card(p.read_text(encoding="utf-8"), cards)
        p.write_text(s, encoding="utf-8")
    # counts
    p = ROOT / "rugby-joints.html"; s = p.read_text(encoding="utf-8"); p.write_text(re.sub(r"\b%d\b" % old_total, str(total), s), encoding="utf-8")
    p = ROOT / "clubs.html"; s = p.read_text(encoding="utf-8"); p.write_text(s.replace(f"Businesses ({old_total})", f"Businesses ({total})"), encoding="utf-8")
    p = ROOT / "index.html"; s = p.read_text(encoding="utf-8"); p.write_text(s.replace(f"Browse {old_total} businesses", f"Browse {total} businesses"), encoding="utf-8")
    for f in (ROOT / "club").glob("*.html"):
        s = f.read_text(encoding="utf-8")
        if "pill-business" in s and f"alongside {old_total} other listings" in s:
            f.write_text(s.replace(f"alongside {old_total} other listings", f"alongside {total - 1} other listings"), encoding="utf-8")
    p = ROOT / "sitemap.xml"; s = p.read_text(encoding="utf-8"); p.write_text(s.replace("</urlset>", sm + "</urlset>"), encoding="utf-8")
    (ROOT / "tools/clubs.json").write_text(json.dumps(clubs, ensure_ascii=False, indent=1), encoding="utf-8")
    (ROOT / "js/clubs-index.json").write_text(json.dumps(idx, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
