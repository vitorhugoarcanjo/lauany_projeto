/* static/js/components/notificacoes.js
============================================
SISTEMA DE NOTIFICAÇÕES - GLOBAL
============================================ */

if (window.Notificacao) {
    console.warn("Notificacao já existe - evitando duplicação");
} else {

    window.Notificacao = {

        _container: null,

        _criarContainer() {
            if (this._container) return this._container;
            this._container = document.createElement('div');
            this._container.className = 'notificacao-container';
            this._container.setAttribute('aria-live', 'polite');
            document.body.appendChild(this._container);
            return this._container;
        },

        _criarItem(mensagem, tipo) {
            const icones = { sucesso: '✅', erro: '❌', aviso: '⚠️' };
            const item = document.createElement('div');
            item.className = `notificacao-item ${tipo}`;
            item.innerHTML = `
                <span class="notificacao-icone">${icones[tipo] || 'ℹ️'}</span>
                <span class="notificacao-mensagem">${mensagem}</span>
                <button class="notificacao-fechar" aria-label="Fechar">✕</button>
            `;
            item.querySelector('.notificacao-fechar').addEventListener('click', () => {
                item.classList.add('saindo');
                setTimeout(() => item.remove(), 300);
            });
            return item;
        },

        _mostrar(mensagem, tipo, duracao = 3000) {
            const container = this._criarContainer();
            const item = this._criarItem(mensagem, tipo);
            container.appendChild(item);
            if (duracao > 0) {
                setTimeout(() => {
                    if (!item.parentElement) return;
                    item.classList.add('saindo');
                    setTimeout(() => item.remove(), 300);
                }, duracao);
            }
            return item;
        },

        sucesso(m, d = 3000) { return window.Notificacao._mostrar(m, 'sucesso', d); },
        erro(m, d = 5000)    { return window.Notificacao._mostrar(m, 'erro', d); },
        aviso(m, d = 4000)   { return window.Notificacao._mostrar(m, 'aviso', d); },

        api(response, duracao) {
            if (!response) return this.erro('Erro desconhecido', duracao);
            const tipo = response.success ? 'sucesso' : 'erro';
            const msg  = response.message || response.error || 'Sem mensagem';
            return this[tipo](msg, duracao);
        }
    };
}