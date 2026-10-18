"""Tabela: usuarios"""

def tabela_usuarios(cursor):
    cursor.execute("""
        SELECT EXISTS (
            SELECT 1 FROM information_schema.tables
            WHERE table_name = 'usuarios'
        )
    """)
    existe = cursor.fetchone()[0]

    if not existe:
        cursor.execute("""
            CREATE TABLE usuarios (
                id SERIAL PRIMARY KEY,

                nome TEXT NOT NULL,
                telefone TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL,

                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ativo INTEGER DEFAULT 1,

                email_verificado INTEGER DEFAULT 0,
                codigo_verificacao VARCHAR(6),
                codigo_expiracao TIMESTAMP,
                tentativas_verificacao INTEGER DEFAULT 0,

                codigo_recuperacao VARCHAR(6),
                codigo_recuperacao_expiracao TIMESTAMP,
                tentativas_recuperacao INTEGER DEFAULT 0
            )
        """)
        print("✅ Tabela usuarios criada")
        return

    print("ℹ️ Tabela usuarios já existe")