"""Tabela: usuarios_master"""


def tabela_usuarios_master(cursor):
    cursor.execute("""
        SELECT EXISTS (
            SELECT 1 FROM information_schema.tables
            WHERE table_name = 'usuarios_master'
        )
    """)
    existe = cursor.fetchone()[0]

    if not existe:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios_master (
                id SERIAL PRIMARY KEY,
                usuario_id INTEGER UNIQUE NOT NULL,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
            )
        """)
        print("✅ Tabela usuarios_master criada")
        return

    cursor.execute("""
        SELECT column_name FROM information_schema.columns
        WHERE table_name = 'usuarios_master'
    """)
    colunas = [r[0] for r in cursor.fetchall()]

    novas = []
    if 'criado_em' not in colunas:
        novas.append("criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP")

    for col in novas:
        try:
            cursor.execute(f"ALTER TABLE usuarios_master ADD COLUMN {col}")
            print(f"✅ Coluna '{col.split()[0]}' adicionada em usuarios_master")
        except Exception as e:
            print(f"⚠️ Erro ao adicionar {col}: {e}")

    if not novas:
        print("ℹ️ Tabela usuarios_master: todas as colunas existem")