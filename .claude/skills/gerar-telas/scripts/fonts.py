"""Caminho das fontes Open Sans que vêm dentro da skill (assets/fonts/, licença SIL OFL 1.1 em OFL.txt).

Uso:
    from fonts import caminho_fonte
    caminho_fonte()               # OpenSans-Bold.ttf (título e corpo)
    caminho_fonte("ExtraBold")    # OpenSans-ExtraBold.ttf (legenda do QR)
"""
from __future__ import annotations

from pathlib import Path

FONT_DIR = Path(__file__).resolve().parent.parent / "assets" / "fonts"
PESOS = ("Bold", "ExtraBold")


def caminho_fonte(peso: str = "Bold") -> Path:
    """Retorna o caminho da Open Sans no peso pedido."""
    if peso not in PESOS:
        raise ValueError(f"Peso desconhecido: {peso!r} (use um de {PESOS})")
    destino = FONT_DIR / f"OpenSans-{peso}.ttf"
    if not destino.is_file():
        raise FileNotFoundError(f"Fonte não encontrada: {destino} (reinstale a skill)")
    return destino
