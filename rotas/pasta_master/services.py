"""MASTER — Services"""

from .queries import MasterQueries


class MasterService:

    def __init__(self, conexao, cursor):
        self.conexao = conexao
        self.cursor = cursor

    def buscar_estatisticas_gerais(self):
        self.cursor.execute(MasterQueries.buscar_estatisticas_gerais())
        row = self.cursor.fetchone()
        return {
            'total_usuarios': row[0],
            'total_links': row[1],
            'total_perfis': row[2],
        }

    def buscar_usuarios_com_stats(self):
        self.cursor.execute(MasterQueries.buscar_usuarios_com_stats())
        colunas = ['id', 'nome', 'email', 'data_criacao', 'username', 'foto', 'links_ativos', 'links_inativos']
        return [dict(zip(colunas, row)) for row in self.cursor.fetchall()]

    def verificar_master(self, usuario_id):
        self.cursor.execute(MasterQueries.verificar_master(), (usuario_id,))
        return self.cursor.fetchone() is not None