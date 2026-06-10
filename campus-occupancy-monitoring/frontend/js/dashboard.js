/**
 * Dashboard de Monitoreo de Ocupación – Laboratorios UAO
 */

const CONFIG = {
    API_BASE_URL: 'http://localhost:5000/api',
    UPDATE_INTERVAL_MS: 15 * 60 * 1000,
    TOAST_DURATION_MS: 3500,
    PEOPLE_THRESHOLDS: { empty_max: 30, partial_max: 60 },
};

const AUTO_INTERVAL_SECONDS = 15 * 60; // 15 minutos
const LS_KEY = 'ocupacion_next_analysis'; // clave en localStorage

let state = {
    currentData: null,
    isLoading: false,
    countdownTimer: null,
};

const el = {
    peopleCount:         document.getElementById('peopleCount'),
    imagesAnalyzedLabel: document.getElementById('imagesAnalyzedLabel'),
    occupancyProgress:   document.getElementById('occupancyProgress'),
    siteName:            document.getElementById('siteName'),
    lastUpdate:          document.getElementById('lastUpdate'),
    statusBadge:         document.getElementById('statusBadge'),
    statusCard:          document.getElementById('statusCard'),
    nextUpdate:          document.getElementById('nextUpdate'),
    lastUpdateTime:      document.getElementById('lastUpdateTime'),
    analyzeBtn:          document.getElementById('analyzeBtn'),
    resultsSection:      document.getElementById('resultsSection'),
    resultsGrid:         document.getElementById('resultsGrid'),
    resultsSummary:      document.getElementById('resultsSummary'),
    alertsList:          document.getElementById('alertsList'),
    alertsCount:         document.getElementById('alertsCount'),
    loadingOverlay:      document.getElementById('loadingOverlay'),
    loadingText:         document.getElementById('loadingText'),
    toastContainer:      document.getElementById('toastContainer'),
    refreshBtn:          document.getElementById('refreshBtn'),
    exportCsvBtn:        document.getElementById('exportCsvBtn'),
};

function showLoading(show, text = 'Analizando con YOLO...') {
    el.loadingText.textContent = text;
    el.loadingOverlay.classList.toggle('hidden', !show);
}

function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    el.toastContainer.appendChild(toast);
    setTimeout(() => {
        toast.style.animation = 'slideIn 0.3s ease reverse';
        setTimeout(() => toast.remove(), 300);
    }, CONFIG.TOAST_DURATION_MS);
}

function addAlert(type, message) {
    const icons = {
        info:    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>',
        success: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>',
        warning: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
        danger:  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>',
    };
    const time = new Date().toLocaleTimeString('es-CO', { hour: '2-digit', minute: '2-digit' });
    const li = document.createElement('li');
    li.className = `alert-item alert-${type}`;
    li.innerHTML = `${icons[type] || icons.info}<div class="alert-content"><span class="alert-title">${message}</span><span class="alert-time">${time}</span></div>`;
    el.alertsList.insertBefore(li, el.alertsList.firstChild);
    const all = el.alertsList.querySelectorAll('.alert-item');
    if (all.length > 15) all[all.length - 1].remove();
    el.alertsCount.textContent = el.alertsList.querySelectorAll('.alert-item').length;
}

function updateDashboard(data) {
    state.currentData = data;
    el.peopleCount.textContent    = data.people_count;
    el.siteName.textContent       = data.site || '--';
    el.lastUpdate.textContent     = `Última actualización: ${data.last_update}`;
    el.lastUpdateTime.textContent = data.last_update || '--';
    el.imagesAnalyzedLabel.textContent = `${data.images_analyzed ?? 0} imagen(es) analizadas`;
    updateProgressBar(data.people_count);
    updateStatusBadge(data.status);
    // nextUpdate lo maneja exclusivamente el countdown — no se toca aquí
}

function updateProgressBar(count) {
    const pct = Math.min((count / 60) * 100, 100);
    el.occupancyProgress.style.width = `${pct}%`;
    el.occupancyProgress.classList.remove('low', 'medium', 'high');
    if (count <= CONFIG.PEOPLE_THRESHOLDS.empty_max)        el.occupancyProgress.classList.add('low');
    else if (count <= CONFIG.PEOPLE_THRESHOLDS.partial_max) el.occupancyProgress.classList.add('medium');
    else                                                     el.occupancyProgress.classList.add('high');
}

function updateStatusBadge(status) {
    el.statusBadge.textContent = status || '--';
    el.statusBadge.className   = 'status-badge';
    el.statusCard.className    = 'stat-card';
    if (status === 'Vacío')                   { el.statusBadge.classList.add('empty');   el.statusCard.classList.add('card-empty'); }
    else if (status === 'Parcialmente lleno') { el.statusBadge.classList.add('partial'); el.statusCard.classList.add('card-partial'); }
    else if (status === 'Lleno')              { el.statusBadge.classList.add('full');    el.statusCard.classList.add('card-full'); }
}

function displayImageResults(imageResults) {
    if (!imageResults || imageResults.length === 0) { el.resultsSection.classList.add('hidden'); return; }
    el.resultsGrid.innerHTML = '';
    imageResults.forEach(result => {
        const card = document.createElement('div');
        card.className = 'result-card';
        const imgSrc = result.processed_image_filename
            ? `${CONFIG.API_BASE_URL}/imagen/procesada/${result.processed_image_filename}` : null;
        const simTag = result.simulated ? '<span class="sim-tag">Simulado</span>' : '';
        card.innerHTML = `
            <div class="result-img-wrap">
                ${imgSrc
                    ? `<img src="${imgSrc}" alt="Resultado YOLO" class="result-img lb-trigger"
                           onerror="this.parentElement.innerHTML='<div class=\\'img-placeholder\\'>Sin imagen procesada</div>'">`
                    : '<div class="img-placeholder">Sin imagen procesada</div>'}
            </div>
            <div class="result-info">
                <span class="result-count">${result.count} persona${result.count !== 1 ? 's' : ''}</span>
                ${simTag}
            </div>`;
        el.resultsGrid.appendChild(card);
    });
    el.resultsSection.classList.remove('hidden');
}

async function analyzeDataset() {
    if (state.isLoading) return;
    state.isLoading = true;
    el.analyzeBtn.disabled = true;
    // Reinicia el temporizador global al analizar manualmente
    localStorage.setItem(LS_KEY, Date.now() + AUTO_INTERVAL_SECONDS * 1000);
    showLoading(true, 'Capturando 5 imágenes y analizando con YOLO...');
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/analizar-dataset`, { method: 'POST' });
        if (!response.ok) throw new Error(`Error HTTP ${response.status}`);
        const result = await response.json();
        if (result.status !== 'success') throw new Error(result.message || 'Error desconocido');
        updateDashboard(result.data);
        displayImageResults(result.data.image_results);
        el.resultsSummary.textContent = `Total: ${result.data.people_count} persona(s) en ${result.data.images_analyzed} imagen(es)`;
        addAlert('success', `Análisis completado – ${result.data.people_count} persona(s) → ${result.data.status} · Reporte guardado`);
        showToast(`${result.data.status}: ${result.data.people_count} persona(s)`, 'success');
    } catch (error) {
        showToast(`Error: ${error.message}`, 'error');
        addAlert('danger', `Error en análisis: ${error.message}`);
    } finally {
        state.isLoading = false;
        el.analyzeBtn.disabled = false;
        showLoading(false);
    }
}

async function loadCurrentStatus() {
    if (state.isLoading) return;
    state.isLoading = true;
    showLoading(true, 'Cargando estado actual...');
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/estado-actual`);
        if (!response.ok) throw new Error(`Error HTTP ${response.status}`);
        const result = await response.json();
        if (result.status !== 'success') throw new Error(result.message || 'Error');
        updateDashboard(result.data);
        displayImageResults(result.data.image_results);
        addAlert('info', result.data.message || `Estado actualizado – ${result.data.people_count} persona(s) → ${result.data.status}`);
    } catch (error) {
        addAlert('danger', `Error al obtener estado: ${error.message}`);
        showToast(`Error: ${error.message}`, 'error');
    } finally {
        state.isLoading = false;
        showLoading(false);
    }
}

function getNextAnalysisTime() {
    const stored = localStorage.getItem(LS_KEY);
    if (stored) {
        const t = parseInt(stored, 10);
        if (t > Date.now()) return t; // todavía vigente
    }
    // No hay registro o ya venció → programar nuevo ciclo
    const next = Date.now() + AUTO_INTERVAL_SECONDS * 1000;
    localStorage.setItem(LS_KEY, next);
    return next;
}

function formatCountdown(seconds) {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
}

function startCountdown() {
    if (state.countdownTimer) clearInterval(state.countdownTimer);

    state.countdownTimer = setInterval(async () => {
        const remaining = Math.ceil((parseInt(localStorage.getItem(LS_KEY), 10) - Date.now()) / 1000);

        if (remaining > 0) {
            el.nextUpdate.textContent = formatCountdown(remaining);
        } else {
            // Programar el próximo ciclo ANTES de analizar para que no se solapen
            localStorage.setItem(LS_KEY, Date.now() + AUTO_INTERVAL_SECONDS * 1000);
            await analyzeDataset();
        }
    }, 1000);
}

function exportToCsv() {
    if (!state.currentData) { showToast('No hay datos para exportar', 'error'); return; }
    const d = state.currentData;
    const rows = [['Sitio', d.site], ['Personas detectadas', d.people_count], ['Estado', d.status],
                  ['Imágenes analizadas', d.images_analyzed], ['Última actualización', d.last_update]];
    if (d.image_results) { rows.push(['', '']); rows.push(['Imagen', 'Personas']); d.image_results.forEach(r => rows.push([r.source_image, r.count])); }
    const csv = rows.map(r => r.join(',')).join('\n');
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `ocupacion_${new Date().toISOString().slice(0,10)}.csv`;
    link.style.visibility = 'hidden';
    document.body.appendChild(link); link.click(); document.body.removeChild(link);
    showToast('CSV exportado', 'success');
}

function setupEventListeners() {
    el.analyzeBtn.addEventListener('click', analyzeDataset);
    el.refreshBtn.addEventListener('click', loadCurrentStatus);
    if (el.exportCsvBtn) el.exportCsvBtn.addEventListener('click', exportToCsv);
}

function init() {
    setupEventListeners();
    const next = getNextAnalysisTime(); // asegura timestamp en localStorage
    const remaining = Math.max(1, Math.ceil((next - Date.now()) / 1000));
    el.nextUpdate.textContent = formatCountdown(remaining);
    loadCurrentStatus();
    startCountdown();
    addAlert('info', `Dashboard listo – análisis automático cada 15 min · presiona "Analizar Sótanos" para analizar ahora`);
}

document.addEventListener('DOMContentLoaded', init);
