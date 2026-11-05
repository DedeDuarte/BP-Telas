"""Testes do renderizador de telas. Rodar da raiz: py -m unittest discover tests"""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "gerar-telas" / "scripts"))

import render  # noqa: E402
from fonts import ensure_font  # noqa: E402

AZUL = render.AZUL[:3]


def altura_do_texto(img):
    """Altura (px) do bloco de texto azul desenhado dentro da faixa branca."""
    x0, y0, x1, y1 = render.FAIXA
    px = img.load()
    ys = [
        y for y in range(y0, y1 + 1)
        if any(px[x, y][:3] != (255, 255, 255) for x in range(x0 + 1, x1))
    ]
    return ys[-1] - ys[0] + 1 if ys else 0


def numero_de_linhas(img):
    # Uma linha (com acentos/descendentes) mede < 50 px; duas medem > 55 px.
    return 1 if altura_do_texto(img) < 50 else 2


class TestRender(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.font = ensure_font()

    def test_corpo_de_uma_linha(self):
        img = render.render_tela("Culto de Quarta", "Hoje, às 19h30. Esperamos você!", self.font)
        self.assertEqual(numero_de_linhas(img), 1)
        _, linhas = render.ajustar_corpo("HOJE, ÀS 19H30. ESPERAMOS VOCÊ!", self.font)
        self.assertEqual(len(linhas), 1)

    def test_corpo_de_duas_linhas(self):
        corpo = ("Amanhã, às 10h, o Pr. José Orlando encerra a série “Coração e Mente” "
                 "com a mensagem “Mente e Coração Saudáveis”. Esperamos você!")
        img = render.render_tela("Culto de Domingo", corpo, self.font)
        self.assertEqual(numero_de_linhas(img), 2)

    def test_corpo_longo_demais(self):
        with self.assertRaises(ValueError):
            render.render_tela("Teste", "palavra " * 80, self.font)

    def test_titulo_longo_demais(self):
        with self.assertRaises(ValueError):
            render.render_tela("título " * 40, "Corpo curto.", self.font)

    def test_canvas_e_elementos_fixos(self):
        img = render.render_tela("Secretaria", "Corpo curto.", self.font)
        self.assertEqual((img.size, img.mode), ((1920, 1080), "RGBA"))
        self.assertEqual(img.getpixel((5, 5))[3], 0)            # fundo transparente
        self.assertEqual(img.getpixel((210, 960)), (255, 255, 255, 255))  # faixa branca
        self.assertEqual(img.getpixel((1000, 975))[3], 0)       # abaixo da faixa
        self.assertEqual(img.getpixel((210, 780))[:3], AZUL)    # barra de título

    def test_barra_acompanha_titulo(self):
        def fim_barra(titulo):
            img = render.render_tela(titulo, "Corpo curto.", self.font)
            y = render.BAR_Y0 + 2
            return max(x for x in range(render.BAR_X0, 1600) if img.getpixel((x, y))[:3] == AZUL)
        self.assertLess(fim_barra("ASA"), fim_barra("Mutirão de Natal 2025"))

    def test_slugify(self):
        self.assertEqual(render.slugify("Culto de Domingo!"), "culto-de-domingo")
        self.assertEqual(render.slugify("Mutirão Ação"), "mutirao-acao")


if __name__ == "__main__":
    unittest.main()
