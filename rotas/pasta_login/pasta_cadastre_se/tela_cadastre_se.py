"""CADASTRO DE USUÁRIO — View"""

import re
from flask import Blueprint, request, render_template, jsonify, url_for
from utils.database.conexao_global import ini_conexao
from .autenticador_email.email_utils import (
    gerar_codigo,
    enviar_email_confirmacao,
    salvar_codigo_verificacao,
    verificar_codigo,
)
from .validacoes.criptografia_snh import criptografar_senha
from .validacoes.validar_usuario import (
    validar_email_formato,
    validar_e_limpar_telefone,
)

bp_cadastre_se = Blueprint('cadastre_se', __name__)


# ==========================================================
# SLUGS RESERVADOS (não podem ser username)
# ==========================================================
SLUGS_RESERVADOS = {
    'login', 'cadastre_se', 'recuperar', 'painel', 'meus-links',
    'logout', 'admin', 'static', 'api', 'sobre', 'contato',
    'artigos', 'projetos', 'arquitetura-2099', 'auditoria',
    'meulinks', 'sistema', 'suporte', 'ajuda', 'termos',
    'privacidade', 'config', 'dashboard', 'perfil',
}


def _validar_username(username):
    """Valida o formato do username"""
    if not username:
        return False, 'Username é obrigatório.'

    if len(username) < 3:
        return False, 'Username deve ter no mínimo 3 caracteres.'

    if len(username) > 30:
        return False, 'Username deve ter no máximo 30 caracteres.'

    if not re.match(r'^[a-z0-9_]+$', username):
        return False, 'Username só pode ter letras minúsculas, números e _.'

    if username[0] in '0123456789_':
        return False, 'Username deve começar com uma letra.'

    if username in SLUGS_RESERVADOS:
        return False, 'Este username está reservado. Escolha outro.'

    return True, None


def _username_disponivel(cursor, username):
    """Verifica se o username já está em uso"""
    cursor.execute('SELECT 1 FROM perfis WHERE username = %s', (username,))
    return not cursor.fetchone()


def _gerar_username_automatico(cursor, nome, email):
    """Gera um username automático a partir do nome ou email"""
    # Tenta nome primeiro
    base = re.sub(r'[^a-z0-9_]', '', nome.lower().replace(' ', '_'))

    if not base or len(base) < 3:
        # Fallback: usa email
        base = re.sub(r'[^a-z0-9_]', '', email.split('@')[0].lower())

    if not base:
        base = 'usuario'

    base = base[:20]

    # Se não começa com letra, adiciona prefixo
    if base[0] in '0123456789_':
        base = 'user_' + base

    # Verifica disponibilidade
    username = base
    if _username_disponivel(cursor, username):
        return username

    # Adiciona número
    contador = 1
    while contador <= 999:
        username = f"{base}{contador}"
        if _username_disponivel(cursor, username):
            return username
        contador += 1

    # Último recurso: timestamp
    import time
    return f"user_{int(time.time())}"


@bp_cadastre_se.route('/', methods=['GET', 'POST'])
def tela_cadastre_se():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        telefone = request.form.get('telefone', '').strip()
        email = request.form.get('email', '').strip()
        username_input = request.form.get('username', '').strip().lower()
        senha = request.form.get('senha', '')
        confirmar_senha = request.form.get('confirmar_senha', '')

        # VALIDAÇÕES
        erros = []

        if not nome or not telefone or not email or not senha or not confirmar_senha:
            erros.append('Preencha todos os campos.')

        if senha and confirmar_senha and senha != confirmar_senha:
            erros.append('As senhas não coincidem.')

        if email and not validar_email_formato(email):
            erros.append('E-mail inválido.')

        if senha and len(senha) < 6:
            erros.append('Senha deve ter no mínimo 6 caracteres.')

        telefone_limpo = validar_e_limpar_telefone(telefone)
        if not telefone_limpo:
            erros.append('Telefone inválido. Use DDD + número.')

        if erros:
            return jsonify({
                'success': False,
                'message': erros[0],
                'errors': erros,
            }), 400

        conexao, cursor = ini_conexao()

        # Verifica email único
        cursor.execute('SELECT id FROM usuarios WHERE email = %s', (email,))
        if cursor.fetchone():
            return jsonify({
                'success': False,
                'message': 'E-mail já cadastrado.',
            }), 400

        # ==========================================================
        # USERNAME
        # ==========================================================
        if username_input:
            # Usuário escolheu — valida
            valido, msg = _validar_username(username_input)
            if not valido:
                return jsonify({'success': False, 'message': msg}), 400

            if not _username_disponivel(cursor, username_input):
                return jsonify({
                    'success': False,
                    'message': 'Este username já está em uso. Escolha outro.',
                }), 400

            username_final = username_input
        else:
            # Gera automático
            username_final = _gerar_username_automatico(cursor, nome, email)

        # Criptografa senha
        senha_criptografada = criptografar_senha(senha)

        try:
            cursor.execute("""
                INSERT INTO usuarios (nome, telefone, email, senha)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (nome, telefone_limpo, email, senha_criptografada))

            user_id = cursor.fetchone()[0]

            # Cria perfil
            cursor.execute("""
                INSERT INTO perfis (usuario_id, username)
                VALUES (%s, %s)
            """, (user_id, username_final))

            conexao.commit()

            # Envia email
            codigo = gerar_codigo()
            sucesso, mensagem = enviar_email_confirmacao(email, codigo)

            if sucesso:
                salvar_codigo_verificacao(user_id, codigo)
                return jsonify({
                    'success': True,
                    'message': 'Cadastro realizado! Verifique seu email.',
                    'redirect': url_for('cadastre_se.confirmar_email', user_id=user_id),
                }), 201
            else:
                # Rollback se falhar email
                cursor.execute('DELETE FROM perfis WHERE usuario_id = %s', (user_id,))
                cursor.execute('DELETE FROM usuarios WHERE id = %s', (user_id,))
                conexao.commit()
                return jsonify({
                    'success': False,
                    'message': f'Erro ao enviar email: {mensagem}',
                }), 500

        except Exception as e:
            conexao.rollback()
            return jsonify({
                'success': False,
                'message': f'Erro ao cadastrar: {str(e)}',
            }), 500

    return render_template('pasta_login/pasta_cadastre_se/tela_cadastro.html.jinja')


@bp_cadastre_se.route('/verificar-username/<username>')
def verificar_username(username):
    """Endpoint AJAX pra checar se username tá disponível em tempo real"""
    username = username.strip().lower()

    valido, msg = _validar_username(username)
    if not valido:
        return jsonify({'success': False, 'disponivel': False, 'message': msg}), 200

    conexao, cursor = ini_conexao()
    disponivel = _username_disponivel(cursor, username)

    if disponivel:
        return jsonify({
            'success': True,
            'disponivel': True,
            'message': 'Username disponível!',
        }), 200
    else:
        return jsonify({
            'success': True,
            'disponivel': False,
            'message': 'Este username já está em uso.',
        }), 200


@bp_cadastre_se.route('/confirmar-email/<int:user_id>')
def confirmar_email(user_id):
    return render_template(
        'pasta_login/pasta_cadastre_se/tela_confirmar_email.html.jinja',
        user_id=user_id,
    )


@bp_cadastre_se.route('/validar-codigo', methods=['POST'])
def validar_codigo():
    user_id = request.form.get('user_id')
    codigo = request.form.get('codigo', '').strip()

    if not codigo:
        return jsonify({'success': False, 'message': 'Digite o código.'}), 400

    sucesso, mensagem = verificar_codigo(user_id, codigo)

    if sucesso:
        return jsonify({
            'success': True,
            'message': mensagem,
            'redirect': url_for('login.validar_login'),
        }), 200
    else:
        return jsonify({'success': False, 'message': mensagem}), 400


@bp_cadastre_se.route('/reenviar-codigo/<int:user_id>')
def reenviar_codigo(user_id):
    conexao, cursor = ini_conexao()
    cursor.execute("SELECT email FROM usuarios WHERE id = %s", (user_id,))
    resultado = cursor.fetchone()

    if not resultado:
        return jsonify({'success': False, 'message': 'Usuário não encontrado.'}), 404

    email = resultado[0]
    codigo = gerar_codigo()
    sucesso, mensagem = enviar_email_confirmacao(email, codigo)

    if sucesso:
        salvar_codigo_verificacao(user_id, codigo)
        return jsonify({'success': True, 'message': 'Novo código enviado!'}), 200

    return jsonify({'success': False, 'message': mensagem}), 500