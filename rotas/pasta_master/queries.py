"""MASTER — Queries SQL"""


class MasterQueries:

    @staticmethod
    def buscar_estatisticas_gerais():
        return """
            SELECT
                (SELECT COUNT(*) FROM usuarios WHERE ativo = 1) AS total_usuarios,
                (SELECT COUNT(*) FROM links WHERE ativo = 1) AS total_links,
                (SELECT COUNT(*) FROM perfis WHERE ativo = 1) AS total_perfis
        """

    @staticmethod
    def buscar_usuarios_com_stats():
        return """
            SELECT
                u.id,
                u.nome,
                u.email,
                u.data_criacao,
                p.username,
                p.foto,
                (SELECT COUNT(*) FROM links l WHERE l.usuario_id = u.id AND l.ativo = 1) AS links_ativos,
                (SELECT COUNT(*) FROM links l WHERE l.usuario_id = u.id AND l.ativo = 0) AS links_inativos
            FROM usuarios u
            LEFT JOIN perfis p ON p.usuario_id = u.id
            WHERE u.ativo = 1
            ORDER BY u.data_criacao DESC
        """

    @staticmethod
    def verificar_master():
        return "SELECT 1 FROM usuarios_master WHERE usuario_id = %s"