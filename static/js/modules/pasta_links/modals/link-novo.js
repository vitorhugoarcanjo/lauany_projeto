/* static/js/modules/pasta_links/modals/link-novo.js
============================================
MODAL NOVO LINK — abre/fecha/submete
============================================ */

(function() {
    'use strict';

    let formInstance = null;
    let submitVinculado = false;

    function instanciar() {
        const formEl = document.getElementById('formNovoLink');
        if (!formEl) return null;
        if (formInstance && formInstance.form === formEl) return formInstance;

        formInstance = new window.LinkForm(formEl, {
            mode: 'create',
            onSubmitSuccess: function(result) {
                Notificacao.sucesso(result.message || 'Link criado!');
                fechar();
                recarregarTabela();
            }
        });

        return formInstance;
    }

    function fechar() {
        const modal = document.querySelector('#modal-novo-container [data-modal]');
        if (modal) {
            modal.style.animation = 'modalFadeOut 0.15s ease forwards';
            setTimeout(() => {
                modal.remove();
                document.body.style.overflow = '';
            }, 150);
        }
        formInstance = null;
        submitVinculado = false;
    }

    function recarregarTabela() {
        if (window.htmx) {
            htmx.ajax('GET', '/links', '#tabela-container');
        } else {
            setTimeout(() => window.location.reload(), 400);
        }
    }

    // ==========================================================
    // Vincula o submit (idempotente + captura)
    // ==========================================================
    function vincularSubmit(formEl) {
        if (!formEl) return;
        if (submitVinculado && formEl.dataset.submitVinculado === '1') return;

        formEl.addEventListener('submit', function(ev) {
            // 🔥 Bloqueia submit nativo de TODAS as formas
            ev.preventDefault();
            ev.stopPropagation();
            ev.stopImmediatePropagation();

            const f = instanciar();
            if (!f) return;

            const btn = document.getElementById('btnSalvarNovoLink');
            if (btn) {
                btn.classList.add('loading');
                btn.disabled = true;
            }

            f.submit('/links/novo_link/salvar')
                .catch((err) => console.error('❌ Erro submit novo link:', err))
                .finally(() => {
                    if (btn) {
                        btn.classList.remove('loading');
                        btn.disabled = false;
                    }
                });

            return false;
        }, true); // ← capture: intercepta ANTES de qualquer outro

        formEl.dataset.submitVinculado = '1';
        submitVinculado = true;
    }

    // ==========================================================
    // Inicializa modal (HTMX injetou OU já tá no DOM)
    // ==========================================================
    function inicializarModal() {
        const formEl = document.getElementById('formNovoLink');
        if (!formEl) return;

        document.body.style.overflow = 'hidden';
        instanciar();
        vincularSubmit(formEl);
    }

    // 1. Quando HTMX injeta o modal
    document.body.addEventListener('htmx:afterSwap', function(e) {
        const target = e.detail && e.detail.target;
        if (!target) return;

        // Modal foi injetado no container novo?
        if (target.id === 'modal-novo-container' ||
            target.closest('#modal-novo-container') ||
            document.getElementById('formNovoLink')) {
            inicializarModal();
        }
    });

    // 2. Quando a página carrega (F5 com modal aberto — raro, mas cobre)
    document.addEventListener('DOMContentLoaded', function() {
        const formEl = document.getElementById('formNovoLink');
        if (formEl) {
            inicializarModal();
        }
    });

    window.fecharModalNovoLink = fechar;

})();