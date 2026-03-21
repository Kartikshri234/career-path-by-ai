/**
 * careers_list.js — Career Tracks Page
 * Handles: filter, card toggle, tab switch, radar chart
 */

/* ── Radar data injected from Django template ── */
/* RADAR_DATA is set inline in the template as a <script> block */
let radarCharts = {};

/* ══ FILTER ══ */
function applyFilter(btn) {
  document.querySelectorAll('.cf-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  const f = btn.dataset.filter;

  let visible = 0;
  document.querySelectorAll('.career-card').forEach(card => {
    const demand = card.dataset.demandLevel || '';
    const salary = card.dataset.salaryLevel || '';
    const diff   = card.dataset.difficulty  || '';

    let show = true;
    if (f === 'very_high')    show = demand === 'very_high';
    if (f === 'high')         show = demand === 'high' || demand === 'very_high';
    if (f === 'salary_top')   show = salary === 'very_high' || salary === 'high';
    if (f === 'medium_diff')  show = diff === 'medium';
    if (f === 'hard_diff')    show = diff === 'hard';

    card.classList.toggle('filtered-out', !show);
    if (show) visible++;
  });

  document.getElementById('no-cards').classList.toggle('show', visible === 0);
}

/* ══ TOGGLE CARD ══ */
function toggleCard(cardId, idx) {
  const card = document.getElementById(cardId);
  const wasOpen = card.classList.contains('open');
  document.querySelectorAll('.career-card').forEach(c => c.classList.remove('open'));
  if (!wasOpen) {
    card.classList.add('open');
    setTimeout(() => card.scrollIntoView({ behavior: 'smooth', block: 'nearest' }), 80);
  }
}

/* ══ TAB SWITCH ══ */
function switchTab(idx, tabName, btn) {
  const card = btn.closest('.career-card');
  card.querySelectorAll('.cc-tab').forEach(t => t.classList.remove('active'));
  card.querySelectorAll('.cc-panel').forEach(p => p.classList.remove('active'));
  btn.classList.add('active');
  document.getElementById(`panel-${idx}-${tabName}`).classList.add('active');
  if (tabName === 'radar') renderRadar(idx);
}

/* ══ RADAR CHART (lazy render) ══ */
function renderRadar(idx) {
  if (radarCharts[idx]) return;
  const data = window.RADAR_DATA[idx];
  if (!data) return;

  const dark       = document.documentElement.getAttribute('data-theme') !== 'light';
  const gridColor  = dark ? 'rgba(255,255,255,.07)' : 'rgba(0,0,0,.07)';
  const labelColor = dark ? '#94a3b8' : '#475569';

  radarCharts[idx] = new Chart(
    document.getElementById(`radar-${idx}`).getContext('2d'), {
    type: 'radar',
    data: {
      labels: data.labels,
      datasets: [{
        label: 'Required Level',
        data: data.required,
        borderColor: 'rgba(99,102,241,.85)',
        backgroundColor: 'rgba(99,102,241,.12)',
        pointBackgroundColor: '#6366f1',
        borderWidth: 2,
        pointRadius: 4,
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      scales: { r: {
        min: 0, max: 10, ticks: { display: false },
        grid: { color: gridColor },
        pointLabels: { color: labelColor, font: { size: 11, family: "'Syne',sans-serif" } }
      }},
      plugins: { legend: { labels: { color: labelColor, font: { family: "'DM Sans',sans-serif", size: 11 } } } }
    }
  });
}

/* ══ REBUILD RADAR ON THEME TOGGLE ══ */
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('themeBtn')?.addEventListener('click', () => {
    Object.values(radarCharts).forEach(c => c.destroy());
    radarCharts = {};
  });
});
