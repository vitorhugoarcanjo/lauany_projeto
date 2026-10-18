# rotas\pasta_financas\queries.py
"""QUERIES SQL do módulo Links"""


class LinksQueries:
    """Todas as queries SQL do módulo de Links"""

    @staticmethod
    def get_links_base():
        return """
            SELECT
                l.id,
                l.sequencia_links,
                l.titulo,
                l.url,
                l.icone,
                l.descricao,
                l.ordem,
                l.abrir_nova_aba,
                l.destaque,
                l.ativo,
                l.data_criacao
            FROM links l
            WHERE l.usuario_id = %s
        """

    @staticmethod
    def get_link_detalhes():
        return """
            SELECT
                l.id,
                l.sequencia_links,
                l.titulo,
                l.url,
                l.icone,
                l.descricao,
                l.ordem,
                l.ativo
            FROM links l
            WHERE l.sequencia_links = %s AND l.usuario_id = %s
        """

    @staticmethod
    def get_links_publicos():
        """Busca links ativos de um usuário pra página pública"""
        return """
            SELECT
                l.id,
                l.titulo,
                l.url,
                l.icone,
                l.descricao,
                l.abrir_nova_aba,
                l.destaque,
                l.ordem
            FROM links l
            WHERE l.usuario_id = %s AND l.ativo = 1
            ORDER BY l.destaque DESC, l.ordem ASC, l.id ASC
        """