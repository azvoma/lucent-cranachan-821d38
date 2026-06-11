// netlify/plugins/generate-blog/index.js
// Runs at build time (onPostBuild) — reads content/blog/*.md and outputs:
//   /blog/index.html           → article listing page
//   /blog/<slug>/index.html    → individual article pages
//
// Header, nav, footer and scripts are copied verbatim from the live site.
// They NEVER change when articles are added — only editing this file changes them.

const fs   = require("fs");
const path = require("path");

// ─── Frontmatter parser ───────────────────────────────────────────────────────
function parseFrontmatter(text) {
  const fm = {};
  let body = text;
  const match = text.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?([\s\S]*)$/);
  if (match) {
    body = match[2];
    for (const line of match[1].split(/\r?\n/)) {
      const kv = line.match(/^([\w-]+):\s*["']?(.+?)["']?\s*$/);
      if (kv) fm[kv[1].toLowerCase()] = kv[2].trim();
    }
  }
  return { fm, body: body.trim() };
}

// ─── Markdown → HTML ─────────────────────────────────────────────────────────
function mdToHtml(md) {
  let html = md
    .replace(/&/g,  "&amp;")
    .replace(/</g,  "&lt;")
    .replace(/>/g,  "&gt;")
    .replace(/^#### (.+)$/gm, "<h4>$1</h4>")
    .replace(/^### (.+)$/gm,  "<h3>$1</h3>")
    .replace(/^## (.+)$/gm,   "<h2>$1</h2>")
    .replace(/^# (.+)$/gm,    "<h1>$1</h1>")
    .replace(/\*\*\*(.+?)\*\*\*/g, "<strong><em>$1</em></strong>")
    .replace(/\*\*(.+?)\*\*/g,     "<strong>$1</strong>")
    .replace(/\*(.+?)\*/g,         "<em>$1</em>")
    .replace(/`(.+?)`/g,           "<code>$1</code>")
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" rel="noopener">$1</a>');

  html = html.replace(/((?:^[-*] .+$\n?)+)/gm, block => {
    const items = block.trim().split("\n").map(l => `<li>${l.replace(/^[-*] /, "")}</li>`).join("");
    return `<ul>${items}</ul>\n`;
  });
  html = html.replace(/((?:^\d+\. .+$\n?)+)/gm, block => {
    const items = block.trim().split("\n").map(l => `<li>${l.replace(/^\d+\. /, "")}</li>`).join("");
    return `<ol>${items}</ol>\n`;
  });
  html = html.split(/\n{2,}/).map(block => {
    block = block.trim();
    if (!block) return "";
    if (/^<[huo]/.test(block)) return block;
    return `<p>${block.replace(/\n/g, " ")}</p>`;
  }).join("\n");

  return html;
}

function fmtDate(str) {
  if (!str) return "";
  try {
    return new Date(str).toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" });
  } catch { return str; }
}

// ─── STATIC HEADER — copied verbatim from the live site ──────────────────────
// Edit here if the site header ever changes. Never regenerated automatically.
function siteHeader() {
  return `<header id="site-header">
  <div class="con hdr-inner">
    <a href="/index.html" class="logo" aria-label="UK Rugby Club Directory">
      <svg viewBox="0 0 220 48" xmlns="http://www.w3.org/2000/svg" height="48" role="img" aria-label="UK Rugby Club Directory" style="display:block">
        <title>UK Rugby Club Directory</title>
        <text x="0" y="31" font-family="Arial,Helvetica,sans-serif" font-size="12" font-weight="700" fill="#c8102e" letter-spacing="3">UK</text>
        <rect x="35" y="7" width="2.5" height="34" rx="1.25" fill="white"/>
        <text x="46" y="26" font-family="Arial,Helvetica,sans-serif" font-size="17" font-weight="700" fill="white" letter-spacing="-0.3">Rugby Club</text>
        <text x="46" y="40" font-family="Arial,Helvetica,sans-serif" font-size="9.5" fill="rgba(255,255,255,0.5)" letter-spacing="3.5">DIRECTORY</text>
      </svg>
    </a>
    <nav id="main-nav" aria-label="Main navigation">
      <a href="/index.html" class="nav-link">Home</a>
      <div class="nav-dropdown">
        <button class="nav-link nav-drop-btn" aria-expanded="false" aria-haspopup="true">
          Rugby Union <svg class="drop-caret" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M6 9l6 6 6-6"/></svg>
        </button>
        <div class="dropdown-panel">
          <div class="dp-inner">
            <div class="dp-col">
              <span class="dp-heading">Browse by Region</span>
              <a href="/rugby-union.html" class="dp-link">All Union Clubs</a>
              <a href="/rugby-union.html?region=london-se" class="dp-link">London &amp; South East</a>
              <a href="/rugby-union.html?region=north-west" class="dp-link">North West</a>
              <a href="/rugby-union.html?region=yorkshire" class="dp-link">Yorkshire</a>
              <a href="/rugby-union.html?region=midlands" class="dp-link">Midlands</a>
              <a href="/rugby-union.html?region=south-west" class="dp-link">South West</a>
              <a href="/rugby-union.html?region=north-east" class="dp-link">North East</a>
              <a href="/rugby-union.html?region=wales" class="dp-link">Wales</a>
              <a href="/rugby-union.html?region=scotland" class="dp-link">Scotland</a>
              <a href="/rugby-union.html?region=northern-ireland" class="dp-link">N. Ireland</a>
            </div>
            <div class="dp-col">
              <span class="dp-heading">Popular</span>
              <a href="/rugby-union.html?region=yorkshire" class="dp-link dp-tag">Rugby in Yorkshire</a>
              <a href="/rugby-union.html?region=london-se" class="dp-link dp-tag">Rugby in Surrey</a>
              <a href="/rugby-union.html?region=south-west" class="dp-link dp-tag">Rugby in the South West</a>
            </div>
          </div>
        </div>
      </div>
      <div class="nav-dropdown">
        <button class="nav-link nav-drop-btn" aria-expanded="false" aria-haspopup="true">
          Rugby League <svg class="drop-caret" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M6 9l6 6 6-6"/></svg>
        </button>
        <div class="dropdown-panel">
          <div class="dp-inner">
            <div class="dp-col">
              <span class="dp-heading">Browse Clubs</span>
              <a href="/rugby-league.html" class="dp-link">All League Clubs</a>
              <a href="/rugby-league.html?region=yorkshire" class="dp-link">Yorkshire</a>
              <a href="/rugby-league.html?region=north-west" class="dp-link">North West</a>
            </div>
          </div>
        </div>
      </div>
      <a href="/rugby-joints.html" class="nav-link">Businesses</a>
      <a href="/blog" class="nav-link active">Blog</a>
      <a href="/contact-us.html" class="nav-link">Contact</a>
      <a href="/register.html" class="nav-link nav-cta btn btn-red btn-sm">+ Register Club</a>
    </nav>
    <button id="hamburger" aria-label="Open menu" aria-expanded="false"><span></span><span></span><span></span></button>
  </div>
</header>`;
}

// ─── STATIC FOOTER — copied verbatim from the live site ──────────────────────
function siteFooter() {
  return `<footer>
  <div class="ft-top">
    <div class="con ft-grid">
      <div class="ft-brand">
        <a href="/index.html" class="ft-logo">
          <svg viewBox="0 0 200 40" xmlns="http://www.w3.org/2000/svg" height="40" role="img" aria-label="UK Rugby Club Directory" style="display:block">
            <title>UK Rugby Club Directory</title>
            <text x="0" y="26" font-family="Arial,Helvetica,sans-serif" font-size="10" font-weight="700" fill="#c8102e" letter-spacing="2.5">UK</text>
            <rect x="29" y="5" width="2" height="30" rx="1" fill="white"/>
            <text x="39" y="21" font-family="Arial,Helvetica,sans-serif" font-size="14" font-weight="700" fill="white" letter-spacing="-0.3">Rugby Club</text>
            <text x="39" y="33" font-family="Arial,Helvetica,sans-serif" font-size="8" fill="rgba(255,255,255,0.45)" letter-spacing="3">DIRECTORY</text>
          </svg>
        </a>
        <p class="ft-strapline">The UK's most comprehensive free rugby club directory. 620 clubs each with their own full profile page, unique SEO and verified contact details across England, Scotland, Wales and Northern Ireland.</p>
        <div class="ft-socials">
          <a href="https://twitter.com" target="_blank" rel="noopener" class="ft-soc" aria-label="Twitter/X"><svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-4.714-6.231-5.401 6.231H2.744l7.736-8.856L1.999 2.25H8.08l4.258 5.63 5.906-5.63zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg></a>
          <a href="https://facebook.com" target="_blank" rel="noopener" class="ft-soc" aria-label="Facebook"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M18 2h-3a5 5 0 00-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 011-1h3z"/></svg></a>
          <a href="https://instagram.com" target="_blank" rel="noopener" class="ft-soc" aria-label="Instagram"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1.5" fill="currentColor" stroke="none"/></svg></a>
        </div>
      </div>
      <div class="ft-col"><h3>Directory</h3><ul>
        <li><a href="/index.html">Home</a></li>
        <li><a href="/clubs.html">All Clubs</a></li>
        <li><a href="/rugby-union.html">Rugby Union</a></li>
        <li><a href="/rugby-league.html">Rugby League</a></li>
        <li><a href="/rugby-joints.html">Businesses</a></li>
      </ul></div>
      <div class="ft-col"><h3>Regions</h3><ul>
        <li><a href="/rugby-union.html?region=london-se">London &amp; South East</a></li>
        <li><a href="/rugby-union.html?region=yorkshire">Yorkshire</a></li>
        <li><a href="/rugby-union.html?region=midlands">Midlands</a></li>
        <li><a href="/rugby-union.html?region=north-west">North West</a></li>
        <li><a href="/rugby-union.html?region=south-west">South West</a></li>
        <li><a href="/rugby-union.html?region=wales">Wales</a></li>
        <li><a href="/rugby-union.html?region=scotland">Scotland</a></li>
        <li><a href="/rugby-union.html?region=northern-ireland">N. Ireland</a></li>
      </ul></div>
      <div class="ft-col"><h3>Get Involved</h3><ul>
        <li><a href="/register.html">Register Your Club</a></li>
        <li><a href="/contact-us.html">Contact Us</a></li>
        <li><a href="https://www.englandrugby.com" target="_blank" rel="noopener">England Rugby</a></li>
        <li><a href="https://www.rugby-league.com" target="_blank" rel="noopener">Rugby League</a></li>
        <li><a href="https://www.wru.wales" target="_blank" rel="noopener">Welsh Rugby Union</a></li>
        <li><a href="https://www.scottishrugby.org" target="_blank" rel="noopener">Scottish Rugby</a></li>
      </ul></div>
      <div class="ft-col"><h3>Legal</h3><ul>
        <li><a href="/privacy-policy.html">Privacy Policy</a></li>
        <li><a href="/terms-of-service.html">Terms of Service</a></li>
        <li><a href="/cookie-policy.html">Cookie Policy</a></li>
        <li><a href="/sitemap.xml">Sitemap</a></li>
        <li><a href="/register.html">List Your Club Free</a></li>
      </ul></div>
    </div>
  </div>
  <div class="ft-bottom">
    <div class="con ft-bottom-inner">
      <p>&copy; 2025 UK Rugby Club Directory. All rights reserved. 620 individual club profiles across England, Scotland, Wales and Northern Ireland.</p>
      <div class="ft-bottom-links">
        <a href="/privacy-policy.html">Privacy</a><span>·</span>
        <a href="/terms-of-service.html">Terms</a><span>·</span>
        <a href="/cookie-policy.html">Cookies</a><span>·</span>
        <a href="/contact-us.html">Contact</a><span>·</span>
        <a href="/sitemap.xml">Sitemap</a>
      </div>
    </div>
  </div>
</footer>`;
}

// ─── Full page shell ──────────────────────────────────────────────────────────
function shell({ title, description, canonical, ogType, bodyContent }) {
  return `<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${title} | UK Rugby Club Directory</title>
  <meta name="description" content="${description}">
  <link rel="canonical" href="${canonical}">
  <meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
  <meta property="og:title"       content="${title}">
  <meta property="og:description" content="${description}">
  <meta property="og:url"         content="${canonical}">
  <meta property="og:type"        content="${ogType || "website"}">
  <meta property="og:site_name"   content="UK Rugby Club Directory">
  <meta name="twitter:card"        content="summary_large_image">
  <meta name="twitter:title"       content="${title}">
  <meta name="twitter:description" content="${description}">
  <meta name="geo.region" content="GB">
  <meta name="theme-color" content="#0a1628">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;600;700&family=Source+Sans+3:ital,wght@0,300;0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/style.css">
  <style>
    /* ── Blog-specific styles ───────────────────────────────────────────── */
    .blog-hero{background:var(--navy,#0a1628);padding:3.5rem 1.5rem 3rem;color:#fff;text-align:center}
    .blog-eyebrow{display:inline-flex;align-items:center;gap:.4rem;font-size:.7rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#f5c500;margin:0 0 .65rem}
    .blog-hero h1{font-family:var(--fd,'Oswald',sans-serif);font-size:clamp(2.8rem,7vw,4.5rem);font-weight:700;text-transform:uppercase;margin:0 0 .6rem;line-height:1.05}
    .blog-hero-meta{font-size:.9rem;color:rgba(255,255,255,.55);margin:0}
    .blog-section{max-width:1160px;margin:0 auto;padding:3rem 1.5rem}
    .blog-section-hd{margin-bottom:2rem}
    .blog-section-eyebrow{font-size:.68rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#c8102e;margin:0 0 .3rem}
    .blog-section-title{font-family:var(--fd,'Oswald',sans-serif);font-size:1.7rem;font-weight:700;text-transform:uppercase;color:var(--navy,#0a1628);margin:0 0 .4rem}
    .blog-section-sub{color:#64748b;font-size:.95rem;margin:0}
    .blog-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1.75rem;margin-top:2rem}
    @media(max-width:1060px){.blog-grid{grid-template-columns:repeat(2,1fr)}}
    @media(max-width:640px){.blog-grid{grid-template-columns:1fr}}
    .blog-card{background:#fff;border:1px solid var(--gl,#e2e8f0);border-radius:var(--rad,8px);overflow:hidden;box-shadow:var(--sh1,0 1px 4px rgba(0,0,0,.06));transition:box-shadow .25s,transform .25s;display:flex;flex-direction:column;text-decoration:none;color:inherit}
    .blog-card:hover{box-shadow:var(--sh3,0 8px 24px rgba(0,0,0,.12));transform:translateY(-4px)}
    .blog-card-img{height:190px;background:linear-gradient(135deg,var(--navy,#0a1628) 0%,#1e3050 100%);position:relative;overflow:hidden;flex-shrink:0;display:flex;align-items:center;justify-content:center}
    .blog-card-cat{position:absolute;top:.85rem;left:.85rem;font-size:.65rem;font-weight:700;letter-spacing:.07em;text-transform:uppercase;background:#c8102e;color:#fff;padding:.22rem .65rem;border-radius:100px}
    .blog-card-body{padding:1.35rem;display:flex;flex-direction:column;gap:.5rem;flex:1}
    .blog-card-date{font-size:.73rem;color:#94a3b8;font-weight:500}
    .blog-card-title{font-family:var(--fd,'Oswald',sans-serif);font-size:1.05rem;font-weight:700;text-transform:uppercase;letter-spacing:.3px;color:var(--navy,#0a1628);line-height:1.25;margin:0}
    .blog-card:hover .blog-card-title{color:#c8102e}
    .blog-card-excerpt{font-size:.86rem;color:#475569;line-height:1.6;margin:0;flex:1}
    .blog-card-cta{margin-top:auto;padding-top:.75rem;border-top:1px solid var(--off,#f1f5f9);font-size:.78rem;font-weight:700;color:#c8102e;display:flex;align-items:center;gap:.3rem;transition:gap .15s}
    .blog-card:hover .blog-card-cta{gap:.55rem}
    .blog-empty{grid-column:1/-1;text-align:center;padding:5rem 2rem;color:#94a3b8}
    .blog-empty h3{font-family:var(--fd,'Oswald',sans-serif);font-size:1.3rem;color:var(--navy,#0a1628);margin-bottom:.75rem}
    /* Article page */
    .article-hero{background:var(--navy,#0a1628);padding:3rem 1.5rem 2.5rem;color:#fff}
    .article-hero-inner{max-width:800px;margin:0 auto}
    .breadcrumb{font-size:.8rem;color:#64748b;margin:0 0 1rem}
    .breadcrumb a{color:#94a3b8;text-decoration:none}
    .breadcrumb a:hover{color:#fff}
    .article-cat{display:inline-block;font-size:.65rem;font-weight:700;letter-spacing:.07em;text-transform:uppercase;background:#c8102e;color:#fff;padding:.22rem .65rem;border-radius:100px;margin-bottom:.75rem}
    .article-hero h1{font-family:var(--fd,'Oswald',sans-serif);font-size:clamp(1.8rem,4.5vw,2.8rem);font-weight:700;text-transform:uppercase;margin:0 0 1rem;line-height:1.1;color:#fff}
    /* Req 4: author/date meta — displayed neatly with avatar-style author chip */
    .article-meta{display:flex;align-items:center;flex-wrap:wrap;gap:.65rem;margin-top:.25rem}
    .article-meta-date{font-size:.82rem;color:#94a3b8;display:flex;align-items:center;gap:.35rem}
    .article-meta-date svg{opacity:.6}
    .article-meta-author{display:inline-flex;align-items:center;gap:.4rem;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.12);border-radius:100px;padding:.2rem .65rem .2rem .2rem;font-size:.78rem;color:#cbd5e1}
    .article-meta-author-avatar{width:22px;height:22px;border-radius:50%;background:#c8102e;display:flex;align-items:center;justify-content:center;font-size:.6rem;font-weight:700;color:#fff;flex-shrink:0}
    .article-meta-sep{color:#475569;font-size:.75rem}
    /* Req 2: hero image */
    .article-hero-image-wrap{max-width:1160px;margin:-1px auto 0;padding:0 1.5rem}
    .article-hero-image-wrap img{width:100%;max-height:480px;object-fit:cover;border-radius:0 0 16px 16px;display:block;box-shadow:0 8px 32px rgba(0,0,0,.18)}
    .article-layout{max-width:1160px;margin:0 auto;padding:2.5rem 1.5rem;display:grid;grid-template-columns:1fr 300px;gap:2.5rem;align-items:start}
    @media(max-width:900px){.article-layout{grid-template-columns:1fr}}
    /* Req 3: improved typography */
    .article-body{color:#1e293b;line-height:1.85;font-size:1.05rem}
    .article-body>*+*{margin-top:0}
    .article-body h2{font-family:var(--fd,'Oswald',sans-serif);font-size:1.4rem;font-weight:700;text-transform:uppercase;color:var(--navy,#0a1628);margin:2.5rem 0 .85rem;padding-bottom:.45rem;border-bottom:2px solid #c8102e;line-height:1.2}
    .article-body h3{font-size:1.1rem;font-weight:700;color:var(--navy,#0a1628);margin:2rem 0 .6rem;line-height:1.3}
    .article-body h4{font-size:1rem;font-weight:600;color:#334155;margin:1.5rem 0 .5rem}
    .article-body p{margin:0 0 1.4rem;line-height:1.85}
    .article-body p:last-child{margin-bottom:0}
    .article-body ul,.article-body ol{margin:0 0 1.4rem;padding-left:1.6rem}
    .article-body ul{list-style:none;padding-left:0}
    .article-body ul li{padding-left:1.4rem;position:relative;margin-bottom:.55rem}
    .article-body ul li::before{content:"";position:absolute;left:0;top:.65em;width:6px;height:6px;border-radius:50%;background:#c8102e;flex-shrink:0}
    .article-body ol li{margin-bottom:.55rem;padding-left:.25rem}
    .article-body ol li::marker{color:#c8102e;font-weight:700}
    .article-body li p{margin-bottom:.4rem}
    .article-body strong{color:var(--navy,#0a1628);font-weight:700}
    .article-body em{color:#475569}
    .article-body a{color:#c8102e;text-decoration:underline;text-underline-offset:2px}
    .article-body a:hover{color:#a00d25}
    .article-body blockquote{border-left:4px solid #c8102e;margin:2rem 0;padding:1rem 1.5rem;background:linear-gradient(135deg,#fafafa 0%,#f1f5f9 100%);border-radius:0 8px 8px 0;color:#475569;font-style:italic;font-size:1.05rem}
    .article-body blockquote p{margin:0}
    .article-body code{background:#f1f5f9;padding:.15rem .45rem;border-radius:4px;font-family:'Courier New',Courier,monospace;font-size:.86em;color:#c8102e;border:1px solid #e2e8f0}
    .article-body pre{background:#0f172a;color:#e2e8f0;padding:1.25rem 1.5rem;border-radius:10px;overflow-x:auto;margin:0 0 1.5rem;font-size:.88rem;line-height:1.65}
    .article-body pre code{background:none;border:none;color:inherit;font-size:inherit;padding:0}
    .article-body hr{border:none;border-top:2px solid #e2e8f0;margin:2.5rem 0}
    .article-body img{max-width:100%;border-radius:10px;margin:1.5rem 0;box-shadow:0 4px 16px rgba(0,0,0,.1)}
    .article-body table{width:100%;border-collapse:collapse;margin:0 0 1.5rem;font-size:.92rem}
    .article-body th{background:var(--navy,#0a1628);color:#fff;padding:.6rem .9rem;text-align:left;font-weight:600}
    .article-body td{padding:.55rem .9rem;border-bottom:1px solid #e2e8f0}
    .article-body tr:nth-child(even) td{background:#f8fafc}
    .article-sidebar{position:sticky;top:1.5rem;display:flex;flex-direction:column;gap:1.25rem}
    .sidebar-card{background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:1.35rem}
    .sidebar-card h3{font-family:var(--fd,'Oswald',sans-serif);font-size:1rem;font-weight:700;text-transform:uppercase;color:var(--navy,#0a1628);margin:0 0 .5rem}
    .sidebar-card p{font-size:.85rem;color:#64748b;line-height:1.55;margin:0 0 1rem}
    .sidebar-cta{display:inline-block;padding:.6rem 1.1rem;background:#c8102e;color:#fff;border-radius:8px;font-size:.85rem;font-weight:600;text-decoration:none;transition:background .15s}
    .sidebar-cta:hover{background:#a00d25}
    .back-link{display:inline-flex;align-items:center;gap:.35rem;color:#c8102e;font-size:.85rem;font-weight:600;text-decoration:none;margin-bottom:2rem}
    .back-link:hover{text-decoration:underline}
    .back-link svg{flex-shrink:0}
    /* ── Table of Contents ───────────────────────────────────────────────── */
    .toc-card{background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:1.35rem;position:sticky;top:1.5rem}
    .toc-card-title{font-family:var(--fd,'Oswald',sans-serif);font-size:.95rem;font-weight:700;text-transform:uppercase;color:var(--navy,#0a1628);margin:0 0 .85rem;display:flex;align-items:center;gap:.4rem}
    .toc-list{list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:.1rem}
    .toc-list li a{display:block;font-size:.82rem;color:#475569;text-decoration:none;padding:.32rem .5rem;border-radius:5px;border-left:2px solid transparent;transition:all .15s;line-height:1.35}
    .toc-list li a:hover{color:#c8102e;background:#fef2f2;border-left-color:#c8102e}
    .toc-list li a.toc-active{color:#c8102e;background:#fef2f2;border-left-color:#c8102e;font-weight:600}
    /* ── E-E-A-T trust bar ───────────────────────────────────────────────── */
    .eeat-bar{display:flex;flex-wrap:wrap;gap:.5rem;margin:1.25rem 0 0;padding-top:1.25rem;border-top:1px solid rgba(255,255,255,.1)}
    .eeat-badge{display:inline-flex;align-items:center;gap:.35rem;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.12);border-radius:100px;padding:.25rem .75rem;font-size:.72rem;color:#cbd5e1;font-weight:500}
    .eeat-badge svg{opacity:.7;flex-shrink:0}
    /* ── Author bio box ──────────────────────────────────────────────────── */
    .author-bio{background:linear-gradient(135deg,#f8fafc 0%,#f1f5f9 100%);border:1px solid #e2e8f0;border-radius:14px;padding:1.5rem;margin:2.5rem 0;display:flex;gap:1.25rem;align-items:flex-start}
    .author-bio-avatar{width:56px;height:56px;border-radius:50%;background:var(--navy,#0a1628);display:flex;align-items:center;justify-content:center;font-size:1.3rem;font-weight:700;color:#fff;flex-shrink:0;border:3px solid #c8102e}
    .author-bio-content{flex:1}
    .author-bio-name{font-family:var(--fd,'Oswald',sans-serif);font-size:1rem;font-weight:700;text-transform:uppercase;color:var(--navy,#0a1628);margin:0 0 .2rem}
    .author-bio-role{font-size:.75rem;color:#c8102e;font-weight:600;letter-spacing:.04em;text-transform:uppercase;margin:0 0 .5rem}
    .author-bio-text{font-size:.85rem;color:#475569;line-height:1.6;margin:0}
    /* ── Inline article images ───────────────────────────────────────────── */
    .article-inline-img{margin:2rem 0;border-radius:12px;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,.1)}
    .article-inline-img img{width:100%;height:auto;display:block;max-height:400px;object-fit:cover}
    .article-inline-img figcaption{background:#f8fafc;padding:.55rem 1rem;font-size:.78rem;color:#64748b;font-style:italic;border-top:1px solid #e2e8f0}
    /* ── Social share ────────────────────────────────────────────────────── */
    .share-section{margin:2.5rem 0 0;padding:1.5rem;background:var(--navy,#0a1628);border-radius:14px;display:flex;align-items:center;flex-wrap:wrap;gap:1rem}
    .share-label{font-family:var(--fd,'Oswald',sans-serif);font-size:.9rem;font-weight:700;text-transform:uppercase;color:#fff;margin:0;flex-shrink:0}
    .share-buttons{display:flex;gap:.5rem;flex-wrap:wrap}
    .share-btn{display:inline-flex;align-items:center;gap:.45rem;padding:.45rem 1rem;border-radius:8px;font-size:.8rem;font-weight:600;text-decoration:none;transition:opacity .15s,transform .1s;white-space:nowrap}
    .share-btn:hover{opacity:.88;transform:translateY(-1px)}
    .share-btn-x{background:#000;color:#fff}
    .share-btn-fb{background:#1877f2;color:#fff}
    .share-btn-wa{background:#25d366;color:#fff}
    .share-btn-li{background:#0a66c2;color:#fff}
    .share-btn-copy{background:rgba(255,255,255,.12);color:#fff;border:1px solid rgba(255,255,255,.2);cursor:pointer;font-family:inherit}
    .share-btn-copy.copied{background:#16a34a}
  </style>
</head>
<body>
${siteHeader()}
<main>${bodyContent}</main>
${siteFooter()}
<div id="cookie-banner">
  <div class="con cookie-inner">
    <p>We use cookies to give you the best experience. <a href="/cookie-policy.html">Cookie Policy</a></p>
    <div class="cookie-btns">
      <button id="cookie-reject" class="btn btn-outline-wh btn-sm">Reject</button>
      <button id="cookie-accept" class="btn btn-red btn-sm">Accept All</button>
    </div>
  </div>
</div>
<script src="/js/main.js"></script>
<script src="/js/fixes.js"></script>
<script>
// TOC active section highlight on scroll
(function(){
  var links = document.querySelectorAll('.toc-list a');
  if(!links.length) return;
  var sections = Array.from(links).map(function(a){
    return document.getElementById(a.getAttribute('href').slice(1));
  }).filter(Boolean);
  function onScroll(){
    var scrollY = window.scrollY + 120;
    var active = sections[0];
    sections.forEach(function(s){ if(s.offsetTop <= scrollY) active = s; });
    links.forEach(function(a){
      a.classList.toggle('toc-active', a.getAttribute('href') === '#' + (active && active.id));
    });
  }
  window.addEventListener('scroll', onScroll, {passive:true});
  onScroll();
})();
// Smooth scroll for TOC links
document.querySelectorAll('.toc-list a').forEach(function(a){
  a.addEventListener('click', function(e){
    var target = document.getElementById(this.getAttribute('href').slice(1));
    if(target){ e.preventDefault(); target.scrollIntoView({behavior:'smooth', block:'start'}); }
  });
});
</script>
</body>
</html>`;
}

// ─── Extract H2 headings for Table of Contents ───────────────────────────────
function extractToc(html) {
  const toc = [];
  const re = /<h2[^>]*>(.*?)<\/h2>/gi;
  let m;
  let i = 0;
  while ((m = re.exec(html)) !== null) {
    const text = m[1].replace(/<[^>]+>/g, "").trim();
    const id   = "section-" + (++i);
    toc.push({ id, text });
  }
  return toc;
}

// ─── Inject IDs into H2s and insert inline images at section breaks ───────────
// Uses Unsplash rugby-themed source images (no API key needed, served via CDN)
const RUGBY_IMAGES = [
  { src: "https://images.unsplash.com/photo-1544279428-a5c58e35fa17?w=800&q=80", alt: "Rugby players in action" },
  { src: "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=800&q=80", alt: "Rugby match at a UK club ground" },
  { src: "https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=800&q=80", alt: "Rugby team training session" },
  { src: "https://images.unsplash.com/photo-1560272564-c83b66b1ad12?w=800&q=80", alt: "Rugby scrum at grassroots level" },
  { src: "https://images.unsplash.com/photo-1566577739112-5180d4bf9390?w=800&q=80", alt: "Rugby players celebrating" },
];

function enrichArticleHtml(html, slug) {
  let sectionCount = 0;
  let imageIndex   = 0;
  // Deterministic image picks per article so they don't change on rebuild
  const offset = slug.length % RUGBY_IMAGES.length;

  // Add IDs to h2s and inject an image after the 2nd and 4th h2
  html = html.replace(/<h2([^>]*)>(.*?)<\/h2>/gi, (match, attrs, text) => {
    sectionCount++;
    const id = `section-${sectionCount}`;
    let result = `<h2${attrs} id="${id}">${text}</h2>`;
    // Inject image after 2nd and 4th section headings (giving 2 inline images minimum)
    if (sectionCount === 2 || sectionCount === 4 || sectionCount === 6) {
      const img = RUGBY_IMAGES[(offset + imageIndex) % RUGBY_IMAGES.length];
      imageIndex++;
      result += `\n<figure class="article-inline-img">
  <img src="${img.src}" alt="${img.alt}" loading="lazy" width="800" height="450">
  <figcaption>${img.alt}</figcaption>
</figure>`;
    }
    return result;
  });
  return html;
}

// ─── Blog index page ──────────────────────────────────────────────────────────
function buildIndexPage(articles) {
  const cards = articles.length === 0
    ? `<div class="blog-empty"><h3>Coming Soon</h3><p>Rugby guides, club tips and county breakdowns are on the way.</p></div>`
    : articles.map(a => `
      <a href="/blog/${a.slug}/" class="blog-card">
        <div class="blog-card-img">
          <svg viewBox="0 0 200 40" xmlns="http://www.w3.org/2000/svg" height="36" role="img" aria-label="UK Rugby Club Directory" style="opacity:.35">
            <text x="0" y="26" font-family="Arial,Helvetica,sans-serif" font-size="10" font-weight="700" fill="#c8102e" letter-spacing="2.5">UK</text>
            <rect x="29" y="5" width="2" height="30" rx="1" fill="white"/>
            <text x="39" y="21" font-family="Arial,Helvetica,sans-serif" font-size="14" font-weight="700" fill="white" letter-spacing="-0.3">Rugby Club</text>
            <text x="39" y="33" font-family="Arial,Helvetica,sans-serif" font-size="8" fill="rgba(255,255,255,0.6)" letter-spacing="3">DIRECTORY</text>
          </svg>
          ${a.category ? `<span class="blog-card-cat">${a.category}</span>` : ""}
        </div>
        <div class="blog-card-body">
          <span class="blog-card-date">${fmtDate(a.date)}</span>
          <h2 class="blog-card-title">${a.title}</h2>
          <p class="blog-card-excerpt">${a.excerpt || ""}</p>
          <span class="blog-card-cta">Read article <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg></span>
        </div>
      </a>`).join("\n");

  const bodyContent = `
    <div class="blog-hero">
      <p class="blog-eyebrow">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
        Rugby Knowledge Hub
      </p>
      <h1>Blog</h1>
      <p class="blog-hero-meta">${articles.length} article${articles.length !== 1 ? "s" : ""} &nbsp;&bull;&nbsp; Club guides, tips &amp; rugby news</p>
    </div>
    <div class="blog-section">
      <div class="blog-section-hd">
        <p class="blog-section-eyebrow">Latest Articles</p>
        <h2 class="blog-section-title">Rugby Guides &amp; Insights</h2>
        <p class="blog-section-sub">Club guides, beginner tips, county breakdowns and the latest from grassroots rugby across the UK.</p>
      </div>
      <div class="blog-grid">${cards}</div>
    </div>`;

  return shell({
    title:       "Rugby Blog — Guides, Tips & Club Advice",
    description: "Rugby tips, club guides, county breakdowns and grassroots rugby news from the UK Rugby Club Directory team. Find your local club today.",
    canonical:   "https://ukrugbyclubdirectory.co.uk/blog",
    ogType:      "website",
    bodyContent,
  });
}

// ─── Article page ─────────────────────────────────────────────────────────────
function buildArticlePage(slug, fm, bodyHtml) {
  // Hero image from frontmatter
  const heroImg = fm.heroimage || fm.heroImage || fm.image || "";
  const heroImageHtml = heroImg
    ? `<div class="article-hero-image-wrap">
        <img src="${heroImg}" alt="${fm.title || slug}" loading="lazy">
      </div>`
    : "";

  // Author initial for avatar
  const authorName    = fm.author || "UK Rugby Club Directory";
  const authorInitial = authorName.trim().charAt(0).toUpperCase();

  // Inject IDs into h2s and insert inline images at section breaks
  const enrichedHtml = enrichArticleHtml(bodyHtml, slug);

  // Build Table of Contents from h2s
  const toc = extractToc(enrichedHtml);
  const tocHtml = toc.length >= 2
    ? `<div class="toc-card">
        <p class="toc-card-title">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>
          In this article
        </p>
        <ul class="toc-list">
          ${toc.map(t => `<li><a href="#${t.id}">${t.text}</a></li>`).join("\n          ")}
        </ul>
      </div>`
    : "";

  // Canonical URL for share buttons
  const pageUrl = `https://ukrugbyclubdirectory.co.uk/blog/${slug}/`;
  const shareTitle = encodeURIComponent(fm.title || slug);
  const shareUrl   = encodeURIComponent(pageUrl);

  // Social share buttons
  const shareHtml = `
    <div class="share-section">
      <p class="share-label">Share this article</p>
      <div class="share-buttons">
        <a class="share-btn share-btn-x"
           href="https://twitter.com/intent/tweet?text=${shareTitle}&url=${shareUrl}"
           target="_blank" rel="noopener" aria-label="Share on X">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-4.714-6.231-5.401 6.231H2.744l7.736-8.856L1.999 2.25H8.08l4.258 5.63 5.906-5.63zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
          X / Twitter
        </a>
        <a class="share-btn share-btn-fb"
           href="https://www.facebook.com/sharer/sharer.php?u=${shareUrl}"
           target="_blank" rel="noopener" aria-label="Share on Facebook">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M18 2h-3a5 5 0 00-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 011-1h3z"/></svg>
          Facebook
        </a>
        <a class="share-btn share-btn-wa"
           href="https://wa.me/?text=${shareTitle}%20${shareUrl}"
           target="_blank" rel="noopener" aria-label="Share on WhatsApp">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.124.558 4.121 1.532 5.857L.054 23.35l5.637-1.479A11.953 11.953 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 21.882a9.876 9.876 0 01-5.031-1.378l-.361-.214-3.741.981.998-3.648-.235-.374A9.861 9.861 0 012.118 12C2.118 6.963 6.963 2.118 12 2.118S21.882 6.963 21.882 12 17.037 21.882 12 21.882z"/></svg>
          WhatsApp
        </a>
        <a class="share-btn share-btn-li"
           href="https://www.linkedin.com/shareArticle?mini=true&url=${shareUrl}&title=${shareTitle}"
           target="_blank" rel="noopener" aria-label="Share on LinkedIn">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M16 8a6 6 0 016 6v7h-4v-7a2 2 0 00-2-2 2 2 0 00-2 2v7h-4v-7a6 6 0 016-6zM2 9h4v12H2z"/><circle cx="4" cy="4" r="2"/></svg>
          LinkedIn
        </a>
        <button class="share-btn share-btn-copy" onclick="
          navigator.clipboard.writeText('${pageUrl}').then(()=>{
            this.textContent='✓ Copied!';
            this.classList.add('copied');
            setTimeout(()=>{this.innerHTML='<svg width=\\'14\\' height=\\'14\\' viewBox=\\'0 0 24 24\\' fill=\\'none\\' stroke=\\'currentColor\\' stroke-width=\\'2\\'><rect x=\\'9\\' y=\\'9\\' width=\\'13\\' height=\\'13\\' rx=\\'2\\'/><path d=\\'M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1\\'/></svg> Copy link';this.classList.remove('copied')},2000)
          })" aria-label="Copy link">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/></svg>
          Copy link
        </button>
      </div>
    </div>`;

  // Author bio box (E-E-A-T: Experience + Authoritativeness)
  const authorBioHtml = `
    <div class="author-bio">
      <div class="author-bio-avatar">${authorInitial}</div>
      <div class="author-bio-content">
        <p class="author-bio-name">${authorName}</p>
        <p class="author-bio-role">Rugby Content Team · UK Rugby Club Directory</p>
        <p class="author-bio-text">Our editorial team combines years of grassroots rugby experience with in-depth knowledge of clubs across England, Scotland, Wales and Northern Ireland. Every article is written to help players, coaches and supporters get the most from the game.</p>
      </div>
    </div>`;

  // E-E-A-T trust badge bar (Experience, Expertise, Authoritativeness, Trustworthiness)
  const eeatHtml = `
    <div class="eeat-bar">
      <span class="eeat-badge">
        <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
        Expert-reviewed
      </span>
      <span class="eeat-badge">
        <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
        ${fm.date ? `Updated ${fmtDate(fm.date)}` : "Regularly updated"}
      </span>
      <span class="eeat-badge">
        <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
        Trusted rugby resource
      </span>
      <span class="eeat-badge">
        <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75"/></svg>
        620+ clubs verified
      </span>
    </div>`;

  const bodyContent = `
    <div class="article-hero">
      <div class="article-hero-inner">
        <nav class="breadcrumb" aria-label="Breadcrumb">
          <a href="/index.html">Home</a> &rsaquo;
          <a href="/blog">Blog</a> &rsaquo;
          ${fm.title || slug}
        </nav>
        ${fm.category ? `<span class="article-cat">${fm.category}</span>` : ""}
        <h1>${fm.title || slug}</h1>
        <div class="article-meta">
          ${fm.date ? `<span class="article-meta-date">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>
            <time datetime="${fm.date}">${fmtDate(fm.date)}</time>
          </span>` : ""}
          ${fm.date && fm.author ? `<span class="article-meta-sep">&bull;</span>` : ""}
          ${fm.author ? `<span class="article-meta-author">
            <span class="article-meta-author-avatar">${authorInitial}</span>
            ${authorName}
          </span>` : ""}
        </div>
        ${eeatHtml}
      </div>
    </div>
    ${heroImageHtml}
    <div class="article-layout">
      <div>
        <a href="/blog" class="back-link">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
          Back to Blog
        </a>
        <article class="article-body">${enrichedHtml}</article>
        ${authorBioHtml}
        ${shareHtml}
      </div>
      <aside class="article-sidebar">
        ${tocHtml}
        <div class="sidebar-card">
          <h3>Find a Rugby Club</h3>
          <p>Search 620+ clubs across England, Scotland, Wales and Northern Ireland.</p>
          <a class="sidebar-cta" href="/rugby-union.html">Browse clubs &rarr;</a>
        </div>
        <div class="sidebar-card">
          <h3>Register Your Club</h3>
          <p>Get your club listed in the UK's most comprehensive rugby directory — free.</p>
          <a class="sidebar-cta" href="/register.html">Register free &rarr;</a>
        </div>
      </aside>
    </div>`;

  return shell({
    title:       fm.title || slug,
    description: fm.metadescription || fm.excerpt || `Read about ${fm.title || slug} on UK Rugby Club Directory.`,
    canonical:   pageUrl,
    ogType:      "article",
    bodyContent,
  });
}

// ─── Plugin entry point ───────────────────────────────────────────────────────
module.exports = {
  onPostBuild: async ({ constants, utils }) => {
    const { PUBLISH_DIR } = constants;
    const contentDir = path.join(process.cwd(), "content", "blog");
    const outDir     = path.join(PUBLISH_DIR, "blog");

    console.log("📝 generate-blog: reading markdown from", contentDir);

    if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

    let mdFiles = [];
    try {
      mdFiles = fs.readdirSync(contentDir)
        .filter(f => f.endsWith(".md") && f !== "BLOG_README.md");
    } catch (e) {
      utils.build.failBuild(`Could not read ${contentDir}: ${e.message}`);
      return;
    }

    const articles = [];

    for (const file of mdFiles) {
      const slug = file.replace(/\.md$/, "");
      const raw  = fs.readFileSync(path.join(contentDir, file), "utf8");
      const { fm, body } = parseFrontmatter(raw);

      if (!fm.title) {
        console.warn(`  ⚠ Skipping ${file} — no title in frontmatter`);
        continue;
      }

      const bodyHtml    = mdToHtml(body);
      const articleHtml = buildArticlePage(slug, fm, bodyHtml);

      const articleDir = path.join(outDir, slug);
      if (!fs.existsSync(articleDir)) fs.mkdirSync(articleDir, { recursive: true });
      fs.writeFileSync(path.join(articleDir, "index.html"), articleHtml, "utf8");

      articles.push({
        slug,
        title:    fm.title,
        date:     fm.date     || "",
        category: fm.category || "",
        excerpt:  fm.excerpt  || fm.metadescription || "",
      });

      console.log(`  ✓ /blog/${slug}/`);
    }

    // Newest first
    articles.sort((a, b) => b.date.localeCompare(a.date));

    fs.writeFileSync(path.join(outDir, "index.html"), buildIndexPage(articles), "utf8");
    console.log(`📝 generate-blog: done — ${articles.length} article(s) + index written to ${outDir}`);
  },
};
