document.addEventListener('DOMContentLoaded', function () {
  // Sidebar toggle (mobile)
  const menuToggle = document.querySelector('.mobile-menu-toggle');
  const sidebar = document.querySelector('.sidebar');
  const overlay = document.querySelector('.sidebar-overlay');

  if (menuToggle && sidebar) {
    menuToggle.addEventListener('click', function () {
      sidebar.classList.toggle('show');
      if (overlay) overlay.classList.toggle('show');
    });

    if (overlay) {
      overlay.addEventListener('click', function () {
        sidebar.classList.remove('show');
        overlay.classList.remove('show');
      });
    }
  }

  // Auto-dismiss alerts after 5s
  document.querySelectorAll('.alert-dismissible').forEach(function (alert) {
    setTimeout(function () {
      const btn = alert.querySelector('.btn-close');
      if (btn) btn.click();
    }, 5000);
  });

  // Highlight active nav item
  const currentPath = window.location.pathname;
  document.querySelectorAll('.sidebar-nav-item').forEach(function (item) {
    const href = item.getAttribute('href');
    if (currentPath === href || (href !== '/' && currentPath.startsWith(href))) {
      item.classList.add('active');
    }
  });

  // Delete confirmations
  document.querySelectorAll('[data-confirm]').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      if (!confirm(this.dataset.confirm || 'Are you sure?')) {
        e.preventDefault();
      }
    });
  });
});
