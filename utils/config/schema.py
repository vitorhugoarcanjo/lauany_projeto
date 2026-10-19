"""UTILS — Schema JSON do config (perfis.config)"""

import jsonschema
import logging

logger = logging.getLogger(__name__)


# ==========================================================
# SCHEMA DO CONFIG
# ==========================================================
SCHEMA_CONFIG = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "cores": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "primaria":   {"type": "string", "pattern": "^#[0-9a-fA-F]{6}$"},
                "secundaria": {"type": "string", "pattern": "^#[0-9a-fA-F]{6}$"},
                "fundo":      {"type": "string", "pattern": "^#[0-9a-fA-F]{6}$"},
                "texto":      {"type": "string", "pattern": "^#[0-9a-fA-F]{6}$"},
                "botao":      {"type": "string", "pattern": "^#[0-9a-fA-F]{6}$"},
            },
        },
        "tipografia": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "fonte":        {"enum": ["padrao", "serif", "mono", "handwritten"]},
                "estilo_botao": {"enum": ["arredondado", "quadrado", "pilula"]},
            },
        },
        "layout": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "tamanho_foto":       {"enum": ["pequena", "medio", "grande"]},
                "tamanho_link":       {"enum": ["pequeno", "medio", "grande"]},
                "espacamento_links":  {"enum": ["compacto", "medio", "espacoso"]},
                "borda_link":         {"enum": ["sem", "fina", "media", "grossa"]},
            },
        },
        "efeitos": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "hover_efeito":      {"enum": ["nenhum", "subir", "escalar", "brilho"]},
                "animacao_entrada":  {"enum": ["nenhuma", "fade", "slide", "scale"]},
                # ⬇️ opcional — compatibilidade com POST antigo que mandava background
                "background":        {"type": "string"},
            },
        },
    },
}


# ==========================================================
# FUNÇÃO DE VALIDAÇÃO
# ==========================================================
def validar_config(config):
    """
    Valida o config contra o schema JSON.

    Retorna:
        (config_valido, erro)
        - config_valido: dict (config validado)
        - erro: str (mensagem) ou None
    """
    if not config:
        return {}, None

    try:
        jsonschema.validate(instance=config, schema=SCHEMA_CONFIG)
        return config, None
    except jsonschema.ValidationError as e:
        caminho = " → ".join(str(p) for p in e.path) if e.path else "raiz"
        return None, f'Config inválido em "{caminho}": {e.message}'
    except Exception as e:
        logger.exception(f"Erro ao validar config: {e}")
        return None, 'Erro ao validar configuração.'