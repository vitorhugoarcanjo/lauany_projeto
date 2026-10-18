# rotas\pasta_links\crud\pasta_delete\services.py
"""INATIVAR LINK — Services"""

import logging

logger = logging.getLogger(__name__)


class InativarLinkService:

    @staticmethod
    def buscar_link(cursor, link_id, usuario_id):
        """Busca link por ID"""
        cursor.execute("""
            SELECT id, titulo
            FROM links
            WHERE id = %s AND usuario_id = %s AND ativo = 1
        """, (link_id, usuario_id))

        row = cursor.fetchone()
        if not row:
            return None

        return {'id': row[0], 'titulo': row[1]}

    @staticmethod
    def inativar_link(cursor, link_id, usuario_id):
        """Marca link como inativo (soft delete)"""
        cursor.execute("""
            UPDATE links
            SET ativo = 0
            WHERE id = %s AND usuario_id = %s
        """, (link_id, usuario_id))