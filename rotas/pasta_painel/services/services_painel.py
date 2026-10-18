"""PAINEL — Services"""

import logging
from rotas.pasta_painel.queries import PainelQueries

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
            'id': row[0], 'username': row[1], 'bio': row[2], 'foto': row[3],
            'cor_primaria': row[4], 'cor_secundaria': row[5], 'tema': row[6],
        }

    def buscar_perfil_visual(self, usuario_id):
        self.cursor.execute(PainelQueries.buscar_perfil_visual(), (usuario_id,))
        row = self.cursor.fetchone()
        if not row:
            return None

        perfil = {
            'username': row[0],
            'nome_exibicao': row[1],
            'nome': row[2],
            'bio': row[3],
            'foto': row[4],
            'foto_posicao': row[5] or 'top',
            'titulo_pagina': row[6],
            'meta_descricao': row[7],
            'cor_primaria': row[8] or '#3b82f6',
            'cor_secundaria': row[9] or '#06b6d4',
            'cor_fundo': row[10],
            'cor_texto': row[11],
            'cor_botao': row[12],
            'tema': row[13] or 'claro',
            'fonte': row[14] or 'padrao',
            'estilo_botao': row[15] or 'arredondado',
            'template': row[16] or 'cosmic',
            'tamanho_foto': row[17] or 'medio',
            'tamanho_link': row[18] or 'medio',
            'espacamento_links': row[19] or 'medio',
            'borda_link': row[20] or 'media',
            'hover_efeito': row[21] or 'subir',
            'animacao_entrada': row[22] or 'fade',
            'ativo': row[23],
            'links_preview': [],
        }

        perfil['nome_display'] = (
            perfil['nome_exibicao']
            or perfil['nome']
            or perfil['username']
            or 'Sem nome'
        )

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