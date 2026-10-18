"""APARÊNCIA — Validações"""

import re

TEMAS_VALIDOS = {'claro', 'escuro', 'cosmic'}
FONTES_VALIDAS = {'padrao', 'serif', 'mono', 'handwritten'}
ESTILOS_BOTAO_VALIDOS = {'arredondado', 'quadrado', 'pilula'}
TEMPLATES_VALIDOS = {'wellness', 'cosmic', 'fresh', 'classic', 'sunset'}
TAMANHOS_FOTO_VALIDOS = {'pequena', 'medio', 'grande'}
TAMANHOS_LINK_VALIDOS = {'pequeno', 'medio', 'grande'}
ESPACAMENTOS_VALIDOS = {'compacto', 'medio', 'espacoso'}
BORDAS_VALIDAS = {'sem', 'fina', 'media', 'grossa'}
HOVERS_VALIDOS = {'nenhum', 'subir', 'escalar', 'brilho'}
ANIMACOES_VALIDAS = {'nenhuma', 'fade', 'slide', 'scale'}


def cor_valida(cor):
    if not cor:
        return True
    return bool(re.match(r'^#[0-9a-fA-F]{6}$', cor))


def validar_tema(tema):
    return tema if tema in TEMAS_VALIDOS else 'claro'


def validar_fonte(fonte):
    return fonte if fonte in FONTES_VALIDAS else 'padrao'


def validar_estilo_botao(estilo):
    return estilo if estilo in ESTILOS_BOTAO_VALIDOS else 'arredondado'


def validar_template(template):
    return template if template in TEMPLATES_VALIDOS else 'cosmic'


def validar_tamanho_foto(tamanho):
    return tamanho if tamanho in TAMANHOS_FOTO_VALIDOS else 'medio'


def validar_tamanho_link(tamanho):
    return tamanho if tamanho in TAMANHOS_LINK_VALIDOS else 'medio'


def validar_espacamento(espacamento):
    return espacamento if espacamento in ESPACAMENTOS_VALIDOS else 'medio'


def validar_borda(borda):
    return borda if borda in BORDAS_VALIDAS else 'media'


def validar_hover(hover):
    return hover if hover in HOVERS_VALIDOS else 'subir'


def validar_animacao(animacao):
    return animacao if animacao in ANIMACOES_VALIDAS else 'fade'


def validar_cores(cor_primaria, cor_secundaria, cor_fundo, cor_texto, cor_botao):
    for nome_campo, cor in [
        ('cor_primaria', cor_primaria),
        ('cor_secundaria', cor_secundaria),
        ('cor_fundo', cor_fundo),
        ('cor_texto', cor_texto),
        ('cor_botao', cor_botao),
    ]:
        if not cor_valida(cor):
            return f'Cor inválida em {nome_campo}.'
    return None