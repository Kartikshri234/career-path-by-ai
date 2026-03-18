/**
 * history.js — Analysis History Page
 * Handles: search, filter, sort, pagination, delete modal, toast,
 *          and the Progress Tracking chart (Feature 2).
 */

const PER_PAGE = 8;
let currentPage = 1;
let activeFilter = 'all';
let pendingDeleteId = null;

/* Progress chart state */
let progressChart = null;
let activeProgressName = null;
let allHistoryData = [];

const FILTER_MAP = {
  sde:   'software development',
  data:  'data scientist',
  cloud: 'cloud',
  cyber: 'cybersecurity',
  pm:    'product manager',
};

/* ══════════════════════════════════════════
   PROGRESS TRACKER
══════════════════════════════════════════ */

function initProgressTracker() {
  const dataEl = document.getElementById('history-data');
  if (!dataEl) return;

  try {
    allHistoryData = JSON.parse(dataEl.textContent);
  } catch (e) { return; }

  if (!allHistoryData.length) return;

  /* Sort oldest → newest for the chart */
  allHistoryData.sort((a, b) => parseInt(a.dateTs) - parseInt(b.dateTs));

  /* Find unique names */
  const names = [...new Set(allHistoryData.map(d => d.name))];

  /* Build name pill buttons */
  const namesWrap = document.getElementById('progress-names');
  if (!namesWrap) return;

  names.forEach((name, i) => {
    const btn = document.createElement('button');
    btn.className = 'pn-pill' + (i === 0 ? ' active' : '');
    btn.textContent = name;
    btn.onclick = () => selectProgressName(name, btn);
    namesWrap.appendChild(btn);
  });

  /* Default: show first name */
  activeProgressName = names[0];
  renderProgressChart(activeProgressName);
}

function selectProgressName(name, btn) {
  activeProgressName = name;
  document.querySelectorAll('.pn-pill').forEach(p => p.classList.remove('active'));
  btn.classList.add('active');
  renderProgressChart(name);
}

function renderProgressChart(name) {
  const entries = allHistoryData.filter(d => d.name === name);
  const wrap = document.querySelector('.progress-chart-wrap');
  if (!wrap) return;

  /* Need at least 1 entry */
  if (!entries.length) {
    wrap.innerHTML = `<div class="progress-empty"><span>📭</span><p>No data for this name yet.</p></div>`;
    document.getElementById('progress-stats').innerHTML = '';
    return;
  }

  /* If only 1 data point, show a friendly message but still chart it */
  const labels  = entries.map(d => formatChartDate(d.date));
  const scores  = entries.map(d => d.topScore);
  const careers = entries.map(d => d.topCareer);

  /* Restore canvas if needed */
  if (!wrap.querySelector('canvas')) {
    wrap.innerHTML = '<canvas id="progress-chart"></canvas>';
  }
  const canvas = wrap.querySelector('canvas');

  /* Destroy old chart */
  if (progressChart) { progressChart.destroy(); progressChart = null; }

  const isDark = document.documentElement.getAttribute('data-theme') !== 'light';
  const gridCol  = isDark ? 'rgba(129,140,248,.08)' : 'rgba(79,70,229,.07)';
  const tickCol  = isDark ? '#64748b' : '#94a3b8';
  const tooltipBg = isDark ? '#161b32' : '#ffffff';
  const tooltipBorder = isDark ? 'rgba(129,140,248,.35)' : 'rgba(79,70,229,.22)';

  /* Gradient fill */
  const ctx = canvas.getContext('2d');
  const gradient = ctx.createLinearGradient(0, 0, 0, 200);
  gradient.addColorStop(0,   isDark ? 'rgba(129,140,248,.30)' : 'rgba(79,70,229,.20)');
  gradient.addColorStop(1,   'rgba(0,0,0,0)');

  progressChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [{
        label: 'Top Match Score',
        data: scores,
        borderColor: isDark ? '#818cf8' : '#4f46e5',
        backgroundColor: gradient,
        borderWidth: 2.5,
        pointBackgroundColor: isDark ? '#818cf8' : '#4f46e5',
        pointBorderColor: isDark ? '#0c0f1e' : '#ffffff',
        pointBorderWidth: 2,
        pointRadius: 5,
        pointHoverRadius: 7,
        tension: 0.35,
        fill: true,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: tooltipBg,
          borderColor: tooltipBorder,
          borderWidth: 1,
          titleColor: isDark ? '#e2e8f0' : '#0f172a',
          bodyColor:  isDark ? '#94a3b8' : '#475569',
          padding: 12,
          callbacks: {
            title: (items) => labels[items[0].dataIndex],
            label: (item) => {
              const career = careers[item.dataIndex];
              return [`Score: ${item.raw}%`, career ? `Career: ${career}` : ''];
            },
          }
        }
      },
      scales: {
        x: {
          grid: { color: gridCol },
          ticks: { color: tickCol, font: { family: "'DM Sans', sans-serif", size: 11 } },
        },
        y: {
          min: 0, max: 100,
          grid: { color: gridCol },
          ticks: {
            color: tickCol,
            font: { family: "'DM Sans', sans-serif", size: 11 },
            callback: v => v + '%',
          }
        }
      }
    }
  });

  /* Render summary stats */
  renderProgressStats(scores, entries);
}

function renderProgressStats(scores, entries) {
  const statsEl = document.getElementById('progress-stats');
  if (!statsEl) return;

  const latest  = scores[scores.length - 1];
  const best    = Math.max(...scores);
  const first   = scores[0];
  const gain    = latest - first;
  const gainStr = (gain >= 0 ? '+' : '') + gain + '%';
  const gainCls = gain >= 0 ? 'up' : 'down';

  const count   = entries.length;

  statsEl.innerHTML = `
    <div class="ps-card">
      <div class="ps-val">${latest}%</div>
      <div class="ps-lbl">Latest Score</div>
    </div>
    <div class="ps-card">
      <div class="ps-val up">${best}%</div>
      <div class="ps-lbl">Personal Best</div>
    </div>
    <div class="ps-card">
      <div class="ps-val ${gainCls}">${gainStr}</div>
      <div class="ps-lbl">Total Growth</div>
    </div>
    <div class="ps-card">
      <div class="ps-val">${count}</div>
      <div class="ps-lbl">Analyses Done</div>
    </div>
  `;
}

function formatChartDate(dateStr) {
  /* dateStr is "YYYY-MM-DD" */
  const d = new Date(dateStr + 'T00:00:00');
  return d.toLocaleDateString('en-IN', { day: 'numeric', month: 'short' });
}

/* ══════════════════════════════════════════
   FILTER
══════════════════════════════════════════ */
function setFilter(key, btn) {
  activeFilter = key;
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  currentPage = 1;
  applyFilters();
}

/* ══════════════════════════════════════════
   SEARCH + SORT + PAGINATE
══════════════════════════════════════════ */
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

/* ══════════════════════════════════════════
   PAGINATION
══════════════════════════════════════════ */
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

/* ══════════════════════════════════════════
   DELETE
══════════════════════════════════════════ */
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
        setTimeout(() => {
          el.remove();
          applyFilters();
          /* Remove this entry from allHistoryData and re-render chart */
          allHistoryData = allHistoryData.filter(d =>
            !(d.name.toLowerCase() === el.dataset.name)
          );
          if (activeProgressName) renderProgressChart(activeProgressName);
        }, 300);
      }
      showToast('✅ Analysis deleted successfully');
    } else {
      showToast('❌ Could not delete — please try again');
    }
  })
  .catch(() => showToast('❌ Network error — please try again'));
}

/* ══════════════════════════════════════════
   TOAST
══════════════════════════════════════════ */
function showToast(msg) {
  const t = document.getElementById('h-toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 3000);
}

/* ══════════════════════════════════════════
   CSRF
══════════════════════════════════════════ */
function getCookie(name) {
  const v = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
  return v ? v.pop() : '';
}

/* ══════════════════════════════════════════
   INIT
══════════════════════════════════════════ */
document.addEventListener('DOMContentLoaded', () => {
  applyFilters();
  initProgressTracker();

  document.getElementById('delete-modal')?.addEventListener('click', function(e) {
    if (e.target === this) closeModal();
  });

  /* Re-render chart on theme change */
  const observer = new MutationObserver(() => {
    if (activeProgressName) renderProgressChart(activeProgressName);
  });
  observer.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
});
