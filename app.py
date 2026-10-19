# app.py
"""ARQUIVO PRINCIPAL — MeuLinks"""

from dotenv import load_dotenv
import os
load_dotenv()

import hashlib
from datetime import timedelta
from flask import Flask, redirect, url_for
from werkzeug.middleware.proxy_fix import ProxyFix

import logging
logging.basicConfig(
    level=logging.DEBUG if os.getenv('FLASK_ENV') == 'development' else logging.INFO
)

from config.database import criar_todas_tabelas
from config.imports_rotas import logica_imports
from utils.database.conexao_global import init_conexao



app = Flask(__name__)

# BANCO DE DADOS
init_conexao(app)

# PROXY (Nginx)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# ROTAS
logica_imports(app)

# SECRET
app.secret_key = os.getenv('SECRET_KEY')

# SESSÃO
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=240)


# CACHE DE ESTÁTICOS
STATIC_VERSION_CACHE = {}
VERSAO_EXTRA = "1"

@app.context_processor
def inject_global_contexts():
    def static_v(filename):
        if filename in STATIC_VERSION_CACHE:
            return url_for('static', filename=filename, v=STATIC_VERSION_CACHE[filename] + VERSAO_EXTRA)

        file_path = os.path.join(app.static_folder, filename)
        try:
            with open(file_path, 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()[:10]
                version = file_hash
        except (OSError, IOError):
            version = str(int(os.path.getmtime(file_path))) if os.path.exists(file_path) else '1'

        STATIC_VERSION_CACHE[filename] = version
        return url_for('static', filename=filename, v=version + VERSAO_EXTRA)

    return {
        'static_v': static_v,
        'versao_sistema': '1.0.1',
    }

@app.route('/')
def ini_app():
    """Redireciona pra login (por enquanto)."""
    return redirect(url_for('login.validar_login'))

if __name__ == '__main__':
    with app.app_context():
        criar_todas_tabelas()
    app.run(host='0.0.0.0', port=5000, debug=True)