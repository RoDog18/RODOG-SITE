// Home page tabs: All Plugins shows every plugin grouped by effect, a series tab shows only that series.
document.querySelectorAll('.tab').forEach(function (tab) {
  tab.addEventListener('click', function () {
    var pick = tab.dataset.tab;
    document.querySelectorAll('.tab').forEach(function (t) { t.classList.toggle('on', t === tab); });
    document.getElementById('by-effect').hidden = pick !== 'all';
    document.getElementById('by-series').hidden = pick === 'all';
    document.querySelectorAll('#by-series .pcard').forEach(function (c) { c.hidden = c.dataset.series !== pick; });
    document.querySelectorAll('.blurb').forEach(function (b) { b.hidden = b.dataset.blurb !== pick; });
    try { history.replaceState(null, '', pick === 'all' ? '#plugins' : '#' + pick); } catch (e) {}
  });
});
var start = location.hash.slice(1);
var startTab = document.querySelector('.tab[data-tab="' + start + '"]');
if (startTab) startTab.click();

// Fade the logo and dog back as the page scrolls, so the plugins pass over them.
var stage = document.querySelector('.stage');
if (stage) {
  var fade = function () {
    var t = Math.min(window.scrollY / (window.innerHeight * 0.6), 1);
    stage.style.opacity = String(1 - t * 0.85);
  };
  window.addEventListener('scroll', fade, { passive: true });
  fade();
}
