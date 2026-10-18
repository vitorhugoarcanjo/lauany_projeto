/* static/js/components/tema.js
============================================
TEMA claro/escuro — Global
============================================ */

(function() {
    'use strict';

    const STORAGE_KEY = 'meulinks-tema';
    const html = document.documentElement;

    // ─── Detecta tema salvo (ou preferência do sistema) ───
    function obterTemaInicial() {
        const salvo = localStorage.getItem(STORAGE_KEY);
        if (salvo === 'light' || salvo === 'dark') return salvo;
        return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }

    function aplicarTema(tema) {
        html.setAttribute('data-theme', tema);
        localStorage.setItem(STORAGE_KEY, tema);

        // Atualiza o ícone do botão (se existir)
        const icone = document.querySelector('[data-toggle-tema] i');
        if (icone) {
            icone.className = tema === 'dark' ? 'fas fa-moon' : 'fas fa-sun';
        }
    }

    // ─── Aplica na hora (evita flash) ───
    aplicarTema(obterTemaInicial());

    // ─── Botão de toggle ───
    document.addEventListener('click', (e) => {
        const btn = e.target.closest('[data-toggle-tema]');
        if (!btn) return;

        const atual = html.getAttribute('data-theme');
        const novo = atual === 'dark' ? 'light' : 'dark';
        aplicarTema(novo);

        // Notificação opcional
        if (window.Notificacao) {
            Notificacao.sucesso(novo === 'dark' ? 'Modo escuro ativado 🌙' : 'Modo claro ativado ☀️');
        }
    });

    // ─── Detecta mudança do sistema (se o usuário não escolheu) ───
    const mq = window.matchMedia('(prefers-color-scheme: dark)');
    mq.addEventListener('change', (e) => {
        if (!localStorage.getItem(STORAGE_KEY)) {
            aplicarTema(e.matches ? 'dark' : 'light');
        }
    });
})();