"""PASTA DELETE - Registro de rotas"""

from flask import Blueprint

bp_delete = Blueprint('delete_links', __name__)

from .delete_link import inativar_link_view, inativar_link_modal

bp_delete.add_url_rule('/modal/<int:link_id>', view_func=inativar_link_modal, methods=['GET'])
bp_delete.add_url_rule('/executar/<int:link_id>', view_func=inativar_link_view, methods=['POST'])