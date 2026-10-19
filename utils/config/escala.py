"""Expõe a escala visual pros templates Jinja."""
from rotas.pasta_painel.services.escala_visual import (
    resolver, vars_para_style, resolver_meta, tabela_js, TAMANHOS,
)


def registrar(app):
    app.jinja_env.globals["escala_vars"]       = resolver
    app.jinja_env.globals["escala_vars_style"] = vars_para_style
    app.jinja_env.globals["escala_meta"]       = resolver_meta
    app.jinja_env.globals["escala_tabela"]     = tabela_js
    app.jinja_env.globals["escala_tamanhos"]   = TAMANHOS