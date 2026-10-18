"""
BUILD PAINEL — Combina CSS/JS do módulo Painel (com sub-módulos).
Gera:
    static/css/modules/pasta_painel/painel.min.css
    static/js/modules/pasta_painel/painel.min.js
"""

import os
import re
from datetime import datetime


CSS_FILES = [
    # Painel principal
    'static/css/modules/pasta_painel/painel.css',

    # Sub-módulos
    'static/css/modules/pasta_painel/modulos/perfil/perfil.css',
    'static/css/modules/pasta_painel/modulos/aparencia/aparencia.css',
    'static/css/modules/pasta_painel/modulos/config/config.css',
]

JS_FILES = [
    # Painel principal
    'static/js/modules/pasta_painel/painel.js',

    # Sub-módulos
    'static/js/modules/pasta_painel/modulos/perfil/perfil.js',
    'static/js/modules/pasta_painel/modulos/aparencia/aparencia.js',
    'static/js/modules/pasta_painel/modulos/config/config.js',
]


def resolve_imports(content, file_path):
    pattern = r'@import\s+url\([\'"]?([^\'"]+)[\'"]?\);?'
    def replace_import(match):
        import_path = match.group(1)
        if import_path.startswith('/static/'):
            import_path = import_path[8:]
        elif import_path.startswith('static/'):
            import_path = import_path[7:]
        full_path = os.path.join('static', import_path)
        if os.path.exists(full_path):
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read()
        return ''
    return re.sub(pattern, replace_import, content, flags=re.IGNORECASE)


def combinar_css():
    output = 'static/css/modules/pasta_painel/painel.min.css'
    os.makedirs(os.path.dirname(output), exist_ok=True)

    print('\n📦 Combinando CSS PAINEL...')
    with open(output, 'w', encoding='utf-8') as out:
        out.write(f'/* PAINEL — {datetime.now().strftime("%d/%m/%Y %H:%M")} */\n\n')
        for file in CSS_FILES:
            if os.path.exists(file):
                nome = os.path.basename(file)
                out.write(f'/* ===== {nome} ===== */\n')
                with open(file, 'r', encoding='utf-8') as f:
                    content = resolve_imports(f.read(), file)
                    out.write(content)
                    out.write('\n\n')
                print(f'  ✅ {nome}')
            else:
                print(f'  ⚠️  {file} não encontrado')


def combinar_js():
    output = 'static/js/modules/pasta_painel/painel.min.js'
    os.makedirs(os.path.dirname(output), exist_ok=True)

    print('\n📦 Combinando JS PAINEL...')
    with open(output, 'w', encoding='utf-8') as out:
        out.write(f'// PAINEL — {datetime.now().strftime("%d/%m/%Y %H:%M")}\n\n')
        for file in JS_FILES:
            if os.path.exists(file):
                nome = os.path.basename(file)
                out.write(f'// ==== {nome} ====\n')
                with open(file, 'r', encoding='utf-8') as f:
                    out.write(f.read())
                    out.write('\n\n')
                print(f'  ✅ {nome}')
            else:
                print(f'  ⚠️  {file} não encontrado')


def main():
    print('=' * 60)
    print('🏗️  BUILD PAINEL — MeuLinks')
    print('=' * 60)
    combinar_css()
    combinar_js()
    print('\n' + '=' * 60)
    print('✅ PRONTO!')
    print('   📄 static/css/modules/pasta_painel/painel.min.css')
    print('   📄 static/js/modules/pasta_painel/painel.min.js')
    print('=' * 60)


if __name__ == '__main__':
    main()