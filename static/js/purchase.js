/**
 * Nhập hàng — gợi nhớ mã phiếu giữa các form (localStorage).
 */
(function () {
  var formCreate = document.querySelector('form[action*="purchase/create"]');
  if (formCreate) {
    formCreate.addEventListener('submit', function () {
      var ma = formCreate.querySelector('[name="ma_hdn"]');
      if (ma && ma.value) {
        try {
          localStorage.setItem('pur_last_ma_hdn', ma.value.trim());
        } catch (e) {}
      }
    });
  }
  try {
    var last = localStorage.getItem('pur_last_ma_hdn');
    var inp = document.getElementById('pur_ma_hdn');
    if (last && inp && !inp.value) inp.value = last;
  } catch (e) {}
})();
