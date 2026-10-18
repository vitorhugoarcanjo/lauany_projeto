# rotas/pasta_links/crud/pasta_insert/services.py
"""INSERIR LINK — Services"""

import logging

logger = logging.getLogger(__name__)


class InserirLinkService:

    @staticmethod
    def get_proxima_sequencia(cursor, usuario_id):
        """Retorna a próxima sequência de links para o usuário"""
        cursor.execute("""
            SELECT COALESCE(MAX(sequencia_links), 0) + 1
            FROM links
            WHERE usuario_id = %s
        """, (usuario_id,))
        res = cursor.fetchone()
        return res[0] if res else 1

    @staticmethod
    def criar_link(cursor, usuario_id, dados):
        """Cria um novo link"""
        try:
            sequencia = InserirLinkService.get_proxima_sequencia(cursor, usuario_id)

            cursor.execute("""
                INSERT INTO links (
                    usuario_id, sequencia_links,
                    titulo, url, icone, descricao,
                    abrir_nova_aba, destaque, cor_especial,
                    ordem, ativo
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1)
                RETURNING id
            """, (
                usuario_id,
                sequencia,
                dados['titulo'],
                dados['url'],
                dados['icone'],
                dados['descricao'] or None,
                dados['abrir_nova_aba'],
                dados['destaque'],
                dados['cor_especial'],
                dados['ordem'],
            ))

            link_id = cursor.fetchone()[0]

            return True, {
                'link_id': link_id,
                'sequencia': sequencia,
                'mensagem': 'Link criado com sucesso!',
            }

        except KeyError as e:
            msg = f"Campo obrigatório ausente: {str(e)}"
            logger.error(msg)
            return False, msg
        except Exception as e:
            msg = f"Erro ao inserir link: {str(e)}"
            logger.error(msg)
            return False, msg