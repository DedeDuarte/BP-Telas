# Especificação visual

Medidas extraídas dos PNGs de `examples/telas/` e de `assets/modelo.png`.

## Canvas

- 1920 × 1080 px, RGBA, **fundo totalmente transparente** (é um overlay sobre o vídeo).
- Tudo fica no terço inferior; acima de y≈600 não há nada.

## Cores

| Token | Valor | Uso |
|---|---|---|
| `azul` | `#003366` (0, 51, 102) | Barra de título, caixa do logo, caixa do QR, texto do corpo |
| `branco` | `#FFFFFF` | Texto do título, faixa atrás do corpo |

> Atenção ao conferir: a tela é transparente. Vista sobre fundo branco, a faixa branca
> some. Confira sempre sobre fundo escuro (o `_preview.jpg` gerado pelo script já usa cinza).

## Tipografia

- Fonte: **Open Sans Bold**, sempre em CAIXA ALTA. Obtida por `scripts/fonts.py`
  (`ensure_font()`), que baixa para `assets/fonts/` na primeira execução.
- Título (sobre a barra): branco, ~36 px de altura de versal.
- Corpo (sobre transparente): azul, 26–34 px (o maior que couber em 2 linhas), entrelinha 1,38 × tamanho.

Os valores exatos usados pelo renderizador estão no topo de `scripts/render.py`.

## Layout

| Elemento | Caixa (x0, y0 → x1, y1) | Observação |
|---|---|---|
| Logo | 20, 775 → 185, 972 | `assets/logo-brooklin.png`, fixo |
| Barra de título | 205, 776 → *largura variável*, 862 | largura = texto + ~22 px de respiro à esquerda e ~30–40 px à direita |
| Texto do título | x≈228, centro vertical da barra (y≈819) | |
| Faixa branca do corpo | 205, 884 → 1593, 971 | desenhada pelo código, **opaca**, fixa (largura não varia) |
| Corpo | x=228, 2 linhas dentro da faixa branca | limite direito 1570 px |
| Bloco QR | 1617, 608 → 1896, 971 | `assets/qr-visitante.png` ou QR personalizado (abaixo) |

## Bloco de QR personalizado

Mesma caixa do QR de visitante (279 × 363 px em 1617, 608), desenhada pelo código
(`render_bloco_qr` em `scripts/render.py`). Coordenadas relativas ao canto da caixa:

| Elemento | Caixa | Observação |
|---|---|---|
| Caixa | 0, 0 → 279, 363 | `azul` |
| Área branca do código | 7, 10 → 271, 274 (264 × 264) | 1 módulo de margem branca |
| Código QR | dentro da área branca | gerado com `segno`, correção de erro **H** (30%), link exato |
| Logo central | ~24% da altura do código | `assets/logo-brooklin.png` com 1 módulo de respiro branco |
| Legenda | 10, 280 → 269, 356 | `branco`, Open Sans Bold 24→16 px, até 2 linhas, centralizada |

Módulo mínimo de 4 px: links que exigem um QR mais denso são recusados (ilegíveis na transmissão).
