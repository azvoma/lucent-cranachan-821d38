#!/usr/bin/env python3
"""
apply_club_profile_template.py - rewrite every club/<slug>.html in the new 11-section profile layout.

Nothing existing is thrown away. For each club the script reads the current page and keeps:
  * the <head> (title, meta description, keywords, canonical, OG/Twitter, analytics, FAQPage JSON-LD)
  * About / History / At-a-glance / England Rugby fixtures link / Venue hire / Contact / FAQ / county club list
These move into a "More about <club>" band under the new template sections. The old SportsTeam JSON-LD
is replaced by the template's single @graph (SportsClub + Place + BreadcrumbList).

Live settings (differs from the previews): forms really submit (demo off) and affiliate placeholders are
switched off, so no page links to partner.invalid.

Usage:
  python3 tools/apply_club_profile_template.py                 # every club
  python3 tools/apply_club_profile_template.py aireborough-rfc # some clubs
Pages already in the new layout (body class cp-page) are skipped.
"""
import re, sys
from pathlib import Path
from bs4 import BeautifulSoup
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_club_profile as T
import build_club_profiles_bulk as B

ROOT = T.ROOT
T.CFG["demo_forms"] = False
T.CFG["monetisation"]["enabled"] = False

LD_RE = re.compile(r'<script type="application/ld\+json"(?P<attrs>[^>]*)>.*?</script>\s*', re.S)

def stat(soup, label):
    for s in soup.select(".stat-item"):
        sp = s.find("span")
        if sp and sp.get_text(strip=True) == label:
            st = s.find("strong")
            return st.get_text(strip=True) if st else ""
    return ""

def keep(el):
    return str(el) if el is not None else ""

def build_one(slug, rec_src):
    path = ROOT / "club" / f"{slug}.html"
    old = path.read_text(encoding="utf-8")
    if 'class="cp-page"' in old:
        return "skipped"
    soup = BeautifulSoup(old, "html.parser")

    rec = B.record(rec_src)
    lg = stat(soup, "League")
    if lg:
        rec["division"] = lg
    if not rec["founded"] and stat(soup, "Founded").isdigit():
        rec["founded"] = int(stat(soup, "Founded"))
    pc = stat(soup, "Postcode")
    if pc and not rec["ground"]["postcode"]:
        rec["ground"]["postcode"] = pc
    new = T.build(rec, sample=False)

    # ---- head: old head, minus the old SportsTeam graph, plus new stylesheet + new graph
    old_head = old[old.index("<head>"): old.index("</head>")]
    def drop_old_graph(m):
        return m.group(0) if 'id="guide-ld"' in m.group("attrs") else ""
    old_head = LD_RE.sub(drop_old_graph, old_head)
    new_ld = LD_RE.search(new[: new.index("</head>")]).group(0).strip()
    head = old_head.rstrip() + '\n<link rel="stylesheet" href="../css/club-profile.css">\n' + new_ld + "\n"

    # ---- preserved content
    about = soup.select_one("div.about-block:not(#history):not(#at-a-glance):not(.club-photos)")
    photos = soup.select_one("#club-photos")
    if photos is not None and len(photos.find_all("img")) <= 1:
        photos = None                      # badge only: the new hero already shows it
    hist, glance = soup.select_one("div#history"), soup.select_one("#at-a-glance")
    fixtures = soup.select_one(".fixtures-card")
    venue, contact, faq = (soup.select_one(f"section#{i}") for i in ("venue-hire", "contact", "faq"))
    county = soup.select_one("#county")
    parts = []
    inner = "".join(keep(x) for x in (about, photos, hist, glance, fixtures))
    if inner:
        parts.append(f'<section class="sec cp-more" id="club-about"><div class="con cp-more-inner">{inner}</div></section>')
    parts += [keep(x) for x in (venue, contact, faq)]
    if county is not None:
        parts.append(f'<section class="sec" id="county-clubs"><div class="con">{keep(county)}</div></section>')
    more = "\n".join(parts)

    # old ids that clash with ids the template already uses get a suffix (and their # links follow)
    used = set(re.findall(r'id="([^"]+)"', new))
    for i in sorted(set(re.findall(r'id="([^"]+)"', more)) & used):
        more = more.replace(f'id="{i}"', f'id="{i}-more"').replace(f'href="#{i}"', f'href="#{i}-more"')

    body = new[new.index("<body"):]
    body = body.replace("</main>", more + "\n</main>", 1)
    path.write_text("<!DOCTYPE html>\n<html lang=\"en-GB\">\n" + head + "</head>\n" + body, encoding="utf-8")
    return "ok"

def from_page(slug):
    """Club pages that are not in clubs.json: read the basics off the page itself."""
    soup = BeautifulSoup((ROOT / "club" / f"{slug}.html").read_text(encoding="utf-8"), "html.parser")
    loc = stat(soup, "Location")
    town, _, county = loc.partition(",")
    h1 = soup.find("h1")
    return {"slug": slug, "name": h1.get_text(strip=True) if h1 else slug, "sport": stat(soup, "Sport") or "Rugby Union",
            "town": town.strip(), "county": county.strip(), "founded": stat(soup, "Founded")}

if __name__ == "__main__":
    want = set(sys.argv[1:])
    res = {"ok": 0, "skipped": 0, "missing": 0}
    for c in B.clubs:
        if want and c["slug"] not in want:
            continue
        if not (ROOT / "club" / f'{c["slug"]}.html').exists():
            res["missing"] += 1; print("no page:", c["slug"]); continue
        res[build_one(c["slug"], c)] += 1
    known = {c["slug"] for c in B.clubs}
    for f in sorted((ROOT / "club").glob("*.html")):
        if f.stem in known or (want and f.stem not in want):
            continue
        res[build_one(f.stem, from_page(f.stem))] += 1
    print(res)
