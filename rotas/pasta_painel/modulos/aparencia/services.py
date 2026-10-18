"""APARÊNCIA — Services"""

import logging

logger = logging.getLogger(__name__)


class AparenciaService:

    def __init__(self, conexao, cursor):
        self.conexao = conexao
        self.cursor = cursor

    def buscar_aparencia(self, usuario_id):
        self.cursor.execute("""
            SELECT id, username, tema,
                   cor_primaria, cor_secundaria,
                   cor_fundo, cor_texto, cor_botao,
                   fonte, estilo_botao, template,
                   tamanho_foto, tamanho_link, espacamento_links,
                   borda_link, hover_efeito, animacao_entrada
            FROM perfis WHERE usuario_id = %s
        """, (usuario_id,))
        row = self.cursor.fetchone()
        if not row:
            return None
        return {
            'id': row[0], 'username': row[1], 'tema': row[2] or 'claro',
            'cor_primaria': row[3] or '#3b82f6',
            'cor_secundaria': row[4] or '#06b6d4',
            'cor_fundo': row[5],
            'cor_texto': row[6],
            'cor_botao': row[7],
            'fonte': row[8] or 'padrao',
            'estilo_botao': row[9] or 'arredondado',
            'template': row[10] or 'cosmic',
            'tamanho_foto': row[11] or 'medio',
            'tamanho_link': row[12] or 'medio',
            'espacamento_links': row[13] or 'medio',
            'borda_link': row[14] or 'media',
            'hover_efeito': row[15] or 'subir',
            'animacao_entrada': row[16] or 'fade',
        }

    def atualizar_aparencia(self, usuario_id, tema, cor_primaria,
                            cor_secundaria, cor_fundo, cor_texto,
                            cor_botao, fonte, estilo_botao,
                            template='cosmic',
                            tamanho_foto='medio',
                            tamanho_link='medio',
                            espacamento_links='medio',
                            borda_link='media',
                            hover_efeito='subir',
                            animacao_entrada='fade'):
        self.cursor.execute("""
            UPDATE perfis
            SET tema = %s, cor_primaria = %s, cor_secundaria = %s,
                cor_fundo = %s, cor_texto = %s, cor_botao = %s,
                fonte = %s, estilo_botao = %s, template = %s,
                tamanho_foto = %s, tamanho_link = %s, espacamento_links = %s,
                borda_link = %s, hover_efeito = %s, animacao_entrada = %s
            WHERE usuario_id = %s
        """, (tema, cor_primaria, cor_secundaria, cor_fundo, cor_texto,
              cor_botao, fonte, estilo_botao, template,
              tamanho_foto, tamanho_link, espacamento_links,
              borda_link, hover_efeito, animacao_entrada, usuario_id))