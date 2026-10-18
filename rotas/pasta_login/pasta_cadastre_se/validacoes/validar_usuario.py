"""VALIDAÇÕES DE USUÁRIO"""

from flask import flash
import re


def validar_campos_obrigatorios(nome, telefone, email, senha, confirmar_senha):
    if not nome or not telefone or not email or not senha or not confirmar_senha:
        flash('Falta campos obrigatórios para se cadastrar!', 'warning')
        return False
    return True


def validar_senha_tamanho(senha):
    if len(senha) < 6:
        flash('Senha deve ter no mínimo 6 caracteres', 'error')
        return False
    return True


def validar_confirmacao_senha(senha, confirmar_senha):
    if senha != confirmar_senha:
        flash('As senhas não coincidem!', 'error')
        return False
    return True


def validar_email_formato(email):
    if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        return False
    return True


def validar_email_unico(conexao, email):
    """Verifica se email já existe na tabela usuarios"""
    cursor = conexao.cursor()
    cursor.execute('SELECT id FROM usuarios WHERE email = %s', (email,))
    resultado = cursor.fetchone()

    if resultado:
        flash('E-mail já cadastrado!', 'error')
        return False
    return True


def validar_e_limpar_telefone(telefone):
    """Valida telefone e retorna apenas números"""
    telefone_limpo = re.sub(r'\D', '', telefone)

    if len(telefone_limpo) not in [10, 11]:
        return None

    return telefone_limpo