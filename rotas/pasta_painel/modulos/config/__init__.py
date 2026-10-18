"""SUB-MÓDULO CONFIGURAÇÕES — Painel"""

from flask import Blueprint

bp_config = Blueprint('config_painel', __name__)

from .config import (
    tela_config,
    alterar_senha,
)

bp_config.add_url_rule('/', view_func=tela_config, endpoint='tela_config', methods=['GET'])
bp_config.add_url_rule('/alterar-senha', view_func=alterar_senha, endpoint='alterar_senha', methods=['POST'])