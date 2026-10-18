"""PERFIL — Services"""

import logging

logger = logging.getLogger(__name__)


class PerfilService:

    def __init__(self, conexao, cursor):
        self.conexao = conexao
        self.cursor = cursor

    def username_disponivel(self, username, ignorar_usuario_id=None):
        if ignorar_usuario_id:
            self.cursor.execute(
                'SELECT 1 FROM perfis WHERE username = %s AND usuario_id != %s',
                (username, ignorar_usuario_id)
            )
        else:
            self.cursor.execute('SELECT 1 FROM perfis WHERE username = %s', (username,))
        return not self.cursor.fetchone()

    def buscar_perfil(self, usuario_id):
        self.cursor.execute("""
            SELECT id, username, nome_exibicao, bio, foto, foto_posicao,
                titulo_pagina, meta_descricao
            FROM perfis WHERE usuario_id = %s
        """, (usuario_id,))
        row = self.cursor.fetchone()
        if not row:
            return None
        return {
            'id': row[0], 'username': row[1], 'nome_exibicao': row[2],
            'bio': row[3], 'foto': row[4], 'foto_posicao': row[5] or 'top',
            'titulo_pagina': row[6], 'meta_descricao': row[7],
        }
    
    def atualizar_perfil(self, usuario_id, username, nome_exibicao, bio,
                         titulo_pagina, meta_descricao, foto=None,
                         foto_posicao='top', acao_foto='manter'):
        """
        acao_foto:
            'manter'    -> não toca na coluna foto
            'atualizar' -> seta foto = caminho novo
            'remover'   -> seta foto = NULL
        """
        if acao_foto == 'atualizar':
            self.cursor.execute("""
                UPDATE perfis
                SET username = %s, nome_exibicao = %s, bio = %s,
                    foto = %s, foto_posicao = %s,
                    titulo_pagina = %s, meta_descricao = %s
                WHERE usuario_id = %s
            """, (username, nome_exibicao, bio, foto, foto_posicao,
                  titulo_pagina, meta_descricao, usuario_id))

        elif acao_foto == 'remover':
            self.cursor.execute("""
                UPDATE perfis
                SET username = %s, nome_exibicao = %s, bio = %s,
                    foto = NULL, foto_posicao = %s,
                    titulo_pagina = %s, meta_descricao = %s
                WHERE usuario_id = %s
            """, (username, nome_exibicao, bio, foto_posicao,
                  titulo_pagina, meta_descricao, usuario_id))

        else:  # manter
            self.cursor.execute("""
                UPDATE perfis
                SET username = %s, nome_exibicao = %s, bio = %s,
                    foto_posicao = %s,
                    titulo_pagina = %s, meta_descricao = %s
                WHERE usuario_id = %s
            """, (username, nome_exibicao, bio, foto_posicao,
                  titulo_pagina, meta_descricao, usuario_id))