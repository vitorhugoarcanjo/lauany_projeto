# config/database.py
"""Cria todas as tabelas do sistema"""

from utils.database.conexao_global import get_conexao_direct
from config.indices_automatico import criar_indices

# TABELA DE USUÁRIOS
from rotas.pasta_login.tabelas.usuarios import tabela_usuarios

# TABELA DE TEMPLATES (catálogo)
from rotas.pasta_painel.tabelas.templates import tabela_templates

# TABELA DE PERFIS
from rotas.pasta_painel.tabelas.perfis import tabela_perfis

# SEED DOS TEMPLATES PADRÃO
from rotas.pasta_painel.templates_personalizados.templates_padroes import popular_templates_padroes

# TABELA DE LINKS
from rotas.pasta_links.tabelas.links import tabela_links

# TABELA DE AUDITORIA
from rotas.auditoria_geral.pasta_links.tabela import tabela_auditoria_links

# TABELAS MASTER - PERMISSOES
from rotas.pasta_master.tabelas.permissoes import tabela_permissoes
from rotas.pasta_master.tabelas.usuarios_master import tabela_usuarios_master


def criar_todas_tabelas():
    conexao = get_conexao_direct()
    cursor = conexao.cursor()

    try:
        # ==================== TABELAS PRINCIPAIS ====================
        tabela_usuarios(cursor)

        # ⚠️ ORDEM: templates ANTES de perfis (perfis tem FK pra templates)
        tabela_templates(cursor)
        tabela_perfis(cursor)

        tabela_links(cursor)

        # ==================== AUDITORIA ====================
        tabela_auditoria_links(cursor)

        # ==================== ÍNDICES + FK ====================
        criar_indices(cursor)

        # ==================== MASTER / PERMISSÕES ====================
        tabela_usuarios_master(cursor)
        tabela_permissoes(cursor)

        # ==================== SEED DE TEMPLATES ====================
        # ⚠️ Roda DEPOIS de tabela_templates e ANTES de qualquer INSERT em perfis
        popular_templates_padroes(cursor)

        print('✅ Tabelas criadas com sucesso!')
        conexao.commit()

    except Exception as e:
        conexao.rollback()
        print(f'❌ Erro ao criar tabelas: {e}')
        raise

    finally:
        cursor.close()
        conexao.close()