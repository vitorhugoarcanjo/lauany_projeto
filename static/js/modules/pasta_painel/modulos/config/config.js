/* static/js/modules/pasta_painel/modulos/config/config.js
============================================
CONFIGURAÇÕES — alterar senha
============================================ */

(function() {
    'use strict';

    const form = document.getElementById('formAlterarSenha');
    if (!form) return;

    const btnAlterar = document.getElementById('btnAlterarSenha');
    const btnDeletar = document.getElementById('btnDeletarConta');

    // ==========================================================
    // ALTERAR SENHA
    // ==========================================================
    form.addEventListener('submit', function(ev) {
        ev.preventDefault();
        const formData = new FormData(form);

        if (btnAlterar) {
            btnAlterar.classList.add('loading');
            btnAlterar.disabled = true;
        }

        fetch('/painel/configuracoes/alterar-senha', {
            method: 'POST',
            body: formData,
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(r => r.json().then(j => ({ ok: r.ok, data: j })))
        .then(({ ok, data }) => {
            if (!ok || !data.success) {
                Notificacao.erro(data.error || 'Erro ao alterar senha.');
                return;
            }
            Notificacao.sucesso(data.message || 'Senha alterada!');
            form.reset();
        })
        .catch(() => Notificacao.erro('Erro de conexão.'))
        .finally(() => {
            if (btnAlterar) {
                btnAlterar.classList.remove('loading');
                btnAlterar.disabled = false;
            }
        });
    });

    // ==========================================================
    // DELETAR CONTA (placeholder — futuro)
    // ==========================================================
    if (btnDeletar) {
        btnDeletar.addEventListener('click', function() {
            Notificacao.aviso('Função em desenvolvimento. Fale com o suporte.');
        });
    }

    console.log('✅ Config carregado');

})();