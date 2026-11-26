#!/usr/bin/env python3
"""Make the 22 Rugby Joints profile pages properly shareable: 1200x630 social card per page, full OG/Twitter image tags,
and a visible 'Share this listing' block (Web Share API + copy link + email/X/Facebook/WhatsApp/LinkedIn). Re-runnable."""
import re, html, urllib.parse, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT = Path(__file__).resolve().parent.parent; SITE = "https://ukrugbyclubdirectory.co.uk"
sys.path.insert(0, str(ROOT / "tools"))
src = open(ROOT / "tools/add_joint_profiles.py", encoding="utf-8").read()
ns = {"__name__": "x", "__file__": str(ROOT / "tools/add_joint_profiles.py")}; exec(compile(src, "ajp", "exec"), ns)
JOINTS, SECNAME = ns["JOINTS"], ns["SECNAME"]
F = "/usr/share/fonts/opentype/inter/"
def font(w, s): return ImageFont.truetype(F + f"Inter-{w}.otf", s)
def wrap(d, text, f, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw: cur = t
        else: lines.append(cur); cur = w
    return lines + [cur]
def card(slug, name, sec, desc):
    im = Image.new("RGB", (1200, 630), "#293241"); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 18, 630], fill="#ee6c4d")
    d.text((80, 70), "UK RUGBY CLUB DIRECTORY", font=font("Bold", 28), fill="#ee6c4d")
    d.text((80, 118), "RUGBY JOINTS  ·  " + SECNAME[sec].upper(), font=font("SemiBold", 24), fill="#c9d1dc")
    f = font("Bold", 84)
    for sz in (84, 72, 62, 54):
        f = font("Bold", sz); L = wrap(d, name, f, 1040)
        if len(L) <= 2: break
    y = 220
    for ln in L[:2]: d.text((80, y), ln, font=f, fill="#ffffff"); y += int(f.size * 1.18)
    first = desc.split(". ")[0].rstrip(".") + "."
    f2 = font("Regular", 32); y += 24
    for ln in wrap(d, first, f2, 1040)[:3]: d.text((80, y), ln, font=f2, fill="#dfe5ec"); y += 46
    d.text((80, 560), "ukrugbyclubdirectory.co.uk", font=font("SemiBold", 28), fill="#ffffff")
    out = ROOT / "imgs/share"; out.mkdir(exist_ok=True)
    im.save(out / f"{slug}.png", optimize=True)
SHARE_CSS = ('<style id="share-css">.share-row{display:flex;flex-wrap:wrap;gap:.5rem;margin-top:.75rem}.share-row a,.share-row button{font:inherit;font-size:.8rem;padding:.4rem .7rem;border:1px solid #cfd6df;border-radius:6px;background:#fff;color:#293241;cursor:pointer;text-decoration:none;line-height:1.2}'
             '.share-row a:hover,.share-row button:hover{border-color:#ee6c4d;color:#ee6c4d}.share-native{display:none}</style>')
SHARE_JS = ('<script id="share-js">(function(){var n=document.querySelector(".share-native"),c=document.querySelector(".share-copy");'
            'if(n&&navigator.share){n.style.display="inline-block";n.addEventListener("click",function(){navigator.share({title:document.title,url:location.href.split("#")[0]}).catch(function(){})})}'
            'if(c){c.addEventListener("click",function(){var u=location.href.split("#")[0];function ok(){c.textContent="Link copied"}'
            'if(navigator.clipboard){navigator.clipboard.writeText(u).then(ok,function(){})}else{var t=document.createElement("textarea");t.value=u;document.body.appendChild(t);t.select();try{document.execCommand("copy");ok()}catch(e){}document.body.removeChild(t)}})}})();</script>')
def patch(J):
    slug, name, site, kind, place, county, desc, sec = J
    p = ROOT / "club" / f"{slug}.html"; t = p.read_text(encoding="utf-8")
    url = f"{SITE}/club/{slug}.html"; img = f"{SITE}/imgs/share/{slug}.png"
    alt = f"{name} – UK Rugby Club Directory listing"
    t = re.sub(r'<meta content="[^"]*" property="og:image"/>', f'<meta content="{img}" property="og:image"/><meta content="1200" property="og:image:width"/><meta content="630" property="og:image:height"/><meta content="{html.escape(alt)}" property="og:image:alt"/><meta content="en_GB" property="og:locale"/>', t, count=1) if 'og:image:width' not in t else re.sub(r'<meta content="[^"]*" property="og:image"/>', f'<meta content="{img}" property="og:image"/>', t, count=1)
    t = re.sub(r'<meta content="[^"]*" name="twitter:image"/>', f'<meta content="{img}" name="twitter:image"/><meta content="{html.escape(alt)}" name="twitter:image:alt"/>' if 'twitter:image:alt' not in t else f'<meta content="{img}" name="twitter:image"/>', t, count=1)
    if "share-css" not in t: t = t.replace("</head>", SHARE_CSS + "</head>", 1)
    q = urllib.parse.quote
    ttl = f"{name} on the UK Rugby Club Directory"
    block = (f'<div class="aside-card" id="share"><h3>Share this listing</h3><div class="share-row">'
             f'<button type="button" class="share-native">Share…</button><button type="button" class="share-copy">Copy link</button>'
             f'<a href="mailto:?subject={q(ttl)}&amp;body={q(url)}">Email</a>'
             f'<a href="https://twitter.com/intent/tweet?text={q(ttl)}&amp;url={q(url)}" target="_blank" rel="noopener">X</a>'
             f'<a href="https://www.facebook.com/sharer/sharer.php?u={q(url)}" target="_blank" rel="noopener">Facebook</a>'
             f'<a href="https://wa.me/?text={q(ttl + " " + url)}" target="_blank" rel="noopener">WhatsApp</a>'
             f'<a href="https://www.linkedin.com/sharing/share-offsite/?url={q(url)}" target="_blank" rel="noopener">LinkedIn</a></div></div>')
    if 'id="share"' in t: t = re.sub(r'<div class="aside-card" id="share">.*?</div></div>', block, t, count=1, flags=re.S)
    else:
        i = t.index('<li><a href="../rugby-joints.html"'); j = t.index("</div>", i) + len("</div>")
        t = t[:j] + "\n" + block + t[j:]
    if "share-js" not in t: t = t.replace("</body>", SHARE_JS + "</body>", 1)
    p.write_text(t, encoding="utf-8"); card(slug, name, sec, desc)
if __name__ == "__main__":
    for J in JOINTS: patch(J)
    # sitemap image entries are not needed; share cards are static assets
    print("patched", len(JOINTS))
