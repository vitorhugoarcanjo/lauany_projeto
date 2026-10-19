"""ÍNDICES AUTOMÁTICOS — otimização de queries"""


def criar_indices(cursor):
    """Cria índices e constraints para otimizar consultas."""
    print("📊 Criando índices...")

    # ==================== ÍNDICES SIMPLES (B-Tree) ====================
    indices = [
        # USUÁRIOS
        ("idx_usuarios_email", "usuarios", "email"),
        ("idx_usuarios_ativo", "usuarios", "ativo"),
        ("idx_usuarios_email_ativo", "usuarios", "email, ativo"),

        # PERFIS
        ("idx_perfis_usuario_id", "perfis", "usuario_id"),
        ("idx_perfis_username", "perfis", "username"),
        ("idx_perfis_username_ativo", "perfis", "username, ativo"),
        ("idx_perfis_template_slug", "perfis", "template_slug"),

        # TEMPLATES
        ("idx_templates_slug", "templates", "slug"),
        ("idx_templates_categoria", "templates", "categoria"),
        ("idx_templates_ativo", "templates", "ativo"),
        ("idx_templates_ordem", "templates", "ordem"),

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

    # ==================== ÍNDICES GIN (JSONB) ====================
    indices_gin = [
        ("idx_perfis_config", "perfis", "config"),
        ("idx_templates_config", "templates", "config_default"),
    ]

    for nome, tabela, coluna in indices_gin:
        try:
            cursor.execute(f"CREATE INDEX IF NOT EXISTS {nome} ON {tabela} USING GIN ({coluna})")
            print(f"  ✅ Índice GIN {nome}")
        except Exception as e:
            print(f"  ⚠️ Erro ao criar {nome}: {e}")

    # ==================== FOREIGN KEY (template_slug) ====================
    try:
        cursor.execute("""
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM pg_constraint
                    WHERE conname = 'fk_perfis_template_slug'
                ) THEN
                    ALTER TABLE perfis
                    ADD CONSTRAINT fk_perfis_template_slug
                    FOREIGN KEY (template_slug)
                    REFERENCES templates(slug)
                    ON UPDATE CASCADE
                    ON DELETE RESTRICT;
                END IF;
            END $$;
        """)
        print("  ✅ FK fk_perfis_template_slug")
    except Exception as e:
        print(f"  ⚠️ Erro ao criar FK: {e}")

    print("✅ Índices criados/verificados!")