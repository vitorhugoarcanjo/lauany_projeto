# rotas/pasta_publico/services/services_publico.py

from rotas.pasta_painel.services.services_painel import PainelService


class PublicoService:

    def __init__(self, conexao, cursor):
        self.conexao = conexao
        self.cursor = cursor
        self.painel = PainelService(conexao, cursor)

    def buscar_perfil_publico(self, username):
        return self.painel.buscar_perfil_visual_por_username(username)