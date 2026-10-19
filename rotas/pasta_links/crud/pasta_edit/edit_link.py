# rotas/pasta_links/crud/pasta_edit/edit_link.py
"""EDITAR LINK — View"""

import logging
import json
from flask import request, session, jsonify, render_template

from rotas.middleware.autenticacao import login_required
from rotas.auditoria_geral.pasta_links.services_auditoria import AuditoriaService
from utils.database.conexao_global import ini_conexao

from .services import EditarLinkService, montar_url
from .validacoes import validar_dados_edicao

logger = logging.getLogger(__name__)


@login_required
def editar_link_modal(link_id):
    """Retorna o HTML do modal de edição"""
    usuario_id = session.get('user_id')
    conexao, cursor = ini_conexao()

    link = EditarLinkService.buscar_link(cursor, link_id, usuario_id)
    if not link:
        return '', 404

    return render_template(
        'pasta_links/modais/modal_editar_link.html.jinja',
        link=link,
    )


@login_required
def salvar_edicao_link(link_id):
    """Salva edição de um link"""
    usuario_id = session.get('user_id')
    conexao, cursor = ini_conexao()

    try:
        payload = request.json or {}

        tipo = (payload.get('tipo') or 'link').strip().lower()

        dados = {
            'tipo': tipo,
            'titulo': (payload.get('titulo') or '').strip(),
            'icone': (payload.get('icone') or 'fa-link').strip(),
            'descricao': (payload.get('descricao') or '').strip(),
            'ordem': int(payload.get('ordem') or 0),
            'abrir_nova_aba': 1 if payload.get('abrir_nova_aba', True) else 0,
            'destaque': 1 if payload.get('destaque', False) else 0,
            'cor_especial': (payload.get('cor_especial') or '').strip() or None,
            # campos por tipo
            'url': (payload.get('url') or '').strip(),
            'telefone': (payload.get('telefone') or '').strip(),
            'mensagem': (payload.get('mensagem') or '').strip(),
            'email_destino': (payload.get('email_destino') or '').strip(),
            'assunto': (payload.get('assunto') or '').strip(),
        }

        # ⚠️ MONTA A URL BASEADO NO TIPO
        url_final = montar_url(tipo, dados)
        if not url_final:
            return jsonify({
                'success': False,
                'error': f'Dados incompletos para o tipo "{tipo}".'
            }), 400

        dados['url'] = url_final

        # Valida
        erros = validar_dados_edicao(dados)
        if erros:
            return jsonify({'success': False, 'errors': erros}), 400

        # Busca valores antigos (pra auditoria)
        link_antigo = EditarLinkService.buscar_link(cursor, link_id, usuario_id)
        if not link_antigo:
            return jsonify({'success': False, 'error': 'Link não encontrado'}), 404

        # Salva edição
        sucesso, resultado = EditarLinkService.atualizar_link(cursor, link_id, usuario_id, dados)
        if not sucesso:
            conexao.rollback()
            return jsonify({'success': False, 'error': resultado}), 400

        # Auditoria — diff campo a campo
        alteracoes = []
        campos = [
            ('tipo', 'Tipo'),
            ('titulo', 'Título'),
            ('url', 'URL'),
            ('icone', 'Ícone'),
            ('descricao', 'Descrição'),
            ('telefone', 'Telefone'),
            ('mensagem', 'Mensagem'),
            ('email_destino', 'E-mail'),
            ('assunto', 'Assunto'),
            ('ordem', 'Ordem'),
            ('abrir_nova_aba', 'Nova aba'),
            ('destaque', 'Destaque'),
            ('cor_especial', 'Cor especial'),
        ]

        for campo_bd, campo_label in campos:
            antes = link_antigo.get(campo_bd)
            depois = dados.get(campo_bd)

            if antes is None:
                antes = ''
            if depois is None:
                depois = ''

            if str(antes) != str(depois):
                alteracoes.append({
                    'campo': campo_label,
                    'antes': str(antes) if antes != '' else '(vazio)',
                    'depois': str(depois) if depois != '' else '(vazio)',
                })

        if alteracoes:
            AuditoriaService.registrar(
                link_id=link_id,
                acao='editado',
                campo_alterado='multiplos' if len(alteracoes) > 1 else alteracoes[0]['campo'],
                valor_antigo=None,
                valor_novo=json.dumps(alteracoes, ensure_ascii=False),
                conexao=conexao,
            )

        conexao.commit()

        return jsonify({
            'success': True,
            'message': f'Link "{dados["titulo"]}" atualizado!',
        }), 200

    except Exception as e:
        conexao.rollback()
        logger.exception(f"Erro ao editar link usuario_id={usuario_id} link_id={link_id}")
        return jsonify({
            'success': False,
            'error': 'Erro interno ao salvar edição.',
            'details': str(e),
        }), 500