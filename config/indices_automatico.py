"""ÍNDICES AUTOMÁTICOS — otimização de queries"""

def criar_indices(cursor):
    """Cria índices para otimizar consultas"""
    print("📊 Criando índices...")

    indices = [
        # USUÁRIOS
        ("idx_usuarios_email", "usuarios", "email"),
        ("idx_usuarios_ativo", "usuarios", "ativo"),
        ("idx_usuarios_email_ativo", "usuarios", "email, ativo"),

        # PERFIS
        ("idx_perfis_usuario_id", "perfis", "usuario_id"),
        ("idx_perfis_username", "perfis", "username"),
        ("idx_perfis_username_ativo", "perfis", "username, ativo"),

        # LINKS
        ("idx_links_usuario_id", "links", "usuario_id"),
        ("idx_links_ativo", "links", "ativo"),
        ("idx_links_ordem", "links", "ordem"),
        ("idx_links_usuario_ativo", "links", "usuario_id, ativo"),
        ("idx_links_usuario_ativo_ordem", "links", "usuario_id, ativo, ordem"),
        ("idx_links_usuario_sequencia", "links", "usuario_id, sequencia_links"),

        # AUDITORIA
        ("idx_links_auditoria_link_id", "links_auditoria", "link_id"),
        ("idx_links_auditoria_usuario_id", "links_auditoria", "usuario_id"),
        ("idx_links_auditoria_data_hora", "links_auditoria", "data_hora"),
        ("idx_links_auditoria_acao", "links_auditoria", "acao"),
    ]

    for nome, tabela, colunas in indices:
        try:
            cursor.execute(f"CREATE INDEX IF NOT EXISTS {nome} ON {tabela}({colunas})")
            print(f"  ✅ Índice {nome}")
        except Exception as e:
            print(f"  ⚠️ Erro ao criar {nome}: {e}")

    print("✅ Índices criados/verificados!")