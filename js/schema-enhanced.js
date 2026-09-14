/* ============================================================
   schema-enhanced.js — UK Rugby Club Directory
   Advanced JSON-LD Schema Markup — all page types
   
   Injected via: <script src="../js/schema-enhanced.js"></script>
   (or <script src="js/schema-enhanced.js"> on root pages)
   
   Covers:
   • Homepage      — WebSite + Organization + SiteNavigationElement
   • Club listing  — SportsOrganization + LocalBusiness + FAQPage + Event
   • Category page — CollectionPage + ItemList
   • Blog article  — Article + BreadcrumbList + Person (author)
   • Pricing page  — Product + Offer
   • Breadcrumbs   — BreadcrumbList (all pages)
   ============================================================ */

(function () {
  'use strict';

  var BASE = 'https://ukrugbyclubdirectory.co.uk';
  var path = window.location.pathname;
  var isClub = document.querySelector('.club-hero') !== null;
  var isHome = path === '/' || path.endsWith('/index.html');
  var isUnion = path.includes('rugby-union');
  var isLeague = path.includes('rugby-league');
  var isClubs = path.includes('/clubs');
  var isBlog = path.includes('/blog');
  var isPricing = path.includes('/pricing');
  var isClaim = path.includes('/claim');
  var isRegister = path.includes('/register');

  function inject(schema) {
    var s = document.createElement('script');
    s.type = 'application/ld+json';
    s.textContent = JSON.stringify(schema, null, 0);
    document.head.appendChild(s);
  }

  function getClubName() {
    var el = document.querySelector('.hero-name, h1');
    return el ? el.textContent.trim() : 'UK Rugby Club';
  }
  function getClubDesc() {
    var el = document.querySelector('.hero-info p, .rich-text p');
    return el ? el.textContent.trim().slice(0, 250) : '';
  }
  function getClubLocation() {
    var el = document.querySelector('.hm-item, .club-loc');
    return el ? el.textContent.trim().replace(/^[^\w]+/, '') : '';
  }
  function getClubType() {
    var pill = document.querySelector('.pill-union, .pill-league');
    if (!pill) return 'Rugby Union';
    return pill.classList.contains('pill-union') ? 'Rugby Union' : 'Rugby League';
  }
  function getClubFounded() {
    var el = document.querySelector('.hero-stat strong, .stat-item strong, .info-list dd');
    if (!el) return null;
    var txt = el.textContent.trim();
    return /^\d{4}$/.test(txt) ? txt : null;
  }
  function getClubWebsite() {
    var link = document.querySelector('a[href^="http"]:not([href*="ukrugbyclubdirectory"])');
    return link ? link.href : null;
  }
  function getPageUrl() {
    return BASE + path.replace(/\/index\.html$/, '/');
  }

  /* ── HOMEPAGE ─────────────────────────────────────────── */
  if (isHome) {
    // Organization schema
    inject({
      "@context": "https://schema.org",
      "@type": ["Organization", "WebSite"],
      "@id": BASE + "/#organization",
      "name": "UK Rugby Club Directory",
      "url": BASE,
      "logo": {
        "@type": "ImageObject",
        "url": BASE + "/logo.svg",
        "width": 220,
        "height": 56
      },
      "description": "The UK's most comprehensive rugby club directory. 620+ clubs across England, Scotland, Wales and Northern Ireland with full profile pages.",
      "foundingDate": "2024",
      "areaServed": {
        "@type": "Country",
        "name": "United Kingdom"
      },
      "knowsAbout": ["Rugby Union", "Rugby League", "Grassroots Rugby", "UK Rugby Clubs"],
      "sameAs": [
        "https://twitter.com/ukrugbydir",
        "https://facebook.com/ukrugbyclubdirectory"
      ],
      "contactPoint": {
        "@type": "ContactPoint",
        "contactType": "customer service",
        "url": BASE + "/contact-us.html",
        "availableLanguage": "English"
      },
      "potentialAction": {
        "@type": "SearchAction",
        "target": {
          "@type": "EntryPoint",
          "urlTemplate": BASE + "/clubs.html?q={search_term_string}"
        },
        "query-input": "required name=search_term_string"
      }
    });

    // ItemList of featured clubs for homepage rich snippets
    var featuredCards = document.querySelectorAll('.club-card--featured .club-name');
    if (featuredCards.length > 0) {
      var items = Array.from(featuredCards).map(function(el, i) {
        var card = el.closest('.club-card');
        var link = card ? card.querySelector('a.card-link') : null;
        return {
          "@type": "ListItem",
          "position": i + 1,
          "name": el.textContent.trim(),
          "url": link ? BASE + '/' + link.getAttribute('href').replace(/^\.\//, '') : BASE
        };
      });
      inject({
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Featured Rugby Clubs — UK Rugby Club Directory",
        "description": "Featured and verified rugby clubs from across England, Scotland, Wales and Northern Ireland.",
        "url": BASE,
        "numberOfItems": items.length,
        "itemListElement": items
      });
    }

    // WebSite with SearchAction (enhanced)
    inject({
      "@context": "https://schema.org",
      "@type": "WebSite",
      "@id": BASE + "/#website",
      "name": "UK Rugby Club Directory",
      "url": BASE,
      "publisher": { "@id": BASE + "/#organization" },
      "potentialAction": {
        "@type": "SearchAction",
        "target": {
          "@type": "EntryPoint",
          "urlTemplate": BASE + "/clubs.html?q={search_term_string}"
        },
        "query-input": "required name=search_term_string"
      }
    });

    // SiteNavigationElement
    inject({
      "@context": "https://schema.org",
      "@type": "SiteNavigationElement",
      "name": ["Home", "All Clubs", "Rugby Union", "Rugby League", "Blog", "Register Club"],
      "url": [
        BASE + "/",
        BASE + "/clubs.html",
        BASE + "/rugby-union.html",
        BASE + "/rugby-league.html",
        BASE + "/blog",
        BASE + "/register.html"
      ]
    });
  }

  /* ── CLUB LISTING PAGE ────────────────────────────────── */
  if (isClub) {
    var clubName = getClubName();
    var clubDesc = getClubDesc();
    var clubLoc  = getClubLocation();
    var clubType = getClubType();
    var founded  = getClubFounded();
    var website  = getClubWebsite();
    var pageUrl  = getPageUrl();
    var slug     = path.replace(/.*\//, '').replace(/\.html$/, '');

    // SportsOrganization + LocalBusiness combined (maximises rich snippet eligibility)
    var clubSchema = {
      "@context": "https://schema.org",
      "@type": ["SportsOrganization", "LocalBusiness", "SportsActivityLocation"],
      "@id": pageUrl + "#club",
      "name": clubName,
      "url": pageUrl,
      "description": clubDesc || (clubName + " is a " + clubType + " club in the UK. Find contact details, training times, facilities and membership information."),
      "sport": clubType,
      "currenciesAccepted": "GBP",
      "priceRange": "Free to join trial / £ membership fee",
      "address": {
        "@type": "PostalAddress",
        "addressLocality": clubLoc || "",
        "addressCountry": "GB"
      },
      "geo": {
        "@type": "GeoCoordinates"
      },
      "openingHoursSpecification": [
        {
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": ["Tuesday", "Thursday"],
          "opens": "19:00",
          "closes": "21:00",
          "description": "Typical training session times — confirm with club directly"
        }
      ],
      "potentialAction": {
        "@type": "JoinAction",
        "agent": { "@type": "Person" },
        "object": { "@type": "SportsOrganization", "name": clubName }
      },
      "isPartOf": {
        "@id": BASE + "/#organization"
      }
    };

    if (founded) clubSchema.foundingDate = founded;
    if (website) clubSchema.sameAs = [website];

    // Get logo image if present
    var badgeImg = document.querySelector('.hero-badge, .club-badge');
    if (badgeImg && badgeImg.src && !badgeImg.src.includes('fallback')) {
      clubSchema.logo = { "@type": "ImageObject", "url": badgeImg.src };
      clubSchema.image = badgeImg.src;
    }

    inject(clubSchema);

    // FAQPage schema — universal rugby club FAQ (boosts FAQ rich snippet)
    inject({
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "How do I join " + clubName + "?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "To join " + clubName + ", visit their training sessions — most clubs welcome new players for a free trial before committing to membership. Contact the club directly using the details on this page to find out about the next training session and membership fees."
          }
        },
        {
          "@type": "Question",
          "name": "Does " + clubName + " have a women's or girls' section?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Many UK rugby clubs including " + clubName + " offer women's and girls' rugby sections. Check the Teams section on this page or contact the club directly to confirm current arrangements and availability."
          }
        },
        {
          "@type": "Question",
          "name": "Does " + clubName + " offer junior rugby for children?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": clubName + " offers junior and mini rugby sections for children. Most clubs run sessions from age 5 upwards. Contact the club for current age groups, session times and safeguarding information."
          }
        },
        {
          "@type": "Question",
          "name": "Can I hire the hall or venue at " + clubName + "?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Many rugby clubs offer hall and venue hire for parties, corporate events and community gatherings. Check the Hall Hire section on this page or contact " + clubName + " directly to enquire about availability and pricing."
          }
        },
        {
          "@type": "Question",
          "name": "Where is " + clubName + " located?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": clubName + " is based in " + (clubLoc || "the United Kingdom") + ". See the Location section on this page for the full address, Google Maps link and directions."
          }
        }
      ]
    });

    // BreadcrumbList (enhanced)
    var categoryName = clubType === 'Rugby Union' ? 'Rugby Union' : 'Rugby League';
    var categoryUrl  = clubType === 'Rugby Union'
      ? BASE + '/rugby-union.html'
      : BASE + '/rugby-league.html';
    inject({
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Home", "item": BASE },
        { "@type": "ListItem", "position": 2, "name": categoryName, "item": categoryUrl },
        { "@type": "ListItem", "position": 3, "name": clubName, "item": pageUrl }
      ]
    });
  }

  /* ── CATEGORY PAGES (All Clubs / Union / League) ──────── */
  if (isUnion || isLeague || isClubs) {
    var catName = isUnion ? 'Rugby Union Clubs UK'
                : isLeague ? 'Rugby League Clubs UK'
                : 'All Rugby Clubs UK';
    var catDesc = isUnion
      ? 'Browse 453 rugby union clubs across England, Scotland, Wales and Northern Ireland. Every club with a full profile page.'
      : isLeague
      ? 'Browse 101 rugby league clubs across England and Wales. Super League, Championship and community clubs all listed.'
      : 'Browse all 620 rugby clubs across the UK — union, league and rugby businesses.';
    var catUrl = getPageUrl();

    // Build ItemList from visible club cards
    var clubCards = document.querySelectorAll('.club-name');
    var listItems = Array.from(clubCards).slice(0, 20).map(function(el, i) {
      var card = el.closest('article, .card');
      var link = card ? card.querySelector('a') : null;
      return {
        "@type": "ListItem",
        "position": i + 1,
        "name": el.textContent.trim(),
        "url": link ? (link.href.startsWith('http') ? link.href : BASE + '/' + link.getAttribute('href').replace(/^\.\//, '')) : catUrl
      };
    });

    inject({
      "@context": "https://schema.org",
      "@type": "CollectionPage",
      "@id": catUrl + "#page",
      "name": catName,
      "description": catDesc,
      "url": catUrl,
      "isPartOf": { "@id": BASE + "/#website" },
      "breadcrumb": {
        "@type": "BreadcrumbList",
        "itemListElement": [
          { "@type": "ListItem", "position": 1, "name": "Home", "item": BASE },
          { "@type": "ListItem", "position": 2, "name": catName, "item": catUrl }
        ]
      }
    });

    if (listItems.length > 0) {
      inject({
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": catName,
        "description": catDesc,
        "url": catUrl,
        "numberOfItems": listItems.length,
        "itemListElement": listItems
      });
    }
  }

  /* ── BLOG ARTICLE ─────────────────────────────────────── */
  if (isBlog && path.length > 10) {
    var articleTitle = (document.querySelector('h1') || {}).textContent || '';
    var articleDesc  = (document.querySelector('meta[name="description"]') || {}).getAttribute('content') || '';
    var articleDate  = (document.querySelector('.article-date, time') || {}).getAttribute('datetime')
                     || (document.querySelector('.article-date, time') || {}).textContent || '';
    var articleUrl   = getPageUrl();
    var authorName   = (document.querySelector('.author-name') || {}).textContent || 'UK Rugby Club Directory Editorial Team';

    if (articleTitle) {
      inject({
        "@context": "https://schema.org",
        "@type": "Article",
        "@id": articleUrl + "#article",
        "headline": articleTitle,
        "description": articleDesc,
        "url": articleUrl,
        "datePublished": articleDate,
        "dateModified": articleDate,
        "author": {
          "@type": "Person",
          "name": authorName,
          "url": BASE + "/blog"
        },
        "publisher": {
          "@type": "Organization",
          "name": "UK Rugby Club Directory",
          "url": BASE,
          "logo": {
            "@type": "ImageObject",
            "url": BASE + "/logo.svg"
          }
        },
        "mainEntityOfPage": {
          "@type": "WebPage",
          "@id": articleUrl
        },
        "isPartOf": { "@id": BASE + "/blog#website" },
        "inLanguage": "en-GB",
        "about": { "@type": "Thing", "name": "Rugby Union" },
        "keywords": "rugby, rugby union, rugby league, UK rugby clubs, grassroots rugby"
      });
    }
  }

  /* ── PRICING PAGE ─────────────────────────────────────── */
  if (isPricing) {
    inject({
      "@context": "https://schema.org",
      "@type": "WebPage",
      "name": "Pricing — UK Rugby Club Directory",
      "description": "Free and Pro club listing plans for UK rugby clubs. Featured placements and supplier advertising also available.",
      "url": BASE + "/pricing.html",
      "offers": [
        {
          "@type": "Offer",
          "name": "Free Club Listing",
          "price": "0",
          "priceCurrency": "GBP",
          "availability": "https://schema.org/InStock",
          "description": "Full club profile page with SEO, Google Maps and search listing.",
          "url": BASE + "/register.html?plan=free"
        },
        {
          "@type": "Offer",
          "name": "Pro Club Listing",
          "price": "9.99",
          "priceCurrency": "GBP",
          "priceSpecification": { "@type": "RecurringCharge", "billingIncrement": 1 },
          "availability": "https://schema.org/InStock",
          "description": "Pro badge, photo gallery, priority ranking, hall hire listing, verified tick and monthly stats.",
          "url": BASE + "/pricing.html"
        }
      ]
    });
  }

  /* ── BREADCRUMB — all other pages ─────────────────────── */
  if (!isHome && !isClub && !isUnion && !isLeague && !isClubs && !isBlog) {
    var pageTitle = document.title.replace(/ \| UK Rugby Club Directory$/, '');
    inject({
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Home", "item": BASE },
        { "@type": "ListItem", "position": 2, "name": pageTitle, "item": getPageUrl() }
      ]
    });
  }

})();
