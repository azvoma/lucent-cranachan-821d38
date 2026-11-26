/* Rugby Joints: section counts for live search, and opening the A-Z finder from a jump link. */
(function () {
  var input = document.getElementById('listing-search');
  var wraps = document.querySelectorAll('.club-card-wrap');
  var secs = document.querySelectorAll('.rj-section');
  var count = document.getElementById('rj-count');
  var none = document.getElementById('rj-none');
  var total = wraps.length;

  function refresh() {
    var shown = 0;
    secs.forEach(function (sec) {
      var n = 0;
      sec.querySelectorAll('.club-card-wrap').forEach(function (w) { if (w.style.display !== 'none') n++; });
      sec.hidden = n === 0;
      var c = sec.querySelector('.rj-sec-count b');
      if (c) c.textContent = n;
      shown += n;
    });
    if (count) count.textContent = shown === total ? 'Showing all ' + total + ' listings' : 'Showing ' + shown + ' of ' + total + ' listings';
    if (none) none.hidden = shown !== 0;
  }

  if (input) {
    input.addEventListener('input', function () { setTimeout(refresh, 0); });
    if (input.value) setTimeout(refresh, 0);
  }

  function openFinder() {
    var d = document.getElementById('rj-find');
    if (d && !d.open) d.open = true;
  }
  document.querySelectorAll('[data-open="rj-find"]').forEach(function (a) {
    a.addEventListener('click', openFinder);
  });
  if (location.hash === '#rj-find') openFinder();

  /* Opening a listing link from the A-Z finder: keep it simple, the browser scrolls to the card. */
})();
