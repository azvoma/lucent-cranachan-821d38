/* UK Rugby Club Directory — fixes.js v4
   Favicon, .ico and Apple touch icon are now set in each page's <head>.
   This script only adds the SVG favicon if a page is missing one. */
(function(){
  'use strict';
  if (!document.querySelector('link[rel~="icon"]')) {
    var lnk = document.createElement('link');
    lnk.rel = 'icon'; lnk.type = 'image/svg+xml'; lnk.href = '/favicon.svg';
    document.head.appendChild(lnk);
  }
}());
