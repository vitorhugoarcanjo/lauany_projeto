# rotas\pasta_financas\services\services_financas.py
"""SERVIÇOS do módulo Links"""

from rotas.pasta_links.queries import LinksQueries
from rotas.pasta_links.filters import LinksFilters


class LinksServices:
    """Serviços de negócio do módulo Links"""

    def __init__(self, conexao, cursor):
        self.conexao = conexao
        self.cursor = cursor

    def buscar_links(self, usuario_id, filtros):
        """Busca links com filtros"""
        query = LinksQueries.get_links_base()
        params = [usuario_id]

        # Aplica filtros
        query, params = LinksFilters.aplicar_filtros_query(query, params, filtros)

        # Ordenação: destaque primeiro, depois ordem, depois mais recentes
        query += " ORDER BY l.ordem ASC, l.id DESC"

        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def buscar_link_detalhes(self, link_seq, usuario_id):
        """Busca detalhes de um link específico"""
        self.cursor.execute(
            LinksQueries.get_link_detalhes(),
            (link_seq, usuario_id)
        )
        return self.cursor.fetchone()

    def buscar_links_publicos(self, usuario_id):
        """Busca links ativos para a página pública"""
        self.cursor.execute(
            LinksQueries.get_links_publicos(),
            (usuario_id,)
        )
        return self.cursor.fetchall()