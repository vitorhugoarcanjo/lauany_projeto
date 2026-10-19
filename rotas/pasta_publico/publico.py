"""PÁGINA PÚBLICA — View"""
import logging
from flask import render_template, abort

from rotas.pasta_publico import bp_publico
from utils.database.conexao_global import ini_conexao
from .services import PublicoService

logger = logging.getLogger(__name__)


@bp_publico.route('/<username>')
def pagina_publica(username):
    conexao, cursor = ini_conexao()
    service = PublicoService(conexao, cursor)
    perfil = service.buscar_perfil_publico(username)
    if not perfil:
        abort(404)

    return render_template('pasta_publico/tela_publica.html.jinja', perfil=perfil)