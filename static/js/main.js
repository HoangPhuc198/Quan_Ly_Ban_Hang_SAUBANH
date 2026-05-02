/**
 * Script chung — offcanvas menu, flash dismiss.
 */
(function () {
  document.documentElement.classList.add('js-ready');

  var el = document.getElementById('sidebarOffcanvas');
  if (el && typeof bootstrap !== 'undefined') {
    el.querySelectorAll('.sidebar-nav-link').forEach(function (a) {
      a.addEventListener('click', function () {
        var inst = bootstrap.Offcanvas.getInstance(el);
        if (inst) inst.hide();
      });
    });
  }
})();
