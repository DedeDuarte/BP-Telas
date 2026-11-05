---
name: gerar-telas
description: Gera as telas (lower-thirds PNG 1920x1080 com fundo transparente) do informativo "Brooklin em Pauta" da IASD Brooklin a partir de um roteiro de avisos, com QR code personalizado (link direto, logo no centro) quando o usuário passar links. Use quando o usuário colar ou apontar um roteiro do Brooklin em Pauta, pedir "telas", "GCs", "lower thirds" ou "artes dos avisos" da igreja, ou quiser transformar os pontos de um roteiro em telas no padrão do Modelo.
---

# Gerar Telas — Brooklin em Pauta

Transforma cada ponto informativo de um roteiro em uma tela (overlay transparente) no padrão visual da IASD Brooklin.

Nos comandos abaixo, `<skill>` é a pasta onde está este `SKILL.md`. O uso principal é no
**Windows** (`py`; se não existir, `python`); no Linux use `python3`.

## Entrada

Um roteiro em texto, colado na conversa ou em um arquivo. Formato esperado em
[references/roteiro.md](references/roteiro.md). Exemplo real: [examples/roteiros/2026-10-31.txt](examples/roteiros/2026-10-31.txt).

## Saída

Por padrão, na pasta **Downloads** do usuário: `Downloads/Telas AAAA-MM-DD/`, contendo um PNG por
ponto do roteiro (`NN-slug.png`, na ordem do roteiro), o `telas.json` com os textos usados e o
`_preview.jpg` de conferência. Se o usuário pedir outra pasta, use `-o "<pasta>"`.

## Fluxo

1. **Ler o roteiro** e separar os pontos numerados. Identificar a data da edição (1ª linha).
   **Ano: sempre o ano atual**, a não ser que outro ano esteja escrito explicitamente no roteiro
   — ver [references/roteiro.md](references/roteiro.md).
   Cada ponto vira uma tela — ver [references/tipos-de-tela.md](references/tipos-de-tela.md).
2. **Redigir título e corpo** de cada tela seguindo as regras de
   [references/tipos-de-tela.md](references/tipos-de-tela.md#redação): título curto, corpo de
   até ~140 caracteres só com a informação acionável. **Cultos de domingo e de quarta têm
   sempre o título `CULTO DE DOMINGO` / `CULTO DE QUARTA`. Escreva sempre `pastor` por extenso,
   nunca `Pr.`**
   **Links de QR:** se o usuário passou links (dentro do ponto ou no fim, como `link do 3: <url>`),
   o ponto correspondente ganha QR personalizado com legenda — regras em
   [references/tipos-de-tela.md](references/tipos-de-tela.md#qr-code). Use o link **exatamente**
   como foi passado; nunca encurte nem troque.
3. **Mostrar ao usuário a tabela de telas** (nº, título, corpo, QR) e esperar aprovação. Na
   coluna QR: `visitante` ou o link completo + a legenda proposta.
4. **Criar a pasta da edição**: `py <skill>/scripts/render.py --pasta AAAA-MM-DD` — o comando
   imprime o caminho (ex.: `C:\Users\Fulano\Downloads\Telas 2026-10-31`).
5. **Salvar o JSON** aprovado como `telas.json` dentro dessa pasta (formato em
   [examples/roteiros/2026-10-31.json](examples/roteiros/2026-10-31.json)).
6. **Renderizar**: `py <skill>/scripts/render.py "<pasta>/telas.json"`.
   - Falta o Pillow ou o segno → `py -m pip install -r <skill>/requirements.txt` e rode de novo.
   - Link inválido ou longo demais → fale com o usuário (não altere o link por conta própria).
   - A fonte Open Sans Bold é baixada automaticamente na 1ª vez (precisa de internet).
   - Corpo ou título longo demais → encurte o texto no JSON e rode de novo.
7. **Conferir visualmente** abrindo `_preview.jpg` (todas as telas sobre fundo cinza — sobre
   branco a faixa branca do corpo fica invisível) e informar ao usuário a pasta gerada.

## Assets

| Arquivo | Uso |
|---|---|
| `assets/logo-brooklin.png` | Logo isolado (20,775 → 185,972) |
| `assets/qr-visitante.png` | Bloco QR "visitando pela 1ª vez" (1617,608 → 1896,971) |
| `assets/fonts/` | Open Sans Bold, baixada sob demanda (não versionada) |
| `assets/modelo.png` | **Só referência histórica — não use na skill.** O script desenha tudo sozinho. |

## Exemplos

`examples/telas/` tem telas reais já produzidas. Consulte-as para calibrar tom, tamanho de texto e
quebra de linha. Os textos de `examples/roteiros/2026-10-31.json` foram revisados pelo usuário e
são a referência de estilo.
