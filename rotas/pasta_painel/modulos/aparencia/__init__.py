"""SUB-MÓDULO APARÊNCIA — Painel"""

from flask import Blueprint

bp_aparencia = Blueprint('aparencia', __name__)

from .aparencia import (
    tela_aparencia,
    salvar_aparencia,
)

bp_aparencia.add_url_rule('/', view_func=tela_aparencia, endpoint='tela_aparencia', methods=['GET'])
bp_aparencia.add_url_rule('/salvar', view_func=salvar_aparencia, endpoint='salvar_aparencia', methods=['POST'])