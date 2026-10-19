# rotas/pasta_links/crud/pasta_edit/services.py
"""EDITAR LINK — Services"""

import logging
from urllib.parse import quote

logger = logging.getLogger(__name__)


def montar_url(tipo, dados):
    """Mesma lógica do insert"""
    tipo = (tipo or 'link').strip().lower()

    if tipo == 'whatsapp':
        tel = ''.join(c for c in (dados.get('telefone') or '') if c.isdigit())
        if not tel:
            return None
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


class EditarLinkService:

    @staticmethod
    def buscar_link(cursor, link_id, usuario_id):
        """Busca link por ID (só do próprio usuário)"""
        cursor.execute("""
            SELECT
                id, sequencia_links,
                titulo, url, icone, descricao,
                tipo, telefone, mensagem, email_destino, assunto,
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
            'tipo', 'telefone', 'mensagem', 'email_destino', 'assunto',
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
                    tipo = %s,
                    telefone = %s,
                    mensagem = %s,
                    email_destino = %s,
                    assunto = %s,
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
                dados.get('tipo') or 'link',
                dados.get('telefone') or None,
                dados.get('mensagem') or None,
                dados.get('email_destino') or None,
                dados.get('assunto') or None,
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