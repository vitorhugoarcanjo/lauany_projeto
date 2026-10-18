"""APARÊNCIA DO PERFIL — View"""

import logging
from flask import render_template, request, session, jsonify

from rotas.middleware.autenticacao import login_required
from rotas.pasta_painel.modulos.aparencia import bp_aparencia
from rotas.pasta_painel.services.services_painel import PainelService
from utils.database.conexao_global import ini_conexao

from .services import AparenciaService
from .validacoes import (
    validar_tema,
    validar_fonte,
    validar_estilo_botao,
    validar_template,
    validar_tamanho_foto,
    validar_tamanho_link,
    validar_espacamento,
    validar_borda,
    validar_hover,
    validar_animacao,
    validar_cores,
)

logger = logging.getLogger(__name__)


@bp_aparencia.route('/')
@login_required
def tela_aparencia():
    usuario_id = session['user_id']
    conexao, cursor = ini_conexao()

    aparencia_service = AparenciaService(conexao, cursor)
    aparencia = aparencia_service.buscar_aparencia(usuario_id)

    if not aparencia:
        return 'Perfil não encontrado', 404

    painel_service = PainelService(conexao, cursor)
    perfil_visual = painel_service.buscar_perfil_visual(usuario_id)

    return render_template(
        'pasta_painel/modulos/aparencia/tela_aparencia.html.jinja',
        aparencia=aparencia,
        perfil=perfil_visual,
    )


@bp_aparencia.route('/salvar', methods=['POST'])
@login_required
def salvar_aparencia():
    usuario_id = session['user_id']
    conexao, cursor = ini_conexao()

    try:
        # Pega e valida cada campo
        tema = validar_tema((request.form.get('tema') or 'claro').strip())
        fonte = validar_fonte((request.form.get('fonte') or 'padrao').strip())
        estilo_botao = validar_estilo_botao((request.form.get('estilo_botao') or 'arredondado').strip())
        template = validar_template((request.form.get('template') or 'cosmic').strip())
        tamanho_foto = validar_tamanho_foto((request.form.get('tamanho_foto') or 'medio').strip())
        tamanho_link = validar_tamanho_link((request.form.get('tamanho_link') or 'medio').strip())
        espacamento_links = validar_espacamento((request.form.get('espacamento_links') or 'medio').strip())
        borda_link = validar_borda((request.form.get('borda_link') or 'media').strip())
        hover_efeito = validar_hover((request.form.get('hover_efeito') or 'subir').strip())
        animacao_entrada = validar_animacao((request.form.get('animacao_entrada') or 'fade').strip())

        cor_primaria = (request.form.get('cor_primaria') or '').strip()
        cor_secundaria = (request.form.get('cor_secundaria') or '').strip()
        cor_fundo = (request.form.get('cor_fundo') or '').strip()
        cor_texto = (request.form.get('cor_texto') or '').strip()
        cor_botao = (request.form.get('cor_botao') or '').strip()

        erro_cores = validar_cores(cor_primaria, cor_secundaria, cor_fundo, cor_texto, cor_botao)
        if erro_cores:
            return jsonify({'success': False, 'error': erro_cores}), 400

        service = AparenciaService(conexao, cursor)
        service.atualizar_aparencia(
            usuario_id=usuario_id,
            tema=tema,
            cor_primaria=cor_primaria or None,
            cor_secundaria=cor_secundaria or None,
            cor_fundo=cor_fundo or None,
            cor_texto=cor_texto or None,
            cor_botao=cor_botao or None,
            fonte=fonte,
            estilo_botao=estilo_botao,
            template=template,
            tamanho_foto=tamanho_foto,
            tamanho_link=tamanho_link,
            espacamento_links=espacamento_links,
            borda_link=borda_link,
            hover_efeito=hover_efeito,
            animacao_entrada=animacao_entrada,
        )

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