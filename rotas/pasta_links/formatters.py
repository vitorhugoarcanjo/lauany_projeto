# rotas\pasta_links\formatters.py
"""FORMATAÇÕES do módulo Links"""

class LinksFormatters:
    """Formatações específicas do módulo Links"""

    @staticmethod
    def formatar_links(links_raw):
        """Formata a lista de links brutos em DICIONÁRIOS para o Jinja/HTML"""
        links = []

        for l in links_raw:
            link_dict = {
                'id': l[0],
                'sequencia_links': l[1],
                'titulo': l[2] or 'Sem título',
                'url': l[3],
                'icone': l[4] or 'fa-link',
                'descricao': l[5] or '',
                'ordem': l[6] or 0,
                'abrir_nova_aba': l[7] if len(l) > 7 else 1,
                'destaque': l[8] if len(l) > 8 else 0,
                'ativo': l[9] if len(l) > 9 else 1,
                'data_criacao': l[10] if len(l) > 10 else None,
            }
            links.append(link_dict)

        return links


    @staticmethod
    def formatar_link_detalhes(link):
        """Formata detalhes de um link (para JSON/API)"""
        if not link:
            return None

        return {
            'id': link[0],
            'sequencia_links': link[1],
            'titulo': link[2] or 'Sem título',
            'url': link[3],
            'icone': link[4] or 'fa-link',
            'descricao': link[5] or '',
            'ordem': link[6] or 0,
            'ativo': link[7] if len(link) > 7 else 1,
        }