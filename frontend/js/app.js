// ── BOOT: render skill chips ──────────────────────────────────────────────────
document.getElementById('chips').innerHTML = SKILLS.map(s =>
  `<div class="chip" onclick="this.classList.toggle('on')">${s}</div>`
).join('');

// ── HELPERS ───────────────────────────────────────────────────────────────────
function show(id) {
  document.querySelectorAll('.pg').forEach(p => p.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  window.scrollTo(0, 0);
  const map = { 'p-form':'s1', 'p-load':'s2', 'p-res':'s3' };
  document.querySelectorAll('.step').forEach(s => s.classList.remove('active','done'));
  if (map[id]) document.getElementById(map[id]).classList.add('active');
}

function getSelectedSkills() {
  return [...document.querySelectorAll('.chip.on')].map(e => e.textContent);
}

// ── SCORING ALGORITHM ─────────────────────────────────────────────────────────
// Weights: skill overlap 60% | CGPA 20% | LeetCode 10% | GitHub 10%
function calcScore(career, skills, cgpa, lc, gh) {
  const overlap = skills.filter(s => career.need.includes(s)).length;
  let score = (overlap / career.need.length) * 60;
  score += Math.min((cgpa || 7) / 10 * 20, 20);
  score += Math.min((lc  || 0) / 300 * 10, 10);
  score += Math.min((gh  || 0) / 10  * 10, 10);
  return Math.round(Math.min(score + 18, 98)); // floor boost so no one gets 0
}

// ── STATE ─────────────────────────────────────────────────────────────────────
let results = [];
let userSkills = [];

// ── ANALYZE ───────────────────────────────────────────────────────────────────
function analyze() {
  const name = document.getElementById('fn').value || 'Student';
  const cgpa = parseFloat(document.getElementById('fg-cgpa').value) || 7;
  const lc   = parseInt(document.getElementById('flc').value) || 0;
  const gh   = parseInt(document.getElementById('fgh').value) || 0;
  userSkills = getSelectedSkills();

  // Show loading screen
  show('p-load');
  document.getElementById('s1').classList.add('done');
  document.getElementById('s2').classList.add('active');

  // Animate loading steps
  const steps = [
    "Parsing academic profile...",
    "Matching against 50+ career paths...",
    "Running ML scoring model...",
    "Calculating success probabilities...",
    "Generating personalized roadmap..."
  ];
  const el = document.getElementById('ldsteps');
  el.innerHTML = '';
  steps.forEach((txt, i) => {
    setTimeout(() => {
      const d = document.createElement('div');
      d.className = 'ld-step';
      d.style.animationDelay = '0s';
      d.innerHTML = `<div class="ld-dot"></div>${txt}`;
      el.appendChild(d);
      setTimeout(() => d.classList.add('done'), 300);
    }, i * 700);
  });

  // After animation, build results
  setTimeout(() => {
    results = CAREERS
      .map(c => ({ ...c, score: calcScore(c, userSkills, cgpa, lc, gh) }))
      .sort((a, b) => b.score - a.score);
    buildResults(name);
    show('p-res');
    document.getElementById('s2').classList.add('done');
    document.getElementById('s3').classList.add('active');
    // Animate match bars
    setTimeout(() => {
      document.querySelectorAll('.mb').forEach(b => { b.style.width = b.dataset.p + '%'; });
    }, 100);
  }, steps.length * 700 + 600);
}

// ── BUILD RESULTS PAGE ────────────────────────────────────────────────────────
function buildResults(name) {
  document.getElementById('rsub').textContent =
    `Hi ${name}! Based on your profile, here are your top career matches 🎉`;

  // Career match cards
  document.getElementById('ccards').innerHTML = results.map((c, i) => `
    <div class="cc ${i === 0 ? 'top' : ''}">
      <div class="ci">${c.icon}</div>
      <div class="cn">${c.name}</div>
      <div class="cd">${c.desc}</div>
      <div class="mbg"><div class="mb" data-p="${c.score}" style="width:0%"></div></div>
      <div class="mp">${c.score}%</div>
      <div class="ml">Career Match Score</div>
    </div>`).join('');

  const top = results[0];

  // Skill gap
  const have    = userSkills.filter(s =>  top.need.includes(s));
  const missing = top.need.filter(s => !userSkills.includes(s));
  const extra   = userSkills.filter(s => !top.need.includes(s)).slice(0, 5);

  document.getElementById('shv').innerHTML =
    (have.length ? have : ['Keep building skills!']).map(s => `<span class="tag hv">✓ ${s}</span>`).join('') +
    extra.map(s => `<span class="tag lr">~ ${s}</span>`).join('');

  document.getElementById('sms').innerHTML =
    (missing.length ? missing : ['All core skills covered! 🎉']).map(s => `<span class="tag ms">✗ ${s}</span>`).join('');

  // Roadmap
  document.getElementById('rmcon').innerHTML = top.roadmap.map(r => `
    <div class="ri">
      <div class="rw">${r.w}</div>
      <div class="rc-box">
        <h4>${r.t}</h4>
        <p>${r.d}</p>
        <div class="rrs">${r.rs.map(x => `<span class="rt">${x}</span>`).join('')}</div>
      </div>
    </div>`).join('');

  // Salary
  document.getElementById('salgrid').innerHTML = top.salary.map(s => `
    <div class="si">
      <div class="cy">📍 ${s.c}</div>
      <div class="rg">${s.r}</div>
      <div class="ex">${s.e}</div>
    </div>`).join('');
}

// ── RADAR CHART ───────────────────────────────────────────────────────────────
let radarInstance = null;

function renderRadar() {
  if (radarInstance) { radarInstance.destroy(); radarInstance = null; }
  const car = results[0];
  if (!car) return;

  // Estimate user's level per radar dimension from skills count
  const userScores = car.radarLabels.map((_, i) => {
    const req = car.radarRequired[i];
    return Math.max(2, Math.round(req * 0.35 + (userSkills.length / 12) * req * 0.65));
  });

  radarInstance = new Chart(document.getElementById('rc').getContext('2d'), {
    type: 'radar',
    data: {
      labels: car.radarLabels,
      datasets: [
        { label: 'Required',   data: car.radarRequired, borderColor:'rgba(108,99,255,.8)', backgroundColor:'rgba(108,99,255,.1)', pointBackgroundColor:'#6C63FF' },
        { label: 'Your Level', data: userScores,         borderColor:'rgba(67,198,172,.8)',  backgroundColor:'rgba(67,198,172,.1)',  pointBackgroundColor:'#43C6AC' }
      ]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      scales: { r: { min:0, max:10, ticks:{ display:false }, grid:{ color:'rgba(255,255,255,.07)' }, pointLabels:{ color:'#8892a4', font:{ size:12 } } } },
      plugins: { legend: { labels: { color:'#e0e0e0' } } }
    }
  });
}

// ── TABS ──────────────────────────────────────────────────────────────────────
function stab(id, btn) {
  ['t-gap','t-rm','t-radar','t-sal'].forEach(x => {
    document.getElementById(x).style.display = 'none';
  });
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.getElementById(id).style.display = 'block';
  btn.classList.add('active');
  if (id === 't-radar') setTimeout(renderRadar, 50);
}

// ── DEMO DATA ─────────────────────────────────────────────────────────────────
function demo() {
  show('p-form');
  setTimeout(() => {
    document.getElementById('fn').value       = 'Arjun Verma';
    document.getElementById('fb').value       = 'Computer Science Engineering';
    document.getElementById('fg-cgpa').value  = '8.2';
    document.getElementById('fy').value       = '3rd Year';
    document.getElementById('fw').value       = 'Building Products (SDE)';
    document.getElementById('fe').value       = '1 Internship';
    document.getElementById('flc').value      = '120';
    document.getElementById('fgh').value      = '6';
    const preSelect = ['Python','JavaScript','React','Git','SQL','DSA','HTML/CSS','Node.js'];
    document.querySelectorAll('.chip').forEach(chip => {
      if (preSelect.includes(chip.textContent)) chip.classList.add('on');
    });
  }, 200);
}
