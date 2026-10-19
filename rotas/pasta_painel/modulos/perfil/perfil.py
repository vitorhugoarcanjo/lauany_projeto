"""PERFIL DO USUÁRIO — View"""

import os
import time
import logging
from flask import render_template, request, session, jsonify, current_app

from rotas.middleware.autenticacao import login_required
from rotas.pasta_painel.modulos.perfil import bp_perfil
from rotas.pasta_painel.services.services_painel import PainelService
from utils.database.conexao_global import ini_conexao

from .services import PerfilService
from .validacoes import (
    validar_username,
    validar_foto,
    validar_foto_posicao,
    validar_campos_texto,
    extensao_permitida,
)

logger = logging.getLogger(__name__)


def _salvar_foto(arquivo, usuario_id):
    """Salva foto com nome ÚNICO (timestamp) pra não sobrescrever."""
    ext = arquivo.filename.rsplit('.', 1)[-1].lower()
    timestamp = int(time.time())
    nome = f'perfil_{usuario_id}_{timestamp}.{ext}'

    pasta = os.path.join(current_app.static_folder, 'images', 'perfis')
    os.makedirs(pasta, exist_ok=True)

    caminho_absoluto = os.path.join(pasta, nome)
    arquivo.save(caminho_absoluto)

    return f'images/perfis/{nome}'


def _remover_foto_antiga(perfil):
    """Remove a foto antiga do disco (só se for diferente da nova)."""
    if not perfil or not perfil.get('foto'):
        return
    caminho = os.path.join(current_app.static_folder, perfil['foto'])
    try:
        if os.path.exists(caminho):
            os.remove(caminho)
            logger.info(f"Foto antiga removida: {perfil['foto']}")
    except Exception as e:
        logger.warning(f"Falha ao remover foto antiga: {e}")


# ==========================================================
# VIEWS
# ==========================================================
@bp_perfil.route('/')
@login_required
def tela_perfil():
    usuario_id = session['user_id']
    conexao, cursor = ini_conexao()

    service = PainelService(conexao, cursor)
    usuario = service.buscar_usuario(usuario_id)
    perfil_visual = service.buscar_perfil_visual(usuario_id)

    if not usuario:
        return 'Usuário não encontrado', 404

    return render_template(
        'pasta_painel/modulos/perfil/tela_perfil.html.jinja',
        usuario=usuario,
        perfil=perfil_visual,
    )


@bp_perfil.route('/salvar', methods=['POST'])
@login_required
def salvar_perfil():
    usuario_id = session['user_id']
    conexao, cursor = ini_conexao()

    try:
        username = (request.form.get('username') or '').strip().lower()
        nome_exibicao = (request.form.get('nome_exibicao') or '').strip()
        bio = (request.form.get('bio') or '').strip()
        titulo_pagina = (request.form.get('titulo_pagina') or '').strip()
        meta_descricao = (request.form.get('meta_descricao') or '').strip()
        foto = request.files.get('foto')
        remover_foto = (request.form.get('remover_foto') or '0').strip() == '1'
        foto_posicao = validar_foto_posicao(request.form.get('foto_posicao'))

        # Validações
        valido, msg = validar_username(username)
        if not valido:
            return jsonify({'success': False, 'error': msg}), 400

        service = PerfilService(conexao, cursor)
        if not service.username_disponivel(username, usuario_id):
            return jsonify({'success': False, 'error': 'Este username já está em uso.'}), 400

        erro_campos = validar_campos_texto(nome_exibicao, bio, titulo_pagina, meta_descricao)
        if erro_campos:
            return jsonify({'success': False, 'error': erro_campos}), 400

        perfil_atual = service.buscar_perfil(usuario_id)

        caminho_foto = None
        acao_foto = 'manter'

        if foto and foto.filename:
            valido, erro = validar_foto(foto)
            if not valido:
                return jsonify({'success': False, 'error': erro}), 400
            caminho_foto = _salvar_foto(foto, usuario_id)
            acao_foto = 'atualizar'
        elif remover_foto:
            acao_foto = 'remover'

        service.atualizar_perfil(
            usuario_id=usuario_id,
            username=username,
            nome_exibicao=nome_exibicao or None,
            bio=bio or None,
            titulo_pagina=titulo_pagina or None,
            meta_descricao=meta_descricao or None,
            foto=caminho_foto,
            foto_posicao=foto_posicao,
            acao_foto=acao_foto,
        )

        conexao.commit()

        if acao_foto == 'atualizar' and perfil_atual:
            if perfil_atual.get('foto') and perfil_atual['foto'] != caminho_foto:
                _remover_foto_antiga(perfil_atual)
        elif acao_foto == 'remover':
            _remover_foto_antiga(perfil_atual)

        return jsonify({
            'success': True,
            'message': 'Perfil atualizado!',
            'username': username,
        }), 200

    except Exception as e:
        conexao.rollback()
        logger.exception(f"Erro ao salvar perfil usuario_id={usuario_id}")
        return jsonify({
            'success': False,
            'error': 'Erro interno.',
            'details': str(e),
        }), 500


@bp_perfil.route('/verificar-username/<username>')
@login_required
def verificar_username_perfil(username):
    usuario_id = session['user_id']
    username = username.strip().lower()

    valido, msg = validar_username(username)
    if not valido:
        return jsonify({'disponivel': False, 'message': msg}), 200

    conexao, cursor = ini_conexao()
    service = PerfilService(conexao, cursor)
    disponivel = service.username_disponivel(username, usuario_id)

    return jsonify({
        'disponivel': disponivel,
        'message': 'Disponível!' if disponivel else 'Já está em uso.',
    }), 200