#!/usr/bin/env python3
"""
build_club_profiles_bulk.py - render the new profile template for every club from the
data that already exists in the repo (clubs.json, club-contacts.csv, club-grounds.csv,
er-teams.csv, badges/). Nothing is invented: any field the repo does not hold stays
empty and the template shows its fallback prompt ("Add training times" etc).

Output goes to preview/profiles/<slug>.html with noindex, so club/*.html is never touched.
Usage:
  python3 tools/build_club_profiles_bulk.py            # all clubs
  python3 tools/build_club_profiles_bulk.py aireborough-rfc alnwick-rfc
"""
import csv, json, re, sys
from collections import defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_club_profile as T

ROOT = T.ROOT
def rows(name):
    f = ROOT / "tools" / name
    return {r["slug"]: r for r in csv.DictReader(open(f, encoding="utf-8-sig"))} if f.exists() else {}

clubs = json.loads((ROOT / "tools/clubs.json").read_text(encoding="utf-8"))
contacts, grounds, er = rows("club-contacts.csv"), rows("club-grounds.csv"), rows("er-teams.csv")

def division(slug):
    lg = (er.get(slug) or {}).get("league", "")
    return lg.split("|")[0].strip()

by_div = defaultdict(list)
for c in clubs:
    d = division(c["slug"])
    if d:
        by_div[d].append(c)

def record(c):
    slug = c["slug"]; ct = contacts.get(slug, {}); gr = grounds.get(slug, {})
    code = c.get("sport") or "Rugby Union"
    badge = ROOT / "badges" / f"{slug}.png"
    div = division(slug)
    same = [{"name": o["name"], "slug": o["slug"], "town": o.get("town", ""), "code": o.get("sport") or "Rugby Union", "division": div}
            for o in by_div.get(div, []) if o["slug"] != slug][:4]
    socials = {"facebook": ct.get("facebook", "")}
    return {
        "slug": slug, "name": c["name"], "code": code, "division": div,
        "town": c.get("town", ""), "county": c.get("county", ""),
        "region_url": "../rugby-league.html" if "League" in code else "../rugby-union.html",
        "founded": int(c["founded"]) if str(c.get("founded", "")).isdigit() else None,
        "crest": f"../badges/{slug}.png" if badge.exists() else None,
        "claimed": False,
        "ground": {"name": gr.get("ground_name", ""), "address": ct.get("ground_address", ""), "postcode": ct.get("postcode", ""),
                   "lat": None, "lng": None, "surface": "", "station": None},
        "governing_body": "", "colours": "", "nickname": "", "leadership": [],
        "website": ct.get("website") or c.get("ld_website", ""), "socials": socials,
        "teams": [], "standing": None, "fixtures": [],
        "matchday": {"parking": gr.get("travel", "")} if gr.get("travel") else {},
        "history": {"text": "", "honours": [], "alumni": []},
        "ratings": {"count": 0, "overall": 0, "bars": {}},
        "sponsors": [], "nearby_10mi": [], "same_division": same,
    }

def deepen(page):
    """Output lives one folder deeper than club/, so push relative links up a level."""
    return re.sub(r'(href|src)="\.\./', r'\1="../../', page)

if __name__ == "__main__":
    want = set(sys.argv[1:])
    out = ROOT / "preview/profiles"; out.mkdir(parents=True, exist_ok=True)
    n = 0
    for c in clubs:
        if want and c["slug"] not in want:
            continue
        (out / f'{c["slug"]}.html').write_text(deepen(T.build(record(c), sample=True)).replace(
            "SAMPLE DATA: fictional club used to test the profile template. Not indexed.",
            "PREVIEW: built from existing directory data. Not indexed."), encoding="utf-8")
        n += 1
    print(f"wrote {n} pages to preview/profiles/")
