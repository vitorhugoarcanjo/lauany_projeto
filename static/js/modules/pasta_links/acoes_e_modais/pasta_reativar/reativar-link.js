/* static/js/modules/pasta_links/acoes_e_modais/pasta_reativar/reativar-link.js
============================================
REATIVAR LINK — abre modal + executa
============================================ */

(function() {
    'use strict';

    function fechar() {
        const modal = document.querySelector('#modal-reativar-container [data-modal]');
        if (modal) {
            modal.style.animation = 'modalFadeOut 0.15s ease forwards';
            setTimeout(() => {
                modal.remove();
                document.body.style.overflow = '';
            }, 150);
        }
    }

    function inicializarModal() {
        const modal = document.querySelector('#modal-reativar-container [data-modal]');
        if (!modal) return;

        document.body.style.overflow = 'hidden';
    }

    // 1. HTMX injetou o modal
    document.body.addEventListener('htmx:afterSwap', function(e) {
        const target = e.detail && e.detail.target;
        if (!target) return;

        if (target.id === 'modal-reativar-container' ||
            target.closest('#modal-reativar-container')) {
            inicializarModal();
        }
    });

    // 2. Página carregou com modal aberto
    document.addEventListener('DOMContentLoaded', function() {
        if (document.getElementById('btnConfirmarReativacao')) {
            inicializarModal();
        }
    });

    // 3. HTMX terminou o POST — fecha o modal
    document.body.addEventListener('htmx:afterRequest', function(e) {
        if (!e.detail.successful) return;

        const trigger = e.detail.xhr.getResponseHeader('HX-Trigger');
        if (trigger && trigger.includes('linkReativado')) {
            fechar();
        }
    });

    window.fecharModalReativarLink = fechar;

})();