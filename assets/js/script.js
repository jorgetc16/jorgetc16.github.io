// Minimal typed text effect (smart backspace + underline)
(function () {
  const TYPE_DELAY = 80;
  const ERASE_DELAY = 50;
  const HOLD_DELAY = 1200;

  const commonPrefixLen = (a, b) => {
    const L = Math.min(a.length, b.length);
    let i = 0;
    while (i < L && a[i] === b[i]) i++;
    return i;
  };

  function eraseTo(el, fromWord, keep, cb, i = fromWord.length) {
    el.textContent = fromWord.slice(0, i);
    if (i === keep) return setTimeout(cb, 200);
    if (i > keep) {
      setTimeout(() => eraseTo(el, fromWord, keep, cb, i - 1), ERASE_DELAY);
    }
  }

  function typeFrom(el, toWord, start, cb, i = start) {
    el.textContent = toWord.slice(0, i);
    if (i >= toWord.length) return setTimeout(cb, HOLD_DELAY);
    setTimeout(() => typeFrom(el, toWord, start, cb, i + 1), TYPE_DELAY);
  }

  function cycle(el, items, idx = 0, prev = '') {
    const next = items[idx % items.length];
    const keep = commonPrefixLen(prev, next);
    eraseTo(el, prev, keep, () => {
      typeFrom(el, next, keep, () => cycle(el, items, idx + 1, next));
    });
  }

  function initTyped() {
    const els = document.querySelectorAll('.typed');
    els.forEach(el => {
      const list = (el.getAttribute('data-typed-items') || '')
        .split(',')
        .map(s => s.trim())
        .filter(Boolean);
      if (list.length) cycle(el, list, 0, '');
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTyped);
  } else {
    initTyped();
  }
})();

// Theme toggle (single source of truth: root class + 'jt_theme' storage)
(function () {
  const STORAGE_KEY = 'jt_theme';
  function apply(theme) {
    const isDark = theme === 'dark';
    document.documentElement.classList.toggle('dark', isDark);
    const btn = document.getElementById('theme-toggle');
    if (btn) {
      btn.textContent = isDark ? '☀️' : '🌙';
      btn.setAttribute('aria-label', isDark ? 'Switch to light mode' : 'Switch to dark mode');
      btn.setAttribute('title', isDark ? 'Switch to light mode' : 'Switch to dark mode');
    }
  }

  function preferred() {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved === 'light' || saved === 'dark') return saved;
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function init() {
    let theme = preferred();
    apply(theme);

    const btn = document.getElementById('theme-toggle');
    if (btn) {
      btn.addEventListener('click', () => {
        theme = document.documentElement.classList.contains('dark') ? 'light' : 'dark';
        localStorage.setItem(STORAGE_KEY, theme);
        apply(theme);
      });
    }

    if (window.matchMedia) {
      const mq = window.matchMedia('(prefers-color-scheme: dark)');
      mq.addEventListener?.('change', (e) => {
        if (!localStorage.getItem(STORAGE_KEY)) {
          apply(e.matches ? 'dark' : 'light');
        }
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

// Lightbox for gallery images
(function () {
  const lightbox = document.getElementById('lightbox');
  const lightboxImg = document.getElementById('lightbox-img');
  const lightboxCaption = document.getElementById('lightbox-caption');
  const closeBtn = document.querySelector('.lightbox-close');
  const prevBtn = document.querySelector('.lightbox-prev');
  const nextBtn = document.querySelector('.lightbox-next');

  let galleryImages = [];
  let currentIndex = 0;
  let touchStartX = 0;
  let touchEndX = 0;

  function showImage(index) {
    if (index < 0) index = galleryImages.length - 1;
    if (index >= galleryImages.length) index = 0;
    currentIndex = index;

    const img = galleryImages[currentIndex];
    lightboxImg.src = img.src;
    lightboxCaption.textContent = img.alt;
  }

  function openLightbox(index) {
    showImage(index);
    lightbox.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function closeLightbox() {
    lightbox.classList.remove('active');
    document.body.style.overflow = '';
  }

  function nextImage() {
    showImage(currentIndex + 1);
  }

  function prevImage() {
    showImage(currentIndex - 1);
  }

  function handleSwipe() {
    if (touchEndX < touchStartX - 50) nextImage();
    if (touchEndX > touchStartX + 50) prevImage();
  }

  function init() {
    // Collect all gallery images
    galleryImages = Array.from(document.querySelectorAll('.gallery-img'));

    // Attach click handlers to all gallery images
    galleryImages.forEach((img, idx) => {
      img.addEventListener('click', () => openLightbox(idx));
    });

    // Close on X button
    if (closeBtn) {
      closeBtn.addEventListener('click', closeLightbox);
    }

    // Navigation buttons
    if (prevBtn) {
      prevBtn.addEventListener('click', prevImage);
    }
    if (nextBtn) {
      nextBtn.addEventListener('click', nextImage);
    }

    // Close on backdrop click
    if (lightbox) {
      lightbox.addEventListener('click', (e) => {
        if (e.target === lightbox) closeLightbox();
      });
    }

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
      if (!lightbox.classList.contains('active')) return;
      
      if (e.key === 'Escape') closeLightbox();
      if (e.key === 'ArrowRight') nextImage();
      if (e.key === 'ArrowLeft') prevImage();
    });

    // Touch/swipe support for mobile
    if (lightbox) {
      lightbox.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].screenX;
      }, { passive: true });

      lightbox.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
      }, { passive: true });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
