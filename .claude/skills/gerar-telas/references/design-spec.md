# Especificação visual

Medidas extraídas dos PNGs originais (em `design/` no repositório; não vão na skill instalada).

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

- Fonte: **Open Sans Bold**, sempre em CAIXA ALTA. Vem dentro da skill, em
  `assets/fonts/`.
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

## Bloco de QR

Todo QR (personalizado ou de visitante) é desenhado por `render_bloco_qr` em
`scripts/render.py`, na caixa de 279 × 363 px em 1617, 608. Coordenadas relativas à caixa:

| Elemento | Caixa | Observação |
|---|---|---|
| Caixa | 0, 0 → 279, 363 | `azul` |
| Área branca do código | 7, 10 → 271, 274 (264 × 264) | 1 módulo de margem branca |
| Código QR | dentro da área branca | `segno`, correção de erro **Q** (25%), link exato |
| Quadrado do logo | centro, lado = 28% do código | branco, 1:1 |
| Logo | centralizado no quadrado, 86% do lado | `assets/logo-qr.png` (cortado à área visível) |
| Legenda | 10, 280 → 269, 356 | `branco`, **Open Sans ExtraBold**; 1 linha se couber em ≥ 22 px, senão até 2 linhas (26 → 18 px), centralizada |

- Módulo mínimo de 4 px: links que exigem um QR mais denso são recusados (ilegíveis na transmissão).
- Nível Q em vez de H: menos módulos, quadradinhos maiores. O nível M (ainda maior) falhou nos
  testes de leitura com o logo, por isso não é usado.

### QR de visitante

`assets/qr-visitante.png` é um **arquivo fixo** gerado por `scripts/gerar_qr_visitante.py`
(link `https://typebot.co/my-typebot-a6oemdd`, legenda "VISITANDO NOSSA IGREJA PELA 1ª VEZ?").
Não edite o PNG à mão: mude o script e rode-o. Um teste falha se o PNG ficar desatualizado.
