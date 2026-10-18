"""REATIVAR LINK — View"""

import logging
import json
from flask import session, render_template, make_response

from rotas.middleware.autenticacao import login_required
from rotas.auditoria_geral.pasta_links.services_auditoria import AuditoriaService
from utils.database.conexao_global import ini_conexao

from .services import ReativarLinkService

logger = logging.getLogger(__name__)


@login_required
def reativar_link_modal(link_id):
    """Retorna o HTML do modal de confirmação"""
    usuario_id = session.get('user_id')
    conexao, cursor = ini_conexao()

    link = ReativarLinkService.buscar_link(cursor, link_id, usuario_id)
    if not link:
        return '', 404

    return render_template(
        'pasta_links/modais/modal_reativar_link.html.jinja',
        link=link,
    )


@login_required
def reativar_link_view(link_id):
    """Reativa um link inativo"""
    usuario_id = session.get('user_id')
    conexao, cursor = ini_conexao()

    try:
        link = ReativarLinkService.buscar_link(cursor, link_id, usuario_id)
        if not link:
            conexao.close()
            return '', 404

        ReativarLinkService.reativar_link(cursor, link_id, usuario_id)

        AuditoriaService.registrar(
            link_id=link_id,
            acao='reativado',
            campo_alterado='ativo',
            valor_antigo='0',
            valor_novo='1',
            conexao=conexao,
        )

        conexao.commit()

        # Rebusca a lista atualizada
        from rotas.pasta_links.services.services_links import LinksServices
        from rotas.pasta_links.formatters import LinksFormatters
        from rotas.pasta_links.filters import LinksFilters

        service = LinksServices(conexao, cursor)
        filtros = LinksFilters.recuperar_filtros(session)
        links_raw = service.buscar_links(usuario_id, filtros)
        links = LinksFormatters.formatar_links(links_raw)

        html = render_template(
            'pasta_links/_tabela_links.html.jinja',
            links=links,
            descricao=filtros.get('descricao', ''),
            mostrar_inativas=filtros.get('mostrar_inativas', '0'),
        )
        conexao.close()

        resp = make_response(html)
        resp.headers['HX-Trigger'] = json.dumps({
            'linkReativado': {'message': f'"{link["titulo"]}" reativado!'}
        })
        return resp

    except Exception as e:
        conexao.rollback()
        logger.exception(f"Erro ao reativar link usuario_id={usuario_id} link_id={link_id}")
        conexao.close()
        return '', 500