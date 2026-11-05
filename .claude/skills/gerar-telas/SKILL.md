---
name: gerar-telas
description: Gera as telas (lower-thirds PNG 1920x1080 com fundo transparente) do informativo "Brooklin em Pauta" da IASD Brooklin a partir de um roteiro de avisos. Use quando o usuário colar ou apontar um roteiro do Brooklin em Pauta, pedir "telas", "GCs", "lower thirds" ou "artes dos avisos" da igreja, ou quiser transformar os pontos de um roteiro em telas no padrão do Modelo.
---

# Gerar Telas — Brooklin em Pauta

Transforma cada ponto informativo de um roteiro em uma tela (overlay transparente) no padrão visual da IASD Brooklin.

## Entrada

Um roteiro em texto (colado na conversa ou um arquivo em `roteiros/`). Formato esperado em
[references/roteiro.md](references/roteiro.md). Exemplo real: [examples/roteiros/2026-10-31.txt](examples/roteiros/2026-10-31.txt).

## Saída

PNGs em `saida/<AAAA-MM-DD>/`, um por ponto do roteiro que gera tela, nomeados
`NN-slug.png` (ex.: `02-culto-domingo.png`), na ordem do roteiro.

## Fluxo

1. **Ler o roteiro** e separar os pontos numerados. Identificar a data da edição (1ª linha).
   **Ano: sempre o ano atual**, a não ser que outro ano esteja escrito explicitamente no roteiro
   — ver [references/roteiro.md](references/roteiro.md).
   Cada ponto vira uma tela — ver [references/tipos-de-tela.md](references/tipos-de-tela.md).
2. **Redigir título e corpo** de cada tela seguindo as regras de
   [references/tipos-de-tela.md](references/tipos-de-tela.md#redação): título curto, corpo de
   até ~140 caracteres só com a informação acionável. **Cultos de domingo e de quarta têm
   sempre o título `CULTO DE DOMINGO` / `CULTO DE QUARTA`.**
3. **Mostrar ao usuário a tabela de telas** (nº, título, corpo) e esperar aprovação.
4. **Salvar o JSON** aprovado em `roteiros/<AAAA-MM-DD>.json` (formato em
   [examples/roteiros/2026-10-31.json](examples/roteiros/2026-10-31.json)).
5. **Renderizar** (a partir da raiz do projeto). O uso principal é no **Windows**:
   - Windows: `py .claude\skills\gerar-telas\scripts\render.py roteiros\<AAAA-MM-DD>.json`
     (se `py` não existir, use `python`)
   - Linux: `python3 .claude/skills/gerar-telas/scripts/render.py roteiros/<AAAA-MM-DD>.json`

   Se o script disser que falta o Pillow, instale com `py -m pip install -r requirements.txt`
   (Linux: `python3 -m pip install -r requirements.txt`) e rode de novo. A fonte Open Sans Bold
   é baixada automaticamente na 1ª vez. Se o script acusar corpo ou título longo demais,
   encurte o texto e rode de novo.
6. **Conferir visualmente** abrindo `saida/<data>/_preview.jpg` (todas as telas sobre fundo
   cinza — sobre branco a faixa branca do corpo fica invisível) e listar os arquivos ao final.

## Assets

| Arquivo | Uso |
|---|---|
| `assets/modelo.png` | Modelo-base completo (logo + barra de título vazia + QR visitante) |
| `assets/logo-brooklin.png` | Logo isolado (20,775 → 185,972) |
| `assets/qr-visitante.png` | Bloco QR "visitando pela 1ª vez" (1617,608 → 1896,971) || `assets/fonts/` | Open Sans Bold, baixada sob demanda (não versionada) |

## Exemplos

`examples/telas/` tem telas reais já produzidas. Consulte-as para calibrar tom, tamanho de texto e
quebra de linha.
