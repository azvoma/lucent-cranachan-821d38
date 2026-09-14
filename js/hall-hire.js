/* hall-hire.js — UK Rugby Club Directory
   Injects a Hall Hire / Venue section into every club listing page.
   The section appears between the Teams section and the Nearby section.
   Data is driven by hall-hire-data.json — add clubs there to populate real details.
   For clubs with no entry, shows a "not currently listed" state with a claim CTA.
   Add <script src="../js/hall-hire.js"></script> before </body> on listing pages.
   (Or add it to the global footer in the page generator.)
*/
(function () {
  'use strict';

  /* Only run on club listing pages */
  var path = window.location.pathname;
  var isClub = path.includes('/club/') || /\/[a-z0-9-]+-(?:rfc|rlfc|rufc|fc|rugby|rfc)\.html/.test(path);
  /* Also detect by presence of .club-hero on page */
  if (!document.querySelector('.club-hero') && !document.querySelector('.hero-name')) return;

  /* Derive the club slug from the URL */
  var slug = path.replace(/.*\//, '').replace(/\.html$/, '');

  /* Depth prefix for asset paths (listing pages are one level deep) */
  var depth = Math.max(0, (path.match(/\//g) || []).length - 1);
  var prefix = depth === 0 ? '' : '../';

  /* Load the hall hire data */
  fetch(prefix + 'js/hall-hire-data.json')
    .then(function (r) { return r.ok ? r.json() : {}; })
    .catch(function () { return {}; })
    .then(function (data) {
      var info = data[slug] || null;
      buildSection(info, slug, prefix);
    });

  function esc(s) {
    return String(s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function buildSection(info, slug, prefix) {
    var clubName = (document.querySelector('.hero-name') || {}).textContent || 'This Club';

    var html;
    if (info && info.available) {
      /* Full hall hire section */
      var specs = [
        info.capacity ? { label: 'Capacity', value: info.capacity + ' guests' } : null,
        info.size     ? { label: 'Floor size', value: info.size } : null,
        info.hire_rate ? { label: 'Hire from', value: info.hire_rate } : null,
        info.min_hire  ? { label: 'Minimum hire', value: info.min_hire } : null,
      ].filter(Boolean);

      var features = (info.features || []).map(function (f) {
        return '<li class="hall-feature"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>' + esc(f) + '</li>';
      }).join('');

      var specHtml = specs.map(function (s) {
        return '<div class="hall-spec-item"><div class="hall-spec-label">' + esc(s.label) + '</div><div class="hall-spec-value">' + esc(s.value) + '</div></div>';
      }).join('');

      var contact = info.contact_email
        ? '<a href="mailto:' + esc(info.contact_email) + '" class="btn btn-outline-wh" style="width:100%;justify-content:center;margin-top:.5rem">Send Enquiry</a>'
        : '<a href="' + prefix + 'contact-us.html" class="btn btn-outline-wh" style="width:100%;justify-content:center;margin-top:.5rem">Get in Touch</a>';

      html = '<section class="sec sec-off" id="hall-hire">'
        + '<div class="con">'
        + '<div class="sh"><span class="ey">Venue &amp; Facilities</span>'
        + '<h2>Hall Hire at ' + esc(clubName) + '</h2>'
        + '<p>' + esc(info.description || clubName + ' offers hall and venue hire for events, functions, and community gatherings.') + '</p>'
        + '</div>'
        + '<div class="hall-hire-layout">'
        + '<div>'
        + '<div class="hall-specs">' + specHtml + '</div>'
        + (features ? '<ul class="hall-features-list">' + features + '</ul>' : '')
        + (info.notes ? '<p style="font-size:.875rem;color:var(--text-secondary);margin-top:1rem;padding:1rem;background:var(--bg-soft);border-radius:10px;border:1px solid var(--border)">' + esc(info.notes) + '</p>' : '')
        + '</div>'
        + '<div>'
        + '<div class="hall-enquiry-card">'
        + '<h3>Book the Venue</h3>'
        + (info.hire_rate ? '<div class="hall-price">' + esc(info.hire_rate) + ' <span>per session</span></div>' : '')
        + '<p>' + esc(info.booking_note || 'Contact the club directly to check availability and make a booking.') + '</p>'
        + contact
        + '</div>'
        + '</div>'
        + '</div>'
        + '</div>'
        + '</section>';
    } else {
      /* Not available / unclaimed state */
      html = '<section class="sec" id="hall-hire">'
        + '<div class="con">'
        + '<div class="sh"><span class="ey">Venue &amp; Facilities</span>'
        + '<h2>Hall Hire at ' + esc(clubName) + '</h2></div>'
        + '<div class="hall-unavailable">'
        + '<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"><rect x="3" y="3" width="18" height="18" rx="3"/><path d="M9 9h6M9 12h6M9 15h4"/></svg>'
        + '<p><strong>Hall hire information not yet listed</strong><br>Many rugby clubs offer venue hire for events, weddings, parties and corporate functions.<br>If this is your club, <a href="' + prefix + 'claim.html?club=' + esc(slug) + '">claim your listing</a> to add hire details and reach local event bookers.</p>'
        + '<a href="' + prefix + 'claim.html?club=' + esc(slug) + '" class="btn btn-red btn-sm" style="margin-top:.5rem">Claim &amp; Add Venue Details</a>'
        + '</div>'
        + '</div>'
        + '</section>';
    }

    /* Insert before #nearby or before </main> */
    var nearby = document.getElementById('nearby');
    var main   = document.querySelector('main');

    var tmp = document.createElement('div');
    tmp.innerHTML = html;
    var section = tmp.firstElementChild;

    if (nearby) {
      main.insertBefore(section, nearby);
    } else if (main) {
      main.appendChild(section);
    }

    /* Add Hall Hire to sidebar quick links if present */
    var quickLinks = document.querySelector('.aside-card ul');
    if (quickLinks) {
      var li = document.createElement('li');
      li.innerHTML = '<a href="#hall-hire" style="color:var(--violet)">→ Hall &amp; Venue Hire</a>';
      /* Insert after the first link */
      var first = quickLinks.querySelector('li');
      if (first && first.nextSibling) {
        quickLinks.insertBefore(li, first.nextSibling);
      } else {
        quickLinks.appendChild(li);
      }
    }
  }

})();
