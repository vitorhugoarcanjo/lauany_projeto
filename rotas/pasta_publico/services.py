"""PÁGINA PÚBLICA — Services"""
import logging
from rotas.pasta_painel.services.services_painel import PainelService
from rotas.pasta_links.queries import LinksQueries

logger = logging.getLogger(__name__)


class PublicoService:

    def __init__(self, conexao, cursor):
        self.conexao = conexao
        self.cursor = cursor

    def buscar_perfil_publico(self, username):
        """Monta o perfil completo pra render da página pública."""
        painel = PainelService(self.conexao, self.cursor)
        perfil = painel.buscar_perfil_visual_por_username(username)
        if not perfil:
            return None

        # ⚠️ Links são por usuario_id (FK), NÃO por id do perfil
        perfil['links'] = self._buscar_links_publicos(perfil['usuario_id'])
        return perfil

    def _buscar_links_publicos(self, usuario_id):
        self.cursor.execute(LinksQueries.get_links_publicos(), (usuario_id,))
        rows = self.cursor.fetchall()
        return [
            {
                'id': r[0], 'titulo': r[1], 'url': r[2], 'icone': r[3],
                'descricao': r[4],
                'abrir_nova_aba': bool(r[5]),
                'destaque':       bool(r[6]),
                'ordem':          r[7],
            }
            for r in rows
        ]