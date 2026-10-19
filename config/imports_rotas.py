# config\imports_rotas.py
"""ARQUIVO IMPORTS DE ROTAS"""

# LOGIN
from rotas.pasta_login.pasta_acesso_login.logica_login import bp_login
from rotas.pasta_login.recuperar_senha.recuperar_senha import bp_recuperar
from rotas.pasta_login.pasta_cadastre_se.tela_cadastre_se import bp_cadastre_se

# PAINEL (com os sub-módulos dentro)
from rotas.pasta_painel import bp_painel

# LINKS
from rotas.pasta_links import bp_links

# AUDITORIA
from rotas.auditoria_geral import bp_auditoria

# PÚBLICO
from rotas.pasta_publico import bp_publico

# MASTER
from rotas.pasta_master import bp_master

# ===== JINJA GLOBALS (escala visual) =====
from utils.config import escala

def logica_imports(app):
    app.register_blueprint(bp_login, url_prefix="/login")
    app.register_blueprint(bp_recuperar, url_prefix="/recuperar")
    app.register_blueprint(bp_cadastre_se, url_prefix="/cadastre_se")

    # PAINEL (com perfil, aparência e config dentro)
    app.register_blueprint(bp_painel, url_prefix="/painel")

    # LINKS
    app.register_blueprint(bp_links, url_prefix="/links")

    # AUDITORIA
    app.register_blueprint(bp_auditoria, url_prefix="/auditoria")

    # PÚBLICO (último, sem prefixo = rotas na raiz)
    app.register_blueprint(bp_publico)

    # MASTER
    app.register_blueprint(bp_master, url_prefix="/master")

    # ===== JINJA GLOBALS (registro único, mesmo lugar) =====
    escala.registrar(app)

