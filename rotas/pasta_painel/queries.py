"""PAINEL — Queries SQL"""

class PainelQueries:

    @staticmethod
    def buscar_usuario():
        return """
            SELECT id, nome, email, telefone, data_criacao
            FROM usuarios
            WHERE id = %s
        """

    @staticmethod
    def buscar_perfil():
        return """
            SELECT id, username, bio, foto,
                   cor_primaria, cor_secundaria, tema
            FROM perfis
            WHERE usuario_id = %s
        """

    @staticmethod
    def buscar_perfil_visual():
        return """
            SELECT
                p.username, p.nome_exibicao, u.nome, p.bio, p.foto, p.foto_posicao,
                p.titulo_pagina, p.meta_descricao,
                p.cor_primaria, p.cor_secundaria, p.cor_fundo, p.cor_texto, p.cor_botao,
                p.tema, p.fonte, p.estilo_botao, p.template,
                p.tamanho_foto, p.tamanho_link, p.espacamento_links,
                p.borda_link, p.hover_efeito, p.animacao_entrada,
                p.ativo
            FROM perfis p
            INNER JOIN usuarios u ON u.id = p.usuario_id
            WHERE p.usuario_id = %s
        """

    @staticmethod
    def buscar_perfil_por_username():
        return "SELECT usuario_id FROM perfis WHERE username = %s"

    @staticmethod
    def buscar_links_preview():
        return """
            SELECT id, titulo, url, icone, descricao, destaque, abrir_nova_aba
            FROM links
            WHERE usuario_id = %s AND ativo = 1
            ORDER BY ordem ASC, id DESC
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