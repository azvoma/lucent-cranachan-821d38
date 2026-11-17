#!/usr/bin/env python3
"""
Fetch freely licensed ground + club photos from Wikimedia Commons for the club-page gallery.

Run on a machine with internet access (your computer, or a GitHub Action). Wikimedia asks API
users to identify themselves, so set a contact (email or URL) in the environment first:

    export COMMONS_CONTACT="you@example.com"
    python3 tools/fetch_commons_photos.py --limit 10 --dry-run   # safe test: search only
    python3 tools/fetch_commons_photos.py                        # every club still missing photos
    python3 tools/fetch_commons_photos.py --slug bath-rugby
    python3 tools/enhance_site.py                                # then rebuild the pages

What it does, per club:
  * searches Commons (File namespace) for a ground/stadium photo and a club/team photo
  * keeps only files with a reuse-friendly licence (CC BY, CC BY-SA, CC0, Public domain);
    rejects NonCommercial / NoDerivs / unknown licences, logos, crests, maps, kits and tiny images
  * requires the club's distinctive name in the file title/description
  * saves imgs/clubs/<slug>-ground.<ext> and imgs/clubs/<slug>-club.<ext> (1000px wide thumbnails)
  * records photographer + licence in tools/club-photos.csv, which the gallery shows as a credit

Nothing is overwritten: a slot that already has a file is skipped, so you can drop in your own
better photos first. Only the standard library is used.
"""
import argparse, csv, html, json, os, re, sys, time, urllib.parse, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT_DIR = os.path.join(ROOT, 'imgs', 'clubs')
META_CSV = os.path.join(HERE, 'club-photos.csv')
API = 'https://commons.wikimedia.org/w/api.php'
THUMB_W = 1000
MIN_W = 800
PAUSE = 1.0                      # seconds between requests (be polite)

ALLOWED_LICENCE = re.compile(r'^(CC[ -]BY([ -]SA)?([ -]\d|$)|CC0|Public domain|PD[ -])', re.I)
BLOCKED_LICENCE = re.compile(r'(\bNC\b|NonCommercial|\bND\b|NoDerivs|fair use|non-free)', re.I)
BAD_TITLE = re.compile(r'(logo|crest|badge|emblem|flag|\bmap\b|shirt|jersey|\bkit\b|seal|coat of arms|signature|'
                       r'poster|ticket|programme|banner|diagram|\.svg|\.gif|\.pdf|\.tif)', re.I)
GROUND_WORDS = re.compile(r'(ground|stadium|park\b|road\b|field|pitch|pavilion|clubhouse|stand\b|terrace|arena|'
                          r'recreation|\brec\b|oval|gate|entrance)', re.I)
CLUB_WORDS = re.compile(r'(team|players?|match|\bv\.?s?\.?\b|action|squad|lineout|scrum|tackle|game|fixture|'
                        r'celebrat|training|fans|supporters|womens?|ladies|youth|junior)', re.I)
GENERIC = {'rfc', 'rufc', 'rlfc', 'arlfc', 'fc', 'rugby', 'club', 'union', 'league', 'football', 'the', 'of',
           'and', 'old', 'men', 'womens', 'women', 'ladies', 'saint', 'town', 'city', 'united'}
UA = None


# ───────────────────────── helpers ─────────────────────────

def distinctive_tokens(name):
    toks = [t for t in re.findall(r"[a-z0-9']+", name.lower()) if t not in GENERIC and len(t) > 2]
    return toks or re.findall(r"[a-z0-9']+", name.lower())


def strip_html(t):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', t or ''))).strip()


def api_get(params, tries=4):
    params = dict(params, format='json', formatversion='2')
    url = API + '?' + urllib.parse.urlencode(params)
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'application/json'})
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.load(r)
            time.sleep(PAUSE)
            return data
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
            wait = 3 * (i + 1)
            print(f'   ! API retry {i + 1}/{tries} ({e}); waiting {wait}s', file=sys.stderr)
            time.sleep(wait)
    return {}


def search_files(query, limit=15):
    d = api_get({'action': 'query', 'generator': 'search', 'gsrsearch': query + ' filetype:bitmap',
                 'gsrnamespace': 6, 'gsrlimit': limit, 'prop': 'imageinfo',
                 'iiprop': 'url|size|mime|extmetadata', 'iiurlwidth': THUMB_W,
                 'iiextmetadatafilter': 'LicenseShortName|Artist|ImageDescription'})
    out = []
    for p in (d.get('query') or {}).get('pages', []):
        ii = (p.get('imageinfo') or [{}])[0]
        md = ii.get('extmetadata') or {}
        out.append({
            'title': p.get('title', ''),
            'url': ii.get('thumburl') or ii.get('url'),
            'width': ii.get('width', 0), 'height': ii.get('height', 0),
            'mime': ii.get('mime', ''),
            'licence': strip_html((md.get('LicenseShortName') or {}).get('value', '')),
            'artist': strip_html((md.get('Artist') or {}).get('value', '')),
            'desc': strip_html((md.get('ImageDescription') or {}).get('value', '')),
            'page': ii.get('descriptionurl', ''),
        })
    return out


def licence_ok(c):
    lic = c['licence']
    return bool(lic) and bool(ALLOWED_LICENCE.search(lic)) and not BLOCKED_LICENCE.search(lic)


def usable(c, tokens):
    if not c['url'] or c['mime'] not in ('image/jpeg', 'image/png', 'image/webp'):
        return False
    if c['width'] < MIN_W or c['height'] < 400 or c['height'] > c['width'] * 1.3:   # no tiny / tall portraits
        return False
    if BAD_TITLE.search(c['title']) or not licence_ok(c):
        return False
    hay = (c['title'] + ' ' + c['desc']).lower()
    return all(t in hay for t in tokens[:2])


def score(c, kind):
    words = GROUND_WORDS if kind == 'ground' else CLUB_WORDS
    other = CLUB_WORDS if kind == 'ground' else GROUND_WORDS
    s = 3 * len(words.findall(c['title'])) + len(words.findall(c['desc'])) - 2 * len(other.findall(c['title']))
    return s + min(c['width'], 3000) / 1500


def pick(cands, kind, tokens, exclude=()):
    words = GROUND_WORDS if kind == 'ground' else CLUB_WORDS
    good = [c for c in cands if usable(c, tokens) and c['title'] not in exclude
            and words.search(c['title'] + ' ' + c['desc'])]
    return max(good, key=lambda c: score(c, kind)) if good else None


def existing(slug, kind):
    return any(os.path.exists(os.path.join(OUT_DIR, f'{slug}-{kind}.{e}')) for e in ('webp', 'jpg', 'jpeg', 'png'))


def download(url, dest):
    for i in range(3):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
            if len(data) < 5000:
                raise ValueError('suspiciously small file')
            with open(dest, 'wb') as f:
                f.write(data)
            time.sleep(PAUSE)
            return True
        except Exception as e:
            print(f'   ! download retry {i + 1}/3 ({e})', file=sys.stderr)
            time.sleep(3 * (i + 1))
    return False


def ext_for(mime):
    return {'image/jpeg': 'jpg', 'image/png': 'png', 'image/webp': 'webp'}[mime]


def load_meta():
    rows = {}
    if os.path.exists(META_CSV):
        for r in csv.DictReader(open(META_CSV, encoding='utf-8')):
            rows[r['slug']] = r
    return rows


def save_meta(rows):
    cols = ['slug', 'ground_alt', 'club_alt', 'credit', 'ground_source', 'club_source']
    with open(META_CSV, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for k in sorted(rows):
            w.writerow({c: rows[k].get(c, '') for c in cols})


def credit_line(parts):
    bits = [f'{label}: {(c["artist"] or "Wikimedia Commons contributor")[:80]} ({c["licence"]})' for label, c in parts]
    return 'Photos: ' + '; '.join(bits) + ' via Wikimedia Commons'


# ───────────────────────── main ─────────────────────────

def main():
    global UA
    ap = argparse.ArgumentParser()
    ap.add_argument('--slug', help='only this club slug')
    ap.add_argument('--limit', type=int, default=0, help='stop after N clubs processed')
    ap.add_argument('--dry-run', action='store_true', help='search and report, download nothing')
    args = ap.parse_args()

    contact = os.environ.get('COMMONS_CONTACT', '').strip()
    if not contact:
        sys.exit('Set COMMONS_CONTACT (an email or URL) first: Wikimedia requires API clients to identify '
                 'themselves.\n  export COMMONS_CONTACT="you@example.com"')
    UA = f'UKRugbyClubDirectoryPhotoFetcher/1.0 (https://ukrugbyclubdirectory.co.uk; {contact})'

    recs = json.load(open(os.path.join(HERE, 'clubs.json'), encoding='utf-8'))
    grounds = {}
    gp = os.path.join(HERE, 'club-grounds.csv')
    if os.path.exists(gp):
        grounds = {r['slug']: r for r in csv.DictReader(open(gp, encoding='utf-8'))}
    meta = load_meta()
    os.makedirs(OUT_DIR, exist_ok=True)

    done = both = one = 0
    for rec in recs:
        slug, name = rec['slug'], rec['name']
        if not rec.get('type') or (args.slug and slug != args.slug):
            continue
        need_ground, need_club = not existing(slug, 'ground'), not existing(slug, 'club')
        if not (need_ground or need_club):
            continue
        if args.limit and done >= args.limit:
            break
        done += 1
        tokens = distinctive_tokens(name)
        town = rec.get('town') or ''
        print(f'[{done}] {name} ({slug})')

        got = {}
        if need_ground:
            g = grounds.get(slug) or {}
            queries = ([g['ground_name']] if g.get('ground_name') else []) + \
                      [f'{name} ground', f'{name} rugby ground {town}', f'{name} clubhouse']
            for q in queries:
                c = pick(search_files(q), 'ground', tokens)
                if c:
                    got['ground'] = c
                    break
        if need_club:
            exclude = {got['ground']['title']} if 'ground' in got else set()
            for q in (f'{name} rugby', f'{name} match', f'{name} team'):
                c = pick(search_files(q), 'club', tokens, exclude)
                if c:
                    got['club'] = c
                    break

        for kind in list(got):
            c = got[kind]
            print(f'   {kind}: {c["title"]}  [{c["licence"]}] {c["width"]}x{c["height"]}')
            if args.dry_run:
                continue
            if not download(c['url'], os.path.join(OUT_DIR, f'{slug}-{kind}.{ext_for(c["mime"])}')):
                del got[kind]
        if not got:
            print('   (nothing suitable found)')
            continue
        both += len(got) == 2
        one += len(got) == 1
        if not args.dry_run:
            row = meta.get(slug, {'slug': slug})
            if 'ground' in got:
                row['ground_alt'], row['ground_source'] = f'{name} ground', got['ground']['page']
            if 'club' in got:
                row['club_alt'], row['club_source'] = f'{name} rugby', got['club']['page']
            line = credit_line([(k.capitalize(), got[k]) for k in ('ground', 'club') if k in got])
            row['credit'] = (row.get('credit', '') + ' | ' if row.get('credit') else '') + line
            meta[slug] = row
            save_meta(meta)          # saved as we go, so an interrupted run loses nothing

    print(f'\nProcessed {done} clubs: {both} with both photos, {one} with one.')
    print('Next: python3 tools/enhance_site.py   (rebuilds the pages with the new photos and credits)')


if __name__ == '__main__':
    main()
