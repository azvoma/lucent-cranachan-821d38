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
})();
