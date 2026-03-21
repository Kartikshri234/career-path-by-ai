/**
 * results.js — Career Results Page
 * Handles: tab switching, radar chart render
 * Depends on: userSkills, results (injected by Django template)
 */

const RADAR_DATA = {
  "Software Development Engineer":  { labels: ["Coding","System Design","CS Basics","Problem Solving","Communication","Projects"],  required: [9,7,8,9,6,7] },
  "Data Scientist / ML Engineer":   { labels: ["Python","Statistics","ML","Data Viz","Research","Problem Solving"],                  required: [9,8,9,7,8,8] },
  "Cloud / DevOps Engineer":        { labels: ["Linux","Cloud","Scripting","Networking","CI/CD","Security"],                        required: [8,9,7,8,8,7] },
  "Cybersecurity Engineer":         { labels: ["Networking","Linux","Ethical Hacking","Scripting","Web Security","Forensics"],      required: [9,8,9,7,8,6] },
  "Product Manager (Tech)":         { labels: ["Strategy","SQL","UX/Figma","Communication","Analytics","Execution"],               required: [8,7,8,9,8,8] },
};

let radarInst = null;

/* ══ TAB SWITCHING ══ */
function switchTab(id, btn) {
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('tab-' + id).classList.add('active');
  btn.classList.add('active');
  if (id === 'radar') setTimeout(() => renderRadar(), 60);
}

/* ══ RADAR CHART ══ */
function renderRadar() {
  if (radarInst) { radarInst.destroy(); radarInst = null; }

  /* window.userSkills and window.results injected by Django template */
  const rd = RADAR_DATA[window.results[0]?.career];
  if (!rd) return;

  const isDark     = document.documentElement.getAttribute('data-theme') !== 'light';
  const userScores = rd.required.map(r =>
    Math.max(2, Math.round(r * 0.35 + (window.userSkills.length / 12) * r * 0.65))
  );
  const gridColor  = isDark ? 'rgba(255,255,255,.07)' : 'rgba(0,0,0,.07)';
  const labelColor = isDark ? '#94a3b8' : '#475569';

  radarInst = new Chart(document.getElementById('rc').getContext('2d'), {
    type: 'radar',
    data: {
      labels: rd.labels,
      datasets: [
        {
          label: 'Required',
          data: rd.required,
          borderColor: 'rgba(99,102,241,.8)',
          backgroundColor: 'rgba(99,102,241,.08)',
          pointBackgroundColor: '#6366f1',
          borderWidth: 2,
        },
        {
          label: 'Your Level',
          data: userScores,
          borderColor: 'rgba(34,211,238,.8)',
          backgroundColor: 'rgba(34,211,238,.08)',
          pointBackgroundColor: '#22d3ee',
          borderWidth: 2,
        },
      ]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      scales: { r: {
        min: 0, max: 10, ticks: { display: false },
        grid: { color: gridColor },
        pointLabels: { color: labelColor, font: { size: 12, family: "'Syne',sans-serif" } }
      }},
      plugins: { legend: { labels: { color: labelColor, font: { family: "'DM Sans',sans-serif" } } } }
    }
  });
}
