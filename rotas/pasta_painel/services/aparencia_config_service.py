"""APARÊNCIA CONFIG — Service (só o SQL do perfis.config)"""

import json
import logging

logger = logging.getLogger(__name__)


class AparenciaConfigService:

    def __init__(self, conexao, cursor):
        self.conexao = conexao
        self.cursor = cursor

    def buscar_por_usuario(self, usuario_id):
        """Retorna {id, username, template_slug, config}."""
        self.cursor.execute("""
            SELECT id, username, template_slug, config
            FROM perfis WHERE usuario_id = %s
        """, (usuario_id,))
        row = self.cursor.fetchone()
        if not row:
            return None
        return {
            'id': row[0], 'username': row[1],
            'template_slug': row[2] or 'cosmic', 'config': row[3] or {},
        }

    def buscar_por_username(self, username):
        """Retorna {usuario_id, template_slug, config}."""
        self.cursor.execute("""
            SELECT usuario_id, template_slug, config
            FROM perfis WHERE username = %s AND ativo = 1
        """, (username,))
        row = self.cursor.fetchone()
        if not row:
            return None
        return {
            'usuario_id': row[0],
            'template_slug': row[1] or 'cosmic', 'config': row[2] or {},
        }

    def salvar(self, usuario_id, template_slug, config):
        """Salva {template_slug, config} no perfis."""
        self.cursor.execute("""
            UPDATE perfis
            SET template_slug = %s, config = %s
            WHERE usuario_id = %s
        """, (template_slug, json.dumps(config), usuario_id))