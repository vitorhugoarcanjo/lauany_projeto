"""MÓDULO PÚBLICO — Padrão 2099"""

from flask import Blueprint

bp_publico = Blueprint('publico', __name__)

from .publico import pagina_publica

bp_publico.add_url_rule(
    '/<username>',
    view_func=pagina_publica,
    endpoint='pagina_publica',
    methods=['GET']
)