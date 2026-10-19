/* static/js/components/mockup.js
   Rascunho ao vivo. NUNCA salva. Usa window.ESCALA (injetado pelo Jinja).
   Chamado a cada input/change do form via Mockup.aplicar(config_final).

   REGRA DE FUNDO (igual backend):
     - Se user escolheu cor (diferente do default) → cor dele vence.
     - Senão → gradiente do template (se houver) ou default.
*/
(function () {
    'use strict';

    window.Mockup = {
        aplicar: function (configFinal) {
            const tela = document.getElementById('mockupTela');
            if (!tela) return;
            const E = window.ESCALA;
            if (!E) { console.warn('window.ESCALA não definido'); return; }

            const cfg = configFinal || {};
            const c = cfg.cores      || {};
            const t = cfg.tipografia || {};
            const l = cfg.layout     || {};
            const e = cfg.efeitos    || {};

            const fator = (E.FATOR_PREVIEW || 0.65);
            const px = (valor) => Math.round(valor * fator) + 'px';

            const set = (k, v) => {
                if (v != null) tela.style.setProperty(k, v);
            };

            // Cores
            set('--perfil-cor-primaria',   c.primaria   || E.DEFAULTS.primaria);
            set('--perfil-cor-secundaria', c.secundaria || E.DEFAULTS.secundaria);
            set('--perfil-cor-fundo',      c.fundo      || E.DEFAULTS.fundo);
            set('--perfil-cor-texto',      c.texto      || E.DEFAULTS.texto);

            // FUNDO EFETIVO (mesma regra do backend)
            const fundoUser = c.fundo || E.DEFAULTS.fundo;
            const fundoEfetivo = (fundoUser !== E.DEFAULTS.fundo)
                ? fundoUser
                : (e.background || fundoUser);
            set('--perfil-background-efetivo', fundoEfetivo);

            // Tipografia
            set('--perfil-fonte',
                E.FONTE[t.fonte || E.DEFAULTS.fonte] || E.FONTE.padrao);
            set('--perfil-raio-link',
                px(E.RAIO[t.estilo_botao || E.DEFAULTS.estilo] || 12));

            // Layout (tudo multiplicado pelo FATOR_PREVIEW)
            set('--perfil-foto-tamanho',
                px(E.FOTO[l.tamanho_foto || E.DEFAULTS.tamanho_foto] || 128));
            set('--perfil-link-tamanho',
                px(E.LINK[l.tamanho_link || E.DEFAULTS.tamanho_link] || 56));
            set('--perfil-gap',
                px(E.GAP[l.espacamento_links || E.DEFAULTS.gap] || 14));
            set('--perfil-borda-tamanho',
                px(E.BORDA[l.borda_link || E.DEFAULTS.borda] || 3));

            // Hover
            const hover = E.HOVER[e.hover_efeito || E.DEFAULTS.hover] || E.HOVER.subir;
            set('--perfil-hover-transform', hover.transform);
            set('--perfil-hover-brilho',    hover.filter);

            // Animação
            const anim = E.ANIMACAO[e.animacao_entrada || E.DEFAULTS.animacao] || 'fade';
            tela.classList.remove('anim-fade', 'anim-slide', 'anim-scale', 'anim-nenhuma');
            if (anim) tela.classList.add('anim-' + anim);
        },

        // Identidade (não é tema — não passa por config)
        setNome: function (txt) {
            const el = document.getElementById('mockupNome');
            if (el) el.textContent = txt || 'Seu nome';
        },
        setBio: function (txt) {
            const el = document.getElementById('mockupBio');
            if (el) el.textContent = txt || 'Sua bio aparece aqui...';
        },
        setFoto: function (src) {
            const el = document.getElementById('mockupFoto');
            if (!el) return;
            if (src) {
                const sel = document.getElementById('foto_posicao');
                const pos = sel ? sel.value : 'top';
                el.innerHTML = '<img src="' + src + '" alt="Foto" style="object-position: center ' + pos + ';">';
            } else {
                el.innerHTML = '<i class="fas fa-user"></i>';
            }
        },
        setFotoPosicao: function (pos) {
            const img = document.querySelector('#mockupFoto img');
            if (img) img.style.objectPosition = 'center ' + (pos || 'top');
        },
    };

    console.log('✅ Mockup carregado (unificado, cor do user vence gradiente)');
})();