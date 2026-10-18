/* static/js/modules/pasta_auth/auth.js
============================================
AUTH — Login + Cadastro (AJAX)
============================================ */

(function() {
    'use strict';

    // ==========================================================
    // HELPERS
    // ==========================================================
    function comLoading(btn, acao) {
        if (!btn) return Promise.resolve(acao());
        btn.classList.add('loading');
        btn.disabled = true;

        return Promise.resolve(acao())
            .finally(() => {
                btn.classList.remove('loading');
                btn.disabled = false;
            });
    }

    // ==========================================================
    // LOGIN
    // ==========================================================
    const formLogin = document.getElementById('formLogin');
    if (formLogin) {
        formLogin.addEventListener('submit', function(e) {
            e.preventDefault();

            const btn = document.getElementById('btnEntrar');
            const formData = new FormData(formLogin);

            comLoading(btn, () => {
                return fetch('/login/', {
                    method: 'POST',
                    body: formData,
                    headers: { 'X-Requested-With': 'XMLHttpRequest' }
                })
                .then(r => r.json().then(j => ({ ok: r.ok, data: j })))
                .then(({ ok, data }) => {
                    if (!ok || !data.success) {
                        // Se for email não confirmado, avisa E redireciona
                        if (data.redirect) {
                            Notificacao.aviso(data.message || 'Verifique seu email.');
                            setTimeout(() => {
                                window.location.href = data.redirect;
                            }, 1500);
                            return;
                        }

                        Notificacao.erro(data.message || 'Erro ao entrar.');
                        return;
                    }

                    Notificacao.sucesso(data.message || 'Login efetuado!');
                    setTimeout(() => {
                        if (data.redirect) window.location.href = data.redirect;
                    }, 600);
                })
                .catch(() => Notificacao.erro('Erro de conexão. Tente novamente.'));
            });
        });
    }

    // ==========================================================
    // CADASTRO
    // ==========================================================
    const formCadastro = document.getElementById('formCadastro');
    if (formCadastro) {
        // Máscara de telefone
        const inputTelefone = formCadastro.querySelector('input[name="telefone"]');
        if (inputTelefone) {
            inputTelefone.addEventListener('input', function() {
                let v = this.value.replace(/\D/g, '').slice(0, 11);
                if (v.length <= 10) {
                    v = v.replace(/(\d{2})(\d{4})(\d{0,4})/, '($1) $2-$3');
                } else {
                    v = v.replace(/(\d{2})(\d{5})(\d{0,4})/, '($1) $2-$3');
                }
                this.value = v;
            });
        }

                // Verificação de username em tempo real
        const inputUsername = formCadastro.querySelector('input[name="username"]');
        const feedbackUsername = document.getElementById('username-feedback');

        if (inputUsername && feedbackUsername) {
            let timeoutUsername = null;

            inputUsername.addEventListener('input', function() {
                const username = this.value.trim().toLowerCase();
                this.value = username; // força minúsculo

                clearTimeout(timeoutUsername);

                if (!username) {
                    feedbackUsername.textContent = 'Só letras minúsculas, números e _. Começa com letra.';
                    feedbackUsername.className = 'form-hint';
                    return;
                }

                // Validação local primeiro
                if (username.length < 3) {
                    feedbackUsername.textContent = 'Mínimo 3 caracteres.';
                    feedbackUsername.className = 'form-hint form-hint-erro';
                    return;
                }

                if (!/^[a-z][a-z0-9_]*$/.test(username)) {
                    feedbackUsername.textContent = 'Use só letras minúsculas, números e _.';
                    feedbackUsername.className = 'form-hint form-hint-erro';
                    return;
                }

                // Verifica no backend (com debounce)
                feedbackUsername.textContent = 'Verificando...';
                feedbackUsername.className = 'form-hint form-hint-verificando';

                timeoutUsername = setTimeout(() => {
                    fetch('/cadastre_se/verificar-username/' + encodeURIComponent(username))
                        .then(r => r.json())
                        .then(data => {
                            if (data.disponivel) {
                                feedbackUsername.textContent = '✅ Disponível!';
                                feedbackUsername.className = 'form-hint form-hint-ok';
                            } else {
                                feedbackUsername.textContent = '❌ ' + (data.message || 'Não disponível.');
                                feedbackUsername.className = 'form-hint form-hint-erro';
                            }
                        })
                        .catch(() => {
                            feedbackUsername.textContent = 'Erro ao verificar.';
                            feedbackUsername.className = 'form-hint form-hint-erro';
                        });
                }, 500);
            });
        }

        formCadastro.addEventListener('submit', function(e) {
            e.preventDefault();

            const btn = document.getElementById('btnCadastrar');
            const formData = new FormData(formCadastro);

            comLoading(btn, () => {
                return fetch('/cadastre_se/', {
                    method: 'POST',
                    body: formData,
                    headers: { 'X-Requested-With': 'XMLHttpRequest' }
                })
                .then(r => r.json().then(j => ({ ok: r.ok, data: j })))
                .then(({ ok, data }) => {
                    if (!ok || !data.success) {
                        Notificacao.erro(data.message || 'Erro ao cadastrar.');
                        return;
                    }

                    // Sucesso
                    Notificacao.sucesso(data.message || 'Cadastro realizado!');

                    // Redireciona pro /confirmar-email/<user_id>
                    setTimeout(() => {
                        if (data.redirect) {
                            window.location.href = data.redirect;
                        } else {
                            window.location.href = '/login/';
                        }
                    }, 800);
                })
                .catch(() => Notificacao.erro('Erro de conexão. Tente novamente.'));
            });
        });
    }

    // ==========================================================
    // CONFIRMAR EMAIL
    // ==========================================================
    const formConfirmarEmail = document.getElementById('formConfirmarEmail');
    if (formConfirmarEmail) {
        formConfirmarEmail.addEventListener('submit', function(e) {
            e.preventDefault();

            const btn = document.getElementById('btnVerificar');
            const formData = new FormData(formConfirmarEmail);

            comLoading(btn, () => {
                return fetch('/cadastre_se/validar-codigo', {
                    method: 'POST',
                    body: formData,
                    headers: { 'X-Requested-With': 'XMLHttpRequest' }
                })
                .then(r => r.json().then(j => ({ ok: r.ok, data: j })))
                .then(({ ok, data }) => {
                    if (!ok || !data.success) {
                        Notificacao.erro(data.message || 'Código inválido.');
                        return;
                    }

                    Notificacao.sucesso(data.message || 'Email verificado!');

                    setTimeout(() => {
                        if (data.redirect) {
                            window.location.href = data.redirect;
                        } else {
                            window.location.href = '/login/';
                        }
                    }, 800);
                })
                .catch(() => Notificacao.erro('Erro de conexão. Tente novamente.'));
            });
        });
    }

})();