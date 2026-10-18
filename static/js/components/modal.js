/* static/js/components/modal.js
============================================
SISTEMA DE MODAL — Global
============================================ */

(function() {
    'use strict';

    // Fecha modal no X ou no "Cancelar"
    document.addEventListener('click', function(e) {
        const btnFechar = e.target.closest('[data-modal-fechar]');
        if (btnFechar) {
            e.preventDefault();
            const modal = btnFechar.closest('[data-modal]');
            if (modal) fecharModal(modal);
            return;
        }

        // Clica fora (overlay) fecha
        const overlay = e.target.closest('[data-modal]');
        if (overlay && e.target === overlay) {
            fecharModal(overlay);
        }
    });

    // ESC fecha o modal visível
    document.addEventListener('keydown', function(e) {
        if (e.key !== 'Escape') return;
        const modais = document.querySelectorAll('[data-modal]');
        modais.forEach(m => fecharModal(m));
    });

    function fecharModal(modal) {
        modal.style.animation = 'modalFadeOut 0.15s ease forwards';
        setTimeout(() => {
            modal.remove();
            document.body.style.overflow = '';
        }, 150);
    }

    // Quando o HTMX injeta um modal novo, desbloqueia o scroll
    document.body.addEventListener('htmx:afterSwap', function(e) {
        if (e.detail.target.querySelector('[data-modal]') ||
            e.detail.target.matches('[data-modal]')) {
            document.body.style.overflow = 'hidden';
        }
    });

})();