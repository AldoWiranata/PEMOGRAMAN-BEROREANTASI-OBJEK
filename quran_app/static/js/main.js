// ============ STATE ============
let currentPage = 'home';
let allSurat = [];
let showAyatNumber = true;
let currentFontSize = 1.4;
let prayerTimes = {};
let userCity = 'Jakarta';

// ============ PRAYER TIMES API ============
async function getPrayerTimes(city = 'jakarta') {
    try {
        const response = await fetch(`https://api.aladhan.com/v1/timingsByCity?city=${city}&country=Indonesia&method=2`);
        const data = await response.json();
        if (data.code === 200) {
            prayerTimes = data.data.timings;
            userCity = city;
            return true;
        }
        return false;
    } catch (error) {
        return false;
    }
}

function getNextPrayer(timings) {
    const now = new Date();
    const currentTime = now.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' });
    const prayers = [
        { name: 'Subuh', time: timings.Fajr, icon: '🌅' },
        { name: 'Dzuhur', time: timings.Dhuhr, icon: '☀️' },
        { name: 'Ashar', time: timings.Asr, icon: '🌤️' },
        { name: 'Maghrib', time: timings.Maghrib, icon: '🌇' },
        { name: 'Isya', time: timings.Isha, icon: '🌙' }
    ];
    for (let prayer of prayers) {
        if (prayer.time > currentTime) return prayer;
    }
    return prayers[0];
}

function renderPrayerTimes() {
    const grid = document.getElementById('prayerTimesGrid');
    if (!grid) return;
    const prayers = [
        { name: 'Imsak', time: prayerTimes.Imsak || '--:--', icon: '🌙' },
        { name: 'Subuh', time: prayerTimes.Fajr || '--:--', icon: '🌅' },
        { name: 'Dzuhur', time: prayerTimes.Dhuhr || '--:--', icon: '☀️' },
        { name: 'Ashar', time: prayerTimes.Asr || '--:--', icon: '🌤️' },
        { name: 'Maghrib', time: prayerTimes.Maghrib || '--:--', icon: '🌇' },
        { name: 'Isya', time: prayerTimes.Isha || '--:--', icon: '🌙' }
    ];
    const next = getNextPrayer(prayerTimes);
    grid.innerHTML = prayers.map(p => `<div class="prayer-card ${next && p.name === next.name ? 'prayer-next' : ''}"><div class="prayer-name"><span>${p.icon}</span> ${p.name}</div><div class="prayer-time">${p.time}</div>${next && p.name === next.name ? '<small>❖ Berikutnya</small>' : ''}</div>`).join('');
    const locElem = document.getElementById('prayerLocation');
    if (locElem) locElem.innerHTML = `<i class="fas fa-map-marker-alt"></i> ${userCity.toUpperCase()}, Indonesia`;
}

window.refreshPrayerTime = async function() {
    const newCity = prompt('Masukkan nama kota:', userCity);
    if (newCity && newCity.trim()) {
        if (await getPrayerTimes(newCity.trim())) {
            renderPrayerTimes();
        } else {
            alert('Gagal mengambil jadwal sholat.');
        }
    }
};

// ============ DARK MODE ============
const darkBtn = document.getElementById('darkModeBtn');
darkBtn.onclick = () => {
    document.body.classList.toggle('dark-mode');
    document.body.classList.toggle('light-mode');
    const isDark = document.body.classList.contains('dark-mode');
    darkBtn.innerHTML = isDark ? '<i class="fas fa-sun"></i> <span>Mode Terang</span>' : '<i class="fas fa-moon"></i> <span>Mode Gelap</span>';
};

// ============ HAMBURGER MENU ============
const hamburger = document.getElementById('hamburgerBtn');
const sidebarEl = document.getElementById('sidebar');
const overlay = document.getElementById('sidebarOverlay');
const toggleSidebar = () => {
    sidebarEl.classList.toggle('open');
    overlay.classList.toggle('show');
    document.body.style.overflow = sidebarEl.classList.contains('open') ? 'hidden' : '';
};
hamburger.onclick = toggleSidebar;
overlay.onclick = toggleSidebar;

document.querySelectorAll('.menu-btn').forEach(btn => {
    btn.onclick = () => {
        if (window.innerWidth <= 768) toggleSidebar();
    };
});

// ============ SETTINGS MODAL ============
const settingsBtn = document.getElementById('settingsBtn');
const settingsModal = document.getElementById('settingsModal');
settingsBtn.onclick = () => settingsModal.style.display = 'block';

document.querySelectorAll('.settings-close, .modal-close').forEach(btn => {
    btn.onclick = () => {
        document.getElementById('modal').style.display = 'none';
        settingsModal.style.display = 'none';
    };
});

// ============ STAY AWAKE ============
let wakeLock = null;
const stayAwakeToggle = document.getElementById('stayAwakeToggle');
if (stayAwakeToggle) {
    stayAwakeToggle.onchange = async (e) => {
        if (e.target.checked) {
            try {
                wakeLock = await navigator.wakeLock.request('screen');
            } catch (err) {
                alert('Fitur tidak didukung');
            }
        } else {
            if (wakeLock) {
                await wakeLock.release();
                wakeLock = null;
            }
        }
    };
}

// ============ TOGGLE NOMOR AYAT ============
const showAyatNumberToggle = document.getElementById('showAyatNumberToggle');
if (showAyatNumberToggle) {
    showAyatNumberToggle.onchange = (e) => {
        showAyatNumber = e.target.checked;
        refreshCurrentModal();
    };
}

function refreshCurrentModal() {
    const modal = document.getElementById('modal');
    if (modal.style.display === 'block') {
        const title = document.getElementById('modalTitle').innerHTML;
        const match = title.match(/\d+/);
        if (match) showDetail(parseInt(match[0]));
    }
}

// ============ FONT SIZE ============
const fontMinus = document.getElementById('fontMinus');
const fontPlus = document.getElementById('fontPlus');
const fontSizeSpan = document.getElementById('fontSizeValue');

function updateFontSize() {
    document.querySelectorAll('.ayat-arab, .bismillah-text').forEach(el => {
        el.style.fontSize = currentFontSize + 'rem';
    });
    if (fontSizeSpan) fontSizeSpan.textContent = currentFontSize.toFixed(1) + 'rem';
}

if (fontMinus) {
    fontMinus.onclick = () => {
        currentFontSize = Math.max(0.9, currentFontSize - 0.1);
        updateFontSize();
    };
}
if (fontPlus) {
    fontPlus.onclick = () => {
        currentFontSize = Math.min(2.3, currentFontSize + 0.1);
        updateFontSize();
    };
}

// ============ TAJWID PERMANEN ============
function applyPermanentTajwid(arabText) {
    let text = arabText;
    text = text.replace(/ال/g, '<span class="tajwid-idgham">ال</span>');
    text = text.replace(/مّ/g, '<span class="tajwid-idgham">مّ</span>');
    text = text.replace(/نّ/g, '<span class="tajwid-idgham">نّ</span>');
    text = text.replace(/[قطبجد]/g, match => `<span class="tajwid-qalqalah">${match}</span>`);
    text = text.replace(/[ءعحغ]/g, match => `<span class="tajwid-izhar">${match}</span>`);
    return text;
}

function toArabicNumber(num) {
    const arabicDigits = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩'];
    return num.toString().split('').map(d => arabicDigits[parseInt(d)]).join('');
}

// ============ NAVIGASI MENU ============
function goToPage(page) {
    document.querySelector(`.menu-btn[data-page="${page}"]`).click();
}

document.querySelectorAll('.menu-btn').forEach(btn => {
    btn.onclick = () => {
        document.querySelectorAll('.menu-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentPage = btn.dataset.page;
        if (currentPage === 'home') loadHomeWithPrayer();
        else if (currentPage === 'surat') loadSurat();
        else if (currentPage === 'juz') loadJuz();
        else if (currentPage === 'doa') loadDoa();
    };
});

// ============ LOAD HOME ============
async function loadHomeWithPrayer() {
    const c = document.getElementById('contentArea');
    c.innerHTML = '<div class="loading"><i class="fas fa-spinner fa-pulse"></i> Loading...</div>';
    await getPrayerTimes(userCity);
    let randomDoa = { arab: 'بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ', artinya: 'Dengan nama Allah Yang Maha Pengasih, Maha Penyayang' };
    try {
        const r = await fetch('/api/doa/random');
        const d = await r.json();
        if (d.status === 'success') randomDoa = d.data;
    } catch (e) {}
    c.innerHTML = `
        <div class="daily-doa">
            <h3><i class="fas fa-hands-praying"></i> Doa Hari Ini</h3>
            <div class="doa-arab">${randomDoa.arab}</div>
            <div class="doa-arti">${randomDoa.artinya}</div>
        </div>
        <div class="prayer-container">
            <div class="section-header"><h2><i class="fas fa-clock"></i> Jadwal Sholat</h2></div>
            <div class="prayer-grid" id="prayerTimesGrid"></div>
            <div class="location-info" onclick="refreshPrayerTime()">
                <span id="prayerLocation">📍 ${userCity.toUpperCase()}, Indonesia</span>
                <i class="fas fa-sync-alt"></i>
            </div>
        </div>
        <div class="feature-grid">
            <div class="feature-card" onclick="goToPage('surat')">
                <div class="feature-icon">📖</div>
                <h4>Baca Al-Qur'an</h4>
                <p>114 Surat</p>
            </div>
            <div class="feature-card" onclick="goToPage('juz')">
                <div class="feature-icon">📚</div>
                <h4>Navigasi Juz</h4>
                <p>30 Juz</p>
            </div>
            <div class="feature-card" onclick="goToPage('doa')">
                <div class="feature-icon">🤲</div>
                <h4>Doa Harian</h4>
                <p>Kumpulan Doa</p>
            </div>
        </div>
    `;
    renderPrayerTimes();
}

// ============ LOAD SURAT ============
async function loadSurat() {
    const c = document.getElementById('contentArea');
    c.innerHTML = '<div class="loading"><i class="fas fa-spinner fa-pulse"></i> Loading surat...</div>';
    try {
        const r = await fetch('/api/surat');
        const d = await r.json();
        allSurat = d.data;
        c.innerHTML = `
            <div class="section-header"><h2><i class="fas fa-book"></i> Daftar Surat Al-Qur'an</h2></div>
            <div class="surat-grid">
                ${allSurat.map(s => `
                    <div class="surat-card" onclick="showDetail(${s.nomor})">
                        <h3>${s.nomor}. ${s.nama}</h3>
                        <div class="arab">${s.nama_arab}</div>
                        <p>${s.arti}</p>
                        <small><i class="fas fa-verse"></i> ${s.jumlah_ayat} ayat • ${s.tempat} • Juz ${s.juz}</small>
                    </div>
                `).join('')}
            </div>
        `;
    } catch (e) {
        c.innerHTML = '<div class="empty">Gagal memuat surat</div>';
    }
}

// ============ JUZ ============
function loadJuz() {
    const juzList = Array.from({ length: 30 }, (_, i) => i + 1);
    document.getElementById('contentArea').innerHTML = `
        <div class="section-header"><h2><i class="fas fa-layer-group"></i> Navigasi Juz</h2></div>
        <div class="juz-grid">
            ${juzList.map(j => `<div class="juz-item" onclick="loadByJuz(${j})">Juz ${j}</div>`).join('')}
        </div>
        <div id="juzResult" style="margin-top:20px"></div>
    `;
}

async function loadByJuz(juz) {
    const rdiv = document.getElementById('juzResult');
    rdiv.innerHTML = '<div class="loading">Loading...</div>';
    try {
        const r = await fetch(`/api/surat/juz/${juz}`);
        const d = await r.json();
        rdiv.innerHTML = `
            <div class="section-header"><h3><i class="fas fa-book"></i> Surat dalam Juz ${juz}</h3></div>
            <div class="surat-grid">
                ${d.data.map(s => `
                    <div class="surat-card" onclick="showDetail(${s.nomor})">
                        <h3>${s.nomor}. ${s.nama}</h3>
                        <div class="arab">${s.nama_arab}</div>
                        <p>${s.arti}</p>
                        <small>${s.jumlah_ayat} ayat</small>
                    </div>
                `).join('')}
            </div>
        `;
    } catch (e) {
        rdiv.innerHTML = '<div class="empty">Gagal memuat</div>';
    }
}

// ============ DOA ============
async function loadDoa() {
    const c = document.getElementById('contentArea');
    c.innerHTML = '<div class="loading"><i class="fas fa-spinner fa-pulse"></i> Loading doa...</div>';
    try {
        const r = await fetch('/api/doa');
        const d = await r.json();
        c.innerHTML = `
            <div class="section-header"><h2><i class="fas fa-hands-praying"></i> Doa-Doa Harian</h2></div>
            <div class="doa-grid">
                ${d.data.map(d => `
                    <div class="doa-card">
                        <h4><i class="fas fa-praying-hands"></i> ${d.nama}</h4>
                        <div class="arab">${d.arab}</div>
                        <div class="doa-arti">${d.artinya}</div>
                    </div>
                `).join('')}
            </div>
        `;
    } catch (e) {
        c.innerHTML = '<div class="empty">Gagal memuat doa</div>';
    }
}

// ============ SHOW DETAIL SURAT ============
async function showDetail(nomor) {
    const modal = document.getElementById('modal');
    const mt = document.getElementById('modalTitle');
    const mb = document.getElementById('modalBody');
    mt.innerHTML = '<i class="fas fa-spinner fa-pulse"></i> Loading...';
    mb.innerHTML = '<div class="loading">Loading ayat...</div>';
    modal.style.display = 'block';
    document.body.style.overflow = 'hidden';
    try {
        const r = await fetch(`/api/surat/${nomor}`);
        const d = await r.json();
        const s = d.data;
        mt.innerHTML = `${s.nama} (${s.nama_arab})`;
        let ayatHTML = '';
        const isNotTaubah = (nomor !== 9);
        for (let i = 0; i < s.ayat.length; i++) {
            let a = s.ayat[i];
            let rawArab = a.teks_arab;
            let processedArab = applyPermanentTajwid(rawArab);
            let nomorSpan = '';
            if (showAyatNumber) {
                nomorSpan = `<span class="ayat-number-badge-arabic">﴿${toArabicNumber(a.nomor)}﴾</span>`;
            }
            if (i === 0 && isNotTaubah && rawArab.includes('بِسْمِ اللَّهِ')) {
                const bismillahMatch = rawArab.match(/بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ/g);
                if (bismillahMatch) {
                    const bismillahText = bismillahMatch[0];
                    const sisaArab = rawArab.replace(bismillahText, '').trim();
                    const processedBismillah = applyPermanentTajwid(bismillahText);
                    const processedSisa = sisaArab ? applyPermanentTajwid(sisaArab) : '';
                    ayatHTML += `<div class="bismillah-container"><div class="bismillah-text">${processedBismillah}</div></div>`;
                    if (processedSisa) {
                        ayatHTML += `<div class="ayat-item"><div class="ayat-arab-wrapper"><div class="ayat-arab">${processedSisa}</div>${nomorSpan}</div><div class="ayat-terjemah">${a.terjemahan}</div></div>`;
                    } else {
                        ayatHTML += `<div class="ayat-item"><div class="ayat-arab-wrapper"><div class="ayat-arab">ـ</div>${nomorSpan}</div><div class="ayat-terjemah">${a.terjemahan}</div></div>`;
                    }
                    continue;
                }
            }
            ayatHTML += `<div class="ayat-item"><div class="ayat-arab-wrapper"><div class="ayat-arab">${processedArab}</div>${nomorSpan}</div><div class="ayat-terjemah">${a.terjemahan}</div></div>`;
        }
        mb.innerHTML = `<div style="margin-bottom:12px; opacity:0.7;"><strong>${s.arti}</strong> • ${s.jumlah_ayat} ayat • ${s.tempat} • Juz ${s.juz}</div><hr style="margin:12px 0">${ayatHTML}`;
        updateFontSize();
    } catch (e) {
        mb.innerHTML = '<div class="empty">Gagal memuat detail surat</div>';
    }
}

// ============ SEARCH ============
const searchBtn = document.getElementById('searchBtn');
if (searchBtn) {
    searchBtn.onclick = async () => {
        const kw = document.getElementById('searchInput').value;
        if (!kw) return;
        const c = document.getElementById('contentArea');
        c.innerHTML = '<div class="loading">Mencari...</div>';
        try {
            const r = await fetch(`/api/search?q=${encodeURIComponent(kw)}`);
            const d = await r.json();
            if (d.data.length === 0) {
                c.innerHTML = `<div class="empty"><i class="fas fa-search"></i> "${kw}" tidak ditemukan</div>`;
                return;
            }
            c.innerHTML = `
                <div class="section-header"><h2><i class="fas fa-search"></i> Hasil: "${kw}"</h2></div>
                <div class="surat-grid">
                    ${d.data.map(s => `
                        <div class="surat-card" onclick="showDetail(${s.nomor})">
                            <h3>${s.nomor}. ${s.nama}</h3>
                            <div class="arab">${s.nama_arab}</div>
                            <p>${s.arti}</p>
                            <small>${s.jumlah_ayat} ayat</small>
                        </div>
                    `).join('')}
                </div>
            `;
        } catch (e) {
            c.innerHTML = '<div class="empty">Gagal mencari</div>';
        }
    };
}

// ============ MODAL CLOSE ============
window.onclick = e => {
    if (e.target === document.getElementById('modal')) {
        document.getElementById('modal').style.display = 'none';
        document.body.style.overflow = '';
    }
    if (e.target === settingsModal) {
        settingsModal.style.display = 'none';
    }
};

// ============ START ============
loadHomeWithPrayer();