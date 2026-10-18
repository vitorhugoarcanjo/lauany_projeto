"""AUDITORIA DE LINKS — View (modal HTMX)"""

from flask import render_template, session
from rotas.middleware.autenticacao import login_required
from utils.database.conexao_global import ini_conexao

from .services_auditoria import AuditoriaService


@login_required
def historico_links(link_seq):
    """
    Recebe a SEQUÊNCIA do link (URL: /auditoria/link/<seq>).
    Traduz pra ID interno e busca auditoria.
    """
    usuario_id = session['user_id']
    conexao, cursor = ini_conexao()

    # Busca link pelo ID interno + dados pro header
    cursor.execute("""
        SELECT id, sequencia_links, titulo
        FROM links
        WHERE sequencia_links = %s AND usuario_id = %s
    """, (link_seq, usuario_id))
    row = cursor.fetchone()

    if not row:
        return '', 404

    id_interno = row[0]

    # Tupla no formato esperado pelo template
    link = (row[1], row[2])

    # Busca auditoria pelo ID INTERNO
    historico = AuditoriaService.listar_por_link_formatado(id_interno)

    return render_template(
        'pasta_auditoria/pasta_links/modal_auditoria.html.jinja',
        historico=historico,
        link=link,
        link_seq=link_seq,
    )