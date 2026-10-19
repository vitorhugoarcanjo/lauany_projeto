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

        this.el = {
            tipo:           formEl.querySelector('.js-tipo'),
            tipoBtns:       formEl.querySelectorAll('.js-tipo-btn'),
            campos:         formEl.querySelectorAll('.js-campo'),
            titulo:         formEl.querySelector('.js-titulo'),
            url:            formEl.querySelector('.js-url'),
            telefone:       formEl.querySelector('.js-telefone'),
            mensagem:       formEl.querySelector('.js-mensagem'),
            email:          formEl.querySelector('.js-email'),
            assunto:        formEl.querySelector('.js-assunto'),
            descricao:      formEl.querySelector('.js-descricao'),
            icone:          formEl.querySelector('.js-icone'),
            iconePreview:   formEl.querySelector('.js-icone-preview'),
            ordem:          formEl.querySelector('.js-ordem'),
            novaAba:        formEl.querySelector('.js-nova-aba'),
            destaque:       formEl.querySelector('.js-destaque'),
        };

        this._bind();
        this._aplicarTipo(this.el.tipo ? this.el.tipo.value : 'link');

        // ⚠️ ADICIONA O LISTENER DE SUBMIT AQUI (no constructor)
        this._vincularSubmit();
    }

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

    LinkForm.prototype._aplicarTipo = function(tipo) {
        this.el.tipoBtns.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.tipo === tipo);
        });

        this.el.campos.forEach(campo => {
            const isLink    = campo.classList.contains('js-campo-link');
            const isZap     = campo.classList.contains('js-campo-whatsapp');
            const isEmail   = campo.classList.contains('js-campo-email');

            campo.hidden = !(
                (tipo === 'link' && isLink) ||
                (tipo === 'whatsapp' && isZap) ||
                (tipo === 'email' && isEmail)
            );
        });

        if (this.el.icone && this.el.iconePreview) {
            let iconeAuto = null;
            if (tipo === 'whatsapp') iconeAuto = 'fa-whatsapp';
            else if (tipo === 'email') iconeAuto = 'fa-envelope';

            const atual = this.el.icone.value.trim();
            if (!atual || ['fa-link', 'fa-whatsapp', 'fa-envelope'].includes(atual)) {
                if (iconeAuto) {
                    this.el.icone.value = iconeAuto;
                    this.el.iconePreview.className = 'fas ' + iconeAuto + ' js-icone-preview';
                } else if (tipo === 'link' && atual !== 'fa-link') {
                    this.el.icone.value = 'fa-link';
                    this.el.iconePreview.className = 'fas fa-link js-icone-preview';
                }
            }
        }

        if (this.el.tipo) this.el.tipo.value = tipo;
    };

    LinkForm.prototype._bind = function() {
        const self = this;

        this.el.tipoBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                self._aplicarTipo(this.dataset.tipo);
            });
        });

        if (this.el.icone && this.el.iconePreview) {
            this.el.icone.addEventListener('input', function() {
                const cls = this.value.trim() || 'fa-link';
                self.el.iconePreview.className = 'fas ' + cls + ' js-icone-preview';
            });
        }

        if (this.el.telefone) {
            this.el.telefone.addEventListener('input', function() {
                let v = this.value.replace(/\D/g, '').slice(0, 11);
                if (v.length <= 10) {
                    v = v.replace(/(\d{2})(\d{4})(\d{0,4})/, '($1) $2-$3');
                } else {
                    v = v.replace(/(\d{2})(\d{5})(\d{0,4})/, '($1) $2-$3');
                }
                this.value = v;
            });
        }
    };

    // ==========================================================
    // SUBMIT — UM ÚNICO LISTENER (evita nativo + faz o fetch)
    // ==========================================================
    LinkForm.prototype._vincularSubmit = function() {
        const self = this;

        // Evita vincular 2x no mesmo form
        if (this.form.dataset.submitVinculado === '1') return;
        this.form.dataset.submitVinculado = '1';

        this.form.addEventListener('submit', function(ev) {
            ev.preventDefault();
            ev.stopPropagation();

            const btn = self.form.querySelector('button[type="submit"]');
            if (btn) {
                btn.classList.add('loading');
                btn.disabled = true;
            }

            const url = self.mode === 'create'
                ? '/links/novo_link/salvar'
                : '/links/edit_link/salvar/' + self.form.dataset.linkId;

            self.submit(url)
                .catch(err => console.error('❌ Erro submit:', err))
                .finally(() => {
                    if (btn) {
                        btn.classList.remove('loading');
                        btn.disabled = false;
                    }
                });
        });
    };

    // ==========================================================
    // API PÚBLICA
    // ==========================================================
    LinkForm.prototype.setData = function(data) {
        if (!data) return;
        this._limparErrosForm();

        if (data.tipo) this._aplicarTipo(data.tipo);

        if (this.el.titulo)    this.el.titulo.value = data.titulo || '';
        if (this.el.descricao) this.el.descricao.value = data.descricao || '';
        if (this.el.icone)     this.el.icone.value = data.icone || 'fa-link';
        if (this.el.ordem)     this.el.ordem.value = data.ordem || 0;
        if (this.el.novaAba)   this.el.novaAba.checked = data.abrir_nova_aba != 0;
        if (this.el.destaque)  this.el.destaque.checked = data.destaque == 1;

        if (data.tipo === 'whatsapp') {
            if (this.el.telefone) this.el.telefone.value = data.telefone || '';
            if (this.el.mensagem) this.el.mensagem.value = data.mensagem || '';
        } else if (data.tipo === 'email') {
            if (this.el.email)   this.el.email.value = data.email_destino || '';
            if (this.el.assunto) this.el.assunto.value = data.assunto || '';
        } else {
            if (this.el.url) this.el.url.value = data.url || '';
        }

        if (this.el.iconePreview && this.el.icone) {
            this.el.iconePreview.className = 'fas ' + (this.el.icone.value || 'fa-link') + ' js-icone-preview';
        }
    };

    LinkForm.prototype.getData = function() {
        const tipo = this.el.tipo ? this.el.tipo.value : 'link';

        const base = {
            tipo:           tipo,
            titulo:         this.el.titulo ? this.el.titulo.value.trim() : '',
            descricao:      this.el.descricao ? this.el.descricao.value.trim() : '',
            icone:          this.el.icone ? this.el.icone.value.trim() : 'fa-link',
            ordem:          this.el.ordem ? (parseInt(this.el.ordem.value) || 0) : 0,
            abrir_nova_aba: this.el.novaAba ? (this.el.novaAba.checked ? 1 : 0) : 1,
            destaque:       this.el.destaque ? (this.el.destaque.checked ? 1 : 0) : 0,
        };

        if (tipo === 'whatsapp') {
            base.telefone = this.el.telefone ? this.el.telefone.value.trim() : '';
            base.mensagem = this.el.mensagem ? this.el.mensagem.value.trim() : '';
        } else if (tipo === 'email') {
            base.email_destino = this.el.email ? this.el.email.value.trim() : '';
            base.assunto       = this.el.assunto ? this.el.assunto.value.trim() : '';
        } else {
            base.url = this.el.url ? this.el.url.value.trim() : '';
        }

        return base;
    };

    LinkForm.prototype.reset = function() {
        this._limparErrosForm();
        this.form.reset();
        this._aplicarTipo('link');

        if (this.el.url)      this.el.url.value = '';
        if (this.el.telefone) this.el.telefone.value = '';
        if (this.el.mensagem) this.el.mensagem.value = '';
        if (this.el.email)    this.el.email.value = '';
        if (this.el.assunto)  this.el.assunto.value = '';

        if (this.el.icone) this.el.icone.value = 'fa-link';
        if (this.el.ordem) this.el.ordem.value = '0';
        if (this.el.novaAba) this.el.novaAba.checked = true;
        if (this.el.destaque) this.el.destaque.checked = false;

        if (this.el.iconePreview) {
            this.el.iconePreview.className = 'fas fa-link js-icone-preview';
        }
    };

    LinkForm.prototype.submit = function(url) {
        const self = this;
        const data = this.getData();

        if (!data.titulo) {
            Notificacao.aviso('Título é obrigatório.');
            return Promise.reject(new Error('titulo'));
        }

        if (data.tipo === 'link') {
            if (!data.url) {
                Notificacao.aviso('URL é obrigatória.');
                return Promise.reject(new Error('url'));
            }
            if (!/^(https?:\/\/|mailto:|tel:)/.test(data.url)) {
                Notificacao.aviso('URL deve começar com http://, https://, mailto: ou tel:');
                return Promise.reject(new Error('url_formato'));
            }
        } else if (data.tipo === 'whatsapp') {
            if (!data.telefone || data.telefone.replace(/\D/g, '').length < 10) {
                Notificacao.aviso('Telefone do WhatsApp é obrigatório.');
                return Promise.reject(new Error('telefone'));
            }
        } else if (data.tipo === 'email') {
            if (!data.email_destino || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email_destino)) {
                Notificacao.aviso('E-mail inválido.');
                return Promise.reject(new Error('email'));
            }
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