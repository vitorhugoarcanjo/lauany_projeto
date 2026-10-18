"""CONFIG — Services"""

import logging

logger = logging.getLogger(__name__)


class ConfigService:

    def __init__(self, conexao, cursor):
        self.conexao = conexao
        self.cursor = cursor

    def buscar_usuario(self, usuario_id):
        self.cursor.execute("""
            SELECT id, nome, email, telefone, data_criacao
            FROM usuarios WHERE id = %s
        """, (usuario_id,))
        row = self.cursor.fetchone()
        if not row:
            return None
        return {
            'id': row[0], 'nome': row[1], 'email': row[2],
            'telefone': row[3], 'data_criacao': row[4],
        }

    def buscar_senha(self, usuario_id):
        self.cursor.execute(
            'SELECT senha FROM usuarios WHERE id = %s', (usuario_id,)
        )
        row = self.cursor.fetchone()
        return row[0] if row else None

    def atualizar_senha(self, usuario_id, senha_hash):
        self.cursor.execute(
            'UPDATE usuarios SET senha = %s WHERE id = %s',
            (senha_hash, usuario_id)
        )