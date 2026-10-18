"""MÓDULO LINKS — Blueprint principal"""

from flask import Blueprint

bp_links = Blueprint('links', __name__)

# IMPORTS das views principais
from .links import ini_links, limpar_filtros

# IMPORTS dos CRUDs
from .crud.pasta_insert import bp_insert
from .crud.pasta_edit import bp_edit
from .crud.pasta_delete import bp_delete
from .crud.pasta_reativar import bp_reativar

# ==========================================================
# ROTAS PRINCIPAIS
# ==========================================================
bp_links.add_url_rule('/', view_func=ini_links, methods=['GET', 'POST'])
bp_links.add_url_rule('/limpar_filtros', view_func=limpar_filtros)

# ==========================================================
# ROTAS DE CRUD (sub-blueprints)
# ==========================================================
bp_links.register_blueprint(bp_insert, url_prefix='/novo_link')
bp_links.register_blueprint(bp_edit, url_prefix='/edit_link')
bp_links.register_blueprint(bp_delete, url_prefix='/excluir_link')
bp_links.register_blueprint(bp_reativar, url_prefix='/reativar_link')