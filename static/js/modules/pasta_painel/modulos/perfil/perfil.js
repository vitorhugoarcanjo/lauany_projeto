/* static/js/modules/pasta_painel/modulos/perfil/perfil.js
============================================
PERFIL — usa Mockup global
============================================ */

(function() {
    'use strict';

    document.addEventListener('DOMContentLoaded', function() {
        const form = document.getElementById('formPerfil');
        if (!form) return;

        const inputUsername = document.getElementById('username');
        const feedbackUsername = document.getElementById('usernameFeedback');
        const inputBio = document.getElementById('bio');
        const bioContador = document.getElementById('bioContador');
        const inputNomeExibicao = document.getElementById('nome_exibicao');
        const inputFoto = document.getElementById('foto');
        const inputRemoverFoto = document.getElementById('remover_foto');
        const fotoPreview = document.getElementById('fotoPreview');
        const btnRemoverFoto = document.getElementById('btnRemoverFoto');
        const btnSalvar = document.getElementById('btnSalvarPerfilFooter');  // ← ID NOVO
        const inputFotoPosicao = document.getElementById('foto_posicao');

        function atualizarMockup() {
            if (!window.Mockup) return;
            if (inputNomeExibicao) Mockup.setNome(inputNomeExibicao.value.trim());
            if (inputBio) Mockup.setBio(inputBio.value.trim());
        }

        // USERNAME (validação)
        let timeoutUsername = null;
        if (inputUsername) {
            inputUsername.addEventListener('input', function() {
                const username = this.value.trim().toLowerCase();
                this.value = username;
                clearTimeout(timeoutUsername);

                if (!username) {
                    feedbackUsername.textContent = 'Letras minúsculas, números e _.';
                    feedbackUsername.className = 'form-hint';
                    return;
                }
                if (username.length < 3) {
                    feedbackUsername.textContent = 'Mínimo 3 caracteres.';
                    feedbackUsername.className = 'form-hint form-hint-erro';
                    return;
                }
                if (!/^[a-z][a-z0-9_]*$/.test(username)) {
                    feedbackUsername.textContent = 'Só minúsculas, números e _ (começar com letra).';
                    feedbackUsername.className = 'form-hint form-hint-erro';
                    return;
                }

                feedbackUsername.textContent = 'Verificando...';
                feedbackUsername.className = 'form-hint form-hint-verificando';

                timeoutUsername = setTimeout(() => {
                    fetch('/painel/perfil/verificar-username/' + encodeURIComponent(username))
                        .then(r => r.json())
                        .then(data => {
                            if (data.disponivel) {
                                feedbackUsername.textContent = '✅ Disponível!';
                                feedbackUsername.className = 'form-hint form-hint-ok';
                            } else {
                                feedbackUsername.textContent = '❌ ' + (data.message || 'Indisponível.');
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

        // NOME
        if (inputNomeExibicao) {
            inputNomeExibicao.addEventListener('input', atualizarMockup);
        }

        // BIO
        if (inputBio && bioContador) {
            const atualizar = () => {
                bioContador.textContent = inputBio.value.length;
                atualizarMockup();
            };
            inputBio.addEventListener('input', atualizar);
            atualizar();
        }

        // POSIÇÃO DO CORTE
        if (inputFotoPosicao) {
            inputFotoPosicao.addEventListener('change', function() {
                const preview = document.getElementById('fotoPreview');
                if (preview) {
                    const img = preview.querySelector('img');
                    if (img) {
                        img.style.objectPosition = 'center ' + this.value;
                    }
                }
                if (window.Mockup && Mockup.setFotoPosicao) {
                    Mockup.setFotoPosicao(this.value);
                }
            });
        }

        // FOTO — upload
        if (inputFoto) {
            inputFoto.addEventListener('change', function() {
                const file = this.files[0];
                if (!file) return;

                if (file.size > 2 * 1024 * 1024) {
                    if (window.Notificacao) Notificacao.erro('Imagem muito grande. Máximo 2MB.');
                    this.value = '';
                    return;
                }

                const reader = new FileReader();
                reader.onload = (e) => {
                    const src = e.target.result;
                    const posicao = inputFotoPosicao ? inputFotoPosicao.value : 'top';

                    if (fotoPreview) {
                        fotoPreview.innerHTML = `<img src="${src}" alt="Preview" style="object-position: center ${posicao};">`;
                    }
                    if (window.Mockup) {
                        Mockup.setFoto(src);
                    }
                };
                reader.readAsDataURL(file);

                if (inputRemoverFoto) inputRemoverFoto.value = '0';
                if (btnRemoverFoto) btnRemoverFoto.disabled = false;
            });
        }

        // FOTO — remover
        if (btnRemoverFoto) {
            btnRemoverFoto.addEventListener('click', function() {
                if (inputRemoverFoto) inputRemoverFoto.value = '1';
                if (inputFoto) inputFoto.value = '';

                const placeholder = '<div class="pp-foto-placeholder"><i class="fas fa-user"></i></div>';
                if (fotoPreview) fotoPreview.innerHTML = placeholder;

                if (window.Mockup) Mockup.setFoto(null);

                btnRemoverFoto.disabled = true;

                if (window.Notificacao) {
                    Notificacao.aviso('Foto marcada pra remoção. Salva pra confirmar.');
                }
            });
        }

        // ⚠️ BOTÃO DO FOOTER: chama submit do form
        if (btnSalvar) {
            btnSalvar.addEventListener('click', function() {
                form.requestSubmit();
            });
        }

        // SUBMIT
        form.addEventListener('submit', function(ev) {
            ev.preventDefault();

            const formData = new FormData(form);

            // Loading no botão do footer
            if (btnSalvar) {
                btnSalvar.disabled = true;
                const texto = btnSalvar.querySelector('span');
                if (texto) texto.textContent = 'SALVANDO...';
            }

            fetch('/painel/perfil/salvar', {
                method: 'POST',
                body: formData,
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            })
            .then(r => r.json().then(j => ({ ok: r.ok, data: j })))
            .then(({ ok, data }) => {
                if (!ok || !data.success) {
                    const msg = data.error || 'Erro ao salvar.';
                    if (window.Notificacao) Notificacao.erro(msg);
                    return;
                }
                if (window.Notificacao) Notificacao.sucesso(data.message || 'Perfil atualizado!');

                if (inputRemoverFoto) inputRemoverFoto.value = '0';
                if (btnRemoverFoto) btnRemoverFoto.disabled = true;
            })
            .catch(() => {
                if (window.Notificacao) Notificacao.erro('Erro de conexão.');
            })
            .finally(() => {
                if (btnSalvar) {
                    btnSalvar.disabled = false;
                    const texto = btnSalvar.querySelector('span');
                    if (texto) texto.textContent = 'SALVAR';
                }
            });
        });

        atualizarMockup();
        console.log('✅ Perfil carregado');
    });
})();