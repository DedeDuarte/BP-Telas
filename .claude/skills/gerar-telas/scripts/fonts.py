"""Garante que a fonte Open Sans Bold esteja disponível localmente.

Uso como módulo:
    from fonts import ensure_font
    caminho = ensure_font()          # Path para OpenSans-Bold.ttf

Uso direto (pré-baixar a fonte):
    python scripts/fonts.py
"""
from __future__ import annotations

import sys
import urllib.request
from pathlib import Path

FONT_DIR = Path(__file__).resolve().parent.parent / "assets" / "fonts"
FONT_FILE = FONT_DIR / "OpenSans-Bold.ttf"

# Repositório oficial da Open Sans (licença SIL OFL 1.1), arquivo estático Bold.
FONT_URLS = [
    "https://github.com/googlefonts/opensans/raw/main/fonts/ttf/OpenSans-Bold.ttf",
    "https://raw.githubusercontent.com/googlefonts/opensans/main/fonts/ttf/OpenSans-Bold.ttf",
]
MIN_SIZE = 50_000  # bytes; evita aceitar uma página de erro como se fosse a fonte


def _is_valid(path: Path) -> bool:
    if not path.is_file() or path.stat().st_size < MIN_SIZE:
        return False
    with path.open("rb") as f:
        return f.read(4) in (b"\x00\x01\x00\x00", b"true", b"OTTO")


def ensure_font() -> Path:
    """Retorna o caminho da Open Sans Bold, baixando-a na primeira execução."""
    if _is_valid(FONT_FILE):
        return FONT_FILE

    FONT_DIR.mkdir(parents=True, exist_ok=True)
    tmp = FONT_FILE.with_suffix(".part")
    errors = []
    for url in FONT_URLS:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "bp-telas-font-fetcher"})
            with urllib.request.urlopen(req, timeout=30) as resp, tmp.open("wb") as out:
                out.write(resp.read())
            if _is_valid(tmp):
                tmp.replace(FONT_FILE)
                return FONT_FILE
            errors.append(f"{url}: arquivo inválido")
        except Exception as exc:  # rede, HTTP, permissão...
            errors.append(f"{url}: {exc}")
    tmp.unlink(missing_ok=True)
    raise RuntimeError(
        "Não foi possível baixar a Open Sans Bold.\n"
        + "\n".join(errors)
        + f"\nBaixe manualmente e salve em: {FONT_FILE}"
    )


if __name__ == "__main__":
    try:
        print(ensure_font())
    except RuntimeError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
