/* ============================================================
   UK Rugby Club Directory — Region Filter + Blog Nav + Favicon
   Injected as a separate script so it doesn't touch main.js
   ============================================================ */
(function () {

  /* ── 1. Add Blog link to nav on every page ──────────────── */
  function addBlogNav() {
    // Desktop nav — insert Blog before Contact
    var contactLinks = document.querySelectorAll('#main-nav a.nav-link[href*="contact"]');
    contactLinks.forEach(function(contact) {
      if (document.querySelector('#main-nav a[href="/blog"]')) return; // already added
      var blogLink = document.createElement('a');
      blogLink.href = '/blog';
      blogLink.className = 'nav-link';
      blogLink.textContent = 'Blog';
      if (window.location.pathname === '/blog' || window.location.pathname.startsWith('/blog/')) {
        blogLink.classList.add('active');
      }
      contact.parentNode.insertBefore(blogLink, contact);
    });

    // Mobile nav — insert Blog before Contact mob-link
    var mobContactLinks = document.querySelectorAll('#mobile-nav a.mob-link[href*="contact"]');
    mobContactLinks.forEach(function(contact) {
      if (document.querySelector('#mobile-nav a[href="/blog"]')) return;
      var blogMob = document.createElement('a');
      blogMob.href = '/blog';
      blogMob.className = 'mob-link';
      blogMob.textContent = 'Blog';
      contact.parentNode.insertBefore(blogMob, contact);
    });
  }

  /* ── 2. Favicon ─────────────────────────────────────────── */
  function setFavicon() {
    // Remove existing favicons
    document.querySelectorAll('link[rel*="icon"]').forEach(function(el) { el.remove(); });
    // Add new Rule Divide favicon
    var svg = document.createElement('link');
    svg.rel = 'icon';
    svg.type = 'image/svg+xml';
    svg.href = '/favicon.svg';
    document.head.appendChild(svg);
    var ico = document.createElement('link');
    ico.rel = 'icon';
    ico.type = 'image/x-icon';
    ico.href = '/favicon.ico';
    document.head.appendChild(ico);
  }

  /* ── 3. Region filter for listing pages ─────────────────── */
  function applyRegionFilter() {
    var regionParam = new URLSearchParams(window.location.search).get('region');
    if (!regionParam) return;

    // Region → county/area keywords mapping
    var regionMap = {
      'yorkshire':        ['yorkshire','york','leeds','sheffield','bradford','hull','doncaster','harrogate','wakefield','huddersfield','rotherham','barnsley','keighley','scarborough','skipton','whitby','selby','ripon','pontefract','beverley','halifax','ilkley'],
      'london-se':        ['london','surrey','kent','essex','middlesex','hertfordshire','sussex','greater london','richmond','twickenham','blackheath','harlequins','saracens','ealing','greenwich','barnet','croydon','bromley','tonbridge','sevenoaks','guildford','woking','dorking','reigate','crawley','brighton','eastbourne','hastings','folkestone','maidstone','canterbury','dartford','gravesend','medway','colchester','chelmsford','brentwood','cheshunt','stevenage','hertford','harpenden','st albans','watford','hemel hempstead','enfield'],
      'north-west':       ['lancashire','cheshire','cumbria','merseyside','greater manchester','manchester','liverpool','sale','bolton','wigan','warrington','leigh','st helens','chorley','preston','blackburn','burnley','fleetwood','vale of lune','kendal','keswick','penrith','carlisle','whitehaven','workington','barrow','millom','furness','altrincham','stockport','macclesfield','northwich','congleton','crewe','nantwich','chester','salford'],
      'midlands':         ['midlands','leicestershire','warwickshire','nottinghamshire','derbyshire','staffordshire','northamptonshire','worcestershire','shropshire','leicester','coventry','northampton','nottingham','derby','birmingham','wolverhampton','stafford','worcester','shrewsbury','tamworth','lichfield','burton','market harborough','lutterworth','kenilworth','leamington','hinckley','melton mowbray','loughborough','long eaton','matlock','bakewell','ilkeston','solihull','kidderminster','broadstreet','old halesonians','harborne'],
      'south-west':       ['cornwall','devon','somerset','dorset','gloucestershire','wiltshire','bristol','exeter','bath','taunton','gloucester','cheltenham','stroud','cirencester','redruth','camborne','hayle','truro','falmouth','penryn','helston','penzance','newquay','bodmin','launceston','st ives','st austell','liskeard','perranporth','paignton','torquay','newton abbot','teignmouth','sidmouth','exmouth','brixham','tavistock','okehampton','south molton','barnstaple','bideford','torrington','crediton','ivybridge','kingsbridge','yeovil','taunton','bridgwater','clevedon','nailsea','weston-super-mare','chippenham','trowbridge','marlborough','salisbury','bournemouth','dorchester','swanage','wareham','poole','weymouth','wimborne'],
      'north-east':       ['northumberland','tyne and wear','durham','cleveland','teesside','newcastle','sunderland','gateshead','durham','hartlepool','stockton','middlesbrough','darlington','redcar','whitby','morpeth','alnwick','hexham','tynedale','blaydon','dmp','blyth','consett','spennymoor','peterlee','bishop auckland','west hartlepool','norton','thornensians','billingham','ashington'],
      'wales':            ['wales','cardiff','swansea','newport','llanelli','neath','bridgend','pontypridd','rhondda','ebbw vale','caerphilly','merthyr','abergavenny','aberystwyth','carmarthen','pembroke','haverfordwest','lampeter','aberavon','taibach','maesteg','penygraig','ferndale','treherbert','glynneath','skewen','tumble','nant conwy','colwyn bay','llandudno','bangor','llangollen','welshpool','newtown','rhayader','builth wells','llandrindod','aberaeron','cardigan','cross keys','risca','bedwas','caerphilly','pontypool','blaenavon','brynmawr','abertillery','ebbw','dragons','ospreys','scarlets','welsh','glamorgan','gwent','dyfed','gwynedd','clwyd','powys','pembrokeshire','ceredigion','carmarthenshire','monmouthshire'],
      'scotland':         ['scotland','edinburgh','glasgow','aberdeen','dundee','perth','stirling','inverness','elgin','fraserburgh','montrose','forfar','crieff','perthshire','ayr','kilmarnock','gala','hawick','melrose','kelso','jedburgh','jed-forest','langholm','coldstream','peebles','selkirk','linlithgow','haddington','musselburgh','livingston','hillfoots','alloa','boroughmuir','watsonians','heriot','currie','inverleith','gordonians','aberdeen grammar','dundee hsfp','dunfermline','falkirk','stirling county','west of scotland','grangemouth','biggar'],
      'northern-ireland': ['northern ireland','ulster','belfast','armagh','dungannon','ballymena','bangor','instonians','malone'],
    };

    var keywords = regionMap[regionParam];
    if (!keywords) return;

    // Find all club card wrappers
    var cards = document.querySelectorAll('.club-card-wrap, [data-city], [data-name]');
    if (!cards.length) {
      // Try alternative selector — cards may just be direct grid children
      cards = document.querySelectorAll('.clubs-grid > *, .grid > .card, .grid-3 > *, .grid-4 > *');
    }

    var shown = 0;
    var hidden = 0;

    cards.forEach(function(card) {
      // Build a searchable string from all text content + data attributes
      var text = (
        (card.getAttribute('data-city') || '') + ' ' +
        (card.getAttribute('data-name') || '') + ' ' +
        (card.getAttribute('data-region') || '') + ' ' +
        card.textContent
      ).toLowerCase();

      var match = keywords.some(function(kw) {
        return text.indexOf(kw) !== -1;
      });

      if (match) {
        card.style.display = '';
        shown++;
      } else {
        card.style.display = 'none';
        hidden++;
      }
    });

    // Update the count display
    var countEl = document.getElementById('results-count');
    if (countEl && shown > 0) {
      var regionLabel = regionParam.replace(/-/g,' ').replace(/\b\w/g, function(c){return c.toUpperCase();});
      countEl.textContent = shown + ' club' + (shown !== 1 ? 's' : '') + ' in ' + regionLabel;
    }

    // Update page title to reflect region
    var regionLabel = regionParam.replace(/-/g,' ').replace(/\b\w/g, function(c){return c.toUpperCase();});
    var h1 = document.querySelector('h1');
    if (h1 && shown > 0) {
      h1.textContent = 'Rugby Clubs in ' + regionLabel;
    }

    // Highlight the active region filter button if present
    document.querySelectorAll('.filter-btn[data-filter]').forEach(function(btn){
      btn.classList.remove('active');
    });
    var activeBtn = document.querySelector('.filter-btn[data-filter="' + regionParam + '"]');
    if (activeBtn) activeBtn.classList.add('active');
  }

  /* ── 4. Blog index.json loader ──────────────────────────── */
  function loadBlogIndex() {
    var grid = document.getElementById('blog-grid');
    var loading = document.getElementById('blog-loading');
    if (!grid) return; // not on blog page

    function fmtDate(str) {
      try { return new Date(str).toLocaleDateString('en-GB', {day:'numeric',month:'long',year:'numeric'}); }
      catch(e) { return str; }
    }
    function esc(s) {
      return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
    }
    function renderCard(a) {
      var img = a.image
        ? '<img src="'+esc(a.image)+'" alt="'+esc(a.title)+'" loading="lazy">'
        : '<div style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;opacity:.2"><svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="1.5"><ellipse cx="12" cy="12" rx="9.5" ry="6"/></svg></div>';
      var cat = a.category ? '<span class="blog-card-cat">'+esc(a.category)+'</span>' : '';
      return '<a href="/blog/'+esc(a.slug)+'" class="blog-card">'
        +'<div class="blog-card-img">'+img+cat+'</div>'
        +'<div class="blog-card-body">'
        +'<span class="blog-card-date">'+fmtDate(a.date)+'</span>'
        +'<h2 class="blog-card-title">'+esc(a.title)+'</h2>'
        +'<p class="blog-card-excerpt">'+esc(a.excerpt||a.metaDescription||'')+'</p>'
        +'<span class="blog-card-cta">Read article <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg></span>'
        +'</div></a>';
    }

    fetch('/content/blog/index.json?v='+Date.now())
      .then(function(r){ return r.json(); })
      .then(function(articles){
        if (loading) loading.style.display = 'none';
        if (!articles || !articles.length) {
          grid.innerHTML = '<div style="grid-column:1/-1;text-align:center;padding:4rem;color:var(--grey)"><p>No articles published yet. Check back soon.</p></div>';
          return;
        }
        grid.innerHTML = articles.map(renderCard).join('');
        // Update article count in hero
        var countEl = document.querySelector('.blog-meta-item:first-child');
        if (countEl) countEl.innerHTML = countEl.innerHTML.replace(/\d+ article/, articles.length + ' article');
      })
      .catch(function(){
        if (loading) loading.style.display = 'none';
        grid.innerHTML = '<div style="grid-column:1/-1;text-align:center;padding:4rem;color:var(--grey)"><p>Unable to load articles right now.</p></div>';
      });
  }

  /* ── Run everything ─────────────────────────────────────── */
  function init() {
    addBlogNav();
    setFavicon();
    applyRegionFilter();
    loadBlogIndex();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
