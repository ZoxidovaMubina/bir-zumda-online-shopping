const qs = (sel, scope = document) => scope.querySelector(sel);
const qsa = (sel, scope = document) => [...scope.querySelectorAll(sel)];

document.addEventListener('DOMContentLoaded', () => {
  const themeToggle = qs('#theme-toggle');
  const mobileBtn = qs('#mobile-menu-btn');
  const navLinks = qs('#nav-links');
  const currentPage = location.pathname.split('/').pop() || 'index.html';

  if (themeToggle) {
    themeToggle.addEventListener('click', (e) => {
      e.preventDefault();

      const currentTheme = document.documentElement.getAttribute('data-theme');
      const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';

      document.documentElement.setAttribute('data-theme', nextTheme);
      themeToggle.innerHTML = nextTheme === 'dark'
        ? '<i class="fa-solid fa-moon"></i>'
        : '<i class="fa-solid fa-sun"></i>';
    });
  }

  if (mobileBtn && navLinks) {
    mobileBtn.addEventListener('click', () => {
      navLinks.classList.toggle('active');
    });

    qsa('a', navLinks).forEach((link) => {
      link.addEventListener('click', () => {
        navLinks.classList.remove('active');
      });
    });
  }

  qsa('.nav-links a').forEach((link) => {
    const href = link.getAttribute('href');
    if (!href) return;

    if (href === currentPage) {
      link.classList.add('active');
    }

    if (currentPage === 'blog-detail.html' && href === 'blog.html') {
      link.classList.add('active');
    }

    if (currentPage === 'mahsulot-detail.html' && href === 'mahsulotlar.html') {
      link.classList.add('active');
    }

    if ((currentPage === 'savatcha.html' || currentPage === 'checkout.html') && href === 'mahsulotlar.html') {
      link.classList.add('active');
    }
  });

  initImageFallbacks();
});

const fallbackImage = (alt = 'Mahsulot rasmi') => {
  const label = encodeURIComponent(alt);
  return `data:image/svg+xml;charset=UTF-8,<svg xmlns='http://www.w3.org/2000/svg' width='800' height='600' viewBox='0 0 800 600'><rect width='800' height='600' rx='28' fill='%23EEF2FF'/><rect x='110' y='120' width='580' height='360' rx='26' fill='%23C7D2FE'/><text x='400' y='305' text-anchor='middle' fill='%23312E81' font-family='Arial,sans-serif' font-size='42' font-weight='700'>${label}</text></svg>`;
};

const initImageFallbacks = () => {
  qsa('img').forEach((img) => {
    img.addEventListener('error', function handleImageError() {
      if (this.dataset.fallbackApplied === 'true') return;

      this.dataset.fallbackApplied = 'true';
      this.src = fallbackImage(this.alt || 'Rasm topilmadi');
    });
  });
};