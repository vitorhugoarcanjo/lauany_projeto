"""APARÊNCIA DO PERFIL — View"""

import logging
from flask import render_template, request, session, jsonify

from rotas.middleware.autenticacao import login_required
from rotas.pasta_painel.modulos.aparencia import bp_aparencia
from rotas.pasta_painel.services.services_painel import PainelService
from rotas.pasta_painel.services.template_service import TemplateService
from rotas.pasta_painel.services.aparencia_config_service import AparenciaConfigService
from rotas.pasta_painel.services.aparencia_final_service import AparenciaFinalService
from utils.database.conexao_global import ini_conexao

from .validacoes import validar_template_slug, validar_config

logger = logging.getLogger(__name__)


@bp_aparencia.route('/')
@login_required
def tela_aparencia():
    usuario_id = session['user_id']
    conexao, cursor = ini_conexao()

    aparencia_final_service = AparenciaFinalService(conexao, cursor)
    aparencia_final = aparencia_final_service.buscar_por_usuario(usuario_id)

    if not aparencia_final:
        return 'Perfil não encontrado', 404

    template_service = TemplateService(conexao, cursor)
    templates = template_service.listar(apenas_ativos=True)

    painel_service = PainelService(conexao, cursor)
    perfil_visual = painel_service.buscar_perfil_visual(usuario_id)

    return render_template(
        'pasta_painel/modulos/aparencia/tela_aparencia.html.jinja',
        aparencia=aparencia_final,
        templates=templates,
        perfil=perfil_visual,
    )


@bp_aparencia.route('/salvar', methods=['POST'])
@login_required
def salvar_aparencia():
    usuario_id = session['user_id']
    conexao, cursor = ini_conexao()

    try:
        payload = request.json or {}

        template_slug = validar_template_slug(payload.get('template_slug') or 'cosmic')

        config_raw = payload.get('config') or {}
        config, erro = validar_config(config_raw)
        if erro:
            return jsonify({'success': False, 'error': erro}), 400

        # Verifica se o template existe (evita FK órfã)
        template_service = TemplateService(conexao, cursor)
        template = template_service.buscar_por_slug(template_slug)
        if not template:
            return jsonify({
                'success': False,
                'error': f'Template "{template_slug}" não encontrado.',
            }), 400

        aparencia_config_service = AparenciaConfigService(conexao, cursor)
        aparencia_config_service.salvar(usuario_id, template_slug, config)

        conexao.commit()

        return jsonify({
            'success': True,
            'message': 'Aparência atualizada!',
        }), 200

    except Exception as e:
        conexao.rollback()
        logger.exception(f"Erro ao salvar aparência usuario_id={usuario_id}")
        return jsonify({
            'success': False,
            'error': 'Erro interno.',
            'details': str(e),
        }), 500