"""Renderiza as telas do Brooklin em Pauta a partir de um JSON.

Formato do JSON:
    {
      "data": "2026-10-31",
      "telas": [
        {"arquivo": "02-culto-domingo", "titulo": "Série Coração e Mente",
         "corpo": "Amanhã, às 10h, o pastor José Orlando ..."}
      ]
    }

Pasta de saída padrão: <Downloads do usuário>/Telas <data>/

Uso (Windows; no Linux troque `py` por `python3`):
    py scripts\\render.py --pasta 2026-10-31     # cria e mostra a pasta padrão da edição
    py scripts\\render.py telas.json             # gera em Downloads\\Telas <data>\\
    py scripts\\render.py telas.json -o pasta    # gera em outra pasta
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
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
    sys.exit(f"Pillow não está instalado. Rode:  {_py} -m pip install pillow")

_SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPTS))
# segno embutido tem prioridade: mesma versão (e mesmo QR) em qualquer ambiente.
sys.path.insert(0, str(_SCRIPTS / "vendor"))
from fonts import ensure_font  # noqa: E402

SKILL_DIR = _SCRIPTS.parent
ASSETS = SKILL_DIR / "assets"

# Pasta de saída do ambiente do Claude App / claude.ai (arquivos que o usuário pode baixar).
SAIDA_APP = Path("/mnt/user-data/outputs")


def pasta_base() -> Path:
    """Onde criar 'Telas <data>': Downloads do usuário; no ambiente do app, a pasta de saída dele."""
    downloads = pasta_downloads()
    if downloads.is_dir():
        return downloads
    if SAIDA_APP.is_dir():
        return SAIDA_APP
    return Path.cwd()


def pasta_downloads() -> Path:
    """Pasta Downloads real do usuário (respeita redirecionamento/idioma do sistema)."""
    if sys.platform == "win32":
        try:
            import winreg
            chave = r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, chave) as k:
                valor, _ = winreg.QueryValueEx(k, "{374DE290-123F-4655-A0B3-A3D3A2BFC2E0}")
            return Path(os.path.expandvars(valor))
        except OSError:
            pass
    elif shutil.which("xdg-user-dir"):
        try:
            r = subprocess.run(["xdg-user-dir", "DOWNLOAD"], capture_output=True, text=True, timeout=5)
            caminho = Path(r.stdout.strip())
            if r.returncode == 0 and caminho.is_absolute() and caminho != Path.home():
                return caminho
        except (OSError, subprocess.SubprocessError):
            pass
    return Path.home() / "Downloads"


def pasta_padrao(data: str) -> Path:
    return pasta_base() / f"Telas {data}"

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

# Bloco de QR personalizado (coordenadas relativas a QR_POS; mesmas medidas do qr-visitante.png)
QR_BLOCO = (279, 363)
QR_AREA = (7, 10, 264)          # x, y e lado da área branca onde fica o código
QR_ZONA = 1                     # margem branca em módulos (a caixa azul completa o respiro)
QR_MODULO_MIN = 4               # px por módulo; abaixo disso fica difícil de ler na transmissão
QR_LOGO_QUADRADO = 0.28         # lado do quadrado branco central em relação ao código
QR_LOGO_PREENCHE = 0.86         # quanto do quadrado o logo ocupa (o resto é respiro)
LEGENDA_AREA = (10, 280, 269, 356)  # x0, y0, x1, y1 da legenda abaixo do código
LEGENDA_SIZES = range(26, 17, -1)
LEGENDA_UMA_LINHA_MIN = 22      # prefere 1 linha se couber pelo menos neste tamanho
LEGENDA_MAX_LINES = 2


def fonte(font_path: Path, size: int) -> ImageFont.FreeTypeFont:
    """Carrega a fonte sempre com o layout BASIC.

    O Pillow usa o layout RAQM quando a libraqm existe (comum no Linux) e o BASIC quando
    não existe (padrão no Windows). Os dois medem o texto de forma diferente, o que mudaria
    quebras de linha e larguras entre os sistemas. Forçar o BASIC deixa as telas idênticas.
    """
    return ImageFont.truetype(str(font_path), size, layout_engine=ImageFont.Layout.BASIC)


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
        font = fonte(font_path, size)
        linhas = quebrar(texto, font, largura)
        if len(linhas) <= BODY_MAX_LINES and all(font.getlength(l) <= largura for l in linhas):
            return font, linhas
    raise ValueError(
        f"Corpo longo demais para {BODY_MAX_LINES} linhas mesmo em {BODY_SIZES[-1]}px: {texto!r}"
    )


def gerar_codigo_qr(link: str) -> Image.Image:
    """QR estático com o link exato (sem encurtador/redirecionamento) e o logo no centro."""
    if not re.fullmatch(r"https?://\S+", link or ""):
        raise ValueError(f"Link inválido (precisa começar com http:// ou https://): {link!r}")
    import segno  # cópia embutida em scripts/vendor (sem pip/internet)

    # Nível Q (25% de redundância): cobre o logo central com folga e gera menos módulos
    # que o H, deixando os quadradinhos maiores. (M falha com logo um pouco maior.)
    qr = segno.make(link, error="q", micro=False, boost_error=False)
    n = qr.symbol_size(border=0)[0]
    _, _, lado = QR_AREA
    # Módulo fracionário: o código preenche a área branca como no QR original.
    modulo = lado / (n + 2 * QR_ZONA)
    if modulo < QR_MODULO_MIN:
        raise ValueError(f"Link longo demais para um QR legível na tela ({len(link)} caracteres): {link!r}")

    img = Image.new("RGBA", (lado, lado), BRANCO)
    d = ImageDraw.Draw(img)
    off = QR_ZONA * modulo
    pos = lambda i: round(off + i * modulo)  # noqa: E731 — bordas arredondadas, sem frestas
    for y, linha in enumerate(qr.matrix_iter(scale=1, border=0)):
        for x, escuro in enumerate(linha):
            if escuro:
                d.rectangle([pos(x), pos(y), pos(x + 1) - 1, pos(y + 1) - 1], fill=(0, 0, 0, 255))

    # Logo no centro: quadrado branco 1:1 com o logo centralizado dentro dele
    quadrado = round(n * modulo * QR_LOGO_QUADRADO)
    q0 = (lado - quadrado) // 2
    d.rectangle([q0, q0, q0 + quadrado - 1, q0 + quadrado - 1], fill=BRANCO)
    logo = Image.open(ASSETS / "logo-qr.png").convert("RGBA")
    logo = logo.crop(logo.getbbox())  # remove a sobra transparente do arquivo
    logo.thumbnail((round(quadrado * QR_LOGO_PREENCHE),) * 2, Image.LANCZOS)
    img.alpha_composite(logo, ((lado - logo.width) // 2, (lado - logo.height) // 2))
    return img


def ajustar_legenda(texto: str, font_path: Path):
    """Uma linha se couber num tamanho bom; senão, até 2 linhas, reduzindo a fonte."""
    x0, _, x1, _ = LEGENDA_AREA
    largura = x1 - x0
    fontes = [fonte(font_path, s) for s in LEGENDA_SIZES]
    for font in fontes:
        if font.size >= LEGENDA_UMA_LINHA_MIN and font.getlength(texto) <= largura:
            return font, [texto]
    for font in fontes:
        linhas = quebrar(texto, font, largura)
        if len(linhas) <= LEGENDA_MAX_LINES and all(font.getlength(l) <= largura for l in linhas):
            return font, linhas
    raise ValueError(f"Legenda do QR longa demais para {LEGENDA_MAX_LINES} linhas: {texto!r}")


def render_bloco_qr(link: str, legenda: str) -> Image.Image:
    """Bloco no mesmo formato do QR de visitante: caixa azul, QR e legenda branca (ExtraBold)."""
    legenda = " ".join((legenda or "").split()).upper()
    if not legenda:
        raise ValueError(f"QR sem legenda: {link!r}")
    bloco = Image.new("RGBA", QR_BLOCO, AZUL)
    ax, ay, _ = QR_AREA
    bloco.alpha_composite(gerar_codigo_qr(link), (ax, ay))

    font, linhas = ajustar_legenda(legenda, ensure_font("ExtraBold"))
    x0, y0, x1, y1 = LEGENDA_AREA
    passo = font.size * 1.2
    cy = (y0 + y1) / 2 - passo * (len(linhas) - 1) / 2
    d = ImageDraw.Draw(bloco)
    for i, linha in enumerate(linhas):
        d.text(((x0 + x1) / 2, cy + i * passo), linha, font=font, fill=BRANCO, anchor="mm")
    return bloco


def render_tela(titulo: str, corpo: str, font_path: Path, qr: dict | None = None) -> Image.Image:
    """Monta a tela. `qr` = {"link": ..., "legenda": ...}; sem ele usa o QR de visitante."""
    titulo, corpo = titulo.strip().upper(), " ".join(corpo.split()).upper()
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    img.alpha_composite(Image.open(ASSETS / "logo-brooklin.png").convert("RGBA"), LOGO_POS)
    if qr:
        img.alpha_composite(render_bloco_qr(qr.get("link"), qr.get("legenda")), QR_POS)
    else:
        img.alpha_composite(Image.open(ASSETS / "qr-visitante.png").convert("RGBA"), QR_POS)
    d = ImageDraw.Draw(img)
    d.rectangle(FAIXA, fill=BRANCO)

    # Título + barra com largura proporcional ao texto
    f_tit = fonte(font_path, TITLE_SIZE)
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
    ap.add_argument("json", type=Path, nargs="?", help="JSON com as telas")
    ap.add_argument("-o", "--saida", type=Path, help="pasta de saída (padrão: Downloads/Telas <data>)")
    ap.add_argument("--pasta", metavar="AAAA-MM-DD", help="só cria e mostra a pasta padrão da edição")
    args = ap.parse_args(argv)

    if args.pasta:
        pasta = pasta_padrao(args.pasta)
        pasta.mkdir(parents=True, exist_ok=True)
        print(pasta)
        return 0
    if not args.json:
        ap.error("informe o JSON das telas ou --pasta AAAA-MM-DD")

    # utf-8-sig: aceita JSON salvo pelo Bloco de Notas do Windows (com BOM)
    dados = json.loads(args.json.read_text(encoding="utf-8-sig"))
    saida = args.saida or pasta_padrao(dados.get("data", "sem-data"))
    saida.mkdir(parents=True, exist_ok=True)
    # Guarda os textos usados junto das telas, para refazer/ajustar depois.
    registro = saida / "telas.json"
    if args.json.resolve() != registro.resolve():
        shutil.copyfile(args.json, registro)
    font_path = ensure_font()

    erros, geradas = 0, []
    for i, t in enumerate(dados["telas"], 1):
        nome = t.get("arquivo") or f"{i:02d}-{slugify(t['titulo'])}"
        try:
            destino = saida / f"{nome}.png"
            tela = render_tela(t["titulo"], t["corpo"], font_path, t.get("qr"))
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
