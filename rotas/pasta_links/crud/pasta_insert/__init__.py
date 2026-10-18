# rotas\pasta_links\crud\pasta_insert\__init__.py
"""PASTA INSERT - Registro de rotas"""

from flask import Blueprint

bp_insert = Blueprint('insert_links', __name__)

from .insert_link import novo_link_modal, salvar_novo_link

bp_insert.add_url_rule('/modal', view_func=novo_link_modal, methods=['GET'])
bp_insert.add_url_rule('/salvar', view_func=salvar_novo_link, methods=['POST'])