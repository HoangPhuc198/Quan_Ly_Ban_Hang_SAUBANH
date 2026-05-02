/**
 * POS — tìm kiếm bảng sản phẩm, đồng bộ mã khi chọn.
 */
(function () {
  var search = document.getElementById('posProductSearch');
  var table = document.getElementById('posProductTable');
  if (!table) return;

  function filterRows(q) {
    q = (q || '').trim().toLowerCase();
    table.querySelectorAll('.pos-product-row').forEach(function (tr) {
      var hay = tr.getAttribute('data-search') || '';
      tr.style.display = !q || hay.indexOf(q) !== -1 ? '' : 'none';
    });
  }

  if (search) {
    search.addEventListener('input', function () {
      filterRows(search.value);
    });
  }

  document.querySelectorAll('.btn-select-product').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var ma = btn.getAttribute('data-ma') || '';
      var inp = document.getElementById('add_ma_spct');
      if (inp) inp.value = ma;
      inp && inp.focus();
    });
  });

  function syncInvoiceCode(val) {
    ['add_ma_hdb', 'pay_ma_hdb'].forEach(function (id) {
      var el = document.getElementById(id);
      if (el && !el.value) el.value = val;
    });
  }

  var formCreate = document.querySelector('form[action*="create-invoice"]');
  if (formCreate) {
    formCreate.addEventListener('submit', function () {
      var ma = formCreate.querySelector('[name="ma_hdb"]');
      if (ma && ma.value) {
        try {
          localStorage.setItem('pos_last_ma_hdb', ma.value.trim());
        } catch (e) {}
      }
    });
  }

  try {
    var last = localStorage.getItem('pos_last_ma_hdb');
    if (last) syncInvoiceCode(last);
  } catch (e) {}

  var addForm = document.getElementById('formAddItem');
  if (addForm) {
    addForm.addEventListener('submit', function () {
      var ma = document.getElementById('add_ma_hdb');
      if (ma && ma.value) syncInvoiceCode(ma.value.trim());
    });
  }
})();
