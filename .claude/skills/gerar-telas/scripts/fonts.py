"""Garante que a fonte Open Sans esteja disponível localmente (Bold e ExtraBold).

Uso como módulo:
    from fonts import ensure_font
    ensure_font()               # Path para OpenSans-Bold.ttf (título e corpo)
    ensure_font("ExtraBold")    # Path para OpenSans-ExtraBold.ttf (legenda do QR)

Uso direto (pré-baixar as fontes):
    py scripts/fonts.py
"""
from __future__ import annotations

import sys
import urllib.request
from pathlib import Path

FONT_DIR = Path(__file__).resolve().parent.parent / "assets" / "fonts"
PESOS = ("Bold", "ExtraBold")

# Repositório oficial da Open Sans (licença SIL OFL 1.1), arquivos estáticos.
URL_BASES = [
    "https://github.com/googlefonts/opensans/raw/main/fonts/ttf/",
    "https://raw.githubusercontent.com/googlefonts/opensans/main/fonts/ttf/",
]
MIN_SIZE = 50_000  # bytes; evita aceitar uma página de erro como se fosse a fonte

# Compatibilidade: caminho da Bold, usado por código/testes antigos.
FONT_FILE = FONT_DIR / "OpenSans-Bold.ttf"


def _is_valid(path: Path) -> bool:
    if not path.is_file() or path.stat().st_size < MIN_SIZE:
        return False
    with path.open("rb") as f:
        return f.read(4) in (b"\x00\x01\x00\x00", b"true", b"OTTO")


def ensure_font(peso: str = "Bold") -> Path:
    """Retorna o caminho da Open Sans no peso pedido, baixando-a na primeira execução."""
    if peso not in PESOS:
        raise ValueError(f"Peso desconhecido: {peso!r} (use um de {PESOS})")
    nome = f"OpenSans-{peso}.ttf"
    destino = FONT_DIR / nome
    if _is_valid(destino):
        return destino

    FONT_DIR.mkdir(parents=True, exist_ok=True)
    tmp = destino.with_suffix(".part")
    errors = []
    for base in URL_BASES:
        url = base + nome
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "bp-telas-font-fetcher"})
            with urllib.request.urlopen(req, timeout=30) as resp, tmp.open("wb") as out:
                out.write(resp.read())
            if _is_valid(tmp):
                tmp.replace(destino)
                return destino
            errors.append(f"{url}: arquivo inválido")
        except Exception as exc:  # rede, HTTP, permissão...
            errors.append(f"{url}: {exc}")
    tmp.unlink(missing_ok=True)
    raise RuntimeError(
        f"Não foi possível baixar a Open Sans {peso}.\n"
        + "\n".join(errors)
        + f"\nBaixe manualmente e salve em: {destino}"
    )


if __name__ == "__main__":
    try:
        for p in PESOS:
            print(ensure_font(p))
    except RuntimeError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
