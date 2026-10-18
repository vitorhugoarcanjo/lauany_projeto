/* static/js/modules/pasta_painel/modulos/aparencia/aparencia.js */

(function() {
    'use strict';

    document.addEventListener('DOMContentLoaded', function() {
        const form = document.getElementById('formAparencia');
        if (!form) return;

        const inputCorPrimaria = document.getElementById('cor_primaria');
        const inputCorSecundaria = document.getElementById('cor_secundaria');
        const inputCorFundo = document.getElementById('cor_fundo');
        const inputCorTexto = document.getElementById('cor_texto');
        const inputFonte = document.getElementById('fonte');
        const inputEstiloBotao = document.getElementById('estilo_botao');
        const inputTamanhoFoto = document.getElementById('tamanho_foto');
        const inputTamanhoLink = document.getElementById('tamanho_link');
        const inputEspacamento = document.getElementById('espacamento_links');
        const inputBordaLink = document.getElementById('borda_link');
        const inputHoverEfeito = document.getElementById('hover_efeito');
        const inputAnimacaoEntrada = document.getElementById('animacao_entrada');

        const btnSalvarFooter = document.getElementById('btnSalvarFooter');

        const hexPrimaria = document.getElementById('corPrimariaHex');
        const hexSecundaria = document.getElementById('corSecundariaHex');
        const hexFundo = document.getElementById('corFundoHex');
        const hexTexto = document.getElementById('corTextoHex');

        function atualizarMockup() {
            if (!window.Mockup) return;

            // Cores
            Mockup.setCores(
                inputCorPrimaria?.value,
                inputCorSecundaria?.value,
                inputCorFundo?.value,
                inputCorTexto?.value
            );

            // Estilo, fonte, tamanhos
            if (inputEstiloBotao) Mockup.setEstiloBotao(inputEstiloBotao.value);
            if (inputFonte) Mockup.setFonte(inputFonte.value);
            if (Mockup.setTamanhos) {
                Mockup.setTamanhos(
                    inputTamanhoFoto?.value,
                    inputTamanhoLink?.value,
                    inputEspacamento?.value
                );
            }

            // NOVO: borda, hover, animação
            if (inputBordaLink && Mockup.setBorda) Mockup.setBorda(inputBordaLink.value);
            if (inputHoverEfeito && Mockup.setHover) Mockup.setHover(inputHoverEfeito.value);
            if (inputAnimacaoEntrada && Mockup.setAnimacao) Mockup.setAnimacao(inputAnimacaoEntrada.value);
        }

        // Listeners de cor
        if (inputCorPrimaria) inputCorPrimaria.addEventListener('input', function() {
            if (hexPrimaria) hexPrimaria.textContent = this.value;
            atualizarMockup();
        });
        if (inputCorSecundaria) inputCorSecundaria.addEventListener('input', function() {
            if (hexSecundaria) hexSecundaria.textContent = this.value;
            atualizarMockup();
        });
        if (inputCorFundo) inputCorFundo.addEventListener('input', function() {
            if (hexFundo) hexFundo.textContent = this.value;
            atualizarMockup();
        });
        if (inputCorTexto) inputCorTexto.addEventListener('input', function() {
            if (hexTexto) hexTexto.textContent = this.value;
            atualizarMockup();
        });

        // Listeners de estilo + tamanhos + borda + hover + animação
        [
            inputFonte, inputEstiloBotao,
            inputTamanhoFoto, inputTamanhoLink, inputEspacamento,
            inputBordaLink, inputHoverEfeito, inputAnimacaoEntrada
        ].forEach(el => {
            if (el) el.addEventListener('change', atualizarMockup);
        });

        // Templates
        document.querySelectorAll('.template-card').forEach(card => {
            card.addEventListener('click', function() {
                document.querySelectorAll('.template-card').forEach(c => c.classList.remove('active'));
                this.classList.add('active');

                const template = this.dataset.template;
                const primaria = this.dataset.primaria;
                const secundaria = this.dataset.secundaria;
                const fundo = this.dataset.fundo;
                const texto = this.dataset.texto;

                const templateHidden = document.getElementById('template_hidden');
                if (templateHidden) templateHidden.value = template;

                if (inputCorPrimaria && primaria) { inputCorPrimaria.value = primaria; if (hexPrimaria) hexPrimaria.textContent = primaria; }
                if (inputCorSecundaria && secundaria) { inputCorSecundaria.value = secundaria; if (hexSecundaria) hexSecundaria.textContent = secundaria; }
                if (inputCorFundo && fundo) { inputCorFundo.value = fundo; if (hexFundo) hexFundo.textContent = fundo; }
                if (inputCorTexto && texto) { inputCorTexto.value = texto; if (hexTexto) hexTexto.textContent = texto; }

                atualizarMockup();
            });
        });

        // Submit
        function submeter() {
            const formData = new FormData(form);

            if (btnSalvarFooter) {
                btnSalvarFooter.disabled = true;
                const icone = btnSalvarFooter.querySelector('i');
                if (icone) icone.className = 'fas fa-spinner fa-spin';
            }

            fetch('/painel/aparencia/salvar', {
                method: 'POST',
                body: formData,
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            })
            .then(r => r.json().then(j => ({ ok: r.ok, data: j })))
            .then(({ ok, data }) => {
                if (!ok || !data.success) {
                    if (window.Notificacao) Notificacao.erro(data.error || 'Erro ao salvar.');
                    return;
                }
                if (window.Notificacao) Notificacao.sucesso(data.message || 'Aparência atualizada!');
            })
            .catch(() => {
                if (window.Notificacao) Notificacao.erro('Erro de conexão.');
            })
            .finally(() => {
                if (btnSalvarFooter) {
                    btnSalvarFooter.disabled = false;
                    const icone = btnSalvarFooter.querySelector('i');
                    if (icone) icone.className = 'fas fa-save';
                }
            });
        }

        form.addEventListener('submit', function(ev) {
            ev.preventDefault();
            submeter();
        });

        if (btnSalvarFooter) {
            btnSalvarFooter.addEventListener('click', function() {
                submeter();
            });
        }

        atualizarMockup();
        console.log('✅ Aparência carregada');
    });
})();