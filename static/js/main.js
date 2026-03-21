/**
 * CareerCompass — main.js  v2.0
 * Premium AI-field interactions & micro-animations
 */

/* ══════════════════════════════════════════
   THEME
══════════════════════════════════════════ */
(function () {
  const root = document.documentElement;
  const saved = localStorage.getItem('cc-theme') || 'dark';
  root.setAttribute('data-theme', saved);
  const btn = document.getElementById('themeBtn');
  if (btn) btn.textContent = saved === 'dark' ? '☀️' : '🌙';
})();

function toggleTheme() {
  const root = document.documentElement;
  const next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
  root.setAttribute('data-theme', next);
  localStorage.setItem('cc-theme', next);
  const btn = document.getElementById('themeBtn');
  if (btn) btn.textContent = next === 'dark' ? '☀️' : '🌙';
}

/* ══════════════════════════════════════════
   ACTIVE NAV LINK
══════════════════════════════════════════ */
document.addEventListener('DOMContentLoaded', () => {
  const path = location.pathname;
  document.querySelectorAll('.nav-link').forEach(a => {
    const href = a.getAttribute('href') || '';
    if (path === href || (href !== '/' && path.startsWith(href))) {
      a.classList.add('active');
    }
  });

  initScrollReveal();
  initButtonRipple();
  initNavScroll();
  initCountUp();
  initBars();
  initCardTilt();
});

/* ══════════════════════════════════════════
   SCROLL REVEAL  (Intersection Observer)
══════════════════════════════════════════ */
function initScrollReveal() {
  const items = document.querySelectorAll('.reveal');
  if (!items.length) return;
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e, i) => {
      if (e.isIntersecting) {
        setTimeout(() => e.target.classList.add('visible'), i * 70);
        io.unobserve(e.target);
      }
    });
  }, { threshold: 0.12 });
  items.forEach(el => io.observe(el));
}

/* ══════════════════════════════════════════
   BUTTON GLOW-FOLLOW (mouse radial)
══════════════════════════════════════════ */
function initButtonRipple() {
  document.querySelectorAll('.btn-primary').forEach(btn => {
    btn.addEventListener('mousemove', e => {
      const r = btn.getBoundingClientRect();
      btn.style.setProperty('--mx', ((e.clientX - r.left) / r.width * 100) + '%');
      btn.style.setProperty('--my', ((e.clientY - r.top)  / r.height * 100) + '%');
    });
  });
}

/* ══════════════════════════════════════════
   NAV SHRINK ON SCROLL
══════════════════════════════════════════ */
function initNavScroll() {
  const inner = document.querySelector('.nav-inner');
  if (!inner) return;
  let last = 0;
  window.addEventListener('scroll', () => {
    const y = window.scrollY;
    if (y > 60 && y > last) {
      inner.style.transform = 'translateY(-4px)';
      inner.style.opacity = '.92';
    } else {
      inner.style.transform = '';
      inner.style.opacity = '';
    }
    last = y;
  }, { passive: true });
}

/* ══════════════════════════════════════════
   COUNT-UP ANIMATION (stats)
══════════════════════════════════════════ */
function initCountUp() {
  const nums = document.querySelectorAll('.stat-num[data-count]');
  if (!nums.length) return;
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      const el = e.target;
      const target = parseFloat(el.dataset.count);
      const suffix = el.dataset.suffix || '';
      const isFloat = String(target).includes('.');
      let start = null;
      const dur = 1200;
      const step = ts => {
        if (!start) start = ts;
        const progress = Math.min((ts - start) / dur, 1);
        const ease = 1 - Math.pow(1 - progress, 3);
        const val = target * ease;
        el.textContent = (isFloat ? val.toFixed(1) : Math.round(val)) + suffix;
        if (progress < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
      io.unobserve(el);
    });
  }, { threshold: 0.5 });
  nums.forEach(el => io.observe(el));
}

/* ══════════════════════════════════════════
   ANIMATED PROGRESS BARS (results page)
══════════════════════════════════════════ */
function initBars() {
  const bars = document.querySelectorAll('.mc-bar[data-p]');
  if (!bars.length) return;
  setTimeout(() => {
    bars.forEach(b => { b.style.width = b.dataset.p + '%'; });
  }, 300);
}

/* ══════════════════════════════════════════
   3D CARD TILT
══════════════════════════════════════════ */
function initCardTilt() {
  const cards = document.querySelectorAll('.match-card, .feat-card');
  cards.forEach(card => {
    card.addEventListener('mousemove', e => {
      const r = card.getBoundingClientRect();
      const x = ((e.clientX - r.left) / r.width  - 0.5) * 10;
      const y = ((e.clientY - r.top)  / r.height - 0.5) * 10;
      card.style.transform = `perspective(700px) rotateX(${-y * .35}deg) rotateY(${x * .35}deg) translateY(-3px)`;
    });
    card.addEventListener('mouseleave', () => { card.style.transform = ''; });
  });
}

/* ══════════════════════════════════════════
   TAB SWITCHING (results page)
══════════════════════════════════════════ */
function switchTab(id, btn) {
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('tab-' + id).classList.add('active');
  btn.classList.add('active');
  if (id === 'radar') {
    setTimeout(() => {
      if (typeof renderRadar === 'function') renderRadar();
    }, 60);
  }
}

/* ══════════════════════════════════════════
   SKILL CHIP TOGGLE (form page)
══════════════════════════════════════════ */
function toggleSkill(el) {
  el.classList.toggle('on');
  updateHiddenInputs();
}

function updateHiddenInputs() {
  const container = document.getElementById('skill-inputs');
  if (!container) return;
  container.innerHTML = '';
  const chips = document.querySelectorAll('.chip.on');
  chips.forEach(chip => {
    const inp = document.createElement('input');
    inp.type = 'hidden'; inp.name = 'skills'; inp.value = chip.dataset.skill;
    container.appendChild(inp);
  });
  const badge = document.getElementById('skill-count-badge');
  if (badge) {
    badge.textContent = chips.length + ' selected';
  }
  const legacyCount = document.getElementById('skill-count');
  if (legacyCount) legacyCount.textContent = `(${chips.length} selected)`;
}

/* ══════════════════════════════════════════
   FORM FIELD PROGRESS
══════════════════════════════════════════ */
function updateFormProgress() {
  const bar = document.getElementById('form-progress');
  if (!bar) return;
  const inputs = document.querySelectorAll('.field-input');
  let filled = 0;
  inputs.forEach(inp => { if (inp.value && inp.value !== '') filled++; });
  bar.style.width = (filled / inputs.length * 100) + '%';
}
document.addEventListener('change', updateFormProgress);
document.addEventListener('input',  updateFormProgress);

/* ══════════════════════════════════════════
   NOTIFICATION TOAST
══════════════════════════════════════════ */
function showToast(message, type = 'info') {
  const existing = document.querySelector('.cc-toast');
  if (existing) existing.remove();

  const colors = {
    success: 'var(--emerald)',
    error:   'var(--rose)',
    info:    'var(--indigo)',
    warn:    'var(--amber)',
  };

  const toast = document.createElement('div');
  toast.className = 'cc-toast';
  toast.style.cssText = `
    position:fixed; bottom:24px; right:24px; z-index:9999;
    background:var(--surface3); border:1px solid ${colors[type]};
    border-radius:12px; padding:12px 20px;
    color:var(--ink-100); font-size:.87rem; font-weight:500;
    display:flex; align-items:center; gap:10px;
    box-shadow:0 8px 32px rgba(0,0,0,.5);
    transform:translateY(20px); opacity:0;
    transition:all .3s cubic-bezier(.34,1.56,.64,1);
    max-width:360px; font-family:var(--font-body);
  `;
  const dot = document.createElement('span');
  dot.style.cssText = `width:8px;height:8px;border-radius:50%;background:${colors[type]};flex-shrink:0;box-shadow:0 0 8px ${colors[type]};`;
  toast.appendChild(dot);
  toast.appendChild(document.createTextNode(message));
  document.body.appendChild(toast);

  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      toast.style.transform = 'translateY(0)';
      toast.style.opacity = '1';
    });
  });
  setTimeout(() => {
    toast.style.transform = 'translateY(20px)'; toast.style.opacity = '0';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

/* ══════════════════════════════════════════
   AI THINKING INDICATOR
══════════════════════════════════════════ */
function showAIThinking(container) {
  const el = document.createElement('div');
  el.style.cssText = 'display:flex;align-items:center;gap:8px;padding:10px 0;color:var(--cyan);font-size:.83rem;font-weight:500;font-family:var(--font-body);';
  el.innerHTML = `
    <span style="display:flex;gap:4px;align-items:center;">
      <span class="ai-blink-dot"></span>
      <span class="ai-blink-dot" style="animation-delay:.16s;"></span>
      <span class="ai-blink-dot" style="animation-delay:.32s;"></span>
    </span>
    <span>AI analysing your profile…</span>`;

  if (!document.getElementById('ai-dot-style')) {
    const s = document.createElement('style');
    s.id = 'ai-dot-style';
    s.textContent = `.ai-blink-dot{width:5px;height:5px;border-radius:50%;background:var(--cyan);display:inline-block;animation:ai-bounce .9s ease-in-out infinite;}@keyframes ai-bounce{0%,80%,100%{transform:scale(0.6);opacity:.4}40%{transform:scale(1);opacity:1}}`;
    document.head.appendChild(s);
  }
  container.appendChild(el);
  return () => el.remove();
}

/* ══════════════════════════════════════════
   KEYBOARD SHORTCUTS
══════════════════════════════════════════ */
document.addEventListener('keydown', e => {
  if (e.key === '/' && !['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName)) {
    e.preventDefault();
    const first = document.querySelector('.field-input');
    if (first) { first.focus(); first.scrollIntoView({ behavior: 'smooth', block: 'center' }); }
  }
});

/* ══════════════════════════════════════════
   SMOOTH PAGE TRANSITIONS
══════════════════════════════════════════ */
document.querySelectorAll('a[href]:not([href^="#"]):not([href^="mailto"]):not([target])').forEach(a => {
  a.addEventListener('click', e => {
    if (a.hostname !== location.hostname) return;
    e.preventDefault();
    const dest = a.href;
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity .18s ease';
    setTimeout(() => { location.href = dest; }, 180);
  });
});
window.addEventListener('pageshow', () => {
  document.body.style.transition = 'opacity .25s ease';
  document.body.style.opacity = '1';
});

/* ══════════════════════════════════════════
   MOBILE NAV
══════════════════════════════════════════ */
function toggleMobileNav() {
  const links = document.getElementById('navLinks');
  const btn   = document.getElementById('navHamburger');
  const open  = links && links.classList.toggle('mobile-open');
  if (btn) btn.classList.toggle('open', open);
  // Close on outside click
  if (open) {
    setTimeout(() => {
      document.addEventListener('click', closeMobileNavOutside, { once: true });
    }, 10);
  }
}
function closeMobileNavOutside(e) {
  const links = document.getElementById('navLinks');
  const btn   = document.getElementById('navHamburger');
  const nav   = document.querySelector('.nav-inner');
  if (nav && !nav.contains(e.target)) {
    links && links.classList.remove('mobile-open');
    btn && btn.classList.remove('open');
  }
}

/* ══════════════════════════════════════════
   EXPOSE GLOBALS
══════════════════════════════════════════ */
window.toggleTheme    = toggleTheme;
window.switchTab      = switchTab;
window.toggleSkill    = toggleSkill;
window.updateHiddenInputs = updateHiddenInputs;
window.showToast      = showToast;
window.showAIThinking = showAIThinking;
window.toggleMobileNav = toggleMobileNav;
