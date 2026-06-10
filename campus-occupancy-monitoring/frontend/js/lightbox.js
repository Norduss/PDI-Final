/**
 * Lightbox compartido – Monitor de Ocupación UAO
 * Uso: llamar openLightbox(src) o poner class="lb-trigger" en cualquier <img>.
 */
(function () {
    // ── Inyectar HTML del modal ───────────────────────────────────────────
    const modal = document.createElement('div');
    modal.id = 'lb-modal';
    modal.innerHTML = `
        <div id="lb-backdrop"></div>
        <div id="lb-container">
            <button id="lb-close" aria-label="Cerrar imagen">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                    <line x1="18" y1="6"  x2="6"  y2="18"></line>
                    <line x1="6"  y1="6"  x2="18" y2="18"></line>
                </svg>
            </button>
            <img id="lb-img" src="" alt="Imagen ampliada">
        </div>`;
    document.body.appendChild(modal);

    // ── Abrir / cerrar ────────────────────────────────────────────────────
    function openLightbox(src) {
        document.getElementById('lb-img').src = src;
        modal.classList.add('open');
        document.body.classList.add('lb-open');
    }

    function closeLightbox() {
        modal.classList.remove('open');
        document.body.classList.remove('lb-open');
        // Limpiar src evita que la imagen anterior se vea al re-abrir
        setTimeout(() => { document.getElementById('lb-img').src = ''; }, 220);
    }

    // ── Eventos de cierre ─────────────────────────────────────────────────
    document.getElementById('lb-backdrop').addEventListener('click', closeLightbox);
    document.getElementById('lb-close').addEventListener('click', closeLightbox);
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeLightbox();
    });

    // ── Delegación: cualquier img.lb-trigger abre el lightbox ─────────────
    document.addEventListener('click', (e) => {
        if (e.target.classList.contains('lb-trigger')) {
            openLightbox(e.target.src);
        }
    });

    // Exponer globalmente para llamadas directas desde onclick="..."
    window.openLightbox = openLightbox;
})();
