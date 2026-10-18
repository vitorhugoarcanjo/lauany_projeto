"""Tabela: links"""

def tabela_links(cursor):
    cursor.execute("""
        SELECT EXISTS (
            SELECT 1 FROM information_schema.tables
            WHERE table_name = 'links'
        )
    """)
    existe = cursor.fetchone()[0]

    if not existe:
        cursor.execute("""
            CREATE TABLE links (
                id SERIAL PRIMARY KEY,
                usuario_id INTEGER NOT NULL,
                sequencia_links INTEGER,

                -- Dados do link
                titulo TEXT NOT NULL,
                url TEXT NOT NULL,
                icone TEXT,
                descricao TEXT,

                -- Comportamento
                abrir_nova_aba INTEGER DEFAULT 1,
                destaque INTEGER DEFAULT 0,
                cor_especial TEXT,

                -- Ordem e status
                ordem INTEGER DEFAULT 0,
                ativo INTEGER DEFAULT 1,

                -- Auditoria
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
            )
        """)
        print("✅ Tabela links criada")
        return

    # Verifica colunas que faltam
    cursor.execute("""
        SELECT column_name FROM information_schema.columns
        WHERE table_name = 'links'
    """)
    colunas = [r[0] for r in cursor.fetchall()]

    novas = []
    if 'abrir_nova_aba' not in colunas:
        novas.append("abrir_nova_aba INTEGER DEFAULT 1")
    if 'destaque' not in colunas:
        novas.append("destaque INTEGER DEFAULT 0")
    if 'cor_especial' not in colunas:
        novas.append("cor_especial TEXT")

    for col in novas:
        try:
            cursor.execute(f"ALTER TABLE links ADD COLUMN {col}")
            print(f"✅ Coluna '{col.split()[0]}' adicionada em links")
        except Exception as e:
            print(f"⚠️ Erro: {e}")

    if not novas:
        print("ℹ️ Tabela links: todas as colunas existem")