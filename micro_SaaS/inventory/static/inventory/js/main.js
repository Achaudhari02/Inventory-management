/**
 * Modern Inventory SaaS - Main JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
  // Sidebar Toggle for Mobile
  initSidebarToggle();

  // Auto-dismiss alerts
  initAlertAutoDismiss();

  // Active navigation highlighting
  highlightActiveNav();

  // Form enhancements
  initFormEnhancements();

  // Stock badge coloring
  initStockBadges();
});

/**
 * Initialize sidebar toggle functionality for mobile
 */
function initSidebarToggle() {
  const menuToggle = document.querySelector('.mobile-menu-toggle');
  const sidebar = document.querySelector('.sidebar');
  const overlay = document.querySelector('.sidebar-overlay');

  if (!menuToggle || !sidebar) return;

  // Toggle sidebar
  menuToggle.addEventListener('click', function() {
    sidebar.classList.toggle('show');
    if (overlay) {
      overlay.classList.toggle('show');
    }
  });

  // Close sidebar when clicking overlay
  if (overlay) {
    overlay.addEventListener('click', function() {
      sidebar.classList.remove('show');
      overlay.classList.remove('show');
    });
  }

  // Close sidebar on window resize if desktop
  window.addEventListener('resize', function() {
    if (window.innerWidth >= 992) {
      sidebar.classList.remove('show');
      if (overlay) {
        overlay.classList.remove('show');
      }
    }
  });
}

/**
 * Auto-dismiss alert messages after 5 seconds
 */
function initAlertAutoDismiss() {
  const alerts = document.querySelectorAll('.alert-dismissible');

  alerts.forEach(function(alert) {
    setTimeout(function() {
      const closeButton = alert.querySelector('.btn-close');
      if (closeButton) {
        closeButton.click();
      }
    }, 5000);
  });
}

/**
 * Highlight active navigation item based on current URL
 */
function highlightActiveNav() {
  const currentPath = window.location.pathname;
  const navItems = document.querySelectorAll('.sidebar-nav-item');

  navItems.forEach(function(item) {
    const itemPath = item.getAttribute('href');

    // Exact match or starts with path (for nested routes)
    if (currentPath === itemPath ||
        (itemPath !== '/' && currentPath.startsWith(itemPath))) {
      item.classList.add('active');
    }
  });
}

/**
 * Form enhancement - add focus styles and validation feedback
 */
function initFormEnhancements() {
  // Add focus class to form groups
  const formInputs = document.querySelectorAll('.form-control');

  formInputs.forEach(function(input) {
    input.addEventListener('focus', function() {
      this.parentElement.classList.add('focused');
    });

    input.addEventListener('blur', function() {
      this.parentElement.classList.remove('focused');
    });
  });

  // Prevent form double submission
  const forms = document.querySelectorAll('form');
  forms.forEach(function(form) {
    form.addEventListener('submit', function(e) {
      const submitButton = form.querySelector('[type="submit"]');
      if (submitButton && !submitButton.disabled) {
        submitButton.disabled = true;
        submitButton.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';

        // Re-enable after 3 seconds as fallback
        setTimeout(function() {
          submitButton.disabled = false;
          submitButton.innerHTML = submitButton.dataset.originalText || 'Submit';
        }, 3000);
      }
    });
  });
}

/**
 * Automatically color-code stock badges based on quantity vs reorder level
 */
function initStockBadges() {
  const stockRows = document.querySelectorAll('[data-quantity]');

  stockRows.forEach(function(row) {
    const quantity = parseInt(row.dataset.quantity);
    const reorderLevel = parseInt(row.dataset.reorder);
    const badge = row.querySelector('.stock-badge');

    if (!badge || isNaN(quantity) || isNaN(reorderLevel)) return;

    // Remove existing classes
    badge.classList.remove('good', 'low', 'critical');

    // Add appropriate class
    if (quantity === 0) {
      badge.classList.add('critical');
    } else if (quantity <= reorderLevel) {
      badge.classList.add('low');
    } else {
      badge.classList.add('good');
    }
  });
}

/**
 * Product selection handler for transaction form
 * Updates current stock display when product is selected
 */
function initProductStockDisplay() {
  const productSelect = document.querySelector('#id_product');
  const stockDisplay = document.querySelector('#current-stock-display');

  if (!productSelect || !stockDisplay) return;

  productSelect.addEventListener('change', function() {
    const selectedOption = this.options[this.selectedIndex];
    const stockLevel = selectedOption.dataset.stock;

    if (stockLevel !== undefined) {
      stockDisplay.textContent = `Current Stock: ${stockLevel}`;
      stockDisplay.classList.remove('d-none');
    } else {
      stockDisplay.classList.add('d-none');
    }
  });
}

/**
 * Transaction type toggle styling
 */
function initTransactionTypeToggle() {
  const typeInputs = document.querySelectorAll('input[name="type"]');

  typeInputs.forEach(function(input) {
    input.addEventListener('change', function() {
      const label = this.closest('label') || this.nextElementSibling;
      if (!label) return;

      // Remove active class from all labels
      document.querySelectorAll('.transaction-type-label').forEach(function(l) {
        l.classList.remove('active');
      });

      // Add active class to selected
      if (this.checked) {
        label.classList.add('active');
      }
    });
  });
}

/**
 * Search filter enhancement - debounced search
 */
function initSearchDebounce() {
  const searchInput = document.querySelector('input[name="search_query"]');
  let searchTimeout;

  if (!searchInput) return;

  searchInput.addEventListener('input', function() {
    clearTimeout(searchTimeout);
    const form = this.closest('form');

    searchTimeout = setTimeout(function() {
      if (form) {
        // Auto-submit form after 500ms of no typing
        // Uncomment if you want auto-submit:
        // form.submit();
      }
    }, 500);
  });
}

/**
 * Confirmation dialogs for destructive actions
 */
function initDeleteConfirmations() {
  const deleteButtons = document.querySelectorAll('[data-confirm]');

  deleteButtons.forEach(function(button) {
    button.addEventListener('click', function(e) {
      const message = this.dataset.confirm || 'Are you sure you want to delete this item?';

      if (!confirm(message)) {
        e.preventDefault();
        return false;
      }
    });
  });
}

/**
 * Initialize tooltips (if Bootstrap tooltips are used)
 */
function initTooltips() {
  const tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  );

  if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
    tooltipTriggerList.map(function(tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl);
    });
  }
}

// Initialize additional features when needed
// These are called conditionally based on page content
if (document.querySelector('#id_product')) {
  initProductStockDisplay();
}

if (document.querySelector('input[name="type"]')) {
  initTransactionTypeToggle();
}

if (document.querySelector('[data-confirm]')) {
  initDeleteConfirmations();
}

// Initialize tooltips
initTooltips();
