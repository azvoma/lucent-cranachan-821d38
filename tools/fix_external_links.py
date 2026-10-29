#!/usr/bin/env python3
"""
fix_external_links.py
UK Rugby Club Directory — External link audit fixes
Run from the repo root: python3 fix_external_links.py
"""

import os
import re

CLUB_DIR = "club"

# ─── 1. Club-specific URL fixes ──────────────────────────────────────────────
# Key: filename, Value: {dead_url: replacement or None to remove}
CLUB_URL_FIXES = {
    "ealing-trailfinders.html": {
        "https://www.trailfindersrugby.co.uk": "https://www.ealingtrailfinders.com"
    },
    "jersey-reds.html": {
        "https://www.rugbyjersey.je": "https://www.jerseyreds.je"
    },
    "newport-rfc.html": {
        "https://www.newportrugby.co.uk": "https://www.newportrfc.co.uk"
    },
    "loughborough-lightning.html": {
        "https://www.loughboroughlightning.co.uk": "https://www.loughboroughsport.com/lightning"
    },
    # Dead domains — remove website link block entirely
    "doncaster-knights.html": {
        "https://www.doncasterknight.com": None
    },
    "ampthill-rfc.html": {
        "https://www.ampthillrfc.com": None
    },
}

# ─── 2. Global link fixes applied to ALL pages ───────────────────────────────
# twitter.com → x.com (eliminates 3XX redirect flag on every page)
GLOBAL_URL_REPLACEMENTS = {
    'href="https://twitter.com"': 'href="https://x.com"',
    "href='https://twitter.com'": "href='https://x.com'",
}

# ─── Helper: remove anchor tag block containing a specific URL ────────────────
def remove_link_block(html, dead_url):
    """Remove <a href="dead_url">...</a> including surrounding whitespace."""
    # Match full anchor tag containing the dead URL
    pattern = rf'<a[^>]+href=["\'][^"\']*{re.escape(dead_url)}[^"\']*["\'][^>]*>.*?</a>'
    cleaned = re.sub(pattern, '', html, flags=re.DOTALL | re.IGNORECASE)
    # Clean up double blank lines left behind
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
    return cleaned

# ─── Helper: replace URL in href attributes ───────────────────────────────────
def replace_url(html, old_url, new_url):
    """Replace all occurrences of old_url with new_url in href attributes."""
    return html.replace(old_url, new_url)

# ─── Main ─────────────────────────────────────────────────────────────────────
def fix_file(filepath, club_fixes=None):
    with open(filepath, "r", encoding="utf-8") as f:
        original = f.read()
    
    html = original
    changed = False
    
    # Apply club-specific fixes
    if club_fixes:
        for dead_url, replacement in club_fixes.items():
            if dead_url in html:
                if replacement is None:
                    html = remove_link_block(html, dead_url)
                    print(f"  ❌ REMOVED link to {dead_url}")
                else:
                    html = replace_url(html, dead_url, replacement)
                    print(f"  🔄 UPDATED {dead_url} → {replacement}")
                changed = True
    
    # Apply global replacements to every file
    for old, new in GLOBAL_URL_REPLACEMENTS.items():
        if old in html:
            html = html.replace(old, new)
            changed = True
    
    if changed and html != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        return True
    return False

def main():
    print("=== External Link Fixer ===\n")
    
    updated = 0
    skipped = 0
    
    for fname in sorted(os.listdir(CLUB_DIR)):
        if not fname.endswith(".html"):
            continue
        
        filepath = os.path.join(CLUB_DIR, fname)
        club_fixes = CLUB_URL_FIXES.get(fname)
        
        if club_fixes:
            print(f"\n[CLUB FIX] {fname}")
        
        if fix_file(filepath, club_fixes):
            updated += 1
        else:
            skipped += 1
    
    # Also fix non-club pages (index, rugby-union, rugby-league, etc.)
    root_pages = [f for f in os.listdir(".") if f.endswith(".html")]
    print(f"\n[ROOT PAGES] Fixing global links in {len(root_pages)} root .html files...")
    for fname in root_pages:
        if fix_file(fname):
            updated += 1
    
    print(f"\n=== Done ===")
    print(f"  Files updated: {updated}")
    print(f"  Files unchanged: {skipped}")
    print(f"\nNext step: commit all changed files to GitHub.")
    print(f"Netlify will auto-deploy on push.")

if __name__ == "__main__":
    main()
