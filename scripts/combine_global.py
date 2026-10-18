"""
BUILD GLOBAL — Combina CSS/JS compartilhados por TODAS as páginas.
Gera:
    static/css/global.min.css
    static/js/global.min.js

Uso:
    python scripts/combine_global.py
"""

import os
import re
from datetime import datetime


CSS_FILES = [
    # CORE
    'static/css/core/variaveis.css',
    'static/css/core/reset.css',
    'static/css/core/responsive.css',

    # COMPONENTS
    'static/css/components/botoes.css',
    'static/css/components/forms.css',
    'static/css/components/mockup-celular.css',   # ← NOVO
    'static/css/components/tela-padrao.css',
    'static/css/components/modais.css',
    'static/css/components/notificacoes.css',
    'static/css/components/sidebar.css',
    'static/css/components/footer.css',
]

JS_FILES = [
    # CORE
    'static/js/core/eventos.js',

    # COMPONENTS
    'static/js/components/notificacoes.js',
    'static/js/components/mockup.js',             # ← NOVO
    'static/js/components/modal.js',
    'static/js/components/sidebar.js',
    'static/js/components/tema.js',
]

def resolve_imports(content, file_path):
    """Resolve @import dentro de CSS"""
    pattern = r'@import\s+url\([\'"]?([^\'"]+)[\'"]?\);?'

    def replace_import(match):
        import_path = match.group(1)
        if import_path.startswith('/static/'):
            import_path = import_path[8:]
        elif import_path.startswith('static/'):
            import_path = import_path[7:]

        full_path = os.path.join('static', import_path)
        if os.path.exists(full_path):
            print(f'    📄 Resolvendo @import: {import_path}')
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read()
        print(f'    ⚠️ @import não encontrado: {import_path}')
        return ''

    return re.sub(pattern, replace_import, content, flags=re.IGNORECASE)


def combinar_css():
    output = 'static/css/global.min.css'
    os.makedirs(os.path.dirname(output), exist_ok=True)

    print('\n📦 Combinando CSS GLOBAL...')
    with open(output, 'w', encoding='utf-8') as out:
        out.write(f'/* GLOBAL — {datetime.now().strftime("%d/%m/%Y %H:%M")} */\n\n')
        for file in CSS_FILES:
            if os.path.exists(file):
                nome = os.path.basename(file)
                out.write(f'/* ===== {nome} ===== */\n')
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    content = resolve_imports(content, file)
                    out.write(content)
                    out.write('\n\n')
                print(f'  ✅ {nome}')
            else:
                print(f'  ⚠️  {file} não encontrado')


def combinar_js():
    output = 'static/js/global.min.js'
    os.makedirs(os.path.dirname(output), exist_ok=True)

    print('\n📦 Combinando JS GLOBAL...')
    with open(output, 'w', encoding='utf-8') as out:
        out.write(f'// GLOBAL — {datetime.now().strftime("%d/%m/%Y %H:%M")}\n\n')
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
    print('🏗️  BUILD GLOBAL — MeuLinks')
    print('=' * 60)

    combinar_css()
    combinar_js()

    print('\n' + '=' * 60)
    print('✅ PRONTO! Arquivos gerados:')
    print('   📄 static/css/global.min.css')
    print('   📄 static/js/global.min.js')
    print('=' * 60)


if __name__ == '__main__':
    main()