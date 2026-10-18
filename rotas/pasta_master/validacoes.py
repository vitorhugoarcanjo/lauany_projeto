"""MASTER — Validações"""

from functools import wraps
from flask import session, abort


def master_required(f):
    """Bloqueia quem não é master. Assume que o login já foi validado."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('is_master'):
            abort(403)
        return f(*args, **kwargs)
    return decorated