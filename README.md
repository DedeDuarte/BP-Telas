# BP Telas — Brooklin em Pauta

[![Testes](https://github.com/DedeDuarte/BP-Telas/actions/workflows/testes.yml/badge.svg)](https://github.com/DedeDuarte/BP-Telas/actions/workflows/testes.yml)

Skill do Claude Code que transforma o roteiro do informativo **Brooklin em Pauta** (IASD Brooklin)
nas telas de lower-third (PNG 1920×1080 transparente) usadas na transmissão.

## Baixar

- **Claude App / claude.ai:** na [última versão](https://github.com/DedeDuarte/BP-Telas/releases/latest),
  baixe o arquivo `gerar-telas-X.Y.Z.zip` (em **Assets**; ignore os "Source code") e envie-o como skill.
  Passo a passo em [Instalação no Claude App](#instalação-no-claude-app--claudeai).
- **Claude Code:** veja [Como usar](#como-usar).

## Como usar

1. **Instale a skill** — no Claude Code, peça:

   > Instale a skill deste repositório: https://github.com/DedeDuarte/BP-Telas

2. **Peça as telas** — cole o roteiro e peça:

   > Gere as telas deste roteiro: ...

   O Claude mostra uma tabela com título e texto de cada tela para você aprovar antes de gerar.

   **QR code personalizado:** passe o link junto do ponto ou no final do pedido
   (`link do 3: https://...`). A tela 3 ganha um QR com esse link direto (sem site intermediário),
   o logo da igreja no centro e uma legenda curta. Sem link, a tela usa o QR de visitante.

3. **Pegue as imagens** em `Downloads/Telas AAAA-MM-DD/`. Para salvar em outro lugar, é só dizer
   a pasta no pedido.

## Instalação (instruções para o Claude)

Ao receber o pedido do passo 1:

1. Clonar o repositório numa pasta temporária, só a versão atual:
   `git clone --depth 1 https://github.com/DedeDuarte/BP-Telas.git <pasta temporária>`.
2. Copiar a pasta `.claude/skills/gerar-telas/` para a pasta de skills do usuário:
   - Windows: `%USERPROFILE%\.claude\skills\gerar-telas\`
   - Linux: `~/.claude/skills/gerar-telas/`

   Se já existir uma versão instalada, substituí-la (atualização).
3. Garantir o Pillow (único requisito; se já estiver instalado, nada a fazer):
   - Windows: `py -m pip install -r %USERPROFILE%\.claude\skills\gerar-telas\requirements.txt`
   - Linux: `python3 -m pip install -r ~/.claude/skills/gerar-telas/requirements.txt`
4. Apagar o clone temporário e avisar que a skill `gerar-telas` está disponível
   (pode ser preciso reiniciar o Claude Code).

## Instalação no Claude App / claude.ai

1. Baixe o `gerar-telas-X.Y.Z.zip` da [página de releases](https://github.com/DedeDuarte/BP-Telas/releases)
   (ou gere o seu: `py tools/gerar_zip.py` no Windows, `python3 tools/gerar_zip.py` no Linux;
   o ZIP sai em `dist/`, com a pasta `gerar-telas/` na raiz).
2. No app: **Configurações → Capacidades**, ligue a execução de código e, em **Skills**, envie o ZIP.
3. Num chat novo, cole o roteiro e peça as telas. As imagens vêm anexadas na resposta.

Para remover: na mesma tela de Skills, desative ou exclua a skill.

## Requisitos

- Claude Code (Windows ou Linux) ou Claude App / claude.ai
- Python 3.9+ com Pillow — fontes e gerador de QR já vêm na skill; não precisa de internet

## Estrutura

```
BP-Telas/
├── .claude/skills/gerar-telas/     ← a skill (é isto que é instalado)
│   ├── SKILL.md                    ← instruções principais (fluxo)
│   ├── requirements.txt
│   ├── scripts/                    ← render.py (gera as telas) e fonts.py (caminho das fontes)
│   ├── assets/                     ← logo, fontes e bloco de QR
│   ├── references/                 ← especificação visual, regras de redação, formato do roteiro
│   └── examples/                   ← roteiro e JSON de exemplo
├── tools/                          ← gerar_zip.py (ZIP para o Claude App)
├── design/                         ← telas e modelo originais, para comparar com o que a skill gera
│                                     (não são instalados; o QR e algumas regras de texto mudaram depois deles)
├── tests/                          ← testes do renderizador
└── roteiros/                       ← rascunhos locais (ignorados pelo git)
```

## Desenvolvimento

Dentro desta pasta, o Claude Code já carrega a skill direto do repositório.

Renderizar manualmente (no Linux troque `py` por `python3` e `\` por `/`):

```
py .claude\skills\gerar-telas\scripts\render.py --pasta 2026-11-07
py .claude\skills\gerar-telas\scripts\render.py "<pasta>\telas.json"
```

Testes (também rodam no GitHub em Windows e Linux a cada push). O `requirements-dev.txt`
inclui o `zxing-cpp`, que lê os QR gerados para garantir que apontam para o link exato:

```
py -m pip install -r requirements-dev.txt
py -m unittest discover tests
```

## Planos futuros

- **0.4.0:** gerar também a **thumbnail do YouTube** da edição.
- **0.5.0 ou mais:** gerar o **vídeo de introdução**.

## Licença

[MIT](LICENSE) — inclui o código e as imagens do repositório (logo e telas de exemplo).
Componentes de terceiros incluídos na skill, com suas próprias licenças:

- Fonte Open Sans — SIL OFL 1.1 (`assets/fonts/OFL.txt`)
- segno 1.6.6 (gerador de QR) — BSD-3-Clause (`scripts/vendor/segno/LICENSE`)
