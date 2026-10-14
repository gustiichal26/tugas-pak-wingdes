// Dashboard Statistik Deskriptif - JavaScript Frontend
document.addEventListener('DOMContentLoaded', async () => {
  // Tabs switcher
  const tabBtns = document.querySelectorAll('.tab-btn');
  const tabPanels = document.querySelectorAll('.tab-panel');

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const target = btn.dataset.tab;
      tabBtns.forEach(b => b.classList.remove('active'));
      tabPanels.forEach(p => p.classList.remove('active'));
      btn.classList.add('active');
      document.getElementById('panel-' + target).classList.add('active');
    });
  });

  try {
    const res = await fetch('/api/summary');
    const data = await res.json();
    renderDashboard(data);
  } catch (err) {
    console.error('Error fetching data:', err);
  }
});

function renderDashboard(data) {
  // 1. KPI Cards
  document.getElementById('kpi-total').textContent = '100 Nilai';
  document.getElementById('kpi-mean').textContent = data.gabungan.mean.toFixed(2);
  document.getElementById('kpi-sd').textContent = data.gabungan.sd_sampel.toFixed(4);
  document.getElementById('kpi-cv').textContent = data.gabungan.cv.toFixed(2) + '%';
  document.querySelectorAll('.kpi-card').forEach(c => c.classList.remove('loading'));

  // 2. Overview Cards
  const ovContainer = document.getElementById('overview-cards');
  ovContainer.innerHTML = '';
  data.kelompok.forEach(k => {
    const s = data.stats_per_kelompok[k];
    let badgeClass = 'ov-badge-sedang';
    if (s.kategori.includes('lebar')) badgeClass = 'ov-badge-lebar';
    if (s.kategori.includes('sempit')) badgeClass = 'ov-badge-sempit';

    const card = document.createElement('div');
    card.className = 'ov-card';
    card.innerHTML = `
      <div class="ov-card-title">
        <span>${k}</span>
        <span class="ov-badge ${badgeClass}">${s.kategori.replace('Sebaran ', '')}</span>
      </div>
      <div class="ov-stats">
        <div class="ov-stat"><div class="ov-stat-label">Mean</div><div class="ov-stat-val">${s.mean.toFixed(2)}</div></div>
        <div class="ov-stat"><div class="ov-stat-label">Median</div><div class="ov-stat-val">${s.median.toFixed(2)}</div></div>
        <div class="ov-stat"><div class="ov-stat-label">SD Sampel</div><div class="ov-stat-val">${s.sd_sampel.toFixed(4)}</div></div>
        <div class="ov-stat"><div class="ov-stat-label">CV</div><div class="ov-stat-val">${s.cv.toFixed(1)}%</div></div>
      </div>
    `;
    ovContainer.appendChild(card);
  });

  // 3. Statistik Table
  const tbody = document.getElementById('stat-tbody');
  tbody.innerHTML = '';
  data.kelompok.forEach(k => {
    const s = data.stats_per_kelompok[k];
    let tag = '<span class="tag tag-yellow">Sedang</span>';
    if (s.kategori.includes('lebar')) tag = '<span class="tag tag-red">Lebar (Heterogen)</span>';
    if (s.kategori.includes('sempit')) tag = '<span class="tag tag-green">Sempit (Homogen)</span>';

    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><strong>${k}</strong></td>
      <td>${s.n}</td>
      <td>${s.mean.toFixed(2)}</td>
      <td>${s.median.toFixed(2)}</td>
      <td>${s.modus}</td>
      <td>${s.min}</td>
      <td>${s.maks}</td>
      <td>${s.range}</td>
      <td>${s.q1.toFixed(2)}</td>
      <td>${s.q3.toFixed(2)}</td>
      <td>${s.iqr.toFixed(2)}</td>
      <td>${s.varians_sampel.toFixed(4)}</td>
      <td><strong>${s.sd_sampel.toFixed(4)}</strong></td>
      <td>${s.sd_populasi.toFixed(4)}</td>
      <td>${s.selisih_sd.toFixed(4)}</td>
      <td>${s.cv.toFixed(2)}%</td>
      <td>#${s.peringkat_sd}</td>
      <td>${tag}</td>
    `;
    tbody.appendChild(tr);
  });

  // Add Gabungan Row
  const g = data.gabungan;
  const gTr = document.createElement('tr');
  gTr.className = 'gabungan-row';
  gTr.innerHTML = `
    <td><strong>Gabungan (100 org)</strong></td>
    <td>${g.n}</td>
    <td>${g.mean.toFixed(2)}</td>
    <td>${g.median.toFixed(2)}</td>
    <td>${g.modus}</td>
    <td>${g.min}</td>
    <td>${g.maks}</td>
    <td>${g.range}</td>
    <td>${g.q1.toFixed(2)}</td>
    <td>${g.q3.toFixed(2)}</td>
    <td>${g.iqr.toFixed(2)}</td>
    <td>${g.varians_sampel.toFixed(4)}</td>
    <td><strong>${g.sd_sampel.toFixed(4)}</strong></td>
    <td>${g.sd_populasi.toFixed(4)}</td>
    <td>${g.selisih_sd.toFixed(4)}</td>
    <td>${g.cv.toFixed(2)}%</td>
    <td>-</td>
    <td>Seluruh data</td>
  `;
  tbody.appendChild(gTr);

  // 4. Charts (Chart.js)
  Chart.defaults.color = '#8892b0';
  Chart.defaults.font.family = 'Inter';

  // Chart Mean
  new Chart(document.getElementById('chartMean'), {
    type: 'bar',
    data: {
      labels: data.kelompok,
      datasets: [{
        label: 'Mean (Rata-rata)',
        data: data.mean,
        backgroundColor: '#4f8cff',
        borderRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        y: { beginAtZero: true, grid: { color: '#252840' } },
        x: { grid: { display: false } }
      }
    }
  });

  // Chart SD
  new Chart(document.getElementById('chartSD'), {
    type: 'bar',
    data: {
      labels: data.kelompok,
      datasets: [{
        label: 'Standar Deviasi Sampel',
        data: data.sd_sampel,
        backgroundColor: '#a78bfa',
        borderRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        y: { beginAtZero: true, grid: { color: '#252840' } },
        x: { grid: { display: false } }
      }
    }
  });

  // Chart CV
  new Chart(document.getElementById('chartCV'), {
    type: 'line',
    data: {
      labels: data.kelompok,
      datasets: [{
        label: 'Koefisien Variasi (%)',
        data: data.cv,
        borderColor: '#fb923c',
        backgroundColor: 'rgba(251, 146, 60, 0.1)',
        tension: 0.3,
        fill: true,
        pointBackgroundColor: '#fb923c',
        pointRadius: 5
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        y: { beginAtZero: true, grid: { color: '#252840' } },
        x: { grid: { display: false } }
      }
    }
  });

  // Chart Range Box
  new Chart(document.getElementById('chartBox'), {
    type: 'bar',
    data: {
      labels: data.kelompok,
      datasets: [
        {
          label: 'Min',
          data: data.min,
          backgroundColor: '#34d399',
          borderRadius: 4
        },
        {
          label: 'Median',
          data: data.median,
          backgroundColor: '#22d3ee',
          borderRadius: 4
        },
        {
          label: 'Maks',
          data: data.maks,
          backgroundColor: '#f87171',
          borderRadius: 4
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: { beginAtZero: true, grid: { color: '#252840' } },
        x: { grid: { display: false } }
      }
    }
  });

  // Chart SD Comparison
  new Chart(document.getElementById('chartSdComp'), {
    type: 'bar',
    data: {
      labels: data.kelompok,
      datasets: [
        {
          label: 'SD Sampel (n-1)',
          data: data.sd_sampel,
          backgroundColor: '#4f8cff',
          borderRadius: 4
        },
        {
          label: 'SD Populasi (n)',
          data: data.kelompok.map(k => data.stats_per_kelompok[k].sd_populasi),
          backgroundColor: '#a78bfa',
          borderRadius: 4
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: { beginAtZero: true, grid: { color: '#252840' } },
        x: { grid: { display: false } }
      }
    }
  });

  // 5. Raw Data Tab
  const rawSel = document.getElementById('raw-selector');
  rawSel.innerHTML = '';
  data.kelompok.forEach((k, idx) => {
    const btn = document.createElement('button');
    btn.className = 'raw-btn' + (idx === 0 ? ' active' : '');
    btn.innerHTML = `<span class="raw-btn-dot"></span> ${k}`;
    btn.addEventListener('click', () => {
      document.querySelectorAll('.raw-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      showRawDetail(k, data);
    });
    rawSel.appendChild(btn);
  });

  showRawDetail(data.kelompok[0], data);

  // Full Raw Table
  const rThead = document.getElementById('raw-thead');
  const rTbody = document.getElementById('raw-tbody');
  rThead.innerHTML = `<tr><th>Anggota</th>${data.kelompok.map(k => `<th>${k}</th>`).join('')}</tr>`;
  rTbody.innerHTML = '';
  data.orang_labels.forEach((org, i) => {
    const row = `<tr><td><strong>${org}</strong></td>${data.kelompok.map(k => `<td>${data.raw_data[k][i]}</td>`).join('')}</tr>`;
    rTbody.insertAdjacentHTML('beforeend', row);
  });

  // 6. Keputusan List
  const kList = document.getElementById('keputusan-list');
  kList.innerHTML = '';
  data.keputusan.forEach((item, idx) => {
    const div = document.createElement('div');
    div.className = 'keputusan-item';
    div.innerHTML = `
      <div class="ki-num">${idx + 1}</div>
      <div>${item}</div>
    `;
    kList.appendChild(div);
  });

  document.getElementById('kesimpulan-text').innerHTML = `
    Berdasarkan analisis statistik deskriptif di atas, terlihat adanya disparitas performa dan sebaran nilai yang signifikan antar kelompok. 
    <strong>Kelompok 10</strong> mencatatkan capaian nilai rata-rata tertinggi (7.40), sedangkan <strong>Kelompok 1</strong> memerlukan pembinaan khusus karena rata-ratanya paling rendah (3.20) serta memiliki variasi relatif (CV) tertinggi (71.87%). 
    Kelompok dengan sebaran sempit/homogen seperti <strong>Kelompok 5 dan 6</strong> membuktikan keberhasilan pemerataan pemahaman anggota kelompok. 
    Dengan demikian, keputusan instruksional dan manajerial yang tepat adalah mengadakan program mentoring sebaya (peer tutoring), penyesuaian strategi pengajaran untuk kelompok yang heterogen, serta evaluasi lanjutan pada disparitas skor antar kelompok.
  `;
}

function showRawDetail(kelompok, data) {
  const s = data.stats_per_kelompok[kelompok];
  const vals = data.raw_data[kelompok];
  const container = document.getElementById('raw-detail');
  container.innerHTML = `
    <h3>Detail Nilai: ${kelompok}</h3>
    <div class="raw-mini-stats">
      <div class="rms"><div class="rms-label">Mean</div><div class="rms-val">${s.mean.toFixed(2)}</div></div>
      <div class="rms"><div class="rms-label">SD Sampel</div><div class="rms-val">${s.sd_sampel.toFixed(4)}</div></div>
      <div class="rms"><div class="rms-label">Kategori</div><div class="rms-val" style="font-size:0.95rem;">${s.kategori}</div></div>
    </div>
    <p style="font-size:0.8rem; color:var(--text-muted); margin-bottom:10px;">10 Nilai Anggota:</p>
    <div class="raw-values">
      ${vals.map((v, i) => `<div class="rv-item"><span class="rv-item-label">Orang ${i+1}</span><span class="rv-item-val">${v}</span></div>`).join('')}
    </div>
  `;
}
