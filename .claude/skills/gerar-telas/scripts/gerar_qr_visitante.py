"""Regenera o arquivo fixo assets/qr-visitante.png (QR padrão das telas).

O QR de visitante é um arquivo fixo: o render.py só o cola na tela. Rode este script
apenas quando o link ou a legenda mudarem (ou o visual do bloco de QR):

    py scripts/gerar_qr_visitante.py          (Linux: python3 ...)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import render  # noqa: E402

LINK = "https://typebot.co/my-typebot-a6oemdd"
LEGENDA = "Visitando nossa igreja pela 1ª vez?"
DESTINO = render.ASSETS / "qr-visitante.png"


def main() -> int:
    render.render_bloco_qr(LINK, LEGENDA).save(DESTINO)
    print(DESTINO)
    return 0


if __name__ == "__main__":
    sys.exit(main())
