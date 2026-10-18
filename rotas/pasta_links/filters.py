"""FILTROS do módulo Links"""


class LinksFilters:
    """Gerencia todos os filtros do módulo Links"""
    PREFIXO = 'links'

    @classmethod
    def salvar_filtros_post(cls, request, session):
        """SALVA filtros do POST na session"""
        session[f'{cls.PREFIXO}_descricao'] = request.form.get('descricao', '')

        mostrar_inativas = request.form.get('mostrar_inativas')
        if mostrar_inativas in ('0', '1', '2'):
            session[f'{cls.PREFIXO}_mostrar_inativas'] = mostrar_inativas
        else:
            session[f'{cls.PREFIXO}_mostrar_inativas'] = '0'

    @classmethod
    def recuperar_filtros(cls, session):
        """RECUPERA filtros da session (SÓ LÊ)"""
        return {
            'descricao': session.get(f'{cls.PREFIXO}_descricao', ''),
            'mostrar_inativas': session.get(f'{cls.PREFIXO}_mostrar_inativas', '0'),
        }

    @classmethod
    def limpar_filtros(cls, session):
        """LIMPA todos os filtros"""
        chaves = ['descricao', 'mostrar_inativas']

        for chave in chaves:
            session.pop(f'{cls.PREFIXO}_{chave}', None)

    @classmethod
    def aplicar_filtros_query(cls, query, params, filtros):
        """APLICA filtros na query SQL"""
        # FILTRO ATIVO/INATIVO
        if filtros.get('mostrar_inativas') == '1':
            query += " AND l.ativo = 0"
        elif filtros.get('mostrar_inativas') == '0':
            query += " AND l.ativo = 1"

        # FILTRO DESCRIÇÃO
        if filtros.get('descricao'):
            query += " AND l.titulo ILIKE %s"
            params.append(f"%{filtros['descricao']}%")

        return query, params