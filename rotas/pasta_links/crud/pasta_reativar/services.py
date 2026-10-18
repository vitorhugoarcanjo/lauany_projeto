# rotas\pasta_links\crud\pasta_reativar\services.py
"""REATIVAR LINK — Services"""

import logging

logger = logging.getLogger(__name__)


class ReativarLinkService:

    @staticmethod
    def buscar_link(cursor, link_id, usuario_id):
        """Busca link inativo por ID"""
        cursor.execute("""
            SELECT id, titulo
            FROM links
            WHERE id = %s AND usuario_id = %s AND ativo = 0
        """, (link_id, usuario_id))

        row = cursor.fetchone()
        if not row:
            return None

        return {'id': row[0], 'titulo': row[1]}

    @staticmethod
    def reativar_link(cursor, link_id, usuario_id):
        """Reativa link"""
        cursor.execute("""
            UPDATE links
            SET ativo = 1
            WHERE id = %s AND usuario_id = %s
        """, (link_id, usuario_id))