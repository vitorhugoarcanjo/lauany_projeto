# rotas/pasta_links/crud/pasta_insert/insert_link.py
"""INSERIR LINK — View"""

import logging
import json
from flask import request, session, jsonify, render_template

from rotas.middleware.autenticacao import login_required
from rotas.auditoria_geral.pasta_links.services_auditoria import AuditoriaService
from utils.database.conexao_global import ini_conexao

from .services import InserirLinkService
from .validacoes import validar_dados_insercao

logger = logging.getLogger(__name__)


@login_required
def novo_link_modal():
    """Retorna o HTML do modal de novo link"""
    return render_template('pasta_links/modais/modal_novo_link.html.jinja')


@login_required
def salvar_novo_link():
    """Salva um novo link via JSON"""
    usuario_id = session.get('user_id')
    conexao, cursor = ini_conexao()

    try:
        payload = request.json or {}

        dados = {
            'titulo': (payload.get('titulo') or '').strip(),
            'url': (payload.get('url') or '').strip(),
            'icone': (payload.get('icone') or 'fa-link').strip(),
            'descricao': (payload.get('descricao') or '').strip(),
            'ordem': int(payload.get('ordem') or 0),
            'abrir_nova_aba': 1 if payload.get('abrir_nova_aba', True) else 0,
            'destaque': 1 if payload.get('destaque', False) else 0,
            'cor_especial': (payload.get('cor_especial') or '').strip() or None,
        }

        # Valida
        erros = validar_dados_insercao(dados)
        if erros:
            return jsonify({'success': False, 'errors': erros}), 400

        # Insere
        sucesso, resultado = InserirLinkService.criar_link(cursor, usuario_id, dados)
        if not sucesso:
            conexao.rollback()
            return jsonify({'success': False, 'error': resultado}), 400

        link_id = resultado.get('link_id')

        # Auditoria — captura todos os campos
        alteracoes = [
            {'campo': 'Título', 'depois': dados['titulo']},
            {'campo': 'URL', 'depois': dados['url']},
            {'campo': 'Ícone', 'depois': dados['icone']},
            {'campo': 'Descrição', 'depois': dados['descricao'] or '(vazio)'},
            {'campo': 'Ordem', 'depois': str(dados['ordem'])},
            {'campo': 'Nova aba', 'depois': 'Sim' if dados['abrir_nova_aba'] else 'Não'},
            {'campo': 'Destaque', 'depois': 'Sim' if dados['destaque'] else 'Não'},
        ]

        AuditoriaService.registrar(
            link_id=link_id,
            acao='criado',
            campo_alterado='multiplos',
            valor_antigo=None,
            valor_novo=json.dumps(alteracoes, ensure_ascii=False),
            conexao=conexao,
        )

        conexao.commit()

        return jsonify({
            'success': True,
            'message': f'Link "{dados["titulo"]}" criado com sucesso!',
            'sequencia': resultado.get('sequencia'),
            'link_id': link_id,
        }), 201

    except Exception as e:
        conexao.rollback()
        logger.exception(f"Erro ao salvar novo link usuario_id={usuario_id}")
        return jsonify({
            'success': False,
            'error': 'Erro interno ao salvar o link.',
            'details': str(e),
        }), 500