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
  function openMob(){if(!ham||!mobNav)return;ham.setAttribute('aria-expanded','true');ham.classList.add('open');mobNav.removeAttribute('aria-hidden');mobNav.classList.add('open');document.body.style.overflow='hidden';}
  function closeMob(){if(!ham||!mobNav)return;ham.setAttribute('aria-expanded','false');ham.classList.remove('open');mobNav.setAttribute('aria-hidden','true');mobNav.classList.remove('open');document.body.style.overflow='';}
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
