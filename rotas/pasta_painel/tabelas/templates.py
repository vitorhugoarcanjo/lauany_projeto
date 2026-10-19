"""Tabela: templates (catálogo de templates)"""


def tabela_templates(cursor):
    cursor.execute("""
        SELECT EXISTS (
            SELECT 1 FROM information_schema.tables
            WHERE table_name = 'templates'
        )
    """)
    existe = cursor.fetchone()[0]

    if not existe:
        cursor.execute("""
            CREATE TABLE templates (
                id SERIAL PRIMARY KEY,
                slug VARCHAR(50) UNIQUE NOT NULL,
                nome VARCHAR(100) NOT NULL,
                descricao TEXT,
                categoria VARCHAR(30) DEFAULT 'gratuito',
                config_default JSONB NOT NULL,
                preview_url TEXT,
                ativo INTEGER DEFAULT 1,
                ordem INTEGER DEFAULT 0,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Tabela templates criada")
        return

    print("ℹ️ Tabela templates já existe")