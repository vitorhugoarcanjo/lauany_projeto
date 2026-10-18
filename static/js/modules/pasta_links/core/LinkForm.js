/* static/js/modules/pasta_links/core/LinkForm.js
============================================
LinkForm — Classe base pros modais Novo/Editar
============================================ */

(function() {
    'use strict';

    function LinkForm(formEl, options) {
        if (!formEl) throw new Error('LinkForm: formEl obrigatório');

        this.form = formEl;
        this.options = options || {};
        this.mode = this.options.mode || 'create';
        this.onSubmitSuccess = this.options.onSubmitSuccess || null;
        this.onSubmitError = this.options.onSubmitError || null;

        // Elementos internos (escopados via .js-*)
        this.el = {
            titulo:       formEl.querySelector('.js-titulo'),
            url:          formEl.querySelector('.js-url'),
            descricao:    formEl.querySelector('.js-descricao'),
            icone:        formEl.querySelector('.js-icone'),
            iconePreview: formEl.querySelector('.js-icone-preview'),
            ordem:        formEl.querySelector('.js-ordem'),
            novaAba:      formEl.querySelector('.js-nova-aba'),
            destaque:     formEl.querySelector('.js-destaque'),
        };

        this._bind();
    }

    // ==========================================================
    // MAPA DE VALIDAÇÃO (campo backend -> seletor)
    // ==========================================================
    LinkForm.prototype._MAPA_IDS = {
        'titulo':    '.js-titulo',
        'url':       '.js-url',
        'descricao': '.js-descricao',
        'icone':     '.js-icone',
        'ordem':     '.js-ordem',
    };

    LinkForm.prototype._limparErrosForm = function() {
        this.form.querySelectorAll('.campo-erro').forEach(el => el.classList.remove('campo-erro'));
        this.form.querySelectorAll('.msg-erro-campo').forEach(el => el.remove());
    };

    LinkForm.prototype._mostrarErrosForm = function(errors) {
        this._limparErrosForm();
        const self = this;

        errors.forEach(er => {
            const selector = self._MAPA_IDS[er.campo];
            if (!selector) return;

            const input = self.form.querySelector(selector);
            if (!input) return;

            input.classList.add('campo-erro');

            const msg = document.createElement('span');
            msg.className = 'msg-erro-campo';
            msg.textContent = er.mensagem;
            input.parentNode.appendChild(msg);
        });
    };

    // ==========================================================
    // EVENTOS
    // ==========================================================
    LinkForm.prototype._bind = function() {
        const self = this;

        // Preview do ícone em tempo real
        if (this.el.icone && this.el.iconePreview) {
            this.el.icone.addEventListener('input', function() {
                const cls = this.value.trim() || 'fa-link';
                self.el.iconePreview.className = 'fas ' + cls + ' js-icone-preview';
            });
        }
    };

    // ==========================================================
    // API PÚBLICA: setData
    // ==========================================================
    LinkForm.prototype.setData = function(data) {
        if (!data) return;
        this._limparErrosForm();

        if (this.el.titulo)    this.el.titulo.value = data.titulo || '';
        if (this.el.url)       this.el.url.value = data.url || '';
        if (this.el.descricao) this.el.descricao.value = data.descricao || '';
        if (this.el.icone)     this.el.icone.value = data.icone || 'fa-link';
        if (this.el.ordem)     this.el.ordem.value = data.ordem || 0;
        if (this.el.novaAba)   this.el.novaAba.checked = data.abrir_nova_aba != 0;
        if (this.el.destaque)  this.el.destaque.checked = data.destaque == 1;

        // Atualiza preview do ícone
        if (this.el.iconePreview && this.el.icone) {
            this.el.iconePreview.className = 'fas ' + (this.el.icone.value || 'fa-link') + ' js-icone-preview';
        }
    };

    // ==========================================================
    // API PÚBLICA: getData
    // ==========================================================
    LinkForm.prototype.getData = function() {
        return {
            titulo:         this.el.titulo ? this.el.titulo.value.trim() : '',
            url:            this.el.url ? this.el.url.value.trim() : '',
            descricao:      this.el.descricao ? this.el.descricao.value.trim() : '',
            icone:          this.el.icone ? this.el.icone.value.trim() : 'fa-link',
            ordem:          this.el.ordem ? (parseInt(this.el.ordem.value) || 0) : 0,
            abrir_nova_aba: this.el.novaAba ? (this.el.novaAba.checked ? 1 : 0) : 1,
            destaque:       this.el.destaque ? (this.el.destaque.checked ? 1 : 0) : 0,
        };
    };

    // ==========================================================
    // API PÚBLICA: reset
    // ==========================================================
    LinkForm.prototype.reset = function() {
        this._limparErrosForm();
        this.form.reset();

        if (this.el.icone) this.el.icone.value = 'fa-link';
        if (this.el.ordem) this.el.ordem.value = '0';
        if (this.el.novaAba) this.el.novaAba.checked = true;
        if (this.el.destaque) this.el.destaque.checked = false;

        if (this.el.iconePreview) {
            this.el.iconePreview.className = 'fas fa-link js-icone-preview';
        }
    };

    // ==========================================================
    // API PÚBLICA: submit
    // ==========================================================
    LinkForm.prototype.submit = function(url) {
        const self = this;
        const data = this.getData();

        // Validações front
        if (!data.titulo) {
            Notificacao.aviso('Título é obrigatório.');
            return Promise.reject(new Error('titulo'));
        }
        if (!data.url) {
            Notificacao.aviso('URL é obrigatória.');
            return Promise.reject(new Error('url'));
        }
        if (!/^(https?:\/\/|mailto:|tel:)/.test(data.url)) {
            Notificacao.aviso('URL deve começar com http://, https://, mailto: ou tel:');
            return Promise.reject(new Error('url_formato'));
        }

        return fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify(data)
        })
        .then(r => r.json().then(j => ({ ok: r.ok, data: j })))
        .then(res => {
            if (!res.ok || res.data.success === false) {
                let msg;
                if (res.data.errors && res.data.errors.length > 0) {
                    self._mostrarErrosForm(res.data.errors);
                    msg = 'Corrija os campos em vermelho.';
                } else {
                    msg = res.data.error || res.data.message || 'Erro ao salvar.';
                }
                if (self.onSubmitError) self.onSubmitError(msg);
                else Notificacao.erro(msg);
                throw new Error(msg);
            }

            if (self.onSubmitSuccess) self.onSubmitSuccess(res.data);
            return res.data;
        });
    };

    window.LinkForm = LinkForm;
    console.log('✅ LinkForm carregado');

})();