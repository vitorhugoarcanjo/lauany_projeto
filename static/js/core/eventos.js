/* static/js/core/eventos.js
============================================
HELPERS GLOBAIS — Padrão 2099
============================================ */

// Atalhos de querySelector
window.$  = (sel, ctx) => (ctx || document).querySelector(sel);
window.$$ = (sel, ctx) => Array.from((ctx || document).querySelectorAll(sel));

// Delegação de eventos (evita listeners repetidos)
window.delegar = (elemento, evento, seletor, callback) => {
    elemento.addEventListener(evento, (e) => {
        const alvo = e.target.closest(seletor);
        if (alvo) callback(e, alvo);
    });
};

// Debounce (útil pra inputs)
window.debounce = (fn, delay) => {
    let timer;
    return (...args) => {
        clearTimeout(timer);
        timer = setTimeout(() => fn(...args), delay || 300);
    };
};