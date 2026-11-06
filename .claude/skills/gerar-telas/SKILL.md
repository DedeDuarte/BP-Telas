---
name: gerar-telas
description: Gera as telas (lower-thirds PNG transparentes, com QR code) do "Brooklin em Pauta" a partir de um roteiro de avisos. Use ao receber um roteiro ou pedido de "telas", "GCs" ou "lower thirds".
---

# Gerar Telas — Brooklin em Pauta

Transforma cada ponto informativo de um roteiro em uma tela (overlay transparente) no padrão visual da IASD Brooklin.

Nos comandos abaixo, `<skill>` é a pasta onde está este `SKILL.md`. O uso principal é no
**Windows** (`py`; se não existir, `python`); no Linux, no Claude App e no claude.ai use `python3`.

**Requisito único: Pillow.** Fontes e gerador de QR (`segno`) já vêm dentro da skill — nada é
baixado nem instalado com pip. Funciona sem internet (ex.: ambiente do Claude App).

## Entrada

Um roteiro em texto, colado na conversa ou em um arquivo. Formato esperado em
[references/roteiro.md](references/roteiro.md). Exemplo real: [examples/roteiros/2026-10-31.txt](examples/roteiros/2026-10-31.txt).

## Saída

Por padrão, na pasta **Downloads** do usuário: `Downloads/Telas AAAA-MM-DD/`, contendo um PNG por
ponto do roteiro (`NN-slug.png`, na ordem do roteiro), o `telas.json` com os textos usados e o
`_preview.jpg` de conferência. Se o usuário pedir outra pasta, use `-o "<pasta>"`.

**Sem pasta Downloads** (Claude App, claude.ai, sessões na nuvem): o script usa, nesta ordem,
`$OUTPUT_DIR`, `/mnt/user-data/outputs/` ou a pasta atual, criando `Telas AAAA-MM-DD/` dentro dela.
O script imprime os caminhos finais: **use esses caminhos**, não suponha nenhum. Nesse caso os
arquivos **não** estão no computador do usuário, e o script gera sozinho `Telas AAAA-MM-DD.zip`
(na raiz do ZIP ficam só os PNGs, sem pasta interna; o `_preview.jpg` e o `telas.json` vão na
subpasta `extras/`). Ao final, **confirme que o
ZIP existe** (`ls`) e **entregue somente esse ZIP** como anexo (um único arquivo; não anexe os PNGs
soltos).
Se não houver como anexar, entregue ao menos o `telas.json` para ele rodar no computador dele.

## Fluxo

1. **Ler o roteiro** e separar os pontos numerados. Identificar a data da edição (1ª linha).
   **Ano: sempre o ano atual**, a não ser que outro ano esteja escrito explicitamente no roteiro
   — ver [references/roteiro.md](references/roteiro.md).
   Cada ponto vira uma tela — ver [references/tipos-de-tela.md](references/tipos-de-tela.md).
2. **Redigir título e corpo** de cada tela seguindo as regras de
   [references/tipos-de-tela.md](references/tipos-de-tela.md#redação): título curto, corpo de
   até ~140 caracteres só com a informação acionável. **Cultos de domingo e de quarta têm
   sempre o título `CULTO DE DOMINGO` / `CULTO DE QUARTA`. Escreva sempre `pastor` por extenso,
   nunca `Pr.` Corrija os erros de português do roteiro sem mudar o sentido.**
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
   - Falta o Pillow → `py -m pip install -r <skill>/requirements.txt` e rode de novo.
   - Link inválido ou longo demais → fale com o usuário (não altere o link por conta própria).
   - Corpo ou título longo demais → encurte o texto no JSON e rode de novo.
   - **Nunca troque a fonte** por outra nem gere as telas por outro meio: se o script falhar,
     explique o erro ao usuário.
7. **Conferir visualmente** abrindo `_preview.jpg` (todas as telas sobre fundo cinza — sobre
   branco a faixa branca do corpo fica invisível) e informar ao usuário a pasta gerada — ou,
   sem pasta Downloads, entregar o ZIP (ver **Saída**).

## Assets

| Arquivo | Uso |
|---|---|
| `assets/logo-brooklin.png` | Logo isolado (20,775 → 185,972) |
| `assets/qr-visitante.png` | Bloco QR padrão "visitando pela 1ª vez" (1617,608 → 1896,971). Arquivo fixo gerado por `scripts/gerar_qr_visitante.py` — não edite à mão |
| `assets/logo-qr.png` | Logo usado no centro dos QR |
| `assets/fonts/` | Open Sans Bold e ExtraBold (licença em `OFL.txt`) |
| `scripts/vendor/segno/` | Cópia do gerador de QR `segno` 1.6.6 (licença BSD em `LICENSE`) |

## Exemplos

Os textos de `examples/roteiros/2026-10-31.json` foram revisados pelo usuário e
são a referência de estilo.
