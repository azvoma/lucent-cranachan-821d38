// ============================================================
//  UK Rugby Club Directory — Blog Edge Function
//  Handles:  /blog            → article index
//            /blog/           → article index
//            /blog/{slug}     → individual article
// ============================================================

export default async function handler(request, context) {
  const url = new URL(request.url);
  const path = url.pathname.replace(/\/$/, "") || "/blog";

  // ── Route: index ──────────────────────────────────────────
  if (path === "/blog") {
    return renderIndex(request, context);
  }

  // ── Route: individual article ─────────────────────────────
  const match = path.match(/^\/blog\/([a-z0-9-]+)$/);
  if (match) {
    return renderArticle(match[1], request, context);
  }

  // ── Fallthrough ───────────────────────────────────────────
  return new Response(null, { status: 404 });
}

// ── Fetch & parse a .md file ──────────────────────────────────
async function fetchMarkdown(slug, context) {
  const mdUrl = new URL(`/content/blog/${slug}.md`, "http://localhost");
  try {
    const res = await context.next(new Request(mdUrl.toString()));
    if (!res.ok) return null;
    return await res.text();
  } catch {
    return null;
  }
}

// ── Parse frontmatter ─────────────────────────────────────────
function parseFrontmatter(raw) {
  const fm = {};
  const match = raw.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$/);
  if (!match) return { meta: fm, body: raw };
  const lines = match[1].split("\n");
  for (const line of lines) {
    const colon = line.indexOf(":");
    if (colon === -1) continue;
    const key = line.slice(0, colon).trim();
    const val = line.slice(colon + 1).trim();
    fm[key] = val;
  }
  return { meta: fm, body: match[2] };
}

// ── Markdown → HTML (no external deps) ───────────────────────
function mdToHtml(md) {
  let html = md
    // Headings
    .replace(/^###### (.+)$/gm, "<h6>$1</h6>")
    .replace(/^##### (.+)$/gm, "<h5>$1</h5>")
    .replace(/^#### (.+)$/gm, "<h4>$1</h4>")
    .replace(/^### (.+)$/gm, "<h3>$1</h3>")
    .replace(/^## (.+)$/gm, "<h2>$1</h2>")
    .replace(/^# (.+)$/gm, "<h1>$1</h1>")
    // Bold & italic
    .replace(/\*\*\*(.+?)\*\*\*/g, "<strong><em>$1</em></strong>")
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(.+?)\*/g, "<em>$1</em>")
    // Inline code
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    // Horizontal rule
    .replace(/^---$/gm, "<hr>")
    // Blockquote
    .replace(/^> (.+)$/gm, "<blockquote><p>$1</p></blockquote>")
    // Links
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');

  // Unordered lists
  html = html.replace(/((?:^[*-] .+\n?)+)/gm, (block) => {
    const items = block.trim().split("\n").map(l =>
      `<li>${l.replace(/^[*-] /, "")}</li>`
    ).join("\n");
    return `<ul>\n${items}\n</ul>\n`;
  });

  // Ordered lists
  html = html.replace(/((?:^\d+\. .+\n?)+)/gm, (block) => {
    const items = block.trim().split("\n").map(l =>
      `<li>${l.replace(/^\d+\. /, "")}</li>`
    ).join("\n");
    return `<ol>\n${items}\n</ol>\n`;
  });

  // Paragraphs — wrap non-tagged lines
  const lines = html.split("\n");
  const out = [];
  let inBlock = false;
  const blockTags = /^<(h[1-6]|ul|ol|li|blockquote|hr|pre|code)/;
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed) { inBlock = false; out.push(""); continue; }
    if (blockTags.test(trimmed) || trimmed.startsWith("</")) {
      inBlock = false; out.push(trimmed); continue;
    }
    if (!inBlock) { out.push(`<p>${trimmed}`); inBlock = true; }
    else { out[out.length - 1] += " " + trimmed; }
  }
  // Close open paragraphs
  return out.map(l => (l.startsWith("<p>") && !l.endsWith("</p>") ? l + "</p>" : l)).join("\n");
}

// ── Format date ───────────────────────────────────────────────
function fmtDate(str) {
  if (!str) return "";
  try {
    return new Date(str).toLocaleDateString("en-GB", {
      day: "numeric", month: "long", year: "numeric"
    });
  } catch { return str; }
}

// ── Shared header/nav/footer HTML ─────────────────────────────
function siteChrome(title, metaDesc, canonical) {
  const LOGO_DARK = `<svg viewBox="0 0 220 48" xmlns="http://www.w3.org/2000/svg" height="48" role="img" aria-label="UK Rugby Club Directory" style="display:block">
        <title>UK Rugby Club Directory</title>
        <text x="0" y="31" font-family="Arial,Helvetica,sans-serif" font-size="12" font-weight="700" fill="#c8102e" letter-spacing="3">UK</text>
        <rect x="35" y="7" width="2.5" height="34" rx="1.25" fill="white"/>
        <text x="46" y="26" font-family="Arial,Helvetica,sans-serif" font-size="17" font-weight="700" fill="white" letter-spacing="-0.3">Rugby Club</text>
        <text x="46" y="40" font-family="Arial,Helvetica,sans-serif" font-size="9.5" fill="rgba(255,255,255,0.5)" letter-spacing="3.5">DIRECTORY</text>
      </svg>`;
  const LOGO_MOB = `<svg viewBox="0 0 220 48" xmlns="http://www.w3.org/2000/svg" height="40" role="img" aria-label="UK Rugby Club Directory" style="display:block">
        <title>UK Rugby Club Directory</title>
        <text x="0" y="31" font-family="Arial,Helvetica,sans-serif" font-size="12" font-weight="700" fill="#c8102e" letter-spacing="3">UK</text>
        <rect x="35" y="7" width="2.5" height="34" rx="1.25" fill="white"/>
        <text x="46" y="26" font-family="Arial,Helvetica,sans-serif" font-size="17" font-weight="700" fill="white" letter-spacing="-0.3">Rugby Club</text>
        <text x="46" y="40" font-family="Arial,Helvetica,sans-serif" font-size="9.5" fill="rgba(255,255,255,0.5)" letter-spacing="3.5">DIRECTORY</text>
      </svg>`;
  const LOGO_FT = `<svg viewBox="0 0 200 40" xmlns="http://www.w3.org/2000/svg" height="40" role="img" aria-label="UK Rugby Club Directory" style="display:block">
            <title>UK Rugby Club Directory</title>
            <text x="0" y="26" font-family="Arial,Helvetica,sans-serif" font-size="10" font-weight="700" fill="#c8102e" letter-spacing="2.5">UK</text>
            <rect x="29" y="5" width="2" height="30" rx="1" fill="white"/>
            <text x="39" y="21" font-family="Arial,Helvetica,sans-serif" font-size="14" font-weight="700" fill="white" letter-spacing="-0.3">Rugby Club</text>
            <text x="39" y="33" font-family="Arial,Helvetica,sans-serif" font-size="8" fill="rgba(255,255,255,0.45)" letter-spacing="3">DIRECTORY</text>
          </svg>`;

  return {
    head: `<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>${escHtml(title)} | UK Rugby Club Directory</title>
<meta name="description" content="${escHtml(metaDesc)}">
<meta name="robots" content="index,follow">
<link rel="canonical" href="https://ukrugbyclubdirectory.co.uk${canonical}">
<meta property="og:type" content="article">
<meta property="og:title" content="${escHtml(title)}">
<meta property="og:description" content="${escHtml(metaDesc)}">
<meta property="og:url" content="https://ukrugbyclubdirectory.co.uk${canonical}">
<meta property="og:site_name" content="UK Rugby Club Directory">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="${escHtml(title)}">
<meta name="twitter:description" content="${escHtml(metaDesc)}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;600;700&family=Source+Sans+3:ital,wght@0,300;0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/style.css">
<style>
/* ── Blog-specific styles ─────────────────────────────── */
.blog-hero{background:var(--navy);padding:3.5rem 0 4rem;position:relative;overflow:hidden}
.blog-hero::after{content:"";position:absolute;inset:0;background:linear-gradient(135deg,rgba(200,16,46,.06) 0%,transparent 60%);pointer-events:none}
.blog-hero-inner{position:relative;z-index:1}
.blog-breadcrumb{display:flex;align-items:center;gap:.4rem;font-size:.78rem;margin-bottom:1.5rem;flex-wrap:wrap}
.blog-breadcrumb a{color:rgba(255,255,255,.5);text-decoration:none;transition:color .15s}
.blog-breadcrumb a:hover{color:#fff}
.blog-breadcrumb .bc-sep{color:rgba(255,255,255,.2)}
.blog-breadcrumb .bc-cur{color:rgba(255,255,255,.8);font-weight:600}
.blog-hero-tag{display:inline-flex;align-items:center;gap:.35rem;font-size:.7rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--gold);margin-bottom:.9rem}
.blog-hero h1{font-size:clamp(1.9rem,4vw,3rem);font-weight:900;color:#fff;line-height:1.1;margin-bottom:1rem;text-transform:uppercase;letter-spacing:.3px}
.blog-hero-meta{display:flex;align-items:center;gap:1.25rem;flex-wrap:wrap}
.blog-meta-item{display:flex;align-items:center;gap:.4rem;font-size:.82rem;color:rgba(255,255,255,.6)}
.blog-meta-item svg{color:var(--gold);flex-shrink:0}

/* ── Article layout ────────────────────────────────────── */
.article-wrap{padding:4rem 0 5rem}
.article-layout{display:grid;grid-template-columns:1fr 300px;gap:4rem;align-items:flex-start}
.article-body{min-width:0}
.article-body h2{font-size:clamp(1.3rem,2.5vw,1.75rem);color:var(--navy);margin:2.25rem 0 .85rem;padding-bottom:.5rem;border-bottom:2px solid var(--gl)}
.article-body h3{font-size:clamp(1.1rem,2vw,1.35rem);color:var(--navy);margin:1.75rem 0 .7rem}
.article-body h4{font-size:1rem;color:var(--navy);margin:1.25rem 0 .5rem}
.article-body p{font-size:1.05rem;color:var(--gd);line-height:1.82;margin-bottom:1.2rem}
.article-body ul,.article-body ol{margin:0 0 1.25rem 1.5rem;display:flex;flex-direction:column;gap:.45rem}
.article-body li{font-size:1rem;color:var(--gd);line-height:1.7}
.article-body strong{color:var(--navy);font-weight:700}
.article-body em{font-style:italic}
.article-body code{background:var(--off);border:1px solid var(--gl);border-radius:4px;padding:.1rem .4rem;font-size:.88em;font-family:monospace;color:var(--red)}
.article-body blockquote{border-left:4px solid var(--red);padding:.75rem 1.25rem;margin:1.5rem 0;background:var(--off);border-radius:0 var(--rad) var(--rad) 0}
.article-body blockquote p{color:var(--navy);font-size:1.05rem;font-style:italic;margin:0}
.article-body hr{border:none;border-top:2px solid var(--gl);margin:2.5rem 0}
.article-body a{color:var(--red);text-decoration:underline;text-underline-offset:2px}
.article-body a:hover{color:var(--red-dk)}

/* ── Sidebar ───────────────────────────────────────────── */
.article-sidebar{position:sticky;top:90px;display:flex;flex-direction:column;gap:1.5rem}
.sidebar-card{background:#fff;border:1px solid var(--gl);border-radius:12px;padding:1.5rem;box-shadow:var(--sh1)}
.sidebar-card h3{font-family:var(--fd);font-size:.65rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--grey);margin-bottom:1rem;padding-bottom:.75rem;border-bottom:1px solid var(--gl)}
.sidebar-cta{background:var(--navy);border-color:var(--navy);text-align:center}
.sidebar-cta h3{color:rgba(255,255,255,.45)}
.sidebar-cta p{font-size:.875rem;color:rgba(255,255,255,.65);line-height:1.6;margin-bottom:1.25rem}
.sidebar-related-link{display:flex;flex-direction:column;gap:.2rem;padding:.65rem 0;border-bottom:1px solid var(--gl);text-decoration:none;transition:color .15s}
.sidebar-related-link:last-child{border-bottom:none;padding-bottom:0}
.sidebar-related-link:hover .srl-title{color:var(--red)}
.srl-title{font-size:.875rem;font-weight:600;color:var(--navy);line-height:1.35;transition:color .15s}
.srl-date{font-size:.72rem;color:var(--grey)}

/* ── Blog index grid ───────────────────────────────────── */
.blog-index-wrap{padding:4rem 0 5rem}
.blog-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1.75rem;margin-top:2.5rem}
.blog-card{background:#fff;border:1px solid var(--gl);border-radius:var(--rad);overflow:hidden;box-shadow:var(--sh1);transition:box-shadow .25s,transform .25s;display:flex;flex-direction:column;text-decoration:none;color:inherit}
.blog-card:hover{box-shadow:var(--sh3);transform:translateY(-4px)}
.blog-card-img{height:190px;background:linear-gradient(135deg,var(--navy) 0%,#1e3050 100%);position:relative;overflow:hidden;flex-shrink:0}
.blog-card-img img{width:100%;height:100%;object-fit:cover;display:block;opacity:.75;transition:opacity .3s,transform .4s}
.blog-card:hover .blog-card-img img{opacity:.9;transform:scale(1.04)}
.blog-card-img-placeholder{width:100%;height:100%;display:flex;align-items:center;justify-content:center}
.blog-card-img-placeholder svg{opacity:.25}
.blog-card-cat{position:absolute;top:.85rem;left:.85rem;font-size:.65rem;font-weight:700;letter-spacing:.07em;text-transform:uppercase;background:var(--red);color:#fff;padding:.22rem .65rem;border-radius:100px}
.blog-card-body{padding:1.35rem;display:flex;flex-direction:column;gap:.6rem;flex:1}
.blog-card-date{font-size:.73rem;color:var(--grey);font-weight:500}
.blog-card-title{font-family:var(--fd);font-size:1.05rem;font-weight:700;text-transform:uppercase;letter-spacing:.3px;color:var(--navy);line-height:1.25;margin:0}
.blog-card:hover .blog-card-title{color:var(--red)}
.blog-card-excerpt{font-size:.86rem;color:var(--gd);line-height:1.6;margin:0;flex:1}
.blog-card-cta{margin-top:auto;padding-top:.75rem;border-top:1px solid var(--off);font-size:.78rem;font-weight:700;color:var(--red);display:flex;align-items:center;gap:.3rem;transition:gap .15s}
.blog-card:hover .blog-card-cta{gap:.55rem}

/* ── Responsive ────────────────────────────────────────── */
@media(max-width:1060px){
  .article-layout{grid-template-columns:1fr}
  .article-sidebar{position:static}
  .blog-grid{grid-template-columns:repeat(2,1fr)}
}
@media(max-width:640px){
  .blog-grid{grid-template-columns:1fr}
  .blog-card-img{height:160px}
  .article-wrap{padding:2.5rem 0 3.5rem}
}
</style>
</head>
<body>`,

    nav: `<header id="site-header">
  <div class="con hdr-inner">
    <a href="/index.html" class="logo" aria-label="UK Rugby Club Directory">
      ${LOGO_DARK}
    </a>
    <nav id="main-nav" aria-label="Main navigation">
      <a href="/index.html" class="nav-link">Home</a>
      <div class="nav-dropdown">
        <button class="nav-link nav-drop-btn" aria-expanded="false" aria-haspopup="true">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><ellipse cx="12" cy="12" rx="9.5" ry="6"/><line x1="2.5" y1="12" x2="21.5" y2="12"/></svg>
          Rugby Union
          <svg class="drop-caret" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M6 9l6 6 6-6"/></svg>
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
              <a href="/rugby-union.html?region=northern-ireland" class="dp-link">Northern Ireland</a>
            </div>
            <div class="dp-col">
              <span class="dp-heading">Popular Searches</span>
              <a href="/rugby-union.html?region=yorkshire" class="dp-link dp-tag">Rugby in Yorkshire</a>
              <a href="/rugby-union.html?region=london-se" class="dp-link dp-tag">Rugby in Surrey</a>
              <a href="/rugby-union.html?region=south-west" class="dp-link dp-tag">Rugby in the South West</a>
            </div>
          </div>
        </div>
      </div>
      <div class="nav-dropdown">
        <button class="nav-link nav-drop-btn" aria-expanded="false" aria-haspopup="true">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><ellipse cx="12" cy="12" rx="9.5" ry="6"/><line x1="2.5" y1="12" x2="21.5" y2="12"/></svg>
          Rugby League
          <svg class="drop-caret" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M6 9l6 6 6-6"/></svg>
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
      <a href="/register.html" class="nav-link nav-cta btn btn-red btn-sm">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg>
        Register Club
      </a>
    </nav>
    <button id="hamburger" aria-label="Open navigation menu" aria-expanded="false"><span></span><span></span><span></span></button>
  </div>
</header>
<nav id="mobile-nav" aria-hidden="true">
  <div class="mob-header">
    <a href="/index.html" class="mob-logo">
      ${LOGO_MOB}
    </a>
    <button id="mob-close" aria-label="Close menu">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M18 6L6 18M6 6l12 12"/></svg>
    </button>
  </div>
  <div class="mob-links">
    <a href="/index.html" class="mob-link">Home</a>
    <div class="mob-group">
      <button class="mob-group-btn" aria-expanded="false">Rugby Union <svg class="mob-caret" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M6 9l6 6 6-6"/></svg></button>
      <div class="mob-sub" hidden>
        <a href="/rugby-union.html" class="mob-sub-link">All Union Clubs</a>
        <a href="/rugby-union.html?region=london-se" class="mob-sub-link">London &amp; SE</a>
        <a href="/rugby-union.html?region=north-west" class="mob-sub-link">North West</a>
        <a href="/rugby-union.html?region=yorkshire" class="mob-sub-link">Yorkshire</a>
        <a href="/rugby-union.html?region=midlands" class="mob-sub-link">Midlands</a>
        <a href="/rugby-union.html?region=south-west" class="mob-sub-link">South West</a>
        <a href="/rugby-union.html?region=wales" class="mob-sub-link">Wales</a>
        <a href="/rugby-union.html?region=scotland" class="mob-sub-link">Scotland</a>
      </div>
    </div>
    <div class="mob-group">
      <button class="mob-group-btn" aria-expanded="false">Rugby League <svg class="mob-caret" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M6 9l6 6 6-6"/></svg></button>
      <div class="mob-sub" hidden>
        <a href="/rugby-league.html" class="mob-sub-link">All League Clubs</a>
        <a href="/rugby-league.html?region=yorkshire" class="mob-sub-link">Yorkshire</a>
        <a href="/rugby-league.html?region=north-west" class="mob-sub-link">North West</a>
      </div>
    </div>
    <a href="/rugby-joints.html" class="mob-link">Businesses</a>
    <a href="/blog" class="mob-link">Blog</a>
    <a href="/contact-us.html" class="mob-link">Contact</a>
    <div class="mob-divider"></div>
    <a href="/register.html" class="btn btn-red mob-cta">+ Register Your Club Free</a>
  </div>
</nav>`,

    footer: `<footer>
  <div class="ft-top">
    <div class="con ft-grid">
      <div class="ft-brand">
        <a href="/index.html" class="ft-logo">
          ${LOGO_FT}
        </a>
        <p class="ft-strapline">The UK's most comprehensive rugby club directory. Connecting clubs, players and fans across England, Scotland, Wales and Northern Ireland.</p>
        <div class="ft-socials">
          <a href="https://twitter.com" target="_blank" rel="noopener" class="ft-soc" aria-label="Twitter"><svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-4.714-6.231-5.401 6.231H2.744l7.736-8.856L1.999 2.25H8.08l4.258 5.63 5.906-5.63zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg></a>
          <a href="https://facebook.com" target="_blank" rel="noopener" class="ft-soc" aria-label="Facebook"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M18 2h-3a5 5 0 00-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 011-1h3z"/></svg></a>
          <a href="https://instagram.com" target="_blank" rel="noopener" class="ft-soc" aria-label="Instagram"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1.5" fill="currentColor" stroke="none"/></svg></a>
        </div>
      </div>
      <div class="ft-col">
        <h3>Directory</h3>
        <ul>
          <li><a href="/index.html">Home</a></li>
          <li><a href="/clubs.html">All Clubs</a></li>
          <li><a href="/rugby-union.html">Rugby Union</a></li>
          <li><a href="/rugby-league.html">Rugby League</a></li>
          <li><a href="/rugby-joints.html">Businesses</a></li>
        </ul>
      </div>
      <div class="ft-col">
        <h3>Regions</h3>
        <ul>
          <li><a href="/rugby-union.html?region=london-se">London &amp; South East</a></li>
          <li><a href="/rugby-union.html?region=yorkshire">Yorkshire</a></li>
          <li><a href="/rugby-union.html?region=midlands">Midlands</a></li>
          <li><a href="/rugby-union.html?region=north-west">North West</a></li>
          <li><a href="/rugby-union.html?region=wales">Wales</a></li>
          <li><a href="/rugby-union.html?region=scotland">Scotland</a></li>
        </ul>
      </div>
      <div class="ft-col">
        <h3>Content</h3>
        <ul>
          <li><a href="/blog">Blog</a></li>
          <li><a href="/register.html">Register Your Club</a></li>
          <li><a href="/contact-us.html">Contact Us</a></li>
          <li><a href="https://www.englandrugby.com" target="_blank" rel="noopener">England Rugby</a></li>
        </ul>
      </div>
      <div class="ft-col">
        <h3>Legal</h3>
        <ul>
          <li><a href="/privacy-policy.html">Privacy Policy</a></li>
          <li><a href="/terms-of-service.html">Terms of Service</a></li>
          <li><a href="/cookie-policy.html">Cookie Policy</a></li>
          <li><a href="/sitemap.xml">Sitemap</a></li>
        </ul>
      </div>
    </div>
  </div>
  <div class="ft-bottom">
    <div class="con ft-bottom-inner">
      <p>&copy; 2026 UK Rugby Club Directory. All rights reserved.</p>
      <div class="ft-bottom-links">
        <a href="/privacy-policy.html">Privacy</a><span>·</span>
        <a href="/terms-of-service.html">Terms</a><span>·</span>
        <a href="/cookie-policy.html">Cookies</a><span>·</span>
        <a href="/sitemap.xml">Sitemap</a>
      </div>
    </div>
  </div>
</footer>
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
</body></html>`
  };
}

// ── HTML escape ───────────────────────────────────────────────
function escHtml(s) {
  return String(s || "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

// ── Get all articles (for index + sidebar) ────────────────────
async function getAllArticles(context) {
  // We fetch the blog index JSON that is pre-built (see blog-index.json)
  // Fallback: scan known slugs if index not present
  try {
    const res = await context.next(new Request(new URL("/content/blog/index.json", "http://localhost").toString()));
    if (res.ok) {
      return await res.json();
    }
  } catch { /* fall through */ }
  return [];
}

// ── Render: individual article ────────────────────────────────
async function renderArticle(slug, request, context) {
  const raw = await fetchMarkdown(slug, context);
  if (!raw) {
    return new Response(null, { status: 404 });
  }

  const { meta, body } = parseFrontmatter(raw);
  const content = mdToHtml(body);
  const allArticles = await getAllArticles(context);
  const related = allArticles.filter(a => a.slug !== slug).slice(0, 3);

  const chrome = siteChrome(
    meta.title || "Blog Article",
    meta.metaDescription || meta.title || "",
    `/blog/${slug}`
  );

  const relatedHtml = related.length
    ? related.map(a => `
      <a href="/blog/${escHtml(a.slug)}" class="sidebar-related-link">
        <span class="srl-title">${escHtml(a.title)}</span>
        <span class="srl-date">${fmtDate(a.date)}</span>
      </a>`).join("")
    : `<p style="font-size:.85rem;color:var(--grey)">More articles coming soon.</p>`;

  const html = `${chrome.head}
${chrome.nav}
<main>
  <div class="blog-hero">
    <div class="con blog-hero-inner">
      <nav class="blog-breadcrumb" aria-label="Breadcrumb">
        <a href="/index.html">Home</a>
        <span class="bc-sep">›</span>
        <a href="/blog">Blog</a>
        <span class="bc-sep">›</span>
        <span class="bc-cur">${escHtml(meta.title || slug)}</span>
      </nav>
      ${meta.category ? `<div class="blog-hero-tag">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M20.59 13.41l-7.17 7.17a2 2 0 01-2.83 0L2 12V2h10l8.59 8.59a2 2 0 010 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/></svg>
        ${escHtml(meta.category)}
      </div>` : ""}
      <h1>${escHtml(meta.title || slug)}</h1>
      <div class="blog-hero-meta">
        ${meta.date ? `<span class="blog-meta-item">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
          ${fmtDate(meta.date)}
        </span>` : ""}
        ${meta.author ? `<span class="blog-meta-item">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
          ${escHtml(meta.author)}
        </span>` : ""}
      </div>
    </div>
  </div>

  <div class="article-wrap">
    <div class="con">
      <div class="article-layout">
        <article class="article-body">
          ${content}
        </article>
        <aside class="article-sidebar">
          <div class="sidebar-card sidebar-cta">
            <h3>Find a Club</h3>
            <p>Search over 620 rugby clubs across England, Scotland, Wales and Northern Ireland.</p>
            <a href="/clubs.html" class="btn btn-red" style="width:100%;justify-content:center">Browse All Clubs</a>
          </div>
          <div class="sidebar-card">
            <h3>More Articles</h3>
            ${relatedHtml}
          </div>
          <div class="sidebar-card">
            <h3>Register Your Club</h3>
            <p style="font-size:.875rem;color:var(--gd);margin-bottom:1rem;line-height:1.6">List your club free. Full profile page included.</p>
            <a href="/register.html" class="btn btn-navy btn-sm" style="width:100%;justify-content:center">Register Free</a>
          </div>
        </aside>
      </div>
    </div>
  </div>
</main>
${chrome.footer}`;

  return new Response(html, {
    headers: { "Content-Type": "text/html;charset=UTF-8" }
  });
}

// ── Render: blog index ────────────────────────────────────────
async function renderIndex(request, context) {
  const allArticles = await getAllArticles(context);

  const cardHtml = allArticles.length
    ? allArticles.map(a => `
      <a href="/blog/${escHtml(a.slug)}" class="blog-card">
        <div class="blog-card-img">
          ${a.image
            ? `<img src="${escHtml(a.image)}" alt="${escHtml(a.title)}" loading="lazy">`
            : `<div class="blog-card-img-placeholder"><svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="1.5"><ellipse cx="12" cy="12" rx="9.5" ry="6"/><line x1="2.5" y1="12" x2="21.5" y2="12"/></svg></div>`}
          ${a.category ? `<span class="blog-card-cat">${escHtml(a.category)}</span>` : ""}
        </div>
        <div class="blog-card-body">
          <span class="blog-card-date">${fmtDate(a.date)}</span>
          <h2 class="blog-card-title">${escHtml(a.title)}</h2>
          <p class="blog-card-excerpt">${escHtml(a.excerpt || a.metaDescription || "")}</p>
          <span class="blog-card-cta">Read article <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg></span>
        </div>
      </a>`).join("")
    : `<div style="grid-column:1/-1;text-align:center;padding:4rem 1.5rem;color:var(--grey)">
        <p style="font-size:1rem">No articles published yet. Check back soon.</p>
      </div>`;

  const chrome = siteChrome(
    "Rugby Blog — Guides, News & Club Advice",
    "Rugby tips, club guides, county breakdowns and more from the UK Rugby Club Directory team.",
    "/blog"
  );

  const html = `${chrome.head}
${chrome.nav}
<main>
  <div class="blog-hero">
    <div class="con blog-hero-inner">
      <nav class="blog-breadcrumb" aria-label="Breadcrumb">
        <a href="/index.html">Home</a>
        <span class="bc-sep">›</span>
        <span class="bc-cur">Blog</span>
      </nav>
      <div class="blog-hero-tag">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M2 3h6a4 4 0 014 4v14a3 3 0 00-3-3H2z"/><path d="M22 3h-6a4 4 0 00-4 4v14a3 3 0 013-3h7z"/></svg>
        Rugby Knowledge Hub
      </div>
      <h1>Rugby Blog</h1>
      <div class="blog-hero-meta">
        <span class="blog-meta-item">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M2 3h6a4 4 0 014 4v14a3 3 0 00-3-3H2z"/><path d="M22 3h-6a4 4 0 00-4 4v14a3 3 0 013-3h7z"/></svg>
          ${allArticles.length} article${allArticles.length !== 1 ? "s" : ""}
        </span>
        <span class="blog-meta-item">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><ellipse cx="12" cy="12" rx="9.5" ry="6"/></svg>
          Club guides, tips &amp; rugby news
        </span>
      </div>
    </div>
  </div>

  <div class="blog-index-wrap">
    <div class="con">
      <div class="sh" style="text-align:left;margin-bottom:0">
        <span class="ey">Latest Articles</span>
        <h2>Rugby Guides &amp; Insights</h2>
        <p>Club guides, beginner tips, county breakdowns and the latest from grassroots rugby across the UK.</p>
      </div>
      <div class="blog-grid">
        ${cardHtml}
      </div>
    </div>
  </div>
</main>
${chrome.footer}`;

  return new Response(html, {
    headers: { "Content-Type": "text/html;charset=UTF-8" }
  });
}

export const config = {
  path: ["/blog", "/blog/*"]
};
