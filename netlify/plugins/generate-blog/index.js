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
    .article-hero h1{font-family:var(--fd,'Oswald',sans-serif);font-size:clamp(1.6rem,4vw,2.4rem);font-weight:700;text-transform:uppercase;margin:0 0 .75rem;line-height:1.15;color:#fff}
    .article-meta{font-size:.82rem;color:#94a3b8}
    .article-layout{max-width:1160px;margin:0 auto;padding:2.5rem 1.5rem;display:grid;grid-template-columns:1fr 300px;gap:2.5rem;align-items:start}
    @media(max-width:900px){.article-layout{grid-template-columns:1fr}}
    .article-body{color:#1e293b;line-height:1.78;font-size:1rem}
    .article-body h2{font-family:var(--fd,'Oswald',sans-serif);font-size:1.3rem;font-weight:700;text-transform:uppercase;color:var(--navy,#0a1628);margin:2.25rem 0 .75rem;padding-bottom:.4rem;border-bottom:2px solid #c8102e}
    .article-body h3{font-size:1.05rem;font-weight:600;color:var(--navy,#0a1628);margin:1.75rem 0 .5rem}
    .article-body p{margin:0 0 1.25rem}
    .article-body ul,.article-body ol{margin:0 0 1.25rem;padding-left:1.5rem}
    .article-body li{margin-bottom:.4rem}
    .article-body strong{color:var(--navy,#0a1628)}
    .article-body a{color:#c8102e;text-decoration:underline}
    .article-body blockquote{border-left:4px solid #c8102e;margin:1.5rem 0;padding:.75rem 1.25rem;background:#f8fafc;color:#475569;font-style:italic}
    .article-body code{background:#f1f5f9;padding:.15rem .4rem;border-radius:4px;font-family:monospace;font-size:.88em}
    .article-sidebar{position:sticky;top:1.5rem;display:flex;flex-direction:column;gap:1.25rem}
    .sidebar-card{background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:1.35rem}
    .sidebar-card h3{font-family:var(--fd,'Oswald',sans-serif);font-size:1rem;font-weight:700;text-transform:uppercase;color:var(--navy,#0a1628);margin:0 0 .5rem}
    .sidebar-card p{font-size:.85rem;color:#64748b;line-height:1.55;margin:0 0 1rem}
    .sidebar-cta{display:inline-block;padding:.6rem 1.1rem;background:#c8102e;color:#fff;border-radius:8px;font-size:.85rem;font-weight:600;text-decoration:none;transition:background .15s}
    .sidebar-cta:hover{background:#a00d25}
    .back-link{display:inline-flex;align-items:center;gap:.35rem;color:#c8102e;font-size:.85rem;font-weight:600;text-decoration:none;margin-bottom:2rem}
    .back-link:hover{text-decoration:underline}
    .back-link svg{flex-shrink:0}
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
</body>
</html>`;
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
        <p class="article-meta">
          ${fm.date ? `<time datetime="${fm.date}">${fmtDate(fm.date)}</time>` : ""}
          ${fm.author ? ` &bull; ${fm.author}` : ""}
        </p>
      </div>
    </div>
    <div class="article-layout">
      <div>
        <a href="/blog" class="back-link">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
          Back to Blog
        </a>
        <article class="article-body">${bodyHtml}</article>
      </div>
      <aside class="article-sidebar">
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
    canonical:   `https://ukrugbyclubdirectory.co.uk/blog/${slug}/`,
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
