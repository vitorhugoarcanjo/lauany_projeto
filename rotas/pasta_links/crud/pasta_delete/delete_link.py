"""INATIVAR LINK (soft delete) — View"""

import logging
import json
from flask import session, render_template, make_response

from rotas.middleware.autenticacao import login_required
from rotas.auditoria_geral.pasta_links.services_auditoria import AuditoriaService
from utils.database.conexao_global import ini_conexao

from .services import InativarLinkService

logger = logging.getLogger(__name__)


@login_required
def inativar_link_modal(link_id):
    """Retorna o HTML do modal de confirmação"""
    usuario_id = session.get('user_id')
    conexao, cursor = ini_conexao()

    link = InativarLinkService.buscar_link(cursor, link_id, usuario_id)
    if not link:
        return '', 404

    return render_template(
        'pasta_links/modais/modal_excluir_link.html.jinja',
        link=link,
    )


@login_required
def inativar_link_view(link_id):
    """Inativa (soft delete) um link"""
    usuario_id = session.get('user_id')
    conexao, cursor = ini_conexao()

    try:
        link = InativarLinkService.buscar_link(cursor, link_id, usuario_id)
        if not link:
            conexao.close()
            return '', 404

        InativarLinkService.inativar_link(cursor, link_id, usuario_id)

        AuditoriaService.registrar(
            link_id=link_id,
            acao='inativado',
            campo_alterado='ativo',
            valor_antigo='1',
            valor_novo='0',
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
            'linkInativado': {'message': f'"{link["titulo"]}" inativado!'}
        })
        return resp

    except Exception as e:
        conexao.rollback()
        logger.exception(f"Erro ao inativar link usuario_id={usuario_id} link_id={link_id}")
        conexao.close()
        return '', 500