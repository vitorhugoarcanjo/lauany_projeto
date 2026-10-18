/* static/js/components/mockup.js */

(function() {
    'use strict';

    window.Mockup = {
        setNome: function(texto) {
            const el = document.getElementById('mockupNome');
            if (el) el.textContent = texto || 'Seu nome';
        },

        setBio: function(texto) {
            const el = document.getElementById('mockupBio');
            if (el) el.textContent = texto || 'Sua bio aparece aqui...';
        },

        setFoto: function(src) {
            const el = document.getElementById('mockupFoto');
            if (!el) return;

            if (src) {
                const selectPosicao = document.getElementById('foto_posicao');
                const posicao = selectPosicao ? selectPosicao.value : 'top';
                el.innerHTML = `<img src="${src}" alt="Foto" style="object-position: center ${posicao};">`;
            } else {
                el.innerHTML = '<i class="fas fa-user"></i>';
            }
        },

        setFotoPosicao: function(posicao) {
            const foto = document.getElementById('mockupFoto');
            if (!foto) return;
            const img = foto.querySelector('img');
            if (img) {
                img.style.objectPosition = 'center ' + (posicao || 'top');
            }
        },

        setCores: function(primaria, secundaria, fundo, texto) {
            const tela = document.getElementById('mockupTela');
            if (!tela) return;
            if (primaria)   tela.style.setProperty('--perfil-cor-primaria', primaria);
            if (secundaria) tela.style.setProperty('--perfil-cor-secundaria', secundaria);
            if (fundo)      tela.style.setProperty('--perfil-cor-fundo', fundo);
            if (texto)      tela.style.setProperty('--perfil-cor-texto', texto);
        },

        setEstiloBotao: function(estilo) {
            const tela = document.getElementById('mockupTela');
            if (!tela) return;
            const raios = { arredondado: '12px', quadrado: '4px', pilula: '999px' };
            tela.style.setProperty('--perfil-raio-link', raios[estilo] || '12px');
        },

        setFonte: function(fonte) {
            const tela = document.getElementById('mockupTela');
            if (!tela) return;
            const fontes = {
                padrao: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif",
                serif: "Georgia, 'Times New Roman', serif",
                mono: "'Courier New', Consolas, monospace",
                handwritten: "'Comic Sans MS', 'Caveat', cursive"
            };
            tela.style.fontFamily = fontes[fonte] || fontes.padrao;
        },

        setTamanhos: function(tamanhoFoto, tamanhoLink, gap) {
            const tela = document.getElementById('mockupTela');
            if (!tela) return;
            // Valores do MOCKUP (escala ~0.57x do público)
            const fotos = { pequena: '64px', medio: '80px', grande: '96px' };
            const links = { pequeno: '36px', medio: '42px', grande: '48px' };
            const gaps = { compacto: '6px', medio: '10px', espacoso: '14px' };
            if (tamanhoFoto) tela.style.setProperty('--mockup-foto-tamanho', fotos[tamanhoFoto] || '80px');
            if (tamanhoLink) tela.style.setProperty('--mockup-link-tamanho', links[tamanhoLink] || '42px');
            if (gap) tela.style.setProperty('--mockup-gap', gaps[gap] || '10px');
        },

        setBorda: function(borda) {
            const tela = document.getElementById('mockupTela');
            if (!tela) return;
            const bordas = { sem: '0px', fina: '1px', media: '2px', grossa: '3px' };
            tela.style.setProperty('--mockup-borda-tamanho', bordas[borda] || '2px');
        },

        setHover: function(hover) {
            const tela = document.getElementById('mockupTela');
            if (!tela) return;
            const transforms = {
                nenhum: 'none',
                subir: 'translateY(-4px)',
                escalar: 'scale(1.05)',
                brilho: 'none'
            };
            const brilhos = {
                nenhum: 'none',
                subir: 'none',
                escalar: 'none',
                brilho: 'brightness(1.15)'
            };
            tela.style.setProperty('--mockup-hover-transform', transforms[hover] || 'none');
            tela.style.setProperty('--mockup-hover-brilho', brilhos[hover] || 'none');
        },

        setAnimacao: function(animacao) {
            const tela = document.getElementById('mockupTela');
            if (!tela) return;
            tela.classList.remove('anim-fade', 'anim-slide', 'anim-scale', 'anim-nenhuma');
            if (animacao && animacao !== 'nenhuma') {
                tela.classList.add('anim-' + animacao);
            }
        }
    };

    console.log('✅ Mockup carregado');
})();