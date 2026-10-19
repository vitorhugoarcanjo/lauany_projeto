"""UTILS — Merge recursivo de dicionários (JSON)"""


def merge_recursivo(base, override):
    """
    Merge recursivo de dois dicts.
    - base: dicionário padrão (do template)
    - override: dicionário do usuário (sobrescreve)
    
    Retorna: dict (base + override, com override ganhando)
    """
    resultado = dict(base) if base else {}

    for k, v in (override or {}).items():
        if isinstance(v, dict) and isinstance(resultado.get(k), dict):
            resultado[k] = merge_recursivo(resultado[k], v)
        else:
            resultado[k] = v

    return resultado