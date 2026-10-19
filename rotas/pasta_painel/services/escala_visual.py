"""
FONTE ÚNICA de escala visual do MeuLinks.

Toda medida que o usuário controla (tamanho, cor, espaçamento, efeito)
tem seu valor canônico AQUI. O preview (JS) e a página pública (CSS SSR)
leem daqui — é fisicamente impossível divergirem.

Regra de fundo:
  - Se o user escolheu cor de fundo diferente do default → cor dele VENCE.
  - Se não escolheu → usa gradiente do template (ou default).

Usado por:
  - utils/config/escala.py (expõe pros templates Jinja)
  - static/js/components/mockup.js (via window.ESCALA)
"""

# ============ MAPAS (valores da PÁGINA REAL) ============
FOTO  = {"pequena": 96,  "medio": 128, "grande": 160}
LINK  = {"pequeno": 48,  "medio": 56,  "grande": 64}
GAP   = {"compacto": 8,  "medio": 14,  "espacoso": 20}
BORDA = {"sem": 0,       "fina": 2,    "media": 3,    "grossa": 4}
RAIO  = {"arredondado": 12, "quadrado": 4, "pilula": 999}

# O mockup é 340px de largura; a página real é 480px.
# Fator ~0.65 faz o preview "caber" mantendo a proporção.
FATOR_PREVIEW = 0.65

FONTE = {
    "padrao": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif",
    "serif": "Georgia, 'Times New Roman', serif",
    "mono": "'Courier New', Consolas, monospace",
    "handwritten": "'Comic Sans MS', 'Caveat', cursive",
}

HOVER = {
    "nenhum":  {"transform": "none",             "filter": "none"},
    "subir":   {"transform": "translateY(-4px)", "filter": "none"},
    "escalar": {"transform": "scale(1.05)",      "filter": "none"},
    "brilho":  {"transform": "none",             "filter": "brightness(1.15)"},
}

ANIMACAO = {"nenhuma": "", "fade": "fade", "slide": "slide", "scale": "scale"}

# ============ FALLBACKS ============
DEFAULTS = {
    "primaria":     "#3b82f6",
    "secundaria":   "#06b6d4",
    "fundo":        "#f5f7fa",
    "texto":        "#1a1a1a",
    "fonte":        "padrao",
    "estilo":       "arredondado",
    "tamanho_foto": "medio",
    "tamanho_link": "medio",
    "gap":          "medio",
    "borda":        "media",
    "hover":        "subir",
    "animacao":     "fade",
}

# ============ LABELS DOS <SELECT> ============
TAMANHOS = {
    "foto":   [("pequena", "Pequena"), ("medio", "Média"), ("grande", "Grande")],
    "link":   [("pequeno", "Pequeno"), ("medio", "Médio"), ("grande", "Grande")],
    "gap":    [("compacto", "Compacto"), ("medio", "Médio"), ("espacoso", "Espaçoso")],
    "borda":  [("sem", "Sem borda"), ("fina", "Fina"), ("media", "Média"), ("grossa", "Grossa")],
    "fonte":  [("padrao", "Padrão"), ("serif", "Serifada"),
               ("mono", "Monospace"), ("handwritten", "Manuscrita")],
    "estilo": [("arredondado", "Arredondado"), ("quadrado", "Quadrado"), ("pilula", "Pílula")],
    "hover":  [("nenhum", "Nenhum"), ("subir", "Subir"),
               ("escalar", "Escalar"), ("brilho", "Brilho")],
    "anim":   [("nenhuma", "Nenhuma"), ("fade", "Fade"),
               ("slide", "Slide"), ("scale", "Scale")],
}


def tabela_js():
    """Serializada no <script>window.ESCALA</script>. JS usa a MESMA tabela."""
    return {
        "FOTO": FOTO, "LINK": LINK, "GAP": GAP, "BORDA": BORDA, "RAIO": RAIO,
        "FONTE": FONTE, "HOVER": HOVER, "ANIMACAO": ANIMACAO, "DEFAULTS": DEFAULTS,
        "FATOR_PREVIEW": FATOR_PREVIEW,
    }


def resolver(config_final, contexto="publica"):
    """
    Recebe config_final (merge template+user) e devolve dict de CSS custom
    properties. Usado IGUALZINHO pelo mockup (Jinja) e pela página pública.

    contexto='publica' → valores reais (128px, 56px, 14px...)
    contexto='preview' → valores * FATOR_PREVIEW (83px, 36px, 9px...)
    """
    fator = FATOR_PREVIEW if contexto == "preview" else 1.0

    def px(valor):
        return f"{round(valor * fator)}px"

    cfg = config_final or {}
    c = cfg.get("cores", {}) or {}
    t = cfg.get("tipografia", {}) or {}
    l = cfg.get("layout", {}) or {}
    e = cfg.get("efeitos", {}) or {}

    primaria   = c.get("primaria")   or DEFAULTS["primaria"]
    secundaria = c.get("secundaria") or DEFAULTS["secundaria"]
    fundo      = c.get("fundo")      or DEFAULTS["fundo"]
    texto      = c.get("texto")      or DEFAULTS["texto"]

    fonte_slug  = t.get("fonte")         or DEFAULTS["fonte"]
    estilo_slug = t.get("estilo_botao")  or DEFAULTS["estilo"]

    foto_slug  = l.get("tamanho_foto")      or DEFAULTS["tamanho_foto"]
    link_slug  = l.get("tamanho_link")      or DEFAULTS["tamanho_link"]
    gap_slug   = l.get("espacamento_links") or DEFAULTS["gap"]
    borda_slug = l.get("borda_link")        or DEFAULTS["borda"]

    hover_slug = e.get("hover_efeito")     or DEFAULTS["hover"]

    hover = HOVER.get(hover_slug, HOVER[DEFAULTS["hover"]])

    # FUNDO EFETIVO
    # - Se o user escolheu cor (diferente do default) → cor dele VENCE.
    # - Senão → gradiente do template (se houver) ou default.
    if fundo != DEFAULTS["fundo"]:
        fundo_efetivo = fundo
    else:
        fundo_efetivo = e.get("background") or fundo

    return {
        "--perfil-cor-primaria":       primaria,
        "--perfil-cor-secundaria":     secundaria,
        "--perfil-cor-fundo":          fundo,
        "--perfil-cor-texto":          texto,
        "--perfil-background-efetivo": fundo_efetivo,
        "--perfil-fonte":              FONTE.get(fonte_slug, FONTE["padrao"]),
        "--perfil-raio-link":          px(RAIO.get(estilo_slug, RAIO["arredondado"])),
        "--perfil-foto-tamanho":       px(FOTO.get(foto_slug, FOTO["medio"])),
        "--perfil-link-tamanho":       px(LINK.get(link_slug, LINK["medio"])),
        "--perfil-gap":                px(GAP.get(gap_slug, GAP["medio"])),
        "--perfil-borda-tamanho":      px(BORDA.get(borda_slug, BORDA["media"])),
        "--perfil-hover-transform":    hover["transform"],
        "--perfil-hover-brilho":       hover["filter"],
    }


def resolver_meta(config_final):
    """Metadados não-CSS (classe de animação pro container)."""
    e = (config_final or {}).get("efeitos", {}) or {}
    slug = e.get("animacao_entrada") or DEFAULTS["animacao"]
    return {"animacao": ANIMACAO.get(slug, "fade")}


def vars_para_style(config_final, contexto="publica"):
    """Serializa pro atributo style=\"\" do Jinja."""
    return " ".join(
        f"{k}: {v};" for k, v in resolver(config_final, contexto).items()
    )