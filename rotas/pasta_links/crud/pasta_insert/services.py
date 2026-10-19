# rotas/pasta_links/crud/pasta_insert/services.py
"""INSERIR LINK — Services"""

import logging
from urllib.parse import quote

logger = logging.getLogger(__name__)


def montar_url(tipo, dados):
    """
    Monta a URL final baseada no tipo:
      - link:     a URL crua (validada)
      - whatsapp: https://wa.me/55<telefone>?text=<mensagem>
      - email:    mailto:<email>?subject=<assunto>
    """
    tipo = (tipo or 'link').strip().lower()

    if tipo == 'whatsapp':
        tel = ''.join(c for c in (dados.get('telefone') or '') if c.isdigit())
        if not tel:
            return None
        # Se não começar com 55 (Brasil), adiciona
        if not tel.startswith('55') and len(tel) in (10, 11):
            tel = '55' + tel
        msg = (dados.get('mensagem') or '').strip()
        url = f"https://wa.me/{tel}"
        if msg:
            url += f"?text={quote(msg)}"
        return url

    if tipo == 'email':
        email = (dados.get('email_destino') or '').strip()
        if not email:
            return None
        assunto = (dados.get('assunto') or '').strip()
        url = f"mailto:{email}"
        if assunto:
            url += f"?subject={quote(assunto)}"
        return url

    # ⚠️ link — valida ESQUEMA (evita XSS/javascript:)
    url = (dados.get('url') or '').strip()
    if not url:
        return None
    if not (url.startswith('http://') or url.startswith('https://')
            or url.startswith('mailto:') or url.startswith('tel:')):
        return None
    return url


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
                    tipo, telefone, mensagem, email_destino, assunto,
                    abrir_nova_aba, destaque, cor_especial,
                    ordem, ativo
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1)
                RETURNING id
            """, (
                usuario_id,
                sequencia,
                dados['titulo'],
                dados['url'],
                dados['icone'],
                dados['descricao'] or None,
                dados.get('tipo') or 'link',
                dados.get('telefone') or None,
                dados.get('mensagem') or None,
                dados.get('email_destino') or None,
                dados.get('assunto') or None,
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