"""Renderiza as telas do Brooklin em Pauta a partir de um JSON.

Formato do JSON:
    {
      "data": "2026-10-31",
      "telas": [
        {"arquivo": "02-culto-domingo", "titulo": "Série Coração e Mente",
         "corpo": "Amanhã, às 10h, o Pr. José Orlando ..."}
      ]
    }

Uso (Windows):
    py scripts\\render.py telas.json            # saída em saida\\<data>\\
    py scripts\\render.py telas.json -o pasta   # saída em pasta\\
Uso (Linux):
    python3 scripts/render.py telas.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

# Consoles do Windows (cp1252) quebram com acentos/aspas curvas: força UTF-8.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    _py = "py" if sys.platform == "win32" else "python3"
    sys.exit(f"Pillow não está instalado. Rode:  {_py} -m pip install -r requirements.txt")

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fonts import ensure_font  # noqa: E402

SKILL_DIR = Path(__file__).resolve().parent.parent
ASSETS = SKILL_DIR / "assets"
PROJECT_DIR = SKILL_DIR.parent.parent.parent  # BP_Telas/

# ---- Especificação (ver references/design-spec.md) ----
W, H = 1920, 1080
AZUL = (0, 51, 102, 255)
BRANCO = (255, 255, 255, 255)

LOGO_POS = (20, 775)
QR_POS = (1617, 608)
FAIXA = (205, 884, 1593, 971)  # faixa branca opaca atrás do corpo (largura fixa)

BAR_X0, BAR_Y0, BAR_Y1 = 205, 776, 862
TITLE_X = 228
TITLE_SIZE = 35
TITLE_PAD_RIGHT = 28
TITLE_MAX_X = 1590

BODY_X = 228
BODY_MAX_X = 1570
BODY_CENTER_Y = 924          # centro vertical do bloco de 2 linhas
BODY_SIZES = range(34, 25, -1)  # exemplos usam 28–35px; tenta do maior para o menor
BODY_LINE_FACTOR = 1.38
BODY_MAX_LINES = 2


def slugify(texto: str) -> str:
    s = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "tela"


def quebrar(texto: str, font: ImageFont.FreeTypeFont, largura: int) -> list[str]:
    linhas, atual = [], ""
    for palavra in texto.split():
        teste = f"{atual} {palavra}".strip()
        if font.getlength(teste) <= largura:
            atual = teste
        else:
            if atual:
                linhas.append(atual)
            atual = palavra
    if atual:
        linhas.append(atual)
    return linhas


def ajustar_corpo(texto: str, font_path: Path):
    largura = BODY_MAX_X - BODY_X
    for size in BODY_SIZES:
        font = ImageFont.truetype(str(font_path), size)
        linhas = quebrar(texto, font, largura)
        if len(linhas) <= BODY_MAX_LINES and all(font.getlength(l) <= largura for l in linhas):
            return font, linhas
    raise ValueError(
        f"Corpo longo demais para {BODY_MAX_LINES} linhas mesmo em {BODY_SIZES[-1]}px: {texto!r}"
    )


def render_tela(titulo: str, corpo: str, font_path: Path) -> Image.Image:
    titulo, corpo = titulo.strip().upper(), " ".join(corpo.split()).upper()
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    img.alpha_composite(Image.open(ASSETS / "logo-brooklin.png").convert("RGBA"), LOGO_POS)
    img.alpha_composite(Image.open(ASSETS / "qr-visitante.png").convert("RGBA"), QR_POS)
    d = ImageDraw.Draw(img)
    d.rectangle(FAIXA, fill=BRANCO)

    # Título + barra com largura proporcional ao texto
    f_tit = ImageFont.truetype(str(font_path), TITLE_SIZE)
    larg_tit = f_tit.getlength(titulo)
    bar_x1 = round(TITLE_X + larg_tit + TITLE_PAD_RIGHT)
    if bar_x1 > TITLE_MAX_X:
        raise ValueError(f"Título longo demais: {titulo!r}")
    d.rectangle([BAR_X0, BAR_Y0, bar_x1, BAR_Y1], fill=AZUL)
    d.text((TITLE_X, (BAR_Y0 + BAR_Y1) / 2), titulo, font=f_tit, fill=BRANCO, anchor="lm")

    # Corpo: até 2 linhas, fonte reduzida até caber
    f_corpo, linhas = ajustar_corpo(corpo, font_path)
    passo = f_corpo.size * BODY_LINE_FACTOR
    y0 = BODY_CENTER_Y - passo * (len(linhas) - 1) / 2
    for i, linha in enumerate(linhas):
        d.text((BODY_X, y0 + i * passo), linha, font=f_corpo, fill=AZUL, anchor="lm")
    return img


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("json", type=Path)
    ap.add_argument("-o", "--saida", type=Path)
    args = ap.parse_args(argv)

    # utf-8-sig: aceita JSON salvo pelo Bloco de Notas do Windows (com BOM)
    dados = json.loads(args.json.read_text(encoding="utf-8-sig"))
    saida = args.saida or PROJECT_DIR / "saida" / dados.get("data", "sem-data")
    saida.mkdir(parents=True, exist_ok=True)
    font_path = ensure_font()

    erros, geradas = 0, []
    for i, t in enumerate(dados["telas"], 1):
        nome = t.get("arquivo") or f"{i:02d}-{slugify(t['titulo'])}"
        try:
            destino = saida / f"{nome}.png"
            tela = render_tela(t["titulo"], t["corpo"], font_path)
            tela.save(destino)
            geradas.append(tela)
            print(destino)
        except ValueError as e:
            erros += 1
            print(f"ERRO [{nome}]: {e}", file=sys.stderr)
    if geradas:
        print(salvar_preview(geradas, saida / "_preview.jpg"))
    return 1 if erros else 0


def salvar_preview(telas: list[Image.Image], destino: Path) -> Path:
    """Folha de conferência: o terço inferior de cada tela sobre fundo cinza.

    O fundo cinza deixa visíveis os elementos brancos (faixa do corpo), que
    sumiriam se a tela transparente fosse vista sobre branco.
    """
    corte = (0, 590, W, 1000)
    alt = corte[3] - corte[1]
    folha = Image.new("RGBA", (W, alt * len(telas)), (128, 128, 128, 255))
    for i, t in enumerate(telas):
        folha.alpha_composite(t.crop(corte), (0, i * alt))
    folha.convert("RGB").save(destino, quality=85)
    return destino


if __name__ == "__main__":
    sys.exit(main())
