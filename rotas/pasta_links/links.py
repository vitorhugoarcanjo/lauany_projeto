"""LINKS — View principal"""

import logging
from flask import render_template, session, request, redirect, url_for

from rotas.middleware.autenticacao import login_required
from utils.database.conexao_global import ini_conexao

from .filters import LinksFilters
from .services.services_links import LinksServices
from .formatters import LinksFormatters

logger = logging.getLogger(__name__)


@login_required
def ini_links():
    """Página principal de gerenciamento de links"""
    usuario_id = session['user_id']
    is_htmx = request.headers.get('HX-Request') == 'true'

    if request.method == 'POST':
        LinksFilters.salvar_filtros_post(request, session)

    filtros = LinksFilters.recuperar_filtros(session)

    try:
        conexao, cursor = ini_conexao()
        service = LinksServices(conexao, cursor)
        links_raw = service.buscar_links(usuario_id, filtros)
        links = LinksFormatters.formatar_links(links_raw)
    except Exception as e:
        logger.exception(f"Erro ao buscar links usuario_id={usuario_id}")
        links = []

    if is_htmx:
        return render_template(
            'pasta_links/_tabela_links.html.jinja',
            links=links,
            descricao=filtros['descricao'],
            mostrar_inativas=filtros['mostrar_inativas'],
        )

    return render_template(
        'pasta_links/tela_links.html.jinja',
        links=links,
        descricao=filtros['descricao'],
        mostrar_inativas=filtros['mostrar_inativas'],
        user_nome=session.get('user_nome'),
    )


@login_required
def limpar_filtros():
    LinksFilters.limpar_filtros(session)
    return redirect(url_for('links.ini_links'))