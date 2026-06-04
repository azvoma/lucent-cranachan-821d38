/* UK Rugby Club Directory — fixes.js v3
   Blog nav is hard-coded in HTML.
   Region filter is in main.js.
   This file handles: favicon only. */
(function(){
  'use strict';
  document.querySelectorAll('link[rel*="icon"]').forEach(function(el){ el.parentNode.removeChild(el); });
  var lnk = document.createElement('link');
  lnk.rel = 'icon'; lnk.type = 'image/svg+xml'; lnk.href = '/favicon.svg';
  document.head.appendChild(lnk);
}());
