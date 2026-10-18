# rotas\pasta_links\crud\pasta_edit\services.py

"""EDITAR LINK — Services"""

import logging

logger = logging.getLogger(__name__)


class EditarLinkService:

    @staticmethod
    def buscar_link(cursor, link_id, usuario_id):
        """Busca link por ID (só do próprio usuário)"""
        cursor.execute("""
            SELECT
                id, sequencia_links,
                titulo, url, icone, descricao,
                ordem, abrir_nova_aba, destaque, cor_especial,
                ativo
            FROM links
            WHERE id = %s AND usuario_id = %s
        """, (link_id, usuario_id))

        row = cursor.fetchone()
        if not row:
            return None

        colunas = [
            'id', 'sequencia_links',
            'titulo', 'url', 'icone', 'descricao',
            'ordem', 'abrir_nova_aba', 'destaque', 'cor_especial',
            'ativo'
        ]
        return dict(zip(colunas, row))

    @staticmethod
    def atualizar_link(cursor, link_id, usuario_id, dados):
        """Atualiza link existente"""
        try:
            cursor.execute("""
                UPDATE links
                SET titulo = %s,
                    url = %s,
                    icone = %s,
                    descricao = %s,
                    ordem = %s,
                    abrir_nova_aba = %s,
                    destaque = %s,
                    cor_especial = %s
                WHERE id = %s AND usuario_id = %s
            """, (
                dados['titulo'],
                dados['url'],
                dados['icone'],
                dados['descricao'] or None,
                dados['ordem'],
                dados['abrir_nova_aba'],
                dados['destaque'],
                dados['cor_especial'],
                link_id,
                usuario_id,
            ))

            if cursor.rowcount == 0:
                return False, "Nenhum link atualizado"

            return True, {'mensagem': 'Link atualizado com sucesso!'}

        except Exception as e:
            msg = f"Erro ao atualizar link: {str(e)}"
            logger.error(msg)
            return False, msg