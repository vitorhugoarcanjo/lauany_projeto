# rotas\pasta_links\crud\pasta_reativar\__init__.py
"""PASTA REATIVAR - Registro de rotas"""

from flask import Blueprint

bp_reativar = Blueprint('reativar_links', __name__)

from .reativar_link import reativar_link_view, reativar_link_modal

bp_reativar.add_url_rule('/modal/<int:link_id>', view_func=reativar_link_modal, methods=['GET'])
bp_reativar.add_url_rule('/executar/<int:link_id>', view_func=reativar_link_view, methods=['POST'])