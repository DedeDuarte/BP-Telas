"""Testes do renderizador de telas. Rodar da raiz: py -m unittest discover tests"""
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

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

    def test_fonte_usa_layout_basic(self):
        # Garante telas idênticas no Windows (sem libraqm) e no Linux (com libraqm).
        self.assertEqual(render.fonte(self.font, 30).layout_engine, render.ImageFont.Layout.BASIC)

    def test_slugify(self):
        self.assertEqual(render.slugify("Culto de Domingo!"), "culto-de-domingo")
        self.assertEqual(render.slugify("Mutirão Ação"), "mutirao-acao")


try:
    import zxingcpp  # leitor de QR, só para testes (requirements-dev.txt)
except ImportError:
    zxingcpp = None

LINKS = [
    "https://chat.whatsapp.com/KxY7aBcDeFgHiJkLmNoPq1",
    "https://forms.gle/abcdEFGH1234",
    "https://www.youtube.com/@iasdbrooklin/videos?view=0&sort=dd&shelf_id=1",
    "http://exemplo.com.br/inscricao?evento=mutirao-natal&ano=2026",
]


class TestQR(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.font = ensure_font()

    def tela(self, link, legenda="Entre na comunidade"):
        return render.render_tela("Teste", "Corpo curto.", self.font, {"link": link, "legenda": legenda})

    @unittest.skipUnless(zxingcpp, "zxing-cpp não instalado (py -m pip install -r requirements-dev.txt)")
    def test_qr_le_o_link_exato_mesmo_com_logo(self):
        # Lê a tela inteira, também reduzida (transmissão em 720p/540p): o conteúdo
        # tem de ser o link original, caractere por caractere — sem redirecionamento.
        for link in LINKS:
            for tamanho in [(1920, 1080), (1280, 720), (960, 540)]:
                with self.subTest(link=link, tamanho=tamanho):
                    lidos = zxingcpp.read_barcodes(self.tela(link).convert("RGB").resize(tamanho))
                    self.assertEqual([r.text for r in lidos], [link])

    @unittest.skipUnless(zxingcpp, "zxing-cpp não instalado (py -m pip install -r requirements-dev.txt)")
    def test_qr_visitante_le_o_link(self):
        import gerar_qr_visitante
        img = render.render_tela("Teste", "Corpo curto.", self.font)
        for tamanho in [(1920, 1080), (1280, 720), (960, 540)]:
            with self.subTest(tamanho=tamanho):
                lidos = zxingcpp.read_barcodes(img.convert("RGB").resize(tamanho))
                self.assertEqual([r.text for r in lidos], [gerar_qr_visitante.LINK])

    def test_qr_visitante_atualizado(self):
        # O arquivo fixo tem de ser exatamente o que o gerador produz hoje.
        # Se falhar: rode scripts/gerar_qr_visitante.py e faça commit do PNG.
        # Tolerância: versões diferentes do Pillow/FreeType mudam a suavização de bordas em
        # poucos tons; link ou legenda diferentes mudam centenas de pixels por completo.
        from PIL import ImageChops
        import gerar_qr_visitante
        esperado = render.render_bloco_qr(gerar_qr_visitante.LINK, gerar_qr_visitante.LEGENDA)
        atual = render.Image.open(gerar_qr_visitante.DESTINO).convert("RGBA")
        self.assertEqual(atual.size, esperado.size)
        diff = ImageChops.difference(atual.convert("L"), esperado.convert("L"))
        muito_diferentes = sum(diff.histogram()[65:])
        self.assertLess(muito_diferentes, 30, "rode scripts/gerar_qr_visitante.py")

    def test_qr_mesma_caixa_do_visitante(self):
        x, y = render.QR_POS
        w, h = render.QR_BLOCO
        img = self.tela(LINKS[0])
        for px in [(x + 2, y + 2), (x + w - 3, y + h - 3)]:   # cantos azuis
            self.assertEqual(img.getpixel(px)[:3], AZUL)
        self.assertEqual(img.getpixel((x - 3, y + 2))[3], 0)  # fora da caixa: transparente
        self.assertEqual(img.getpixel((x + 2, y - 3))[3], 0)

    def test_sem_qr_usa_visitante(self):
        img = render.render_tela("Teste", "Corpo curto.", self.font)
        visitante = render.Image.open(render.ASSETS / "qr-visitante.png").convert("RGBA")
        x, y = render.QR_POS
        recorte = img.crop((x, y, x + visitante.width, y + visitante.height))
        self.assertEqual(recorte.tobytes(), visitante.tobytes())

    def test_usa_segno_embutido(self):
        # A skill não pode depender de pip/internet (Claude App): o segno vem de scripts/vendor.
        import segno
        vendor = Path(render.__file__).resolve().parent / "vendor"
        self.assertTrue(Path(segno.__file__).resolve().is_relative_to(vendor), segno.__file__)

    def test_fontes_embutidas(self):
        fontes = Path(render.ASSETS) / "fonts"
        for nome in ["OpenSans-Bold.ttf", "OpenSans-ExtraBold.ttf", "OFL.txt"]:
            self.assertTrue((fontes / nome).is_file(), nome)

    def test_link_invalido(self):
        for link in ["chat.whatsapp.com/abc", "ftp://x.com/a", "https://x.com/a b", ""]:
            with self.subTest(link=link), self.assertRaises(ValueError):
                self.tela(link)

    def test_link_longo_demais(self):
        with self.assertRaises(ValueError):
            self.tela("https://exemplo.com/" + "a" * 200)

    def test_legenda_obrigatoria_e_curta(self):
        with self.assertRaises(ValueError):
            self.tela(LINKS[0], legenda="")
        with self.assertRaises(ValueError):
            self.tela(LINKS[0], legenda="texto muito comprido " * 6)




class PastaBaseTest(unittest.TestCase):
    """Sem Downloads (ambiente do app): $OUTPUT_DIR, depois /mnt/user-data/outputs, depois a pasta atual."""

    def test_usa_output_dir_sem_downloads(self):
        with tempfile.TemporaryDirectory() as tmp:
            inexistente = Path(tmp) / "nao-existe"
            with mock.patch.object(render, "pasta_downloads", return_value=inexistente), \
                    mock.patch.dict(os.environ, {"OUTPUT_DIR": tmp}):
                self.assertEqual(render.pasta_base(), Path(tmp))

    def test_downloads_tem_prioridade_sobre_output_dir(self):
        with tempfile.TemporaryDirectory() as dl, tempfile.TemporaryDirectory() as out:
            with mock.patch.object(render, "pasta_downloads", return_value=Path(dl)), \
                    mock.patch.dict(os.environ, {"OUTPUT_DIR": out}):
                self.assertEqual(render.pasta_base(), Path(dl))

    def test_output_dir_inexistente_e_ignorado(self):
        with tempfile.TemporaryDirectory() as tmp:
            falso = Path(tmp) / "falso"
            with mock.patch.object(render, "pasta_downloads", return_value=falso), \
                    mock.patch.object(render, "SAIDA_APP", falso), \
                    mock.patch.dict(os.environ, {"OUTPUT_DIR": str(falso)}):
                self.assertEqual(render.pasta_base(), Path.cwd())


class ZipTest(unittest.TestCase):
    """O ZIP da skill tem gerar-telas/ na raiz, SKILL.md dentro e nada de cache."""

    def test_estrutura_do_zip(self):
        import zipfile
        sys.path.insert(0, str(ROOT / "tools"))
        import gerar_zip
        with tempfile.TemporaryDirectory() as tmp:
            destino = gerar_zip.gerar_zip(Path(tmp) / "gerar-telas-teste.zip")
            nomes = zipfile.ZipFile(destino).namelist()
        self.assertIn("gerar-telas/SKILL.md", nomes)
        self.assertTrue(all(n.startswith("gerar-telas/") for n in nomes))
        self.assertFalse([n for n in nomes if "__pycache__" in n or n.endswith(".pyc")])
        self.assertTrue(all("\\" not in n for n in nomes))


if __name__ == "__main__":
    unittest.main()
