from rotas.tela_principal import bp_tela_principal

def import_blueprints(app):
    app.register_blueprint(bp_tela_principal)