/* static/js/modules/pasta_links/modals/link-editar.js
============================================
MODAL EDITAR LINK — abre/fecha/submete
============================================ */

(function() {
    'use strict';

    let formInstance = null;
    let submitVinculado = false;

    function instanciar() {
        const formEl = document.getElementById('formEditarLink');
        if (!formEl) return null;
        if (formInstance && formInstance.form === formEl) return formInstance;

        formInstance = new window.LinkForm(formEl, {
            mode: 'edit',
            onSubmitSuccess: function(result) {
                Notificacao.sucesso(result.message || 'Link atualizado!');
                fechar();
                recarregarTabela();
            }
        });

        return formInstance;
    }

    function fechar() {
        const modal = document.querySelector('#modal-editar-container [data-modal]');
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
    // Vincula o submit
    // ==========================================================
    function vincularSubmit(formEl) {
        if (!formEl) return;
        if (submitVinculado && formEl.dataset.submitVinculado === '1') return;

        formEl.addEventListener('submit', function(ev) {
            ev.preventDefault();
            ev.stopPropagation();
            ev.stopImmediatePropagation();

            const f = instanciar();
            if (!f) return;

            const linkId = formEl.dataset.linkId;
            const btn = document.getElementById('btnSalvarEdicao');

            if (btn) {
                btn.classList.add('loading');
                btn.disabled = true;
            }

            f.submit('/links/edit_link/salvar/' + linkId)
                .catch((err) => console.error('❌ Erro submit editar:', err))
                .finally(() => {
                    if (btn) {
                        btn.classList.remove('loading');
                        btn.disabled = false;
                    }
                });

            return false;
        }, true);

        formEl.dataset.submitVinculado = '1';
        submitVinculado = true;
    }

    // ==========================================================
    // Inicializa
    // ==========================================================
    function inicializarModal() {
        const formEl = document.getElementById('formEditarLink');
        if (!formEl) return;

        document.body.style.overflow = 'hidden';
        instanciar();
        vincularSubmit(formEl);
    }

    document.body.addEventListener('htmx:afterSwap', function(e) {
        const target = e.detail && e.detail.target;
        if (!target) return;

        if (target.id === 'modal-editar-container' ||
            target.closest('#modal-editar-container') ||
            document.getElementById('formEditarLink')) {
            inicializarModal();
        }
    });

    document.addEventListener('DOMContentLoaded', function() {
        const formEl = document.getElementById('formEditarLink');
        if (formEl) {
            inicializarModal();
        }
    });

    window.fecharModalEditarLink = fechar;

})();