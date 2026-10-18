"""PÁGINA PÚBLICA — View"""

import logging
from flask import render_template, abort

from rotas.pasta_publico.services.services_publico import PublicoService
from utils.database.conexao_global import ini_conexao

logger = logging.getLogger(__name__)


def pagina_publica(username):
    """View da página pública."""
    conexao, cursor = ini_conexao()

    service = PublicoService(conexao, cursor)
    perfil = service.buscar_perfil_publico(username)

    if not perfil or not perfil.get('ativo'):
        abort(404)

    return render_template(
        'pasta_publico/tela_publica.html.jinja',
        perfil=perfil,
    )