"""TEMPLATE — Service (catálogo de templates)"""

import json
import logging
from rotas.pasta_painel.queries import PainelQueries

logger = logging.getLogger(__name__)


class TemplateService:

    def __init__(self, conexao, cursor):
        self.conexao = conexao
        self.cursor = cursor

    # ==================== HELPER ====================
    @staticmethod
    def _parse_jsonb(val):
        """
        Garante que JSONB venha como dict (não string).
        psycopg2 normalmente já retorna dict pra JSONB.
        Isso é blindagem pra outros drivers/ambientes.
        """
        if isinstance(val, dict):
            return val
        if isinstance(val, str):
            try:
                return json.loads(val)
            except Exception as e:
                logger.warning(f"Falha ao parsear config_default: {e}")
                return {}
        return {}

    # ==================== PÚBLICOS ====================
    def listar(self, apenas_ativos=True):
        """Retorna todos os templates (opcionalmente só ativos)."""
        self.cursor.execute(PainelQueries.listar_templates(apenas_ativos))
        rows = self.cursor.fetchall()
        return [
            {
                'id': r[0],
                'slug': r[1],
                'nome': r[2],
                'descricao': r[3],
                'categoria': r[4],
                'config_default': self._parse_jsonb(r[5]),
                'preview_url': r[6],
            }
            for r in rows
        ]

    def buscar_por_slug(self, slug):
        """Retorna um template pelo slug (só ativo)."""
        self.cursor.execute(PainelQueries.buscar_template_por_slug(), (slug,))
        row = self.cursor.fetchone()
        if not row:
            return None
        return {
            'id': row[0],
            'slug': row[1],
            'nome': row[2],
            'descricao': row[3],
            'categoria': row[4],
            'config_default': self._parse_jsonb(row[5]),
            'preview_url': row[6],
        }