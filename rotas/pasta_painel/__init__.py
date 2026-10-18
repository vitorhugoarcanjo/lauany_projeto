"""MÓDULO PAINEL — Padrão 2099"""

from flask import Blueprint

bp_painel = Blueprint('painel', __name__)

# ==========================================================
# IMPORTS — Painel principal
# ==========================================================
from .painel import ini_painel
from .logout import fazer_logout

# ==========================================================
# IMPORTS — Sub-módulos
# ==========================================================
from .modulos.perfil import bp_perfil
from .modulos.aparencia import bp_aparencia
from .modulos.config import bp_config


# ==========================================================
# ROTAS DO PAINEL PRINCIPAL
# ==========================================================
bp_painel.add_url_rule('/', view_func=ini_painel, endpoint='ini_painel', methods=['GET'])
bp_painel.add_url_rule('/logout', view_func=fazer_logout, endpoint='logout', methods=['GET'])


# ==========================================================
# REGISTRA SUB-BLUEPRINTS
# ==========================================================
bp_painel.register_blueprint(bp_perfil, url_prefix='/perfil')
bp_painel.register_blueprint(bp_aparencia, url_prefix='/aparencia')
bp_painel.register_blueprint(bp_config, url_prefix='/configuracoes')