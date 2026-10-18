"""AUDITORIA DE LINKS — Service"""

import json
from flask import request, session
from utils.database.conexao_global import ini_conexao, get_conexao_direct


class AuditoriaService:

    @staticmethod
    def get_db_connection():
        return ini_conexao()

    @staticmethod
    def get_db_connection_direct():
        return get_conexao_direct()

    @staticmethod
    def registrar(link_id, acao, campo_alterado=None, valor_antigo=None,
                  valor_novo=None, conexao=None):
        """Registra ação na auditoria. Se conexão fornecida, usa a MESMA."""
        propria_conexao = False
        try:
            if conexao is None:
                conexao, cursor = AuditoriaService.get_db_connection()
                propria_conexao = True
            else:
                cursor = conexao.cursor()

            if valor_antigo and len(str(valor_antigo)) > 500:
                valor_antigo = str(valor_antigo)[:500] + "..."
            if valor_novo and len(str(valor_novo)) > 500:
                valor_novo = str(valor_novo)[:500] + "..."

            cursor.execute("""
                INSERT INTO links_auditoria
                (link_id, acao, campo_alterado, valor_antigo, valor_novo, usuario_id, ip)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                link_id,
                acao,
                campo_alterado,
                valor_antigo,
                valor_novo,
                session.get('user_id'),
                request.remote_addr
            ))

            if propria_conexao:
                conexao.commit()

            return True
        except Exception as e:
            print(f"Erro ao registrar auditoria: {e}")
            if propria_conexao:
                conexao.rollback()
            return False

    @staticmethod
    def listar_por_link(link_id, limite=50):
        """Lista todas as ações de um link"""
        try:
            conexao, cursor = AuditoriaService.get_db_connection()

            cursor.execute("""
                SELECT la.*, u.nome as usuario_nome
                FROM links_auditoria la
                LEFT JOIN usuarios u ON la.usuario_id = u.id
                WHERE la.link_id = %s
                ORDER BY la.data_hora DESC
                LIMIT %s
            """, (link_id, limite))

            return cursor.fetchall()
        except Exception as e:
            print(f"Erro ao listar auditoria: {e}")
            return []

    @staticmethod
    def listar_por_link_formatado(link_id, limite=50):
        """Lista auditoria com formatação (colunas explícitas)"""
        try:
            conexao, cursor = AuditoriaService.get_db_connection()

            colunas = [
                'id', 'link_id', 'acao', 'campo_alterado',
                'valor_antigo', 'valor_novo', 'usuario_id', 'data_hora', 'ip',
                'usuario_nome', 'data_hora_br'
            ]

            cursor.execute("""
                SELECT
                    la.id, la.link_id, la.acao, la.campo_alterado,
                    la.valor_antigo, la.valor_novo, la.usuario_id, la.data_hora, la.ip,
                    u.nome as usuario_nome,
                    TO_CHAR(la.data_hora AT TIME ZONE 'America/Cuiaba', 'DD/MM/YYYY HH24:MI:SS') as data_hora_br
                FROM links_auditoria la
                LEFT JOIN usuarios u ON la.usuario_id = u.id
                WHERE la.link_id = %s
                ORDER BY la.data_hora DESC
                LIMIT %s
            """, (link_id, limite))

            auditoria = []
            for row in cursor.fetchall():
                item = dict(zip(colunas, row))
                item['data_hora'] = item.get('data_hora_br') or str(item.get('data_hora') or '')
                item['alteracoes'] = []

                # Padrão 2099: só 'multiplos' tem lista de alterações
                if item.get('campo_alterado') == 'multiplos' and item.get('valor_novo'):
                    try:
                        item['alteracoes'] = json.loads(item['valor_novo'])
                    except Exception:
                        item['alteracoes'] = []

                auditoria.append(item)

            return auditoria
        except Exception as e:
            print(f"Erro ao listar auditoria formatada: {e}")
            return []