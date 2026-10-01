// Job Market Intelligence - Core Frontend Interactivity

document.addEventListener('DOMContentLoaded', () => {
  // 1. Mobile Sidebar Toggle
  const sidebarToggleBtn = document.getElementById('sidebar-toggle');
  const mobileSidebar = document.getElementById('mobile-sidebar');
  const sidebarCloseBtn = document.getElementById('sidebar-close');
  const sidebarBackdrop = document.getElementById('sidebar-backdrop');

  if (sidebarToggleBtn && mobileSidebar) {
    sidebarToggleBtn.addEventListener('click', () => {
      mobileSidebar.classList.remove('hidden');
    });
  }

  if (sidebarCloseBtn && mobileSidebar) {
    sidebarCloseBtn.addEventListener('click', () => {
      mobileSidebar.classList.add('hidden');
    });
  }

  if (sidebarBackdrop && mobileSidebar) {
    sidebarBackdrop.addEventListener('click', () => {
      mobileSidebar.classList.add('hidden');
    });
  }

  // 2. Auto Dismiss Alerts / Toasts after 4 seconds
  const alerts = document.querySelectorAll('.toast-alert');
  alerts.forEach(alert => {
    setTimeout(() => {
      alert.style.opacity = '0';
      alert.style.transform = 'translateY(-10px)';
      alert.style.transition = 'all 0.3s ease-out';
      setTimeout(() => alert.remove(), 300);
    }, 4000);
  });

  // 3. Interactive Skill Chip Toggles (in Skill Gap, Predictor & Profile)
  const skillChips = document.querySelectorAll('.skill-chip');
  skillChips.forEach(chip => {
    chip.addEventListener('click', () => {
      chip.classList.toggle('selected');
      const input = chip.querySelector('input[type="checkbox"]');
      if (input) {
        input.checked = !input.checked;
      }
      
      // If there's an update counter callback
      const counterElem = document.getElementById('selected-skills-count');
      if (counterElem) {
        const totalSelected = document.querySelectorAll('.skill-chip.selected').length;
        counterElem.textContent = totalSelected;
      }
    });
  });

  // 4. AJAX Job Bookmark / Save Toggle
  document.querySelectorAll('.save-job-btn').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      e.preventDefault();
      e.stopPropagation();
      
      const jobId = btn.getAttribute('data-job-id');
      if (!jobId) return;

      try {
        const response = await fetch(`/jobs/${jobId}/save/?format=json`, {
          method: 'POST',
          headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCsrfToken(),
          }
        });

        if (response.ok) {
          const data = await response.json();
          const icon = btn.querySelector('i');
          if (data.is_saved) {
            btn.classList.add('text-rose-500', 'bg-rose-500/10');
            btn.classList.remove('text-slate-400', 'hover:text-white');
            if (icon) icon.className = 'fa-solid fa-heart';
            showToast('Job saved to your bookmarks!', 'success');
          } else {
            btn.classList.remove('text-rose-500', 'bg-rose-500/10');
            btn.classList.add('text-slate-400', 'hover:text-white');
            if (icon) icon.className = 'fa-regular fa-heart';
            showToast('Job removed from bookmarks.', 'info');
          }
        } else if (response.status === 403 || response.status === 401 || response.redirected) {
          window.location.href = '/accounts/login/?next=' + window.location.pathname;
        }
      } catch (err) {
        console.error('Error saving job:', err);
      }
    });
  });
});

// Helper: Read CSRF Token from Cookie
function getCsrfToken() {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, 10) === ('csrftoken=')) {
        cookieValue = decodeURIComponent(cookie.substring(10));
        break;
      }
    }
  }
  return cookieValue;
}

// Helper: Floating Toast Generator
function showToast(message, type = 'info') {
  const container = document.getElementById('toast-container') || createToastContainer();
  const toast = document.createElement('div');
  
  const bgClass = type === 'success' ? 'bg-emerald-500/20 border-emerald-500 text-emerald-200' : 'bg-indigo-500/20 border-indigo-500 text-indigo-200';
  const iconClass = type === 'success' ? 'fa-circle-check text-emerald-400' : 'fa-circle-info text-indigo-400';

  toast.className = `flex items-center gap-3 px-4 py-3 rounded-xl border backdrop-blur-md shadow-2xl text-sm font-medium toast-alert ${bgClass}`;
  toast.innerHTML = `<i class="fa-solid ${iconClass}"></i><span>${message}</span>`;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(-10px)';
    toast.style.transition = 'all 0.3s ease-out';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

function createToastContainer() {
  const container = document.createElement('div');
  container.id = 'toast-container';
  container.className = 'fixed top-5 right-5 z-50 flex flex-col gap-2 max-w-sm';
  document.body.appendChild(container);
  return container;
}
