/**
 * history.js — Analysis History Page
 * Handles: search, filter, sort, pagination, delete modal, toast
 */

const PER_PAGE = 8;
let currentPage = 1;
let activeFilter = 'all';
let pendingDeleteId = null;

const FILTER_MAP = {
  sde:   'software development',
  data:  'data scientist',
  cloud: 'cloud',
  cyber: 'cybersecurity',
  pm:    'product manager',
};

/* ══ FILTER ══ */
function setFilter(key, btn) {
  activeFilter = key;
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  currentPage = 1;
  applyFilters();
}

/* ══ SEARCH + SORT + PAGINATE ══ */
function applyFilters() {
  const q    = document.getElementById('history-search').value.trim().toLowerCase();
  const sort = document.getElementById('sort-select').value;
  const items = [...document.querySelectorAll('.history-item')];

  const visible = items.filter(item => {
    const matchSearch = !q ||
      item.dataset.name.includes(q) ||
      item.dataset.branch.includes(q) ||
      item.dataset.topCareer.includes(q) ||
      item.dataset.skills.includes(q);
    const matchFilter = activeFilter === 'all' ||
      item.dataset.topCareer.includes(FILTER_MAP[activeFilter] || activeFilter);
    return matchSearch && matchFilter;
  });

  visible.sort((a, b) => {
    if (sort === 'newest') return parseInt(b.dataset.date)     - parseInt(a.dataset.date);
    if (sort === 'oldest') return parseInt(a.dataset.date)     - parseInt(b.dataset.date);
    if (sort === 'score')  return parseInt(b.dataset.topScore) - parseInt(a.dataset.topScore);
    if (sort === 'name')   return a.dataset.name.localeCompare(b.dataset.name);
    return 0;
  });

  items.forEach(i => i.classList.add('hidden'));
  const list = document.getElementById('history-list');
  visible.forEach(i => list.appendChild(i));

  const total = visible.length;
  const totalPages = Math.ceil(total / PER_PAGE) || 1;
  currentPage = Math.min(currentPage, totalPages);

  const start = (currentPage - 1) * PER_PAGE;
  const end   = start + PER_PAGE;
  visible.forEach((item, idx) => {
    item.classList.toggle('hidden', idx < start || idx >= end);
  });

  document.getElementById('results-count').textContent =
    total === 0 ? '' : `${total} result${total !== 1 ? 's' : ''}`;
  document.getElementById('no-results').style.display = total === 0 ? 'block' : 'none';

  renderPagination(total, totalPages);
}

/* ══ PAGINATION ══ */
function renderPagination(total, totalPages) {
  const pg = document.getElementById('pagination');
  pg.innerHTML = '';
  if (totalPages <= 1) return;

  const prev = document.createElement('button');
  prev.className = 'pg-btn';
  prev.textContent = '←';
  prev.disabled = currentPage === 1;
  prev.onclick = () => { currentPage--; applyFilters(); window.scrollTo({ top: 0, behavior: 'smooth' }); };
  pg.appendChild(prev);

  for (let i = 1; i <= totalPages; i++) {
    if (totalPages > 7 && Math.abs(i - currentPage) > 2 && i !== 1 && i !== totalPages) {
      if (i === currentPage - 3 || i === currentPage + 3) {
        const dots = document.createElement('span');
        dots.className = 'pg-info';
        dots.textContent = '…';
        pg.appendChild(dots);
      }
      continue;
    }
    const btn = document.createElement('button');
    btn.className = 'pg-btn' + (i === currentPage ? ' active' : '');
    btn.textContent = i;
    btn.onclick = ((p) => () => {
      currentPage = p; applyFilters();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    })(i);
    pg.appendChild(btn);
  }

  const next = document.createElement('button');
  next.className = 'pg-btn';
  next.textContent = '→';
  next.disabled = currentPage === totalPages;
  next.onclick = () => { currentPage++; applyFilters(); window.scrollTo({ top: 0, behavior: 'smooth' }); };
  pg.appendChild(next);

  const info = document.createElement('span');
  info.className = 'pg-info';
  const start = (currentPage - 1) * PER_PAGE + 1;
  const end   = Math.min(currentPage * PER_PAGE, total);
  info.textContent = `${start}–${end} of ${total}`;
  pg.appendChild(info);
}

/* ══ DELETE ══ */
function confirmDelete(id, name) {
  pendingDeleteId = id;
  document.getElementById('modal-sub').textContent =
    `This will permanently remove "${name}" and all their recommendations.`;
  document.getElementById('delete-modal').classList.add('show');
}

function closeModal() {
  document.getElementById('delete-modal').classList.remove('show');
  pendingDeleteId = null;
}

function executeDelete() {
  if (!pendingDeleteId) return;
  const id = pendingDeleteId;
  closeModal();

  fetch(`/delete-profile/${id}/`, {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCookie('csrftoken'),
      'Content-Type': 'application/json',
    },
  })
  .then(r => r.json())
  .then(data => {
    if (data.success) {
      const el = document.querySelector(`.history-item[data-id="${id}"]`);
      if (el) {
        el.style.opacity = '0';
        el.style.transform = 'translateX(30px)';
        setTimeout(() => { el.remove(); applyFilters(); }, 300);
      }
      showToast('✅ Analysis deleted successfully');
    } else {
      showToast('❌ Could not delete — please try again');
    }
  })
  .catch(() => showToast('❌ Network error — please try again'));
}

/* ══ TOAST ══ */
function showToast(msg) {
  const t = document.getElementById('h-toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 3000);
}

/* ══ CSRF ══ */
function getCookie(name) {
  const v = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
  return v ? v.pop() : '';
}

/* ══ INIT ══ */
document.addEventListener('DOMContentLoaded', () => {
  applyFilters();

  document.getElementById('delete-modal')?.addEventListener('click', function(e) {
    if (e.target === this) closeModal();
  });
});
