"""CONFIGURAÇÕES DO USUÁRIO — View"""

import logging
from flask import render_template, request, session, jsonify

from rotas.middleware.autenticacao import login_required
from rotas.pasta_painel.modulos.config import bp_config
from utils.database.conexao_global import ini_conexao

from rotas.pasta_login.pasta_cadastre_se.validacoes.criptografia_snh import (
    criptografar_senha, verificar_senha
)

from .services import ConfigService
from .validacoes import validar_campos_senha

logger = logging.getLogger(__name__)


@bp_config.route('/')
@login_required
def tela_config():
    usuario_id = session['user_id']
    conexao, cursor = ini_conexao()

    service = ConfigService(conexao, cursor)
    usuario = service.buscar_usuario(usuario_id)

    return render_template(
        'pasta_painel/modulos/config/tela_config.html.jinja',
        usuario=usuario,
    )


@bp_config.route('/alterar-senha', methods=['POST'])
@login_required
def alterar_senha():
    usuario_id = session['user_id']
    conexao, cursor = ini_conexao()

    try:
        senha_atual = (request.form.get('senha_atual') or '').strip()
        senha_nova = (request.form.get('senha_nova') or '').strip()
        confirmar = (request.form.get('confirmar_senha') or '').strip()

        # Validação
        erro = validar_campos_senha(senha_atual, senha_nova, confirmar)
        if erro:
            return jsonify({'success': False, 'error': erro}), 400

        service = ConfigService(conexao, cursor)
        senha_hash = service.buscar_senha(usuario_id)

        if not senha_hash or not verificar_senha(senha_hash, senha_atual):
            return jsonify({'success': False, 'error': 'Senha atual incorreta.'}), 400

        nova_hash = criptografar_senha(senha_nova)
        service.atualizar_senha(usuario_id, nova_hash)

        conexao.commit()

        return jsonify({
            'success': True,
            'message': 'Senha alterada com sucesso!',
        }), 200

    except Exception as e:
        conexao.rollback()
        logger.exception(f"Erro ao alterar senha usuario_id={usuario_id}")
        return jsonify({'success': False, 'error': 'Erro interno.'}), 500