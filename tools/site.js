// Series tabs on the home page: show only the cards of the picked series.
document.querySelectorAll('.tab').forEach(function (tab) {
  tab.addEventListener('click', function () {
    var pick = tab.dataset.tab;
    document.querySelectorAll('.tab').forEach(function (t) { t.classList.toggle('on', t === tab); });
    document.querySelectorAll('.pcard[data-series]').forEach(function (c) { c.hidden = pick !== 'all' && c.dataset.series !== pick; });
    document.querySelectorAll('.blurb').forEach(function (b) { b.hidden = b.dataset.blurb !== pick; });
    try { history.replaceState(null, '', pick === 'all' ? '#plugins' : '#' + pick); } catch (e) {}
  });
});
var start = location.hash.slice(1);
var startTab = document.querySelector('.tab[data-tab="' + start + '"]');
if (startTab) startTab.click();
