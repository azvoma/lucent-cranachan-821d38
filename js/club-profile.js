/* club-profile.js - interactions for the UK Rugby Club Profile template.
   No dependencies. Loaded with defer after main.js. Progressive enhancement:
   the page content, links and JSON-LD all work without it. */
(function () {
  'use strict';
  var doc = document, root = doc.documentElement;
  var $ = function (s, c) { return (c || doc).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || doc).querySelectorAll(s)); };
  var mqMobile = window.matchMedia('(max-width: 1023px)');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var lastTrigger = null;

  /* ---- 1. Sticky offsets: real header + sub-nav heights ------------------ */
  function setOffsets() {
    var hdr = $('#site-header'), sub = $('.cp-subnav');
    if (hdr) root.style.setProperty('--cp-hdr', hdr.offsetHeight + 'px');
    if (sub) root.style.setProperty('--cp-sub', sub.offsetHeight + 'px');
  }
  setOffsets();
  window.addEventListener('resize', setOffsets, { passive: true });
  if (doc.fonts && doc.fonts.ready) doc.fonts.ready.then(setOffsets);

  /* Keep the mobile action bar above the site's fixed cookie banner (first visit only) */
  var cookie = $('#cookie-banner');
  function syncCookie() {
    root.style.setProperty('--cp-cookie', cookie && cookie.classList.contains('show') ? cookie.offsetHeight + 'px' : '0px');
  }
  if (cookie) { syncCookie(); new MutationObserver(syncCookie).observe(cookie, { attributes: true, attributeFilter: ['class'] }); window.addEventListener('resize', syncCookie, { passive: true }); }

  /* ---- 2. Scroll-spy for the sub-nav ------------------------------------- */
  var links = $$('.cp-subnav a');
  var targets = links.map(function (a) { return $(a.getAttribute('href')); }).filter(Boolean);
  function setCurrent(id) {
    links.forEach(function (a) {
      if (a.getAttribute('href') === '#' + id) a.setAttribute('aria-current', 'true');
      else a.removeAttribute('aria-current');
    });
    var cur = $('.cp-subnav a[aria-current="true"]');
    if (cur && cur.scrollIntoView && mqMobile.matches) {
      var ul = cur.parentNode.parentNode;
      ul.scrollTo({ left: cur.offsetLeft - 16, behavior: reduce ? 'auto' : 'smooth' });
    }
  }
  function spy() {
    var line = (parseFloat(getComputedStyle(root).getPropertyValue('--cp-hdr')) || 72) +
               (parseFloat(getComputedStyle(root).getPropertyValue('--cp-sub')) || 48) + 24;
    var current = null;
    targets.forEach(function (t) { if (t.getBoundingClientRect().top <= line) current = t; });
    setCurrent(current ? current.id : '');
  }
  var ticking = false;
  window.addEventListener('scroll', function () {
    if (ticking) return; ticking = true;
    requestAnimationFrame(function () { spy(); ticking = false; });
  }, { passive: true });
  spy();
  // Move keyboard focus to the section after an anchor jump (scroll-margin handles the offset).
  links.forEach(function (a) {
    a.addEventListener('click', function () {
      var t = $(a.getAttribute('href'));
      if (!t) return;
      setTimeout(function () {
        var h = $('h2', t); if (!h) return;
        h.setAttribute('tabindex', '-1'); h.focus({ preventScroll: true });
      }, reduce ? 0 : 450);
    });
  });

  /* ---- 3. Tabs (teams & age groups) -------------------------------------- */
  $$('[data-tabs]').forEach(function (wrap) {
    var tabs = $$('[role="tab"]', wrap), panels = $$('[role="tabpanel"]', wrap);
    function select(i, focus) {
      tabs.forEach(function (t, n) {
        var on = n === i;
        t.setAttribute('aria-selected', on); t.tabIndex = on ? 0 : -1;
        panels[n].hidden = !on;
      });
      if (focus) tabs[i].focus();
      if (tabs[i].scrollIntoView) tabs[i].parentNode.scrollTo({ left: tabs[i].offsetLeft - 12, behavior: reduce ? 'auto' : 'smooth' });
    }
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { select(i); });
      t.addEventListener('keydown', function (e) {
        var k = e.key, n = null;
        if (k === 'ArrowRight') n = (i + 1) % tabs.length;
        else if (k === 'ArrowLeft') n = (i - 1 + tabs.length) % tabs.length;
        else if (k === 'Home') n = 0; else if (k === 'End') n = tabs.length - 1;
        if (n !== null) { e.preventDefault(); select(n, true); }
      });
    });
  });

  /* ---- 4. Read-more accordions (collapsed on mobile only) ---------------- */
  $$('[data-readmore]').forEach(function (box) {
    var body = $('.cp-rm-body', box), btn = $('.cp-rm-btn', box);
    if (!body || !btn) return;
    function collapsedState() {
      if (!mqMobile.matches) { body.style.maxHeight = ''; box.classList.remove('is-open'); btn.hidden = true; return; }
      // Hide the toggle if the text already fits
      body.style.maxHeight = ''; box.classList.remove('is-open');
      btn.hidden = body.scrollHeight <= body.clientHeight + 4;
      btn.setAttribute('aria-expanded', 'false'); btn.textContent = 'Read more';
    }
    btn.addEventListener('click', function () {
      var open = btn.getAttribute('aria-expanded') !== 'true';
      btn.setAttribute('aria-expanded', open); btn.textContent = open ? 'Show less' : 'Read more';
      box.classList.toggle('is-open', open);
      body.style.maxHeight = open ? body.scrollHeight + 'px' : '';
    });
    collapsedState();
    mqMobile.addEventListener ? mqMobile.addEventListener('change', collapsedState) : mqMobile.addListener(collapsedState);
  });

  /* ---- 5. Dialogs (claim, rate, enquiry drawer) -------------------------- */
  function openDialog(d, trigger) {
    if (!d) return;
    lastTrigger = trigger || doc.activeElement;
    if (d.showModal) d.showModal(); else d.setAttribute('open', '');
    doc.body.classList.add('dialog-open');
    var first = $('input:not([type=hidden]):not([tabindex="-1"]), select, textarea', d);
    if (first) first.focus();
  }
  function closeDialog(d) {
    if (d && d.open) d.close();
  }
  $$('dialog.cp-dialog').forEach(function (d) {
    d.addEventListener('close', function () {
      if (!$$('dialog.cp-dialog[open]').length) doc.body.classList.remove('dialog-open');
      if (d.id === 'enquire-drawer') returnEnquireCard();
      if (lastTrigger && lastTrigger.focus) lastTrigger.focus();
    });
    d.addEventListener('click', function (e) { if (e.target === d) closeDialog(d); }); // backdrop
  });
  $$('[data-open-dialog]').forEach(function (b) {
    b.addEventListener('click', function (e) { e.preventDefault(); openDialog($('#' + b.getAttribute('data-open-dialog')), b); });
  });
  $$('[data-close-dialog]').forEach(function (b) {
    b.addEventListener('click', function () { closeDialog(b.closest('dialog')); });
  });

  /* ---- 6. Enquire / Join: sidebar on desktop, bottom sheet on mobile ----- */
  var card = $('[data-enquire-card]'), aside = card && card.parentNode, drawer = $('#enquire-drawer');
  function returnEnquireCard() {
    if (card && aside && card.parentNode !== aside) aside.insertBefore(card, aside.firstChild);
  }
  function openEnquire(trigger, role) {
    if (!card) return;
    var sel = $('select[name=role]', card);
    if (role && sel) sel.value = role;
    if (mqMobile.matches && drawer) {
      $('[data-drawer-body]', drawer).appendChild(card);
      openDialog(drawer, trigger);
    } else {
      card.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
      setTimeout(function () { var n = $('input[name=name]', card); if (n) n.focus({ preventScroll: true }); }, reduce ? 0 : 400);
    }
  }
  $$('[data-open-enquire]').forEach(function (b) {
    b.addEventListener('click', function (e) { e.preventDefault(); openEnquire(b, b.getAttribute('data-role')); });
  });
  mqMobile.addEventListener && mqMobile.addEventListener('change', function () {
    if (!mqMobile.matches) closeDialog(drawer);
  });

  /* ---- 7. Form validation + submit --------------------------------------- */
  var EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  var uid = 0;
  function errEl(group) {
    var e = $('.cp-err', group);
    if (e && !e.id) e.id = 'cp-err-' + (++uid);
    return e;
  }
  function message(el) {
    var v = (el.value || '').trim();
    if (el.required && !v) {
      if (el.tagName === 'SELECT') return 'Please choose an option.';
      return 'This field is required.';
    }
    if (el.type === 'email' && v && !EMAIL.test(v)) return 'Enter a valid email address, e.g. name@example.com.';
    var min = parseInt(el.getAttribute('minlength'), 10);
    if (min && v && v.length < min) return 'Please enter at least ' + min + ' characters.';
    return '';
  }
  function setState(group, el, msg) {
    var e = errEl(group);
    group.classList.toggle('is-invalid', !!msg);
    group.classList.toggle('is-valid', !msg && !!(el.value || '').trim());
    if (e) e.textContent = msg;
    if (el) { el.setAttribute('aria-invalid', msg ? 'true' : 'false'); if (e) el.setAttribute('aria-describedby', e.id); }
  }
  function validateField(el) {
    var group = el.closest('.cp-field'); if (!group) return true;
    var msg = message(el); setState(group, el, msg); return !msg;
  }
  function validateRatings(set) {
    var checked = $('input:checked', set), e = errEl(set);
    if (e) e.textContent = checked ? '' : 'Please choose a rating from 1 to 5.';
    set.classList.toggle('is-invalid', !checked);
    return !!checked;
  }
  $$('form[data-validate]').forEach(function (form) {
    var touched = new WeakSet();
    $$('.cp-field input, .cp-field select, .cp-field textarea', form).forEach(function (el) {
      el.addEventListener('blur', function () { touched.add(el); validateField(el); });
      el.addEventListener('input', function () { if (touched.has(el) || el.closest('.is-invalid')) validateField(el); });
      el.addEventListener('change', function () { touched.add(el); validateField(el); });
    });
    $$('.cp-rate-set', form).forEach(function (set) {
      $$('input', set).forEach(function (r) { r.addEventListener('change', function () { validateRatings(set); }); });
    });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var firstBad = null;
      $$('.cp-field input, .cp-field select, .cp-field textarea', form).forEach(function (el) {
        touched.add(el); if (!validateField(el) && !firstBad) firstBad = el;
      });
      $$('.cp-rate-set', form).forEach(function (set) { if (!validateRatings(set) && !firstBad) firstBad = $('input', set); });
      var status = $('.cp-form-status', form);
      if (firstBad) {
        status.className = 'cp-form-status bad'; status.textContent = 'Please fix the highlighted fields.';
        firstBad.focus(); return;
      }
      status.className = 'cp-form-status'; status.textContent = '';
      var hp = $('[name=bot-field]', form);
      var btn = $('.cp-submit', form), label = $('.cp-btn-label', btn), orig = label.textContent;
      btn.classList.add('is-loading'); btn.disabled = true; btn.setAttribute('aria-busy', 'true'); label.textContent = 'Sending…';

      function done(ok) {
        btn.classList.remove('is-loading'); btn.disabled = false; btn.removeAttribute('aria-busy'); label.textContent = orig;
        if (ok) {
          var name = form.getAttribute('name');
          var msgs = {
            'club-enquiry': 'Thanks! Your enquiry has been sent to the club. They usually reply within a few days.',
            'club-claim': 'Request received. We will verify your details and email you within 2 working days.',
            'ground-rating': 'Thanks for rating this ground. Your rating will appear once it has been checked.'
          };
          status.className = 'cp-form-status ok'; status.textContent = msgs[name] || 'Thanks, we have received your message.';
          form.reset(); form.classList.add('is-done');
          $$('.is-valid, .is-invalid', form).forEach(function (n) { n.classList.remove('is-valid', 'is-invalid'); });
          status.setAttribute('tabindex', '-1'); status.focus();
        } else {
          status.className = 'cp-form-status bad';
          status.textContent = 'Sorry, that did not send. Please try again or email hello@ukrugbyclubdirectory.co.uk.';
        }
      }
      if ((hp && hp.value) || form.getAttribute('data-demo') === 'true') {   // honeypot or demo: simulate
        setTimeout(function () { done(true); }, 900); return;
      }
      fetch(form.getAttribute('action') || '/', {
        method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams(new FormData(form)).toString()
      }).then(function (r) { done(r.ok); }).catch(function () { done(false); });
    });
  });

  /* ---- 8. Lazy map (loads on approach or on tap; skipped on Save-Data) --- */
  $$('[data-map]').forEach(function (m) {
    var loaded = false;
    function load() {
      if (loaded) return; loaded = true;
      var f = doc.createElement('iframe');
      f.src = m.getAttribute('data-src'); f.title = m.getAttribute('data-title') || 'Map';
      f.loading = 'lazy'; f.referrerPolicy = 'no-referrer-when-downgrade'; f.setAttribute('allowfullscreen', '');
      m.appendChild(f); var b = $('.cp-map-load', m); if (b) b.remove();
    }
    var btn = $('.cp-map-load', m); if (btn) btn.addEventListener('click', load);
    var saveData = navigator.connection && navigator.connection.saveData;
    if ('IntersectionObserver' in window && !saveData) {
      new IntersectionObserver(function (es, o) { if (es[0].isIntersecting) { load(); o.disconnect(); } }, { rootMargin: '400px' }).observe(m);
    }
  });

  /* ---- 9. Hide fixtures that have already been played -------------------- */
  (function () {
    var list = $('.cp-fixtures'); if (!list) return;
    var d = new Date(), today = d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
    var items = $$('.cp-fix', list), left = 0;
    items.forEach(function (li) { if (li.getAttribute('data-date') < today) li.hidden = true; else left++; });
    if (!left) {
      var p = doc.createElement('p'); p.className = 'cp-empty';
      p.innerHTML = '<span><strong>No upcoming fixtures listed</strong></span><a class="btn cp-btn-ghost cp-btn-sm" href="../claim.html">Add fixtures</a>';
      list.replaceWith(p);
    }
  })();
})();
