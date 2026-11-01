#!/usr/bin/env python3
"""
Build the standalone long-form guide pages (rugby-leagues-uk.html,
rugby-union-league-structure.html) from tools/content/leagues.py.

Run from the repo root:  python3 tools/build_guides.py
The page shell (head assets, header, footer) comes from rugby-clubs-surrey.html,
the same as the county hubs, so guides always match the rest of the site.
"""
import html as H
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_hubs import shell, ROOT, SITE  # noqa: E402
from guide_render import render_block, render_ld  # noqa: E402
from content.leagues import RUGBY_LEAGUES_UK, UNION_STRUCTURE  # noqa: E402


def build(g, parts):
    head_tail, header, footer = parts
    url = f'{SITE}/{g["slug"]}.html'
    title, meta = H.escape(g['title'], quote=False), H.escape(g['meta'], quote=True)
    ld = render_ld(g, url, 'Article', crumbs=[('Home', SITE + '/'), (g['crumb'], url)], image=g['image'])
    body = render_block(g)
    page = f'''<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{meta}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:title" content="{H.escape(g['title'], quote=True)}">
<meta property="og:description" content="{meta}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/{g['image']}">
<meta property="og:site_name" content="UK Rugby Club Directory">
<meta property="article:modified_time" content="{g['updated']}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{H.escape(g['title'], quote=True)}">
<meta name="twitter:description" content="{meta}">
<meta name="geo.region" content="GB">
<meta name="theme-color" content="#293241">
{head_tail}{ld}
{header}<main id="main">
<section class="listing-hero-england" style="position:relative;min-height:220px;display:flex;align-items:stretch;overflow:hidden;border-bottom:none">
  <div class="lh-left" style="position:relative;z-index:2;flex:0 0 58%;background:var(--navy);clip-path:polygon(0 0,82% 0,100% 100%,0 100%);padding:2.25rem 5rem 2.25rem 2rem;display:flex;flex-direction:column;justify-content:center">
    <nav class="breadcrumb" style="margin-bottom:.6rem" aria-label="Breadcrumb">
      <a href="index.html">Home</a><span class="bc-sep">›</span>
      <span class="bc-cur">{H.escape(g['crumb'])}</span>
    </nav>
    <span class="lh-eyebrow" style="font-family:Oswald,sans-serif;font-size:.65rem;font-weight:600;letter-spacing:.14em;text-transform:uppercase;margin-bottom:.5rem;display:block">Guide · Updated for 2026-27</span>
    <h1 style="font-family:Oswald,sans-serif;font-size:clamp(1.5rem,3.2vw,2.3rem);font-weight:700;color:#fff;letter-spacing:.03em;text-transform:uppercase;margin:0 0 .5rem;line-height:1.08">{H.escape(g['h1'])}</h1>
    <p style="font-size:.9rem;color:rgba(255,255,255,.85);line-height:1.55;margin-bottom:1rem;max-width:460px">{H.escape(g['hero_sub'])}</p>
    <div class="club-hero-er-btns">
      <a href="clubs.html" class="btn-er-primary">Find a Club ›</a>
      <a href="#{g['sections'][0]['id']}" class="btn-er-ghost">Read the Guide ›</a>
    </div>
  </div>
  <div class="lh-right lh-pattern" aria-hidden="true" style="position:absolute;right:0;top:0;bottom:0;width:42%"></div>
</section>
<section class="sec guide-wrap">
  <div class="con">
{body}
  </div>
</section>
<section class="sec sec-off">
  <div class="con" style="text-align:center">
    <h2 style="font-size:1.5rem;font-weight:700;color:var(--text-primary);margin:0 0 .75rem">Is Your Club Missing?</h2>
    <p style="max-width:620px;margin:0 auto 1rem;color:var(--text-secondary)">We add clubs every week. If your club is not listed, register it for free so players searching near you can find it.</p>
    <a href="register.html" class="btn btn-red">Register Your Club Free</a>
  </div>
</section>
{footer}'''
    open(os.path.join(ROOT, g['slug'] + '.html'), 'w', encoding='utf-8').write(page)
    return len(body.split())


if __name__ == '__main__':
    parts = shell()
    for g in (RUGBY_LEAGUES_UK, UNION_STRUCTURE):
        print(g['slug'], build(g, parts), 'words (approx, incl. markup)')
