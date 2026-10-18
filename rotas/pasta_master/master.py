"""MASTER — View"""

import logging
from flask import render_template

from rotas.middleware.autenticacao import login_required
from utils.database.conexao_global import ini_conexao

from .services import MasterService
from .validacoes import master_required

logger = logging.getLogger(__name__)


@login_required
@master_required
def dashboard_master():
    """Dashboard master (só você)."""
    conexao, cursor = ini_conexao()
    service = MasterService(conexao, cursor)

    stats = service.buscar_estatisticas_gerais()
    usuarios = service.buscar_usuarios_com_stats()

    return render_template(
        'pasta_master/dashboard.html.jinja',
        stats=stats,
        usuarios=usuarios,
    )