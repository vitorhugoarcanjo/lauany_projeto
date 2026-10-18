"""SUB-MÓDULO PERFIL — Painel"""

from flask import Blueprint

bp_perfil = Blueprint('perfil', __name__)

from .perfil import (
    tela_perfil,
    salvar_perfil,
    verificar_username_perfil,
)

bp_perfil.add_url_rule('/', view_func=tela_perfil, endpoint='tela_perfil', methods=['GET'])
bp_perfil.add_url_rule('/salvar', view_func=salvar_perfil, endpoint='salvar_perfil', methods=['POST'])
bp_perfil.add_url_rule('/verificar-username/<username>', view_func=verificar_username_perfil, endpoint='verificar_username_perfil', methods=['GET'])