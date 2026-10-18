"""LOGOUT — View"""

from flask import redirect, url_for, session
from rotas.middleware.autenticacao import login_required
from rotas.pasta_painel import bp_painel


@bp_painel.route('/logout')
@login_required
def fazer_logout():
    """Limpa sessão e redireciona pro login"""
    session.clear()
    return redirect(url_for('login.validar_login'))