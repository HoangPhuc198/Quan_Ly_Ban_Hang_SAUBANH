/**
 * Danh sách sản phẩm — lọc/tìm client-side.
 */
(function () {
  var search = document.getElementById('productSearch');
  var stockFilter = document.getElementById('productStockFilter');
  var rows = document.querySelectorAll('#productTable .product-row');
  if (!rows.length) return;

  function apply() {
    var q = (search && search.value || '').trim().toLowerCase();
    var sf = (stockFilter && stockFilter.value) || 'all';
    rows.forEach(function (tr) {
      var hay = tr.getAttribute('data-search') || '';
      var st = tr.getAttribute('data-stock') || '';
      var okQ = !q || hay.indexOf(q) !== -1;
      var okS = sf === 'all' || st === sf;
      tr.style.display = okQ && okS ? '' : 'none';
    });
  }

  if (search) search.addEventListener('input', apply);
  if (stockFilter) stockFilter.addEventListener('change', apply);
})();
