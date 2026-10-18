"""
BUILD PÚBLICO — Combina CSS/JS da página pública.
Gera:
    static/css/modules/pasta_publico/publico.min.css
    static/js/modules/pasta_publico/publico.min.js
"""

import os
import re
from datetime import datetime


CSS_FILES = [
    'static/css/modules/pasta_publico/publico.css',
    'static/css/components/templates.css',
]

JS_FILES = [
    'static/js/modules/pasta_publico/publico.js',
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
            print(f'    📄 Resolvendo @import: {import_path}')
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read()
        print(f'    ⚠️ @import não encontrado: {import_path}')
        return ''

    return re.sub(pattern, replace_import, content, flags=re.IGNORECASE)


def combinar_css():
    output = 'static/css/modules/pasta_publico/publico.min.css'
    os.makedirs(os.path.dirname(output), exist_ok=True)

    print('\n📦 Combinando CSS PÚBLICO...')
    with open(output, 'w', encoding='utf-8') as out:
        out.write(f'/* PÚBLICO — {datetime.now().strftime("%d/%m/%Y %H:%M")} */\n\n')
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
    output = 'static/js/modules/pasta_publico/publico.min.js'
    os.makedirs(os.path.dirname(output), exist_ok=True)

    print('\n📦 Combinando JS PÚBLICO...')
    with open(output, 'w', encoding='utf-8') as out:
        out.write(f'// PÚBLICO — {datetime.now().strftime("%d/%m/%Y %H:%M")}\n\n')
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
    print('🏗️  BUILD PÚBLICO — MeuLinks')
    print('=' * 60)

    combinar_css()
    combinar_js()

    print('\n' + '=' * 60)
    print('✅ PRONTO! Arquivos gerados:')
    print('   📄 static/css/modules/pasta_publico/publico.min.css')
    print('   📄 static/js/modules/pasta_publico/publico.min.js')
    print('=' * 60)


if __name__ == '__main__':
    main()