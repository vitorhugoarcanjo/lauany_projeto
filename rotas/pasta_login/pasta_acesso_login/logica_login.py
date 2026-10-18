"""LÓGICA DO LOGIN"""

from flask import Blueprint, render_template, request, url_for, session, jsonify
from utils.database.conexao_global import ini_conexao
from rotas.pasta_login.pasta_acesso_login.validacoes.validar_usuario import validar_usuario_bd

# ⚠️ Importa o MasterService (uma vez, sem circular — ele não importa login)
from rotas.pasta_master.services import MasterService

bp_login = Blueprint('login', __name__)


@bp_login.route('/', methods=['GET', 'POST'])
def validar_login():
    """Validação de login"""
    if request.method == 'POST':
        nome_ou_email = request.form.get('nome_ou_email')
        senha = request.form.get('senha')

        # VALIDAÇÃO 1
        if not nome_ou_email or not senha:
            return jsonify({
                'success': False,
                'message': 'Preencha todos os campos!',
                'type': 'aviso'
            }), 400

        # BUSCA USUÁRIO (sem is_master — coluna não existe mais)
        conexao, cursor = ini_conexao()
        cursor.execute(
            'SELECT id, nome, email_verificado FROM usuarios WHERE (nome = %s OR email = %s)',
            (nome_ou_email, nome_ou_email)
        )
        usuario = cursor.fetchone()

        if not usuario:
            return jsonify({
                'success': False,
                'message': 'Usuário não encontrado',
                'type': 'erro'
            }), 404

        # VERIFICA EMAIL CONFIRMADO
        if usuario[2] != 1:
            return jsonify({
                'success': False,
                'message': 'Email não confirmado! Verifique sua caixa de entrada.',
                'type': 'aviso',
                'redirect': url_for('cadastre_se.confirmar_email', user_id=usuario[0])
            }), 403

        # VALIDA SENHA
        resultado = validar_usuario_bd(conexao, nome_ou_email, senha)

        if resultado:
            session.permanent = True
            session['user_id'] = usuario[0]
            session['user_nome'] = usuario[1]

            # ⚠️ Verifica master via MasterService (não via tabela usuarios)
            master_service = MasterService(conexao, cursor)
            session['is_master'] = master_service.verificar_master(usuario[0])

            return jsonify({
                'success': True,
                'message': 'Logado com sucesso!',
                'type': 'sucesso',
                'redirect': url_for('painel.ini_painel')
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Senha incorreta',
                'type': 'erro'
            }), 401

    return render_template('pasta_login/pasta_acesso_login/tela_login.html.jinja')