/* static/js/components/sidebar.js
============================================
SIDEBAR — Menu mobile
============================================ */

(function() {
    'use strict';

    const menuToggle  = document.getElementById('menuToggle');
    const menuClose   = document.getElementById('menuClose');
    const overlay     = document.getElementById('sidebarOverlay');
    const sidebar     = document.getElementById('mainSidebar');

    if (!sidebar) return;

    function abrir() {
        sidebar.classList.add('active');
        overlay?.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function fechar() {
        sidebar.classList.remove('active');
        overlay?.classList.remove('active');
        document.body.style.overflow = '';
    }

    menuToggle?.addEventListener('click', abrir);
    menuClose?.addEventListener('click', fechar);
    overlay?.addEventListener('click', fechar);

    // Fecha ao clicar num link da sidebar (mobile)
    sidebar.querySelectorAll('.sidebar-nav a').forEach(link => {
        link.addEventListener('click', () => {
            if (window.innerWidth <= 992) fechar();
        });
    });

})();