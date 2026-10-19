"""PAINEL — Services"""

import logging
from rotas.pasta_painel.queries import PainelQueries
from rotas.pasta_painel.services.aparencia_final_service import AparenciaFinalService

logger = logging.getLogger(__name__)


class PainelService:

    def __init__(self, conexao, cursor):
        self.conexao = conexao
        self.cursor = cursor

    def buscar_usuario(self, usuario_id):
        self.cursor.execute(PainelQueries.buscar_usuario(), (usuario_id,))
        row = self.cursor.fetchone()
        if not row:
            return None
        return {
            'id': row[0], 'nome': row[1], 'email': row[2],
            'telefone': row[3], 'data_criacao': row[4],
        }

    def buscar_perfil(self, usuario_id):
        self.cursor.execute(PainelQueries.buscar_perfil(), (usuario_id,))
        row = self.cursor.fetchone()
        if not row:
            return None
        return {
            'id': row[0],
            'username': row[1],
            'bio': row[2],
            'foto': row[3],
            'template_slug': row[4] or 'cosmic',
        }

    def buscar_perfil_visual(self, usuario_id):
        self.cursor.execute(PainelQueries.buscar_perfil_visual(), (usuario_id,))
        row = self.cursor.fetchone()
        if not row:
            return None

        perfil = {
            'id': row[0],
            'usuario_id': row[1],
            'username': row[2],
            'nome_exibicao': row[3],
            'nome': row[4],
            'bio': row[5],
            'foto': row[6],
            'foto_posicao': row[7] or 'top',
            'titulo_pagina': row[8],
            'meta_descricao': row[9],
            'template_slug': row[10] or 'cosmic',
            'config': row[11] or {},
            'ativo': row[12],
            'links_preview': [],
        }

        perfil['nome_display'] = (
            perfil['nome_exibicao']
            or perfil['nome']
            or perfil['username']
            or 'Sem nome'
        )

        aparencia_final_service = AparenciaFinalService(self.conexao, self.cursor)
        aparencia_final = aparencia_final_service.buscar_por_usuario(usuario_id)
        perfil['config_final'] = aparencia_final['config_final'] if aparencia_final else {}

        perfil['links_preview'] = self._buscar_links_preview(usuario_id, limite=4)
        return perfil

    def buscar_perfil_visual_por_username(self, username):
        self.cursor.execute(PainelQueries.buscar_perfil_por_username(), (username,))
        row = self.cursor.fetchone()
        if not row:
            return None
        return self.buscar_perfil_visual(row[0])

    def _buscar_links_preview(self, usuario_id, limite=4):
        self.cursor.execute(PainelQueries.buscar_links_preview(), (usuario_id, limite))
        rows = self.cursor.fetchall()
        return [
            {
                'id': r[0], 'titulo': r[1], 'url': r[2],
                'icone': r[3], 'descricao': r[4],
                'destaque': bool(r[5]),
                'abrir_nova_aba': bool(r[6]),
            }
            for r in rows
        ]

    def buscar_estatisticas(self, usuario_id):
        self.cursor.execute(PainelQueries.contar_links_ativos(), (usuario_id,))
        ativos = self.cursor.fetchone()[0]

        self.cursor.execute(PainelQueries.contar_links_inativos(), (usuario_id,))
        inativos = self.cursor.fetchone()[0]

        return {'ativos': ativos, 'inativos': inativos, 'total': ativos + inativos}

    def buscar_ultimos_links(self, usuario_id, limite=5):
        self.cursor.execute(PainelQueries.buscar_ultimos_links(), (usuario_id, limite))
        colunas = ['id', 'titulo', 'url', 'icone', 'ativo', 'data_criacao']
        return [dict(zip(colunas, row)) for row in self.cursor.fetchall()]