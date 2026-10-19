/* static/js/modules/pasta_painel/modulos/aparencia/aparencia.js
   Rascunho ao vivo preservado. SEM merge no cliente — o que tá no input É o config.
   O template só PRE-POPULA. O merge real acontece no backend (AparenciaFinalService).

   Os config_default dos templates vêm de window.__TEMPLATES_CONFIG__
   (injetado pelo Jinja num <script>) — NÃO de data-config (que vem
   escapado com &quot; e quebra o JSON.parse).
*/
(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {
        const form = document.getElementById('formAparencia');
        if (!form) return;

        const $ = (id) => document.getElementById(id);

        const inputCorPrimaria    = $('cor_primaria');
        const inputCorSecundaria  = $('cor_secundaria');
        const inputCorFundo       = $('cor_fundo');
        const inputCorTexto       = $('cor_texto');
        const inputFonte          = $('fonte');
        const inputEstiloBotao    = $('estilo_botao');
        const inputTamanhoFoto    = $('tamanho_foto');
        const inputTamanhoLink    = $('tamanho_link');
        const inputEspacamento    = $('espacamento_links');
        const inputBordaLink      = $('borda_link');
        const inputHoverEfeito    = $('hover_efeito');
        const inputAnimacaoEntrada= $('animacao_entrada');
        const inputTemplateSlug   = $('template_slug_hidden');

        const btnSalvarFooter     = $('btnSalvarFooter');

        const hexPrimaria   = $('corPrimariaHex');
        const hexSecundaria = $('corSecundariaHex');
        const hexFundo      = $('corFundoHex');
        const hexTexto      = $('corTextoHex');

        // ===== CONFIG USER (o que tá no input É o config) =====
        function pegarConfigUser() {
            return {
                cores: {
                    primaria:   inputCorPrimaria?.value,
                    secundaria: inputCorSecundaria?.value,
                    fundo:      inputCorFundo?.value,
                    texto:      inputCorTexto?.value,
                },
                tipografia: {
                    fonte:        inputFonte?.value,
                    estilo_botao: inputEstiloBotao?.value,
                },
                layout: {
                    tamanho_foto:       inputTamanhoFoto?.value,
                    tamanho_link:       inputTamanhoLink?.value,
                    espacamento_links:  inputEspacamento?.value,
                    borda_link:         inputBordaLink?.value,
                },
                efeitos: {
                    hover_efeito:     inputHoverEfeito?.value,
                    animacao_entrada: inputAnimacaoEntrada?.value,
                },
            };
        }

        // ===== APLICA NO PREVIEW (sem merge — input é verdade) =====
        function atualizarMockup() {
            if (!window.Mockup) return;
            window.Mockup.aplicar(pegarConfigUser());
        }

        // ===== LISTENERS DE CORES (input + change, todos navegadores) =====
        [
            { el: inputCorPrimaria,   hex: hexPrimaria },
            { el: inputCorSecundaria, hex: hexSecundaria },
            { el: inputCorFundo,      hex: hexFundo },
            { el: inputCorTexto,      hex: hexTexto },
        ].forEach(function (par) {
            if (!par.el) return;
            const handler = function () {
                if (par.hex) par.hex.textContent = par.el.value;
                atualizarMockup();
            };
            par.el.addEventListener('input',  handler);
            par.el.addEventListener('change', handler);
        });

        // ===== LISTENERS DE ESTILO =====
        [
            inputFonte, inputEstiloBotao,
            inputTamanhoFoto, inputTamanhoLink, inputEspacamento,
            inputBordaLink, inputHoverEfeito, inputAnimacaoEntrada,
        ].forEach(function (el) {
            if (el) el.addEventListener('change', atualizarMockup);
        });

        // ===== TEMPLATES — pré-popula os inputs (usa window.__TEMPLATES_CONFIG__) =====
        document.querySelectorAll('.template-card').forEach(function (card) {
            card.addEventListener('click', function () {
                document.querySelectorAll('.template-card').forEach(c => c.classList.remove('active'));
                this.classList.add('active');

                const slug = this.dataset.template;
                if (inputTemplateSlug) inputTemplateSlug.value = slug;

                // ⬇️ Pega do mapa global (JSON limpo, injetado pelo Jinja)
                const mapa = window.__TEMPLATES_CONFIG__ || {};
                const configDefault = mapa[slug] || {};

                const cores = configDefault.cores || {};
                if (inputCorPrimaria   && cores.primaria)   { inputCorPrimaria.value   = cores.primaria;   if (hexPrimaria)   hexPrimaria.textContent   = cores.primaria; }
                if (inputCorSecundaria && cores.secundaria) { inputCorSecundaria.value = cores.secundaria; if (hexSecundaria) hexSecundaria.textContent = cores.secundaria; }
                if (inputCorFundo      && cores.fundo)      { inputCorFundo.value      = cores.fundo;      if (hexFundo)      hexFundo.textContent      = cores.fundo; }
                if (inputCorTexto      && cores.texto)      { inputCorTexto.value      = cores.texto;      if (hexTexto)      hexTexto.textContent      = cores.texto; }

                const tipografia = configDefault.tipografia || {};
                if (inputFonte       && tipografia.fonte)        inputFonte.value       = tipografia.fonte;
                if (inputEstiloBotao && tipografia.estilo_botao) inputEstiloBotao.value = tipografia.estilo_botao;

                const layout = configDefault.layout || {};
                if (inputTamanhoFoto && layout.tamanho_foto)       inputTamanhoFoto.value = layout.tamanho_foto;
                if (inputTamanhoLink && layout.tamanho_link)       inputTamanhoLink.value = layout.tamanho_link;
                if (inputEspacamento && layout.espacamento_links)  inputEspacamento.value = layout.espacamento_links;
                if (inputBordaLink   && layout.borda_link)         inputBordaLink.value   = layout.borda_link;

                const efeitos = configDefault.efeitos || {};
                if (inputHoverEfeito     && efeitos.hover_efeito)     inputHoverEfeito.value     = efeitos.hover_efeito;
                if (inputAnimacaoEntrada && efeitos.animacao_entrada) inputAnimacaoEntrada.value = efeitos.animacao_entrada;

                atualizarMockup();
            });
        });

        // ===== SUBMIT =====
        function submeter() {
            const templateSlug = inputTemplateSlug?.value || 'cosmic';
            const config       = pegarConfigUser();

            if (btnSalvarFooter) {
                btnSalvarFooter.disabled = true;
                const icone = btnSalvarFooter.querySelector('i');
                if (icone) icone.className = 'fas fa-spinner fa-spin';
            }

            fetch('/painel/aparencia/salvar', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                },
                body: JSON.stringify({ template_slug: templateSlug, config: config }),
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

        form.addEventListener('submit', function (ev) { ev.preventDefault(); submeter(); });
        if (btnSalvarFooter) btnSalvarFooter.addEventListener('click', submeter);

        // ===== INICIALIZA =====
        atualizarMockup();
        console.log('✅ Aparência carregada (input = config, sem merge no cliente)');
    });
})();