# UK Rugby Club Directory — Elite Growth & Enhancement Roadmap
**Prepared by:** Steve (UX/UI Lead) · Sue (AI/SEO Strategist) · Technical Architect
**Platform:** Static HTML · Netlify · n8n automation · 620 club pages
**Primary Goal:** Dominate UK rugby search, scale to 10,000+ listings, monetise directory

---

## Pillar 1 — Technical Architecture & Programmatic Scalability

### Current State Assessment
*(Simulated Screaming Frog + PageSpeed + GSC analysis)*

**Crawl efficiency issues found:**
- 920 HTML pages (300 root + 620 club/) with near-identical meta descriptions
- No pagination or canonical strategy for category pages returning 100+ clubs
- Inline `<style>` blocks on some pages duplicate CSS rules (adds ~8KB per page to parse)
- `font-display` not explicitly set on Google Fonts import (causes FOIT on slow connections)
- No `rel="preload"` on hero images (LCP blocker — typically 2.8–3.4s on 4G)
- No `robots.txt` disallow for `/register.html?plan=*` query strings (creates duplicate index entries)

### Scaling to 10,000+ Listings — Taxonomy & Crawl Budget

**Recommended URL structure:**
```
/club/{slug}.html                    ← individual club (current — keep)
/region/{county-slug}/               ← NEW county hub pages
/competition/{league-slug}/          ← NEW league/competition pages
/facilities/hall-hire/               ← NEW facility filter hub
/facilities/womens-rugby/            ← NEW demographic filter hub
/facilities/junior-rugby/
```

**Canonical strategy:**
```html
<!-- On every filtered/paginated category URL -->
<link rel="canonical" href="https://ukrugbyclubdirectory.co.uk/rugby-union.html">

<!-- On every club page -->
<link rel="canonical" href="https://ukrugbyclubdirectory.co.uk/club/{slug}.html">

<!-- Paginated category pages (when implemented) -->
<link rel="prev" href="/rugby-union.html?page=1">
<link rel="next" href="/rugby-union.html?page=3">
```

**Internal linking for crawl budget:**
- Every club page should link to: its county hub, its category page, 3 geographically nearby clubs
- Category pages should link to: all county hubs + 10 featured clubs + related blog articles
- Blog articles should link to: 3–5 relevant club pages using anchor text like "rugby clubs in [county]"
- Target: every page reachable in ≤ 3 clicks from homepage

### Core Web Vitals Fixes

**LCP (Largest Contentful Paint) — target: < 2.5s**
```html
<!-- Add to <head> of every listing page — preload the hero image -->
<link rel="preload" as="image" href="/imgs/rugby-union-hero.jpg" fetchpriority="high">

<!-- Add to CSS — force eager load on hero badge -->
.hero-badge-wrap img { loading: eager; fetchpriority: high; }

<!-- Add width/height to all club badge images to prevent layout shift -->
<img src="..." width="120" height="120" alt="...">
```

**INP (Interaction to Next Paint) — target: < 200ms**
```javascript
// Debounce the autocomplete search input (currently fires on every keydown)
const searchInput = document.getElementById('hero-search');
let debounceTimer;
searchInput?.addEventListener('input', () => {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(runSearch, 180);
});
```

**CLS (Cumulative Layout Shift) — target: < 0.1**
```css
/* Fix: set explicit aspect-ratio on badge-area to prevent badge image shift */
.badge-area { aspect-ratio: 4/3; min-height: 170px; }
.club-badge { width: 120px; height: 120px; object-fit: contain; }

/* Fix: reserve space for autocomplete dropdown so it doesn't push content */
.search-wrap { position: relative; min-height: 56px; }
```

**robots.txt additions:**
```
User-agent: *
Disallow: /register.html?plan=*
Disallow: /clubs.html?q=
Disallow: /rugby-union.html?region=
Disallow: /rugby-league.html?region=
Crawl-delay: 1

Sitemap: https://ukrugbyclubdirectory.co.uk/sitemap.xml
```

---

## Pillar 2 — Topical Authority & E-E-A-T

### Topic Cluster Map
*(Simulated Ahrefs + Semrush + Surfer analysis)*

**Pillar Page 1: "Find a Rugby Club Near Me" (hub: /find-a-rugby-club/)**
- Supporting: How to join a rugby club as a complete beginner
- Supporting: What to expect at your first rugby training session
- Supporting: Rugby club membership fees — what's a fair price in the UK?
- Supporting: Best rugby clubs for women in England 2025
- Supporting: Mini and junior rugby — what age can children start?
- Supporting: Returning to rugby after injury — a guide for adult players

**Pillar Page 2: "Rugby Club Facilities & Venues" (hub: /rugby-club-facilities/)**
- Supporting: Rugby club hall hire — how to book a club venue
- Supporting: Rugby club pitches — 3G vs grass vs sand-dressed
- Supporting: Clubhouse facilities — what the best rugby clubs offer
- Supporting: Rugby club gyms and strength & conditioning facilities
- Supporting: Wheelchair-accessible rugby clubs in the UK

**Pillar Page 3: "Starting & Running a Rugby Club" (hub: /run-a-rugby-club/)**
- Supporting: How to register a new rugby club with the RFU
- Supporting: Rugby club constitution — what you need and how to write one
- Supporting: Funding and grants for grassroots rugby clubs
- Supporting: Club governance — AGMs, committee roles and good practice
- Supporting: How to get your club listed in national directories

### E-E-A-T Implementation on Listing Pages

**Experience signals:**
- Add "Last verified by club: [date]" to sidebar — even if manual quarterly check
- Show a "Visited by our team" badge on any club you've physically verified
- Embed first-person quotes from club members (request via claim process)

**Expertise signals:**
- Author bylines on all blog posts with role + credentials (not just "UK Rugby Club Directory")
- Link author names to `/author/{name}.html` pages with bio + links to RFU profile
- Cite RFU and World Rugby data in articles with `<cite>` tags

**Authoritativeness signals:**
- Apply for RFU Partner Directory status — will earn an authoritative backlink
- Get listed on EnglandRugby.com, WRU, SRU, and IRU partner pages
- Submit sitemap to Google Search Console and Bing Webmaster Tools
- Build links from rugby county union websites (60+ county unions in England alone)

**Trustworthiness signals:**
- Add `https://` everywhere (already done via Netlify)
- Add visible privacy policy link in footer (done) — also add to register form
- Add last-modified date to every club page `<meta>` and schema `dateModified`
- Add a "Report incorrect information" link on every club page

---

## Pillar 3 — Structured Data (Schema Markup)

See `schema-enhanced.js` — delivered separately. Key schemas per page type:

### Homepage
```json
{
  "@context": "https://schema.org",
  "@type": ["Organization", "WebSite"],
  "@id": "https://ukrugbyclubdirectory.co.uk/#organization",
  "name": "UK Rugby Club Directory",
  "url": "https://ukrugbyclubdirectory.co.uk",
  "logo": {
    "@type": "ImageObject",
    "url": "https://ukrugbyclubdirectory.co.uk/logo.svg",
    "width": 220, "height": 56
  },
  "potentialAction": {
    "@type": "SearchAction",
    "target": {
      "@type": "EntryPoint",
      "urlTemplate": "https://ukrugbyclubdirectory.co.uk/clubs.html?q={search_term_string}"
    },
    "query-input": "required name=search_term_string"
  }
}
```

### Club Listing Page (dynamic template)
```json
{
  "@context": "https://schema.org",
  "@type": ["SportsOrganization", "LocalBusiness"],
  "@id": "https://ukrugbyclubdirectory.co.uk/club/{slug}.html#club",
  "name": "{clubName}",
  "sport": "{Rugby Union|Rugby League}",
  "foundingDate": "{year}",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "{town}",
    "addressRegion": "{county}",
    "postalCode": "{postcode}",
    "addressCountry": "GB"
  },
  "telephone": "{phone}",
  "email": "{email}",
  "url": "https://ukrugbyclubdirectory.co.uk/club/{slug}.html",
  "sameAs": ["{clubWebsite}", "{facebookUrl}"],
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["{trainingDay1}", "{trainingDay2}"],
      "opens": "{trainingTime}",
      "closes": "{trainingEndTime}"
    }
  ]
}
```

### FAQPage (per club — auto-generated)
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How do I join {clubName}?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Visit training sessions — most clubs offer a free trial..."
      }
    }
  ]
}
```

### Blog Article
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{title}",
  "author": {
    "@type": "Person",
    "name": "{authorName}",
    "jobTitle": "Rugby Content Writer"
  },
  "publisher": {
    "@type": "Organization",
    "name": "UK Rugby Club Directory",
    "logo": { "@type": "ImageObject", "url": "https://ukrugbyclubdirectory.co.uk/logo.svg" }
  },
  "datePublished": "{isoDate}",
  "dateModified": "{isoDate}"
}
```

**Validation:** Test every schema type at https://search.google.com/test/rich-results

---

## Pillar 4 — Local Visibility & Reputation Systems

### Hyper-Local Authority Strategy

**County hub pages** (quick win — 47 English counties + Wales/Scotland regions):
```
/county/somerset-rugby-clubs/
/county/yorkshire-rugby-clubs/
/county/kent-rugby-clubs/
```
Each county page needs: unique H1, 150-word intro, list of clubs in that county, county rugby union link, and a "clubs near {main town}" section. These pages target "[county] rugby clubs" searches — low competition, high conversion intent.

**NAP consistency system** — Name, Address, Phone:
```javascript
// In your n8n automation: monthly NAP audit workflow
// 1. Export club data from clubs-index.json
// 2. Compare against Google Business Profile API data
// 3. Flag mismatches for manual correction
// 4. Auto-update schema markup from single source of truth

const napAuditWorkflow = {
  trigger: 'schedule:monthly',
  steps: [
    { name: 'fetch-club-data', source: 'clubs-index.json' },
    { name: 'compare-google-business', api: 'Google Business Profile API' },
    { name: 'flag-mismatches', webhook: 'slack-notify' },
    { name: 'generate-correction-report', output: 'csv' }
  ]
};
```

**Citation building targets** (priority order):
1. RFU Club Finder — rugbyfootballunion.com/clubs
2. England Rugby county union websites (direct outreach)
3. Yelp UK — business listing
4. Yell.com — free directory
5. Thomson Local — free listing
6. UK Sports Network
7. Sports England partner directories

**Review capture system:**
```javascript
// Trigger email after a visitor has viewed 5+ club pages in a session
// Ask: "Did you find a club to join? Tell us about your experience."
// Link to Google review form for ukrugbyclubdirectory.co.uk

// n8n automation:
// 1. Visitor completes register form → wait 14 days → send "Did you join?" email
// 2. If yes → send review request with 1-click link
// 3. Track review acquisition in Airtable/Notion
```

---

## Pillar 5 — Accessibility (a11y) & UX

### WCAG 2.2 AA Checklist — Critical Items
*(Simulated axe DevTools + Pa11y analysis)*

**1. Missing or duplicate ARIA labels:**
```html
<!-- WRONG (current) — search button has no label -->
<button id="hero-search-btn" class="btn btn-red btn-sm search-btn">Search</button>

<!-- CORRECT -->
<button id="hero-search-btn" class="btn btn-red btn-sm search-btn" aria-label="Search for a rugby club">Search</button>

<!-- WRONG — hamburger button -->
<button id="hamburger">...</button>

<!-- CORRECT -->
<button id="hamburger" aria-label="Open navigation menu" aria-expanded="false" aria-controls="mobile-nav">...</button>
```

**2. Keyboard trap prevention:**
```javascript
// Mobile nav must trap focus INSIDE when open and release when closed
const mobileNav = document.getElementById('mobile-nav');
const focusable = 'a[href], button:not([disabled]), input, select, textarea, [tabindex]:not([tabindex="-1"])';

function trapFocus(el) {
  const els = el.querySelectorAll(focusable);
  const first = els[0], last = els[els.length - 1];
  el.addEventListener('keydown', function(e) {
    if (e.key === 'Tab') {
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault(); last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault(); first.focus();
      }
    }
    if (e.key === 'Escape') closeMobileNav();
  });
}
```

**3. Semantic HTML structure:**
```html
<!-- WRONG — missing landmark roles -->
<div class="hero">...</div>
<div class="content">...</div>

<!-- CORRECT -->
<header role="banner">...</header>
<nav aria-label="Main navigation">...</nav>
<main id="main-content">
  <article>
    <header>
      <h1>Club Name</h1>
    </header>
    <section aria-label="Club information">...</section>
    <section aria-label="Teams and age groups">...</section>
  </article>
</main>
<footer role="contentinfo">...</footer>
```

**4. Colour contrast — all failing pairs fixed in CSS:**
- `.text-muted` (#8b87a8 on white) — ratio 3.2:1 (fails AA for normal text) → change to `#5a5475` (4.6:1 ✓)
- `.est-chip` on badge area background — check actual background colour
- Footer muted text at `rgba(255,255,255,.28)` on `#0f0c1d` — ratio 1.7:1 (fails) → already fixed in V5/V6 to .6 opacity

**5. Image alt text audit:**
```html
<!-- WRONG — missing meaningful alt on club badges -->
<img src="bath-badge.png" alt="">

<!-- CORRECT -->
<img src="bath-badge.png" alt="Bath Rugby official club badge">

<!-- WRONG — decorative with alt text -->
<img src="hero-bg.jpg" alt="rugby stadium">

<!-- CORRECT — decorative image, empty alt, role=presentation -->
<img src="hero-bg.jpg" alt="" role="presentation">
```

**6. Form accessibility:**
```html
<!-- WRONG (register form) -->
<input type="text" placeholder="Club name">

<!-- CORRECT -->
<label for="club-name">Club name <span aria-label="required">*</span></label>
<input id="club-name" name="club_name" type="text" required
       aria-required="true"
       aria-describedby="club-name-hint">
<span id="club-name-hint" class="form-hint">Enter your club's full official name</span>
```

### UX Conversion Funnel Improvements

**Register form — current friction points:**
- 7 fields before a user commits — too many for cold traffic
- No progress indication
- Error states not described to screen readers
- No autofill attributes on address/contact fields

**Recommended 2-step form:**
```
Step 1 (30 seconds): Club name + email → "Check if listed" CTA
Step 2 (2 minutes): Full details + plan selection → Submit
```

**Search result friction:**
- Add "No results? Try [suggestion]" state with 3 popular nearby clubs
- Add postcode search alongside name search
- Add "Filter by: Women's · Juniors · Hall Hire · 3G Pitch" above results

---

## Prioritised Action Matrix

### Quick Wins (< 1 day each)

| Action | Impact | Effort | File |
|--------|--------|--------|------|
| Remove all topbar links (CSS fix) | High | Done | style.css |
| Add `.tb-actions {display:none}` | High | Done | style.css |
| Deploy schema-enhanced.js | High | 1hr | schema-enhanced.js |
| Add `robots.txt` Disallow query strings | Medium | 15min | robots.txt |
| Add `aria-label` to search buttons | Medium | 30min | HTML |
| Add `rel="preload"` to hero images | Medium | 30min | HTML |
| Fix placeholder text contrast | Low | 10min | style.css |
| Add `fetchpriority="high"` to hero badge | Medium | 30min | HTML |

### High Impact / High Effort

| Action | Impact | Effort | Notes |
|--------|--------|--------|-------|
| Build 47 county hub pages | Very High | 2 weeks | Programmatic — n8n + template |
| Add postcode to all 620 club pages | Very High | 1 week | Data sourcing required |
| Build club management dashboard | Very High | 4 weeks | Enables Pro tier features |
| Implement review capture email flow | High | 3 days | n8n automation |
| Add Google Business Profile API integration | High | 1 week | NAP consistency |
| Build lead capture / enquiry routing | High | 1 week | Phase 2 monetisation |
| Launch affiliate link integration | High | 3 days | Lovell Rugby, Gilbert |

### Long-Term Automation

| Action | Impact | Effort | Notes |
|--------|--------|--------|-------|
| n8n: monthly NAP audit vs Google Business | Very High | 2 weeks | Keep 620+ clubs accurate |
| n8n: auto-publish weekly rugby news blog | High | 1 week | Claude API → blog generator |
| n8n: new club registration → Slack → email → build page | Very High | 1 week | Closes claim loop |
| Programmatic county/competition pages (10,000+) | Very High | 1 month | Requires structured data |
| Analytics → personalised "clubs near you" | High | 2 weeks | Cookie consent required |
| Automated sitemap regeneration on new club | Medium | 2 days | Netlify build hook |
| Annual broken link audit automation | Medium | 1 day | n8n → Screaming Frog API |

---

*Roadmap version 1.0 — September 2025. Review quarterly.*
