"""MÓDULO MASTER — Painel de monitoramento (só você)"""

from flask import Blueprint

bp_master = Blueprint('master', __name__)

from .master import dashboard_master

bp_master.add_url_rule('/', view_func=dashboard_master, endpoint='dashboard', methods=['GET'])