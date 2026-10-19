"""Templates padrão (gratuitos) — seed da tabela templates"""

import json


TEMPLATES_PADRAO = [
    {
        "slug": "wellness",
        "nome": "Wellness",
        "descricao": "Tons suaves de rosa, verde e branco. Ideal pra nutrição, saúde e bem-estar.",
        "categoria": "gratuito",
        "ordem": 1,
        "config_default": {
            "cores": {
                "primaria": "#ec4899",
                "secundaria": "#25d366",
                "fundo": "#fdf2f8",
                "texto": "#1e293b",
                "botao": None,
            },
            "tipografia": {
                "fonte": "padrao",
                "estilo_botao": "arredondado",
            },
            "layout": {
                "tamanho_foto": "medio",
                "tamanho_link": "medio",
                "espacamento_links": "medio",
                "borda_link": "media",
            },
            "efeitos": {
                "hover_efeito": "subir",
                "animacao_entrada": "fade",
                "background": "linear-gradient(135deg, #fdf2f8 0%, #f8fafc 50%, #ecfdf5 100%)",
            },
        },
    },
    {
        "slug": "cosmic",
        "nome": "Cosmic",
        "descricao": "Fundo escuro com azul elétrico. Moderno e tech.",
        "categoria": "gratuito",
        "ordem": 2,
        "config_default": {
            "cores": {
                "primaria": "#3b82f6",
                "secundaria": "#06b6d4",
                "fundo": "#0a0f1e",
                "texto": "#f0f0f0",
                "botao": None,
            },
            "tipografia": {
                "fonte": "padrao",
                "estilo_botao": "arredondado",
            },
            "layout": {
                "tamanho_foto": "medio",
                "tamanho_link": "medio",
                "espacamento_links": "medio",
                "borda_link": "media",
            },
            "efeitos": {
                "hover_efeito": "subir",
                "animacao_entrada": "fade",
                "background": "linear-gradient(135deg, #0a0f1e 0%, #121a2e 50%, #1a1b41 100%)",
            },
        },
    },
    {
        "slug": "fresh",
        "nome": "Fresh",
        "descricao": "Verde claro e ciano. Sensação de frescor.",
        "categoria": "gratuito",
        "ordem": 3,
        "config_default": {
            "cores": {
                "primaria": "#10b981",
                "secundaria": "#06b6d4",
                "fundo": "#f0fdf4",
                "texto": "#064e3b",
                "botao": None,
            },
            "tipografia": {
                "fonte": "padrao",
                "estilo_botao": "arredondado",
            },
            "layout": {
                "tamanho_foto": "medio",
                "tamanho_link": "medio",
                "espacamento_links": "medio",
                "borda_link": "media",
            },
            "efeitos": {
                "hover_efeito": "subir",
                "animacao_entrada": "fade",
                "background": "linear-gradient(135deg, #f0fdf4 0%, #ecfeff 100%)",
            },
        },
    },
    {
        "slug": "classic",
        "nome": "Classic",
        "descricao": "Cinza e azul escuro. Sóbrio e profissional.",
        "categoria": "gratuito",
        "ordem": 4,
        "config_default": {
            "cores": {
                "primaria": "#1e40af",
                "secundaria": "#64748b",
                "fundo": "#f8fafc",
                "texto": "#0f172a",
                "botao": None,
            },
            "tipografia": {
                "fonte": "padrao",
                "estilo_botao": "arredondado",
            },
            "layout": {
                "tamanho_foto": "medio",
                "tamanho_link": "medio",
                "espacamento_links": "medio",
                "borda_link": "media",
            },
            "efeitos": {
                "hover_efeito": "subir",
                "animacao_entrada": "fade",
                "background": "linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%)",
            },
        },
    },
    {
        "slug": "sunset",
        "nome": "Sunset",
        "descricao": "Laranja e rosa. Pôr do sol quente.",
        "categoria": "gratuito",
        "ordem": 5,
        "config_default": {
            "cores": {
                "primaria": "#f97316",
                "secundaria": "#ec4899",
                "fundo": "#fff7ed",
                "texto": "#431407",
                "botao": None,
            },
            "tipografia": {
                "fonte": "padrao",
                "estilo_botao": "arredondado",
            },
            "layout": {
                "tamanho_foto": "medio",
                "tamanho_link": "medio",
                "espacamento_links": "medio",
                "borda_link": "media",
            },
            "efeitos": {
                "hover_efeito": "subir",
                "animacao_entrada": "fade",
                "background": "linear-gradient(135deg, #fff7ed 0%, #fef3c7 50%, #fce7f3 100%)",
            },
        },
    },
]


def popular_templates_padroes(cursor):
    """Insere os 5 templates padrão (se a tabela tiver vazia)."""
    cursor.execute("SELECT COUNT(*) FROM templates")
    total = cursor.fetchone()[0]

    if total > 0:
        print(f"ℹ️ Tabela templates já tem {total} templates. Nada a inserir.")
        return

    for t in TEMPLATES_PADRAO:
        cursor.execute("""
            INSERT INTO templates (slug, nome, descricao, categoria, ordem, config_default)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            t["slug"], t["nome"], t["descricao"],
            t["categoria"], t["ordem"],
            json.dumps(t["config_default"]),
        ))

    print(f"✅ {len(TEMPLATES_PADRAO)} templates padrão inseridos")