/* UK Rugby Club Directory — main.js v2 */
(function () {
  'use strict';
  function esc(s) { return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
  function catLabel(t) { return {union:'Rugby Union',league:'Rugby League',business:'Rugby Business'}[t]||t; }
  function catPill(t)  { return {union:'pill-union',league:'pill-league',business:'pill-business'}[t]||'pill-union'; }
  var depth = Math.max(0,(window.location.pathname.match(/\//g)||[]).length-1);
  var prefix = depth===0?'':'../';

  /* Header shadow */
  var header=document.getElementById('site-header');
  if(header) window.addEventListener('scroll',function(){header.classList.toggle('scrolled',window.scrollY>6);},{passive:true});

  /* Active nav */
  var path=window.location.pathname;
  document.querySelectorAll('#main-nav a.nav-link:not(.nav-cta)').forEach(function(link){
    var href=(link.getAttribute('href')||'').replace(/\.html$/,'').replace(/\/index$/,'/');
    var cur=path.replace(/\.html$/,'').replace(/\/index$/,'/');
    if(href===cur||(href!='/'&&href!='/index'&&cur.startsWith(href))) link.classList.add('active');
  });

  /* Dropdowns */
  document.querySelectorAll('.nav-dropdown').forEach(function(dd){
    var btn=dd.querySelector('.nav-drop-btn'),panel=dd.querySelector('.dropdown-panel');
    if(!btn||!panel) return;
    btn.addEventListener('click',function(e){
      e.stopPropagation();
      var open=btn.getAttribute('aria-expanded')==='true';
      document.querySelectorAll('.nav-drop-btn').forEach(function(b){b.setAttribute('aria-expanded','false');});
      btn.setAttribute('aria-expanded',String(!open));
    });
  });
  document.addEventListener('click',function(){
    document.querySelectorAll('.nav-drop-btn').forEach(function(b){b.setAttribute('aria-expanded','false');});
  });

  /* Mobile nav */
  var ham=document.getElementById('hamburger'),mobNav=document.getElementById('mobile-nav'),mobClose=document.getElementById('mob-close');
  function openMob(){if(!ham||!mobNav)return;ham.setAttribute('aria-expanded','true');ham.classList.add('open');mobNav.removeAttribute('aria-hidden');mobNav.removeAttribute('inert');mobNav.classList.add('open');document.body.style.overflow='hidden';}
  function closeMob(){if(!ham||!mobNav)return;ham.setAttribute('aria-expanded','false');ham.classList.remove('open');mobNav.setAttribute('aria-hidden','true');mobNav.setAttribute('inert','');mobNav.classList.remove('open');document.body.style.overflow='';}
  if(ham) ham.addEventListener('click',openMob);
  if(mobClose) mobClose.addEventListener('click',closeMob);
  document.querySelectorAll('.mob-link,.mob-sub-link,.mob-cta').forEach(function(l){l.addEventListener('click',closeMob);});
  document.querySelectorAll('.mob-group-btn').forEach(function(btn){
    var sub=btn.nextElementSibling;
    if(!sub) return;
    btn.addEventListener('click',function(){var open=btn.getAttribute('aria-expanded')==='true';btn.setAttribute('aria-expanded',String(!open));btn.classList.toggle('active',!open);sub.hidden=open;});
  });

  /* Cookies */
  var banner=document.getElementById('cookie-banner');
  if(banner&&!localStorage.getItem('uk_rugby_cookies')) banner.classList.add('show');
  var acceptBtn=document.getElementById('cookie-accept'),rejectBtn=document.getElementById('cookie-reject');
  if(acceptBtn) acceptBtn.addEventListener('click',function(){localStorage.setItem('uk_rugby_cookies','1');if(banner)banner.classList.remove('show');});
  if(rejectBtn) rejectBtn.addEventListener('click',function(){localStorage.setItem('uk_rugby_cookies','0');if(banner)banner.classList.remove('show');});

  /* Badge fallbacks */
  document.querySelectorAll('img.club-badge,img.hero-badge,img.gallery-badge-img').forEach(function(img){
    img.addEventListener('error',function(){var fb=img.parentElement.querySelector('.badge-fallback,.hero-badge-fallback');if(fb){img.style.display='none';fb.style.display='flex';}});
  });

  /* ═══════════════════════════════════════════
     LIVE AUTOCOMPLETE SEARCH
  ═══════════════════════════════════════════ */
  var CLUBS_DATA=null;
  function loadClubs(cb){
    if(CLUBS_DATA){cb(CLUBS_DATA);return;}
    fetch(prefix+'js/clubs-index.json')
      .then(function(r){return r.json();})
      .then(function(d){CLUBS_DATA=d;cb(d);})
      .catch(function(){CLUBS_DATA=[];cb([]);});
  }

  function renderResult(c){
    var badgeSrc=c.b?(prefix+c.b.replace(/^\//,'')):null;
    var badgeHtml=badgeSrc
      ?'<img src="'+esc(badgeSrc)+'" alt="'+esc(c.n)+'" class="ac-badge" loading="lazy" onerror="this.style.display=\'none\';this.nextElementSibling.style.display=\'flex\'"><div class="ac-badge-fb" style="display:none">'+esc(c.n[0])+'</div>'
      :'<div class="ac-badge-fb">'+esc(c.n[0])+'</div>';
    return '<a href="'+prefix+'club/'+esc(c.s)+'.html" class="ac-item">'
      +'<div class="ac-badge-wrap">'+badgeHtml+'</div>'
      +'<div class="ac-info"><span class="ac-name">'+esc(c.n)+'</span>'+(c.c?'<span class="ac-loc">'+esc(c.c)+'</span>':'')+'</div>'
      +'<span class="pill '+catPill(c.t)+' ac-pill">'+catLabel(c.t)+'</span>'
      +'</a>';
  }

  function attachAutocomplete(input,catFilter){
    var wrap=input.closest('.search-wrap')||input.parentElement;
    wrap.style.position='relative';
    var dd=document.createElement('div');
    dd.className='ac-dropdown';dd.setAttribute('role','listbox');
    wrap.appendChild(dd);
    var timer;
    function run(q){
      q=q.trim().toLowerCase();
      if(!q||q.length<2){dd.innerHTML='';dd.classList.remove('open');return;}
      loadClubs(function(clubs){
        var res=clubs.filter(function(c){
          return (!catFilter||c.t===catFilter)&&(c.n.toLowerCase().includes(q)||c.c.toLowerCase().includes(q));
        }).slice(0,8);
        if(!res.length){dd.innerHTML='<div class="ac-empty">No clubs found for "<strong>'+esc(q)+'</strong>"</div>';dd.classList.add('open');return;}
        dd.innerHTML=res.map(renderResult).join('');
        dd.classList.add('open');
      });
    }
    input.addEventListener('input',function(){clearTimeout(timer);timer=setTimeout(function(){run(input.value);},160);});
    input.addEventListener('keydown',function(e){
      if(e.key==='Escape'){dd.innerHTML='';dd.classList.remove('open');}
      if(e.key==='Enter'){
        e.preventDefault();
        var first=dd.querySelector('.ac-item');
        if(first) first.click();
        else if(input.value.trim()) window.location.href=prefix+'clubs.html?q='+encodeURIComponent(input.value.trim());
      }
      if(e.key==='ArrowDown'||e.key==='ArrowUp'){
        e.preventDefault();
        var items=dd.querySelectorAll('.ac-item'),focused=dd.querySelector('.ac-item:focus'),idx=Array.from(items).indexOf(focused);
        if(e.key==='ArrowDown') idx=Math.min(idx+1,items.length-1); else idx=Math.max(idx-1,0);
        if(items[idx]) items[idx].focus();
      }
    });
    document.addEventListener('click',function(e){if(!wrap.contains(e.target)){dd.innerHTML='';dd.classList.remove('open');}});
    input.addEventListener('focus',function(){loadClubs(function(){});});
  }

  /* Homepage hero */
  var heroInput=document.getElementById('hero-search');
  if(heroInput){
    attachAutocomplete(heroInput,null);
    var heroBtn=document.getElementById('hero-search-btn');
    if(heroBtn) heroBtn.addEventListener('click',function(){var q=heroInput.value.trim();window.location.href=prefix+'clubs.html'+(q?'?q='+encodeURIComponent(q):'');});
    heroInput.addEventListener('keydown',function(e){if(e.key==='Enter'&&!document.querySelector('.ac-dropdown.open .ac-item')){var q=heroInput.value.trim();window.location.href=prefix+'clubs.html'+(q?'?q='+encodeURIComponent(q):'');}});
  }

  /* Listing page search */
  var listInput=document.getElementById('listing-search');
  if(listInput){
    var pageCat=listInput.getAttribute('data-category')||null;
    attachAutocomplete(listInput,pageCat);
    listInput.addEventListener('input',function(){applyGrid(listInput.value.trim());});
  }

  /* Grid filter */
  var filterBtns=document.querySelectorAll('.filter-btn[data-filter]');
  var wraps=document.querySelectorAll('.club-card-wrap');
  var countEl=document.getElementById('results-count');
  function applyGrid(query){
    var activeBtn=document.querySelector('.filter-btn.active');
    var cat=activeBtn?activeBtn.getAttribute('data-filter'):'all';
    var q=(query||'').toLowerCase().trim();
    var n=0;
    wraps.forEach(function(w){
      var show=((cat==='all'||w.getAttribute('data-category')===cat))&&(!q||w.getAttribute('data-name').includes(q)||w.getAttribute('data-city').includes(q));
      w.style.display=show?'':'none';
      if(show) n++;
    });
    if(countEl) countEl.textContent=n+' club'+(n!==1?'s':'')+' found';
  }
  filterBtns.forEach(function(btn){
    btn.addEventListener('click',function(){
      filterBtns.forEach(function(b){b.classList.remove('active');});
      btn.classList.add('active');
      var qi=document.getElementById('listing-search');
      applyGrid(qi?qi.value:'');
    });
  });
  var urlQ=new URLSearchParams(window.location.search).get('q')||'';
  if(urlQ){
    var si=document.getElementById('listing-search')||document.getElementById('hero-search');
    if(si) si.value=urlQ;
  }
  if(wraps.length) applyGrid(urlQ);

  /* ═══════════════════════════════════════════
     REGION FILTER — reads ?region= from URL
     Uses data-city attribute (exact city names)
  ═══════════════════════════════════════════ */
  var REGION_CITIES = {
    'yorkshire':        ['barnsley','barnsley','beverley','bingley','bridlington','cleckheaton','doncaster','driffield','guiseley','halifax','harrogate','hull','huddersfield','ilkley','keighley','leeds','malton','morley','ossett','otley','pontefract','penistone','rotherham','scarborough','selby','sheffield','skipton','wakefield','whitby','york'],
    'london-se':        ['barnet','beckenham','blackheath','brentford','brentwood','brighton','broadstairs','camberley','cambridge','canterbury','chelmsford','cheshunt','cheshunt','chichester','cranleigh','crawley','crowborough','dartford','dorking','ealing','eastbourne','enfield','esher','folkestone','farnham','gravesend','grays','guildford','harlow','harpenden','haslemere','hastings','haywards heath','hemel hempstead','henley-on-thames','hertford','horsham','ilford','letchworth','lewes','london','maidenhead','maidstone','midhurst','petersfield','pulborough','reading','reigate','richmond','rochford','rochester','sevenoaks','sidcup','southend-on-sea','st albans','stevenage','sutton','tonbridge','tunbridge wells','twickenham','uckfield','walton-on-thames','watford','windsor','woodford green','worthing'],
    'north-west':       ['altrincham','ambleside','barrow-in-furness','blackburn','blundellsands','bolton','burnley','carlisle','chester','chorley','congleton','crewe','egremont','fleetwood','kendal','keswick','lancaster','leigh','lytham st annes','macclesfield','manchester','millom','northwich','penrith','preston','rochdale','sale','salford','southport','st helens','stockport','warrington','whitehaven','wigan','wilmslow','windermere','wirral'],
    'midlands':         ['bakewell','banbury','bicester','birmingham','boston','burton upon trent','chesterfield','chipping norton','colchester','corby','coventry','derby','dunstable','hinckley','holt','ilkeston','kenilworth','kettering','kidderminster','kingswinford','leamington spa','leicester','lichfield','lincoln','long eaton','loughborough','luton','lutterworth','mansfield','market harborough','matlock','melton mowbray','milton keynes','northampton','nottingham','oldham','oxford','peterborough','retford','rugby','shrewsbury','solihull','stafford','stourbridge','stratford-upon-avon','sutton coldfield','tamworth','telford','wellingborough','wigston','wolverhampton','worcester','worksop'],
    'south-west':       ['bath','bideford','bodmin','bournemouth','bridgwater','brixham','camborne','chippenham','cinderford','cirencester','clevedon','colyton','cornwall','crediton','dorchester','exeter','exmouth','falmouth','gloucester','hartpury','hayle','helston','ivybridge','kingsbridge','launceston','liskeard','marlborough','nailsea','newquay','newton abbot','okehampton','paignton','penryn','penzance','perranporth','plymouth','poole','redruth','salisbury','south molton','st austell','st ives','st peter','stroud','swanage','taunton','tavistock','teignmouth','torquay','totton','trowbridge','truro','weston-super-mare','weymouth','wimborne','yeovil'],
    'north-east':       ['alnwick','ashington','billingham','bishop auckland','blaydon','blyth','consett','corbridge','darlington','durham','egremont','guisborough','hartlepool','hexham','middlesbrough','morpeth','newcastle upon tyne','peterlee','ponteland','redcar','spennymoor','stockton-on-tees','sunderland','thorne'],
    'wales':            ['aberaeron','abercynon','abertillery','aberystwyth','ammanford','bangor','beddau','bedwas','brecon','bridgend','brynamman','builth wells','caerphilly','cardiff','cardigan','carmarthen','colwyn bay','cwmavon','cwmcarn','ebbw vale','ferndale','glynneath','haverfordwest','lampeter','llandrindod wells','llandovery','llandudno','llanelli','llangefni','llangollen','llanrwst','maesteg','merthyr tydfil','neath','newbridge','newport','newtown','pencoed','penygraig','porthcawl','port talbot','pontypridd','resolven','risca','ruthin','skewen','swansea','treherbert','tumble','welshpool'],
    'scotland':         ['aberdeen','alloa','ayr','biggar','coldstream','crieff','currie','dundee','dunfermline','edinburgh','elgin','eyemouth','falkirk','forfar','fraserburgh','galashiels','glasgow','grangemouth','haddington','hamilton','hawick','inverness','jedburgh','kelso','kendal','kirkcaldy','langholm','linlithgow','livingston','melrose','montrose','morpeth','musselburgh','peebles','perth','selkirk','st andrews','stirling'],
    'northern-ireland': ['armagh','ballymena','belfast','dungannon']
  };

  var regionParam = new URLSearchParams(window.location.search).get('region');
  if (regionParam && REGION_CITIES[regionParam] && wraps.length) {
    var citiesForRegion = REGION_CITIES[regionParam];
    var shown = 0;
    wraps.forEach(function(w) {
      var city = (w.getAttribute('data-city') || '').toLowerCase();
      var name = (w.getAttribute('data-name') || '').toLowerCase();
      var matched = citiesForRegion.indexOf(city) !== -1;
      w.style.display = matched ? '' : 'none';
      if (matched) shown++;
    });
    // Update heading and count
    var regionLabel = regionParam.split('-').map(function(w){return w.charAt(0).toUpperCase()+w.slice(1);}).join(' ');
    var h1 = document.querySelector('h1');
    if (h1) h1.textContent = 'Rugby Clubs in ' + regionLabel;
    if (countEl) countEl.textContent = shown + ' club' + (shown !== 1 ? 's' : '') + ' found in ' + regionLabel;
    document.title = 'Rugby Clubs in ' + regionLabel + ' | UK Rugby Club Directory';
  }

})();

/* Click-to-load ground map: Google is only contacted when the visitor asks for the map */
document.querySelectorAll('button.map-load').forEach(function(b){
  b.addEventListener('click',function(){
    var slot=document.getElementById(b.getAttribute('aria-controls'));
    if(!slot||slot.firstChild) return;
    var f=document.createElement('iframe');
    f.src='https://www.google.com/maps?q='+encodeURIComponent(b.getAttribute('data-q'))+'&output=embed';
    f.title='Map: '+b.getAttribute('data-q'); f.loading='lazy'; f.referrerPolicy='no-referrer-when-downgrade';
    f.style.cssText='width:100%;height:220px;border:0;border-radius:6px;margin-top:.75rem';
    slot.appendChild(f); b.hidden=true;
  });
});

/* Open a collapsed <details> when a hash link targets something inside it */
(function () {
  function openForHash() {
    var id = decodeURIComponent((location.hash || '').slice(1));
    if (!id) return;
    var el = document.getElementById(id);
    if (!el) return;
    for (var p = el.closest('details'); p; p = p.parentElement && p.parentElement.closest('details')) {
      p.open = true;
    }
    if (el.scrollIntoView) el.scrollIntoView();
  }
  window.addEventListener('hashchange', openForHash);
  document.addEventListener('DOMContentLoaded', openForHash);
})();


/* ── Share bar ────────────────────────────────────────────────────────────────
   WordPress-style sharing on every page: a floating rail on desktop, a bottom
   bar on mobile. Uses the native share sheet where the browser has one (phones,
   which covers Instagram, WhatsApp etc.), plus X, Facebook, WhatsApp, LinkedIn,
   email and copy-link. Skipped on the 404 page. */
(function () {
  'use strict';
  if (window.__shareBarLoaded) return;
  window.__shareBarLoaded = true;

  function init() {
    if (document.querySelector('.share-rail') || /(^|\/)404\.html$/.test(location.pathname)) return;

    var canon = document.querySelector('link[rel="canonical"]');
    var url = (canon && canon.href) || (location.origin + location.pathname);
    var ogt = document.querySelector('meta[property="og:title"]');
    var title = ((ogt && ogt.content) || document.title || '').replace(/\s+/g, ' ').trim();
    var u = encodeURIComponent(url), t = encodeURIComponent(title);

    var I = {
      share: '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="M8.6 13.5l6.8 4M15.4 6.5l-6.8 4"/></svg>',
      x: '<svg viewBox="0 0 24 24" width="17" height="17" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-4.714-6.231-5.401 6.231H2.744l7.736-8.856L1.999 2.25H8.08l4.258 5.63 5.906-5.63zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>',
      fb: '<svg viewBox="0 0 24 24" width="17" height="17" fill="currentColor"><path d="M18 2h-3a5 5 0 00-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 011-1h3z"/></svg>',
      wa: '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21l1.65-4.9A8.5 8.5 0 1 1 8 19.4L3 21z"/><path d="M9 9.5c.5 2.2 2.3 4 4.5 4.5l1.2-1.2-1.6-.9-.7.5c-.8-.4-1.4-1-1.8-1.8l.5-.7-.9-1.6L9 9.5z" fill="currentColor" stroke="none"/></svg>',
      li: '<svg viewBox="0 0 24 24" width="17" height="17" fill="currentColor"><path d="M16 8a6 6 0 016 6v7h-4v-7a2 2 0 00-2-2 2 2 0 00-2 2v7h-4v-7a6 6 0 016-6zM2 9h4v12H2z"/><circle cx="4" cy="4" r="2"/></svg>',
      mail: '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="M22 7l-10 6L2 7"/></svg>',
      link: '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 007.07 0l3-3a5 5 0 00-7.07-7.07l-1.5 1.5"/><path d="M14 11a5 5 0 00-7.07 0l-3 3a5 5 0 007.07 7.07l1.5-1.5"/></svg>',
      ok: '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg>'
    };

    var items = [
      ['x', 'Share on X', 'https://twitter.com/intent/tweet?text=' + t + '&url=' + u],
      ['fb', 'Share on Facebook', 'https://www.facebook.com/sharer/sharer.php?u=' + u],
      ['wa', 'Share on WhatsApp', 'https://wa.me/?text=' + t + '%20' + u],
      ['li', 'Share on LinkedIn', 'https://www.linkedin.com/sharing/share-offsite/?url=' + u],
      ['mail', 'Share by email', 'mailto:?subject=' + t + '&body=' + t + '%0A%0A' + u]
    ];

    var css = document.createElement('style');
    css.textContent =
      '.share-rail{position:fixed;z-index:900;display:flex;gap:.4rem;align-items:center;font-family:inherit}' +
      '.share-rail-label{display:none}' +
      '.share-rail button,.share-rail a{display:inline-flex;align-items:center;justify-content:center;width:42px;height:42px;border-radius:50%;border:1px solid #d5dbe4;background:#fff;color:#293241;cursor:pointer;padding:0;text-decoration:none;box-shadow:0 2px 8px rgba(0,0,0,.12);transition:transform .12s,background .12s,color .12s}' +
      '.share-rail button:hover,.share-rail a:hover{background:#293241;color:#fff;transform:translateY(-1px)}' +
      '.share-rail button:focus-visible,.share-rail a:focus-visible{outline:3px solid #3d5a80;outline-offset:2px}' +
      '.share-rail .is-copied{background:#16a34a;color:#fff;border-color:#16a34a}' +
      '.share-rail-toast{position:absolute;right:calc(100% + 8px);top:50%;transform:translateY(-50%);background:#293241;color:#fff;font-size:.75rem;font-weight:600;padding:.35rem .7rem;border-radius:6px;white-space:nowrap;opacity:0;pointer-events:none;transition:opacity .15s}' +
      '.share-rail-toast.show{opacity:1}' +
      '.share-rail-toggle{display:none!important}' +
      '@media (min-width:1280px){.share-rail{left:14px;top:50%;transform:translateY(-50%);flex-direction:column}.share-rail-toast{right:auto;left:calc(100% + 8px)}}' +
      '@media (max-width:1279px){.share-rail{right:10px;top:50%;transform:translateY(-50%);flex-direction:column}.share-rail-toast{right:calc(100% + 8px)}' +
      '.share-rail-toggle{display:inline-flex!important;background:#293241!important;color:#fff!important;width:48px!important;height:48px!important;box-shadow:0 4px 14px rgba(0,0,0,.3)!important}' +
      '.share-rail:not(.open) .share-rail-item{display:none!important}}' +
      '@media print{.share-rail{display:none!important}}';
    document.head.appendChild(css);

    var rail = document.createElement('div');
    rail.className = 'share-rail';
    rail.setAttribute('role', 'group');
    rail.setAttribute('aria-label', 'Share this page');

    var label = document.createElement('span');
    label.className = 'share-rail-label';
    label.textContent = 'Share';
    rail.appendChild(label);

    var tg = document.createElement('button');
    tg.type = 'button'; tg.className = 'share-rail-toggle'; tg.innerHTML = I.share;
    tg.setAttribute('aria-label', 'Share this page'); tg.setAttribute('aria-expanded', 'false'); tg.title = 'Share';
    tg.addEventListener('click', function () {
      if (navigator.share) { navigator.share({ title: title, url: url }).catch(function () {}); return; }
      var open = rail.classList.toggle('open');
      tg.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { rail.classList.remove('open'); tg.setAttribute('aria-expanded', 'false'); } });
    rail.appendChild(tg);

    items.forEach(function (it) {
      var a = document.createElement('a');
      a.href = it[2]; a.innerHTML = I[it[0]];
      a.setAttribute('aria-label', it[1]); a.title = it[1];
      a.className = 'share-rail-item';
      if (it[0] !== 'mail') { a.target = '_blank'; a.rel = 'noopener'; }
      rail.appendChild(a);
    });

    var cb = document.createElement('button');
    cb.type = 'button'; cb.innerHTML = I.link;
    cb.setAttribute('aria-label', 'Copy link'); cb.title = 'Copy link';
    var toast = document.createElement('span');
    toast.className = 'share-rail-toast'; toast.setAttribute('role', 'status');
    cb.style.position = 'relative'; cb.className = 'share-rail-item';
    function done() {
      cb.innerHTML = I.ok; cb.classList.add('is-copied');
      toast.textContent = 'Link copied'; toast.classList.add('show');
      setTimeout(function () { cb.innerHTML = I.link; cb.classList.remove('is-copied'); toast.classList.remove('show'); }, 1800);
    }
    cb.addEventListener('click', function () {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(done, fallback);
      } else { fallback(); }
      function fallback() {
        var ta = document.createElement('textarea');
        ta.value = url; ta.style.position = 'fixed'; ta.style.opacity = '0';
        document.body.appendChild(ta); ta.select();
        try { document.execCommand('copy'); done(); } catch (e) {}
        document.body.removeChild(ta);
      }
    });
    cb.appendChild(toast);
    rail.appendChild(cb);

    document.body.appendChild(rail);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
}());
