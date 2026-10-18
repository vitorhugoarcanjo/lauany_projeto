# rotas/middleware/autenticacao.py

from flask import session, redirect, url_for
from functools import wraps


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('login.validar_login'))
        return f(*args, **kwargs)
    return decorated