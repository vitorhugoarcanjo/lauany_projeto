/* static/js/modules/pasta_links/modals/link-editar.js
============================================
MODAL EDITAR LINK
============================================ */

(function() {
    'use strict';

    let formInstance = null;

    function fechar() {
        const modal = document.querySelector('#modal-editar-container [data-modal]')
                    || document.querySelector('body > [data-modal]');

        if (modal) {
            modal.style.animation = 'modalFadeOut 0.15s ease forwards';
            setTimeout(() => {
                modal.remove();
                document.body.style.overflow = '';
            }, 150);
        }
        formInstance = null;
    }

    function recarregarTabela() {
        if (window.htmx) {
            htmx.ajax('GET', '/links/', '#tabela-container');
        } else {
            setTimeout(() => window.location.reload(), 400);
        }
    }

    function portal() {
        document.querySelectorAll('body > [data-modal]').forEach(m => m.remove());

        const modal = document.querySelector('#modal-editar-container [data-modal]');
        if (!modal) return;
        if (modal.parentElement === document.body) return;
        document.body.appendChild(modal);
    }

    function instanciar() {
        const formEl = document.getElementById('formEditarLink');
        if (!formEl) return null;

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

    function inicializarModal() {
        const formEl = document.getElementById('formEditarLink');
        if (!formEl) return;

        document.body.style.overflow = 'hidden';
        portal();
        instanciar();
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