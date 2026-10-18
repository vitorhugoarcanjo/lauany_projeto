"""Tabela: permissoes"""


def tabela_permissoes(cursor):
    cursor.execute("""
        SELECT EXISTS (
            SELECT 1 FROM information_schema.tables
            WHERE table_name = 'permissoes'
        )
    """)
    existe = cursor.fetchone()[0]

    if not existe:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS permissoes (
                id SERIAL PRIMARY KEY,
                usuario_id INTEGER NOT NULL,
                tipo VARCHAR(50) NOT NULL,
                valor VARCHAR(255),
                expira_em TIMESTAMP,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
            )
        """)
        print("✅ Tabela permissoes criada")
        return

    cursor.execute("""
        SELECT column_name FROM information_schema.columns
        WHERE table_name = 'permissoes'
    """)
    colunas = [r[0] for r in cursor.fetchall()]

    novas = []
    if 'criado_em' not in colunas:
        novas.append("criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP")

    for col in novas:
        try:
            cursor.execute(f"ALTER TABLE permissoes ADD COLUMN {col}")
            print(f"✅ Coluna '{col.split()[0]}' adicionada em permissoes")
        except Exception as e:
            print(f"⚠️ Erro ao adicionar {col}: {e}")

    if not novas:
        print("ℹ️ Tabela permissoes: todas as colunas existem")