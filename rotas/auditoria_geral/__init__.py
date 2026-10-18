# rotas/auditoria_geral/__init__.py
"""AUDITORIA GERAL — Blueprint único"""

from flask import Blueprint

bp_auditoria = Blueprint('auditoria', __name__)

# Imports das views (por módulo)
from .pasta_links.logica_auditoria import historico_links

# Rotas
bp_auditoria.add_url_rule(
    '/link/<int:link_seq>',
    view_func=historico_links,
    endpoint='historico_links'
)