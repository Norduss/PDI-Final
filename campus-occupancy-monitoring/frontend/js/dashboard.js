/**
 * Sistema de Monitoreo de Ocupación
 * Dashboard JavaScript - Consumo de API y actualización de UI
 */

// ============================================
// Configuración
// ============================================
const CONFIG = {
    API_BASE_URL: 'http://localhost:5000/api',
    UPDATE_INTERVAL_MS: 15 * 60 * 1000, // 15 minutos en milisegundos
    TOAST_DURATION_MS: 3000
};

// ============================================
// Estado de la aplicación
// ============================================
let state = {
    currentData: null,
    isLoading: false,
    updateInterval: null
};

// ============================================
// Elementos del DOM
// ============================================
const elements = {
    // Stats
    peopleCount: document.getElementById('peopleCount'),
    maxCapacity: document.getElementById('maxCapacity'),
    occupancyPercentage: document.getElementById('occupancyPercentage'),
    occupancyProgress: document.getElementById('occupancyProgress'),
    siteName: document.getElementById('siteName'),
    statusBadge: document.getElementById('statusBadge'),
    nextUpdate: document.getElementById('nextUpdate'),
    lastUpdate: document.getElementById('lastUpdate'),
    
    // Camera
    cameraView: document.getElementById('cameraView'),
    processedImage: document.getElementById('processedImage'),
    
    // Alerts
    alertsList: document.getElementById('alertsList'),
    alertsCount: document.getElementById('alertsCount'),
    emptyAlerts: document.getElementById('emptyAlerts'),
    
    // Buttons
    refreshBtn: document.getElementById('refreshBtn'),
    exportCsvBtn: document.getElementById('exportCsvBtn'),
    
    // Loading & Toast
    loadingOverlay: document.getElementById('loadingOverlay'),
    toastContainer: document.getElementById('toastContainer')
};

// ============================================
// Funciones de API
// ============================================

/**
 * Carga los datos de ocupación desde la API
 */
async function loadOccupancyData() {
    if (state.isLoading) return;
    
    state.isLoading = true;
    showLoading(true);
    
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/estado-actual`);
        
        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }
        
        const result = await response.json();
        
        if (result.status === 'success') {
            state.currentData = result.data;
            updateDashboard(result.data);
            addAlert('success', 'Datos actualizados correctamente');
        } else {
            throw new Error(result.message || 'Error desconocido');
        }
        
    } catch (error) {
        console.error('Error al cargar datos:', error);
        showToast(`Error al cargar datos: ${error.message}`, 'error');
        addAlert('danger', `Error de conexión: ${error.message}`);
    } finally {
        state.isLoading = false;
        showLoading(false);
    }
}

// ============================================
// Funciones de actualización de UI
// ============================================

/**
 * Actualiza todos los elementos del dashboard con los nuevos datos
 * @param {Object} data - Datos de ocupación
 */
function updateDashboard(data) {
    // Actualizar estadísticas
    elements.peopleCount.textContent = data.people_count;
    elements.maxCapacity.textContent = data.max_capacity;
    elements.occupancyPercentage.textContent = data.occupancy_percentage;
    elements.siteName.textContent = data.site;
    elements.nextUpdate.textContent = data.next_update;
    elements.lastUpdate.textContent = data.last_update;
    
    // Actualizar barra de progreso
    updateProgressBar(data.occupancy_percentage);
    
    // Actualizar badge de estado
    updateStatusBadge(data.status);
    
    // Actualizar imagen procesada (si existe)
    if (data.processed_image) {
        updateCameraImage(data.processed_image);
    }
}

/**
 * Actualiza la barra de progreso de ocupación
 * @param {number} percentage - Porcentaje de ocupación
 */
function updateProgressBar(percentage) {
    const progressBar = elements.occupancyProgress;
    progressBar.style.width = `${percentage}%`;
    
    // Cambiar color según nivel de ocupación
    progressBar.classList.remove('low', 'medium', 'high');
    
    if (percentage <= 30) {
        progressBar.classList.add('low');
    } else if (percentage <= 70) {
        progressBar.classList.add('medium');
    } else {
        progressBar.classList.add('high');
    }
}

/**
 * Actualiza el badge de estado
 * @param {string} status - Estado de ocupación
 */
function updateStatusBadge(status) {
    const badge = elements.statusBadge;
    badge.textContent = status;
    
    // Remover clases anteriores
    badge.classList.remove('empty', 'partial', 'full');
    
    // Agregar clase según estado
    if (status === 'Vacío') {
        badge.classList.add('empty');
    } else if (status === 'Parcialmente ocupado') {
        badge.classList.add('partial');
    } else if (status === 'Ocupado') {
        badge.classList.add('full');
    }
}

/**
 * Actualiza la imagen de la cámara
 * @param {string} imagePath - Ruta de la imagen procesada
 */
function updateCameraImage(imagePath) {
    const img = elements.processedImage;
    const placeholder = elements.cameraView.querySelector('.camera-placeholder');
    
    // Por ahora, mostrar placeholder ya que la imagen es simulada
    // Cuando se integre la captura real, descomentar el código de abajo
    
    // img.src = `http://localhost:5000/${imagePath}`;
    // img.classList.remove('hidden');
    // if (placeholder) placeholder.classList.add('hidden');
    
    // img.onerror = () => {
    //     img.classList.add('hidden');
    //     if (placeholder) placeholder.classList.remove('hidden');
    // };
}

// ============================================
// Sistema de Alertas
// ============================================

/**
 * Agrega una alerta a la lista
 * @param {string} type - Tipo de alerta (info, success, warning, danger)
 * @param {string} message - Mensaje de la alerta
 */
function addAlert(type, message) {
    const alertsList = elements.alertsList;
    const emptyAlerts = elements.emptyAlerts;
    
    // Ocultar mensaje de vacío
    emptyAlerts.classList.add('hidden');
    
    // Crear elemento de alerta
    const alertItem = document.createElement('li');
    alertItem.className = `alert-item alert-${type}`;
    
    const icon = getAlertIcon(type);
    const time = new Date().toLocaleTimeString('es-ES', { 
        hour: '2-digit', 
        minute: '2-digit' 
    });
    
    alertItem.innerHTML = `
        ${icon}
        <div class="alert-content">
            <span class="alert-title">${message}</span>
            <span class="alert-time">${time}</span>
        </div>
    `;
    
    // Agregar al inicio de la lista
    alertsList.insertBefore(alertItem, alertsList.firstChild);
    
    // Limitar número de alertas visibles
    const alerts = alertsList.querySelectorAll('.alert-item');
    if (alerts.length > 10) {
        alerts[alerts.length - 1].remove();
    }
    
    // Actualizar contador
    updateAlertsCount();
}

/**
 * Obtiene el ícono SVG según el tipo de alerta
 * @param {string} type - Tipo de alerta
 * @returns {string} - SVG del ícono
 */
function getAlertIcon(type) {
    const icons = {
        info: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="16" x2="12" y2="12"></line>
            <line x1="12" y1="8" x2="12.01" y2="8"></line>
        </svg>`,
        success: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
            <polyline points="22 4 12 14.01 9 11.01"></polyline>
        </svg>`,
        warning: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
            <line x1="12" y1="9" x2="12" y2="13"></line>
            <line x1="12" y1="17" x2="12.01" y2="17"></line>
        </svg>`,
        danger: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="15" y1="9" x2="9" y2="15"></line>
            <line x1="9" y1="9" x2="15" y2="15"></line>
        </svg>`
    };
    
    return icons[type] || icons.info;
}

/**
 * Actualiza el contador de alertas
 */
function updateAlertsCount() {
    const count = elements.alertsList.querySelectorAll('.alert-item').length;
    elements.alertsCount.textContent = count;
}

// ============================================
// Funciones de UI auxiliares
// ============================================

/**
 * Muestra u oculta el overlay de carga
 * @param {boolean} show - Mostrar u ocultar
 */
function showLoading(show) {
    if (show) {
        elements.loadingOverlay.classList.remove('hidden');
    } else {
        elements.loadingOverlay.classList.add('hidden');
    }
}

/**
 * Muestra un toast de notificación
 * @param {string} message - Mensaje a mostrar
 * @param {string} type - Tipo de toast (success, error)
 */
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    
    elements.toastContainer.appendChild(toast);
    
    // Remover después de un tiempo
    setTimeout(() => {
        toast.style.animation = 'slideIn 0.3s ease reverse';
        setTimeout(() => toast.remove(), 300);
    }, CONFIG.TOAST_DURATION_MS);
}

/**
 * Exporta los datos actuales a CSV
 */
function exportToCsv() {
    if (!state.currentData) {
        showToast('No hay datos para exportar', 'error');
        return;
    }
    
    const data = state.currentData;
    const csvContent = [
        ['Campo', 'Valor'],
        ['Sitio', data.site],
        ['Personas Detectadas', data.people_count],
        ['Capacidad Máxima', data.max_capacity],
        ['Porcentaje Ocupación', `${data.occupancy_percentage}%`],
        ['Estado', data.status],
        ['Última Actualización', data.last_update]
    ].map(row => row.join(',')).join('\n');
    
    // Crear y descargar archivo
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    
    link.setAttribute('href', url);
    link.setAttribute('download', `ocupacion_${new Date().toISOString().slice(0, 10)}.csv`);
    link.style.visibility = 'hidden';
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    showToast('CSV exportado correctamente', 'success');
    addAlert('info', 'Datos exportados a CSV');
}

// ============================================
// Event Listeners
// ============================================

/**
 * Configura los event listeners
 */
function setupEventListeners() {
    // Botón de actualizar
    elements.refreshBtn.addEventListener('click', () => {
        loadOccupancyData();
    });
    
    // Botón de exportar CSV
    elements.exportCsvBtn.addEventListener('click', () => {
        exportToCsv();
    });
    
    // Click en sitios (para futura funcionalidad)
    const siteItems = document.querySelectorAll('.site-item');
    siteItems.forEach(item => {
        item.addEventListener('click', () => {
            // Remover clase active de todos
            siteItems.forEach(si => si.classList.remove('active'));
            // Agregar clase active al clickeado
            item.classList.add('active');
            
            // TODO: Cargar datos del sitio seleccionado
            const siteName = item.querySelector('.site-name').textContent;
            showToast(`Sitio seleccionado: ${siteName}`, 'info');
        });
    });
}

/**
 * Inicia el intervalo de actualización automática
 */
function startAutoUpdate() {
    // Limpiar intervalo existente si hay uno
    if (state.updateInterval) {
        clearInterval(state.updateInterval);
    }
    
    // Configurar nuevo intervalo
    state.updateInterval = setInterval(() => {
        loadOccupancyData();
    }, CONFIG.UPDATE_INTERVAL_MS);
    
    console.log(`Auto-actualización configurada cada ${CONFIG.UPDATE_INTERVAL_MS / 60000} minutos`);
}

// ============================================
// Inicialización
// ============================================

/**
 * Función de inicialización principal
 */
function init() {
    console.log('Inicializando Dashboard de Monitoreo de Ocupación...');
    
    // Configurar event listeners
    setupEventListeners();
    
    // Cargar datos iniciales
    loadOccupancyData();
    
    // Iniciar auto-actualización
    startAutoUpdate();
    
    // Agregar alerta de inicio
    addAlert('info', 'Dashboard inicializado correctamente');
    
    console.log('Dashboard inicializado correctamente');
}

// Ejecutar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', init);
