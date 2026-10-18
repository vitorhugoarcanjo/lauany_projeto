# rotas\pasta_links\crud\pasta_edit\__init__.py
"""PASTA EDIT - Registro de rotas"""

from flask import Blueprint

bp_edit = Blueprint('edit_links', __name__)

from .edit_link import editar_link_modal, salvar_edicao_link

bp_edit.add_url_rule('/modal/<int:link_id>', view_func=editar_link_modal, methods=['GET'])
bp_edit.add_url_rule('/salvar/<int:link_id>', view_func=salvar_edicao_link, methods=['POST'])