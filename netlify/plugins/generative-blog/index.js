// netlify/plugins/generate-blog/index.js
// Runs at build time on Netlify — reads content/blog/*.md and outputs:
//   /blog/index.html         → article listing page
//   /blog/<slug>/index.html  → individual article pages
// No Edge Functions, no runtime fetches, no CSP issues. Pure static HTML.

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
      const kv = line.match(/^(\w+):\s*"?(.+?)"?\s*$/);
      if (kv) fm[kv[1]] = kv[2];
    }
  }
  return { fm, body: body.trim() };
}

// ─── Markdown → HTML (no external deps) ──────────────────────────────────────
function mdToHtml(md) {
  let html = md
    .replace(/&/g,  "&amp;")
    .replace(/</g,  "&lt;")
    .replace(/>/g,  "&gt;")
    // headings
    .replace(/^#### (.+)$/gm, "<h4>$1</h4>")
    .replace(/^### (.+)$/gm,  "<h3>$1</h3>")
    .replace(/^## (.+)$/gm,   "<h2>$1</h2>")
    .replace(/^# (.+)$/gm,    "<h1>$1</h1>")
    // bold / italic / inline code
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(.+?)\*/g,     "<em>$1</em>")
    .replace(/`(.+?)`/g,       "<code>$1</code>")
    // links
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');

  // bullet lists
  html = html.replace(/((?:^- .+$\n?)+)/gm, (block) => {
    const items = block.trim().split("\n")
      .map(l => `<li>${l.replace(/^- /, "")}</li>`).join("");
    return `<ul>${items}</ul>\n`;
  });

  // numbered lists
  html = html.replace(/((?:^\d+\. .+$\n?)+)/gm, (block) => {
    const items = block.trim().split("\n")
      .map(l => `<li>${l.replace(/^\d+\. /, "")}</li>`).join("");
    return `<ol>${items}</ol>\n`;
  });

  // paragraphs
  html = html.split(/\n{2,}/).map(block => {
    block = block.trim();
    if (!block) return "";
    if (/^<[huo]/.test(block)) return block;
    return `<p>${block.replace(/\n/g, " ")}</p>`;
  }).join("\n");

  return html;
}

// ─── Nav HTML (matches site design) ──────────────────────────────────────────
function nav(activePage) {
  const links = [
    ["Home",         "/index.html"],
    ["Rugby Union",  "/rugby-union.html"],
    ["Rugby League", "/rugby-league.html"],
    ["Businesses",   "/rugby-joints.html"],
    ["Blog",         "/blog"],
    ["Contact",      "/contact-us.html"],
  ];
  return `
<nav class="site-nav" id="site-nav">
  <div class="nav-inner">
    <a class="nav-logo" href="/index.html">
      <span class="logo-uk">UK</span><span class="logo-rule">|</span>
      <span class="logo-main">Rugby Club<span class="logo-dir">DIRECTORY</span></span>
    </a>
    <div class="nav-links">
      ${links.map(([label, href]) =>
        `<a href="${href}"${label === activePage ? ' class="active"' : ""}>${label}</a>`
      ).join("\n      ")}
      <a href="/register.html" class="nav-cta">+ Register Club</a>
    </div>
  </div>
</nav>`;
}

// ─── Footer HTML ──────────────────────────────────────────────────────────────
function footer() {
  return `
<footer class="site-footer">
  <div class="footer-inner">
    <div class="footer-brand">
      <a class="nav-logo" href="/index.html">
        <span class="logo-uk">UK</span><span class="logo-rule">|</span>
        <span class="logo-main">Rugby Club<span class="logo-dir">DIRECTORY</span></span>
      </a>
      <p>The UK's most comprehensive rugby club directory. Connecting clubs, players and fans across England, Scotland, Wales and Northern Ireland.</p>
    </div>
    <div class="footer-cols">
      <div>
        <h4>Directory</h4>
        <a href="/index.html">Home</a>
        <a href="/clubs.html">All Clubs</a>
        <a href="/rugby-union.html">Rugby Union</a>
        <a href="/rugby-league.html">Rugby League</a>
        <a href="/rugby-joints.html">Businesses</a>
      </div>
      <div>
        <h4>Content</h4>
        <a href="/blog">Blog</a>
        <a href="/register.html">Register Your Club</a>
        <a href="/contact-us.html">Contact Us</a>
      </div>
      <div>
        <h4>Legal</h4>
        <a href="/privacy-policy.html">Privacy Policy</a>
        <a href="/terms-of-service.html">Terms of Service</a>
        <a href="/cookie-policy.html">Cookie Policy</a>
        <a href="/sitemap.xml">Sitemap</a>
      </div>
    </div>
  </div>
  <div class="footer-bottom">
    <p>&copy; 2026 UK Rugby Club Directory. All rights reserved.</p>
  </div>
</footer>`;
}

// ─── Full HTML page shell ─────────────────────────────────────────────────────
function shell({ title, description, canonical, ogType, bodyContent, activePage }) {
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${title} | UK Rugby Club Directory</title>
  <meta name="description" content="${description}">
  <link rel="canonical" href="${canonical}">
  <meta name="robots" content="index,follow">
  <meta property="og:title"       content="${title}">
  <meta property="og:description" content="${description}">
  <meta property="og:url"         content="${canonical}">
  <meta property="og:type"        content="${ogType || "website"}">
  <meta property="og:site_name"   content="UK Rugby Club Directory">
  <meta name="twitter:card"        content="summary_large_image">
  <meta name="twitter:title"       content="${title}">
  <meta name="twitter:description" content="${description}">
  <link rel="stylesheet" href="/css/style.css">
  <style>
    /* ── Blog-specific styles ─────────────────────────────────── */
    .blog-hero{background:#0a1628;padding:3rem 1.5rem 2.5rem;color:#fff;text-align:center}
    .blog-eyebrow{font-size:.75rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#c8102e;margin:0 0 .5rem}
    .blog-hero-title{font-size:2.5rem;font-weight:800;margin:0 0 .5rem;line-height:1.1}
    .blog-hero-sub{font-size:1rem;color:#94a3b8;margin:0}
    .blog-container{max-width:1100px;margin:0 auto;padding:2.5rem 1.5rem}
    .blog-section-eyebrow{font-size:.7rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#c8102e;margin:0 0 .4rem}
    .blog-section-title{font-size:1.6rem;font-weight:700;color:#0a1628;margin:0 0 .5rem}
    .blog-section-sub{color:#64748b;margin:0 0 2rem;font-size:.95rem}
    .blog-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:1.5rem}
    .blog-card{background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:1.5rem;display:flex;flex-direction:column;gap:.5rem;transition:box-shadow .15s}
    .blog-card:hover{box-shadow:0 4px 20px rgba(0,0,0,.08)}
    .blog-card-date{font-size:.75rem;color:#94a3b8;font-weight:500}
    .blog-card-title{font-size:1.05rem;font-weight:700;color:#0a1628;margin:0;line-height:1.35}
    .blog-card-title a{text-decoration:none;color:inherit}
    .blog-card-title a:hover{color:#c8102e}
    .blog-card-excerpt{font-size:.9rem;color:#64748b;line-height:1.55;margin:0;flex:1}
    .blog-card-cta{font-size:.85rem;font-weight:600;color:#c8102e;text-decoration:none;margin-top:.25rem}
    .blog-card-cta:hover{text-decoration:underline}
    .blog-empty{text-align:center;padding:3rem;color:#94a3b8;font-size:1rem;background:#f8fafc;border-radius:12px;border:1px dashed #e2e8f0}
    /* Article */
    .article-hero{background:#0a1628;padding:3rem 1.5rem 2.5rem;color:#fff}
    .article-hero-inner{max-width:780px;margin:0 auto}
    .breadcrumb{font-size:.8rem;color:#64748b;margin:0 0 1rem}
    .breadcrumb a{color:#94a3b8;text-decoration:none}
    .breadcrumb a:hover{color:#fff}
    .article-title{font-size:2rem;font-weight:800;margin:0 0 .75rem;line-height:1.2;color:#fff}
    .article-meta{font-size:.85rem;color:#94a3b8;margin:0}
    .article-layout{max-width:1100px;margin:0 auto;padding:2.5rem 1.5rem;display:grid;grid-template-columns:1fr 300px;gap:2.5rem}
    @media(max-width:768px){.article-layout{grid-template-columns:1fr}}
    .article-body{color:#1e293b;line-height:1.75;font-size:1rem}
    .article-body h2{font-size:1.35rem;font-weight:700;color:#0a1628;margin:2rem 0 .75rem;padding-bottom:.4rem;border-bottom:2px solid #c8102e}
    .article-body h3{font-size:1.1rem;font-weight:600;color:#0a1628;margin:1.5rem 0 .5rem}
    .article-body p{margin:0 0 1.25rem}
    .article-body ul,.article-body ol{margin:0 0 1.25rem;padding-left:1.5rem}
    .article-body li{margin-bottom:.4rem}
    .article-body strong{color:#0a1628}
    .article-body a{color:#c8102e;text-decoration:underline}
    .sidebar-card{background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:1.25rem;position:sticky;top:1.5rem}
    .sidebar-card h3{font-size:1rem;font-weight:700;color:#0a1628;margin:0 0 .5rem}
    .sidebar-card p{font-size:.85rem;color:#64748b;line-height:1.5;margin:0 0 1rem}
    .sidebar-cta{display:inline-block;padding:.6rem 1.1rem;background:#c8102e;color:#fff;border-radius:8px;font-size:.85rem;font-weight:600;text-decoration:none}
    .sidebar-cta:hover{background:#a00d25}
  </style>
</head>
<body>
${nav(activePage)}
<main>${bodyContent}</main>
${footer()}
<script>
  // Cookie consent (matches site pattern)
  document.addEventListener("DOMContentLoaded", function() {
    if (!localStorage.getItem("cookiesAccepted")) {
      var b = document.createElement("div");
      b.innerHTML = '<div style="position:fixed;bottom:0;left:0;right:0;background:#0a1628;color:#fff;padding:1rem 1.5rem;display:flex;justify-content:space-between;align-items:center;z-index:9999;font-size:.85rem;"><span>We use cookies to give you the best experience. <a href="/cookie-policy.html" style="color:#c8102e">Cookie Policy</a></span><div style="display:flex;gap:.5rem;"><button onclick="this.closest(\'div\').parentElement.remove();localStorage.setItem(\'cookiesAccepted\',\'false\')" style="padding:.4rem .9rem;background:transparent;border:1px solid #64748b;color:#fff;border-radius:6px;cursor:pointer;font-size:.8rem;">Reject</button><button onclick="this.closest(\'div\').parentElement.remove();localStorage.setItem(\'cookiesAccepted\',\'true\')" style="padding:.4rem .9rem;background:#c8102e;border:none;color:#fff;border-radius:6px;cursor:pointer;font-size:.8rem;">Accept All</button></div></div>';
      document.body.appendChild(b);
    }
  });
</script>
</body>
</html>`;
}

// ─── Blog index HTML ──────────────────────────────────────────────────────────
function buildIndexPage(articles) {
  const cards = articles.length === 0
    ? `<div class="blog-empty">No articles published yet. Check back soon.</div>`
    : articles.map(a => `
        <article class="blog-card">
          <div class="blog-card-date">${a.date || ""}</div>
          <h2 class="blog-card-title"><a href="/blog/${a.slug}/">${a.title}</a></h2>
          <p class="blog-card-excerpt">${a.excerpt || ""}</p>
          <a class="blog-card-cta" href="/blog/${a.slug}/">Read more →</a>
        </article>`).join("\n");

  const bodyContent = `
    <div class="blog-hero">
      <p class="blog-eyebrow">Rugby Knowledge Hub</p>
      <h1 class="blog-hero-title">Rugby Blog</h1>
      <p class="blog-hero-sub">${articles.length} article${articles.length !== 1 ? "s" : ""} &middot; Club guides, tips &amp; rugby news</p>
    </div>
    <div class="blog-container">
      <p class="blog-section-eyebrow">Latest Articles</p>
      <h2 class="blog-section-title">Rugby Guides &amp; Insights</h2>
      <p class="blog-section-sub">Club guides, beginner tips, county breakdowns and the latest from grassroots rugby across the UK.</p>
      <div class="blog-grid">${cards}</div>
    </div>`;

  return shell({
    title:       "Rugby Blog — Guides, News & Club Advice",
    description: "Rugby tips, club guides, county breakdowns and more from the UK Rugby Club Directory team.",
    canonical:   "https://ukrugbyclubdirectory.co.uk/blog",
    ogType:      "website",
    activePage:  "Blog",
    bodyContent,
  });
}

// ─── Article HTML ─────────────────────────────────────────────────────────────
function buildArticlePage(slug, fm, bodyHtml) {
  const bodyContent = `
    <div class="article-hero">
      <div class="article-hero-inner">
        <nav class="breadcrumb">
          <a href="/index.html">Home</a> &rsaquo;
          <a href="/blog">Blog</a> &rsaquo;
          ${fm.title || slug}
        </nav>
        <h1 class="article-title">${fm.title || slug}</h1>
        <p class="article-meta"><time datetime="${fm.date || ""}">${fm.date || ""}</time></p>
      </div>
    </div>
    <div class="article-layout">
      <article class="article-body">${bodyHtml}</article>
      <aside>
        <div class="sidebar-card">
          <h3>Find a Rugby Club</h3>
          <p>Search 620+ clubs across England, Scotland, Wales and Northern Ireland.</p>
          <a class="sidebar-cta" href="/rugby-union.html">Browse clubs &rarr;</a>
        </div>
      </aside>
    </div>`;

  return shell({
    title:       fm.title || slug,
    description: fm.excerpt || `Read about ${fm.title || slug} on UK Rugby Club Directory.`,
    canonical:   `https://ukrugbyclubdirectory.co.uk/blog/${slug}/`,
    ogType:      "article",
    activePage:  "Blog",
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

    // Ensure output dir exists
    if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

    // Read all .md files
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

      const bodyHtml = mdToHtml(body);
      const articleHtml = buildArticlePage(slug, fm, bodyHtml);

      // Write to /blog/<slug>/index.html
      const articleDir = path.join(outDir, slug);
      if (!fs.existsSync(articleDir)) fs.mkdirSync(articleDir, { recursive: true });
      fs.writeFileSync(path.join(articleDir, "index.html"), articleHtml, "utf8");

      articles.push({
        slug,
        title:   fm.title,
        date:    fm.date   || "",
        excerpt: fm.excerpt || "",
      });

      console.log(`  ✓ ${slug}`);
    }

    // Sort newest first
    articles.sort((a, b) => b.date.localeCompare(a.date));

    // Write blog index
    fs.writeFileSync(path.join(outDir, "index.html"), buildIndexPage(articles), "utf8");
    console.log(`📝 generate-blog: wrote ${articles.length} articles + index → ${outDir}`);
  },
};
