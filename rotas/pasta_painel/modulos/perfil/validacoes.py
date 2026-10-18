"""PERFIL — Validações"""

import re

SLUGS_RESERVADOS = {
    'login', 'cadastre_se', 'recuperar', 'painel', 'links', 'meus-links',
    'logout', 'admin', 'static', 'api', 'sobre', 'contato',
    'artigos', 'projetos', 'arquitetura-2099', 'auditoria',
    'meulinks', 'sistema', 'suporte', 'ajuda', 'termos',
    'privacidade', 'config', 'dashboard', 'perfil', 'aparencia',
}

EXTENSOES_PERMITIDAS = {'jpg', 'jpeg', 'png', 'webp'}

FOTO_POSICOES_VALIDAS = {'top', 'center', 'bottom'}


def validar_username(username):
    if not username:
        return False, 'Username é obrigatório.'
    if len(username) < 3:
        return False, 'Username deve ter no mínimo 3 caracteres.'
    if len(username) > 30:
        return False, 'Username deve ter no máximo 30 caracteres.'
    if not re.match(r'^[a-z0-9_]+$', username):
        return False, 'Username só pode ter letras minúsculas, números e _.'
    if username[0] in '0123456789_':
        return False, 'Username deve começar com uma letra.'
    if username in SLUGS_RESERVADOS:
        return False, 'Este username está reservado.'
    return True, None


def extensao_permitida(nome_arquivo):
    ext = nome_arquivo.rsplit('.', 1)[-1].lower() if '.' in nome_arquivo else ''
    return ext in EXTENSOES_PERMITIDAS


def validar_foto(arquivo):
    if not arquivo or not arquivo.filename:
        return None, 'Nenhum arquivo enviado.'
    if not extensao_permitida(arquivo.filename):
        return None, 'Formato inválido. Use JPG, PNG ou WEBP.'
    return True, None


def validar_foto_posicao(posicao):
    """Valida a posição do corte da foto (top/center/bottom)."""
    if not posicao:
        return 'top'
    posicao = posicao.strip().lower()
    return posicao if posicao in FOTO_POSICOES_VALIDAS else 'top'


def validar_campos_texto(nome_exibicao, bio, titulo_pagina, meta_descricao):
    if len(nome_exibicao) > 60:
        return 'Nome de exibição: máx 60 caracteres.'
    if len(bio) > 160:
        return 'Bio: máx 160 caracteres.'
    if len(titulo_pagina) > 100:
        return 'Título: máx 100 caracteres.'
    if len(meta_descricao) > 255:
        return 'Meta descrição: máx 255 caracteres.'
    return None