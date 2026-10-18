"""Tabela: perfis"""

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

                -- ==========================================
                -- APARÊNCIA (cores e estilo)
                -- ==========================================
                tema TEXT DEFAULT 'claro',
                cor_primaria TEXT DEFAULT '#3b82f6',
                cor_secundaria TEXT DEFAULT '#06b6d4',
                cor_fundo TEXT,
                cor_texto TEXT,
                cor_botao TEXT,
                fonte TEXT DEFAULT 'padrao',
                estilo_botao TEXT DEFAULT 'arredondado',
                template VARCHAR(30) DEFAULT 'cosmic',
                tamanho_foto VARCHAR(20) DEFAULT 'medio',
                tamanho_link VARCHAR(20) DEFAULT 'medio',
                espacamento_links VARCHAR(20) DEFAULT 'medio',
                borda_link VARCHAR(20) DEFAULT 'media',
                hover_efeito VARCHAR(20) DEFAULT 'subir',
                animacao_entrada VARCHAR(20) DEFAULT 'fade',
                foto_posicao VARCHAR(20) DEFAULT 'top',

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
        print("✅ Tabela perfis criada")
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

    for col in novas:
        try:
            cursor.execute(f"ALTER TABLE perfis ADD COLUMN {col}")
            print(f"✅ Coluna '{col.split()[0]}' adicionada em perfis")
        except Exception as e:
            print(f"⚠️ Erro ao adicionar {col}: {e}")

    if not novas:
        print("ℹ️ Tabela perfis: todas as colunas existem")