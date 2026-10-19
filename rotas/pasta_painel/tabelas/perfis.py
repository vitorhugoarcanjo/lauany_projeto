"""Tabela: perfis (com JSONB)"""


def tabela_perfis(cursor):
    cursor.execute("""
        SELECT EXISTS (
            SELECT 1 FROM information_schema.tables
            WHERE table_name = 'perfis'
        )
    """)
    existe = cursor.fetchone()[0]

    if not existe:
        cursor.execute("""
            CREATE TABLE perfis (
                id SERIAL PRIMARY KEY,
                usuario_id INTEGER UNIQUE NOT NULL,

                -- ==========================================
                -- IDENTIDADE PÚBLICA
                -- ==========================================
                username TEXT UNIQUE NOT NULL,
                nome_exibicao TEXT,
                bio TEXT,
                foto TEXT,
                foto_posicao VARCHAR(20) DEFAULT 'top',

                -- ==========================================
                -- APARÊNCIA (JSONB)
                -- ==========================================
                template_slug VARCHAR(50) DEFAULT 'cosmic',
                config JSONB NOT NULL DEFAULT '{}'::jsonb,

                -- ==========================================
                -- SEO
                -- ==========================================
                titulo_pagina TEXT,
                meta_descricao TEXT,

                -- ==========================================
                -- CONTROLE
                -- ==========================================
                ativo INTEGER DEFAULT 1,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
            )
        """)
        print("✅ Tabela perfis criada (com JSONB)")
        return

    # ==========================================================
    # VERIFICA COLUNAS QUE FALTAM (bancos já existentes)
    # ==========================================================
    cursor.execute("""
        SELECT column_name FROM information_schema.columns
        WHERE table_name = 'perfis'
    """)
    colunas = [r[0] for r in cursor.fetchall()]

    novas = []
    if 'foto_posicao' not in colunas:
        novas.append("foto_posicao VARCHAR(20) DEFAULT 'top'")
    if 'template_slug' not in colunas:
        novas.append("template_slug VARCHAR(50) DEFAULT 'cosmic'")
    if 'config' not in colunas:
        novas.append("config JSONB NOT NULL DEFAULT '{}'::jsonb")

    for col in novas:
        try:
            cursor.execute(f"ALTER TABLE perfis ADD COLUMN {col}")
            print(f"✅ Coluna '{col.split()[0]}' adicionada em perfis")
        except Exception as e:
            print(f"⚠️ Erro ao adicionar {col}: {e}")

    if not novas:
        print("ℹ️ Tabela perfis: todas as colunas existem")