"""PAINEL — Queries SQL"""


class PainelQueries:

    # ==================== USUÁRIO ====================
    @staticmethod
    def buscar_usuario():
        return """
            SELECT id, nome, email, telefone, data_criacao
            FROM usuarios
            WHERE id = %s
        """

    # ==================== PERFIL ====================
    @staticmethod
    def buscar_perfil():
        return """
            SELECT id, username, bio, foto, template_slug
            FROM perfis
            WHERE usuario_id = %s
        """

    @staticmethod
    def buscar_perfil_visual():
        return """
            SELECT
                p.id,
                p.usuario_id,
                p.username,
                p.nome_exibicao,
                u.nome,
                p.bio,
                p.foto,
                p.foto_posicao,
                p.titulo_pagina,
                p.meta_descricao,
                p.template_slug,
                p.config,
                p.ativo
            FROM perfis p
            INNER JOIN usuarios u ON u.id = p.usuario_id
            WHERE p.usuario_id = %s
        """

    @staticmethod
    def buscar_perfil_por_username():
        return "SELECT usuario_id FROM perfis WHERE username = %s"

    # ==================== LINKS ====================
    @staticmethod
    def buscar_links_preview():
        return """
            SELECT id, titulo, url, icone, descricao, destaque, abrir_nova_aba
            FROM links
            WHERE usuario_id = %s AND ativo = 1
            ORDER BY destaque DESC, ordem ASC, id ASC
            LIMIT %s
        """

    @staticmethod
    def contar_links_ativos():
        return "SELECT COUNT(*) FROM links WHERE usuario_id = %s AND ativo = 1"

    @staticmethod
    def contar_links_inativos():
        return "SELECT COUNT(*) FROM links WHERE usuario_id = %s AND ativo = 0"

    @staticmethod
    def buscar_ultimos_links():
        return """
            SELECT id, titulo, url, icone, ativo, data_criacao
            FROM links
            WHERE usuario_id = %s
            ORDER BY data_criacao DESC
            LIMIT %s
        """

    # ==================== TEMPLATES ====================
    @staticmethod
    def listar_templates(apenas_ativos=True):
        where = "WHERE ativo = 1" if apenas_ativos else ""
        return f"""
            SELECT id, slug, nome, descricao, categoria, config_default, preview_url
            FROM templates
            {where}
            ORDER BY ordem ASC, id ASC
        """

    @staticmethod
    def buscar_template_por_slug():
        return """
            SELECT id, slug, nome, descricao, categoria, config_default, preview_url
            FROM templates
            WHERE slug = %s AND ativo = 1
        """