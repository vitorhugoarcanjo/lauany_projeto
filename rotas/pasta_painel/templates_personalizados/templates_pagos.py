"""Templates pagos (premium) — futuro"""

# ==========================================================
# TEMPLATES PAGOS (futuro)
# ==========================================================
# Quando criar templates pagos, adicionar aqui:
#
# TEMPLATES_PAGOS = [
#     {
#         "slug": "premium-gold",
#         "nome": "Premium Gold",
#         "descricao": "Dourado e preto. Luxo.",
#         "categoria": "premium",
#         "ordem": 100,
#         "config_default": { ... },
#     },
# ]
#
# E adicionar `popular_templates_pagos(cursor)` (mesma estrutura do padrões).


TEMPLATES_PAGOS = []


def popular_templates_pagos(cursor):
    """Insere os templates pagos (se houver)."""
    if not TEMPLATES_PAGOS:
        return  # Nada a inserir

    for t in TEMPLATES_PAGOS:
        cursor.execute("""
            INSERT INTO templates (slug, nome, descricao, categoria, ordem, config_default)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (slug) DO NOTHING
        """, (
            t["slug"], t["nome"], t["descricao"],
            t["categoria"], t["ordem"],
            json.dumps(t["config_default"]),
        ))
    print(f"✅ {len(TEMPLATES_PAGOS)} templates pagos inseridos")