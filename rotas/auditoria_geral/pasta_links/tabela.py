"""Tabela: links_auditoria"""

def tabela_auditoria_links(cursor):
    cursor.execute("""
        SELECT EXISTS (
            SELECT 1 FROM information_schema.tables
            WHERE table_name = 'links_auditoria'
        )
    """)
    existe = cursor.fetchone()[0]

    if not existe:
        cursor.execute("""
            CREATE TABLE links_auditoria (
                id SERIAL PRIMARY KEY,
                link_id INTEGER,
                acao VARCHAR(50),
                campo_alterado VARCHAR(100),
                valor_antigo TEXT,
                valor_novo TEXT,
                usuario_id INTEGER,
                data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ip VARCHAR(45),

                FOREIGN KEY (link_id) REFERENCES links(id),
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        """)
        print("✅ Tabela links_auditoria criada")
        return

    print("ℹ️ Tabela links_auditoria já existe")