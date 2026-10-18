/* static/js/modules/pasta_links/acoes_e_modais/pasta_excluir/excluir-link.js
============================================
EXCLUIR LINK (inativar) — abre modal + executa
============================================ */

(function() {
    'use strict';

    // ==========================================================
    // Fechar modal
    // ==========================================================
    function fechar() {
        const modal = document.querySelector('#modal-excluir-container [data-modal]');
        if (modal) {
            modal.style.animation = 'modalFadeOut 0.15s ease forwards';
            setTimeout(() => {
                modal.remove();
                document.body.style.overflow = '';
            }, 150);
        }
    }

    // ==========================================================
    // Inicializa quando o modal é injetado
    // ==========================================================
    function inicializarModal() {
        const modal = document.querySelector('#modal-excluir-container [data-modal]');
        if (!modal) return;

        document.body.style.overflow = 'hidden';
        // Nada mais — deixa o HTMX cuidar do POST
    }

    // 1. HTMX injetou o modal
    document.body.addEventListener('htmx:afterSwap', function(e) {
        const target = e.detail && e.detail.target;
        if (!target) return;

        if (target.id === 'modal-excluir-container' ||
            target.closest('#modal-excluir-container')) {
            inicializarModal();
        }
    });

    // 2. Página carregou com modal aberto
    document.addEventListener('DOMContentLoaded', function() {
        if (document.getElementById('btnConfirmarExclusao')) {
            inicializarModal();
        }
    });

    // ==========================================================
    // HTMX terminou o POST — fecha o modal
    // ==========================================================
    document.body.addEventListener('htmx:afterRequest', function(e) {
        if (!e.detail.successful) return;

        const trigger = e.detail.xhr.getResponseHeader('HX-Trigger');
        if (trigger && trigger.includes('linkInativado')) {
            fechar();
        }
    });

    window.fecharModalExcluirLink = fechar;

})();