/* static/js/modules/pasta_links/links.js
============================================
LINKS — orquestrador
============================================ */

(function() {
    'use strict';

    // ==========================================================
    // BOTÕES DE STATUS (Ativos / Inativos / Todos)
    // Atualiza a classe .btn-active-toggle no clique
    // ==========================================================
    document.body.addEventListener('click', function(e) {
        const btn = e.target.closest('[data-filtro-status]');
        if (!btn) return;

        // Tira "active" dos outros botões de status
        document.querySelectorAll('[data-filtro-status]').forEach(b => {
            b.classList.remove('btn-active-toggle');
        });

        // Adiciona "active" no clicado
        btn.classList.add('btn-active-toggle');
    });

    // ==========================================================
    // Reativar/Inativar — HTMX puro (notificação após terminar)
    // ==========================================================
    document.body.addEventListener('htmx:afterRequest', function(e) {
        if (!e.detail.successful) return;

        const trigger = e.detail.xhr.getResponseHeader('HX-Trigger');
        if (!trigger) return;

        try {
            const data = JSON.parse(trigger);

            if (data.linkInativado && data.linkInativado.message) {
                Notificacao.sucesso(data.linkInativado.message);
            }
            if (data.linkReativado && data.linkReativado.message) {
                Notificacao.sucesso(data.linkReativado.message);
            }
        } catch (_) {}
    });

    console.log('✅ Links carregado');

})();