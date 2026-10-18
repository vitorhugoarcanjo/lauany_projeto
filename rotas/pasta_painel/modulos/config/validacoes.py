"""CONFIG — Validações"""

import re

def validar_senha_atual(senha):
    if not senha:
        return 'Preencha a senha atual.'
    return None

def validar_senha_nova(senha_nova, confirmar):
    if not senha_nova:
        return 'Preencha a nova senha.'
    if not confirmar:
        return 'Confirme a nova senha.'
    if senha_nova != confirmar:
        return 'As senhas não coincidem.'
    if len(senha_nova) < 6:
        return 'Senha deve ter no mínimo 6 caracteres.'
    return None

def validar_campos_senha(senha_atual, senha_nova, confirmar):
    erro = validar_senha_atual(senha_atual)
    if erro:
        return erro
    return validar_senha_nova(senha_nova, confirmar)