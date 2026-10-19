"""APARÊNCIA — Validações (usa jsonschema)"""

import re
from utils.config.schema import validar_config


# ==========================================================
# VALORES VÁLIDOS (fallback se o schema falhar)
# ==========================================================
def validar_template_slug(slug):
    """Valida se o slug não está vazio (o banco valida se existe)."""
    if not slug or not slug.strip():
        return 'cosmic'
    return slug.strip()


def validar_cor(cor):
    if not cor:
        return True
    return bool(re.match(r'^#[0-9a-fA-F]{6}$', cor))


# Re-exporta a validação do config (usada na view)
__all__ = ['validar_template_slug', 'validar_cor', 'validar_config']