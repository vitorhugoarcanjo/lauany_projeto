"""PAINEL DO USUÁRIO — View"""

from flask import render_template, session
from rotas.middleware.autenticacao import login_required
from utils.database.conexao_global import ini_conexao

from .services.services_painel import PainelService


@login_required
def ini_painel():
    """Tela inicial do painel (pós-login)"""
    usuario_id = session['user_id']

    conexao, cursor = ini_conexao()
    service = PainelService(conexao, cursor)

    usuario = service.buscar_usuario(usuario_id)
    perfil = service.buscar_perfil(usuario_id)
    stats = service.buscar_estatisticas(usuario_id)
    ultimos_links = service.buscar_ultimos_links(usuario_id, limite=5)

    return render_template(
        'pasta_painel/tela_painel.html.jinja',
        usuario=usuario,
        perfil=perfil,
        stats=stats,
        ultimos_links=ultimos_links,
    )