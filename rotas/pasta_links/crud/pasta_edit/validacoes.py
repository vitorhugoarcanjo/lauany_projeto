# rotas\pasta_links\crud\pasta_edit\validacoes.py
"""EDITAR LINK — Validações"""


def validar_dados_edicao(dados):
    """Valida os dados antes de editar"""
    erros = []

    # 1. Título
    titulo = str(dados.get('titulo') or '').strip()
    if not titulo:
        erros.append({'campo': 'titulo', 'mensagem': 'Título é obrigatório'})
    elif len(titulo) > 100:
        erros.append({'campo': 'titulo', 'mensagem': 'Título deve ter no máximo 100 caracteres'})

    # 2. URL
    url = str(dados.get('url') or '').strip()
    if not url:
        erros.append({'campo': 'url', 'mensagem': 'URL é obrigatória'})
    elif not (url.startswith('http://') or url.startswith('https://') or url.startswith('mailto:') or url.startswith('tel:')):
        erros.append({'campo': 'url', 'mensagem': 'URL deve começar com http://, https://, mailto: ou tel:'})
    elif len(url) > 500:
        erros.append({'campo': 'url', 'mensagem': 'URL deve ter no máximo 500 caracteres'})

    # 3. Ícone
    icone = str(dados.get('icone') or '').strip()
    if icone and len(icone) > 50:
        erros.append({'campo': 'icone', 'mensagem': 'Ícone deve ter no máximo 50 caracteres'})

    # 4. Descrição
    descricao = str(dados.get('descricao') or '').strip()
    if len(descricao) > 255:
        erros.append({'campo': 'descricao', 'mensagem': 'Descrição deve ter no máximo 255 caracteres'})

    # 5. Ordem
    try:
        ordem = int(dados.get('ordem', 0))
        if ordem < 0 or ordem > 9999:
            erros.append({'campo': 'ordem', 'mensagem': 'Ordem deve estar entre 0 e 9999'})
    except (ValueError, TypeError):
        erros.append({'campo': 'ordem', 'mensagem': 'Ordem inválida'})

    return erros