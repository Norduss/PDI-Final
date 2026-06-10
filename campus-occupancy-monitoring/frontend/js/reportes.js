/**
 * Página de Reportes – Monitor de Ocupación UAO
 */

const CONFIG = { API_BASE_URL: 'http://localhost:5000/api', TOAST_DURATION_MS: 3500 };

const AUTO_INTERVAL_SECONDS = 60; // debe coincidir con dashboard.js
const LS_KEY = 'ocupacion_next_analysis';

// ── Utilidades ───────────────────────────────────────────────
function showLoading(show) {
    document.getElementById('loadingOverlay').classList.toggle('hidden', !show);
}

function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    container.appendChild(toast);
    setTimeout(() => {
        toast.style.animation = 'slideIn 0.3s ease reverse';
        setTimeout(() => toast.remove(), 300);
    }, CONFIG.TOAST_DURATION_MS);
}

function getStatusClass(status) {
    if (status === 'Vacío')              return 'empty';
    if (status === 'Parcialmente lleno') return 'partial';
    if (status === 'Lleno')              return 'full';
    return '';
}

// ── Toggle imágenes ──────────────────────────────────────────
function toggleImages(btn) {
    const expand = btn.closest('.report-item').querySelector('.report-expand');
    const isOpen = !expand.classList.contains('hidden');
    expand.classList.toggle('hidden');
    btn.classList.toggle('open', !isOpen);
    btn.querySelector('.toggle-label').textContent = isOpen ? 'Ver imágenes' : 'Ocultar imágenes';
}

// ── Renderizado ──────────────────────────────────────────────
function updateSummaryCards(reports) {
    document.getElementById('totalReports').textContent = reports.length;
    document.getElementById('reportsCount').textContent = reports.length;

    if (reports.length === 0) {
        document.getElementById('lastStatusBadge').textContent = '--';
        document.getElementById('lastPeopleCount').textContent = '--';
        document.getElementById('lastAnalysisDate').textContent = '--';
        return;
    }

    const latest = reports[0];
    const badge = document.getElementById('lastStatusBadge');
    badge.textContent = latest.status;
    badge.className = `status-badge ${getStatusClass(latest.status)}`;

    const card = document.getElementById('lastStatusCard');
    card.className = `stat-card card-${getStatusClass(latest.status)}`;

    document.getElementById('lastPeopleCount').textContent  = latest.people_count;
    document.getElementById('lastAnalysisDate').textContent = latest.date_display;
}

function buildReportItem(report, index, total) {
    const sc = getStatusClass(report.status);

    const namesHtml = '';

    const hasImages = report.processed_images && report.processed_images.length > 0;

    const toggleBtn = hasImages ? `
        <button class="report-toggle-btn" onclick="toggleImages(this)">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
            <span class="toggle-label">Ver imágenes</span>
        </button>` : '';

    const imagesGrid = hasImages ? `
        <div class="report-expand hidden">
            <div class="report-proc-grid">
                ${report.processed_images.map(img => {
                    const filename = img.filename ?? img;
                    const count    = img.count ?? '--';
                    return `
                    <div class="report-proc-card">
                        <div class="report-proc-img-wrap">
                            <img src="${CONFIG.API_BASE_URL}/imagen/procesada/${filename}"
                                 alt="Imagen procesada"
                                 class="lb-trigger"
                                 onerror="this.parentElement.innerHTML='<div class=\\'img-placeholder\\'>Sin imagen</div>'">
                        </div>
                        <div class="report-proc-count">
                            ${count} persona${count !== 1 ? 's' : ''}
                        </div>
                    </div>`;
                }).join('')}
            </div>
        </div>` : '';

    return `
        <div class="report-item ${sc}">
            <div class="report-row">
                <span class="report-number">#${total - index}</span>

                <div class="report-date-block">
                    <span class="report-date">${report.date_display}</span>
                    <span class="report-site">${report.site || 'Sótano 1'}</span>
                </div>

                <div class="report-people">
                    <div class="report-people-count">${report.people_count}</div>
                    <div class="report-people-label">persona${report.people_count !== 1 ? 's' : ''}</div>
                </div>

                <div class="report-status-block">
                    <span class="status-badge ${sc}">${report.status}</span>
                </div>

                <div class="report-images">
                    <strong>${report.images_analyzed}</strong>
                    imagen${report.images_analyzed !== 1 ? 'es' : ''}
                    ${namesHtml}
                </div>

                ${toggleBtn}
            </div>
            ${imagesGrid}
        </div>`;
}

function renderReports(reports) {
    updateSummaryCards(reports);
    const container = document.getElementById('reportsContainer');

    if (reports.length === 0) {
        container.innerHTML = `
            <div class="no-reports">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <line x1="18" y1="20" x2="18" y2="10"></line>
                    <line x1="12" y1="20" x2="12" y2="4"></line>
                    <line x1="6" y1="20" x2="6" y2="14"></line>
                </svg>
                <p>No hay reportes aún.</p>
                <p class="no-reports-sub">
                    Analiza imágenes desde el <a href="index.html">Dashboard</a>
                    para generar el primer reporte.
                </p>
            </div>`;
        return;
    }

    container.innerHTML = reports
        .map((report, i) => buildReportItem(report, i, reports.length))
        .join('');
}

// ── API ──────────────────────────────────────────────────────
async function loadReports() {
    showLoading(true);
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/reportes`);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const result = await response.json();
        if (result.status !== 'success') throw new Error(result.message || 'Error');
        renderReports(result.data);
    } catch (error) {
        showToast(`Error al cargar reportes: ${error.message}`, 'error');
        document.getElementById('reportsContainer').innerHTML = `
            <div class="no-reports">
                <p>No se pudo conectar con el backend.</p>
                <p class="no-reports-sub">Asegúrate de que Flask esté corriendo en el puerto 5000.</p>
            </div>`;
    } finally {
        showLoading(false);
    }
}

async function clearReports() {
    if (!confirm('¿Eliminar todo el historial de reportes? Esta acción no se puede deshacer.')) return;
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/reportes`, { method: 'DELETE' });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        showToast('Historial eliminado correctamente', 'success');
        loadReports();
    } catch (error) {
        showToast(`Error: ${error.message}`, 'error');
    }
}

// ── Timer global (mismo localStorage que dashboard) ──────────
function startBackgroundTimer() {
    setInterval(async () => {
        const stored = parseInt(localStorage.getItem(LS_KEY) || '0', 10);
        const remaining = Math.ceil((stored - Date.now()) / 1000);

        if (remaining <= 0) {
            // Programar siguiente ciclo antes de analizar
            localStorage.setItem(LS_KEY, Date.now() + AUTO_INTERVAL_SECONDS * 1000);
            try {
                const res = await fetch(`${CONFIG.API_BASE_URL}/analizar-dataset`, { method: 'POST' });
                if (res.ok) {
                    showToast('Análisis automático completado', 'success');
                    loadReports(); // refresca la lista con el nuevo reporte
                }
            } catch (_) { /* silencioso si falla */ }
        }
    }, 1000);
}

// ── Init ─────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    loadReports();
    document.getElementById('refreshBtn')?.addEventListener('click', loadReports);
    document.getElementById('clearReportsBtn')?.addEventListener('click', clearReports);
    startBackgroundTimer();
});
