# BP Telas — Brooklin em Pauta

[![Testes](https://github.com/DedeDuarte/BP-Telas/actions/workflows/testes.yml/badge.svg)](https://github.com/DedeDuarte/BP-Telas/actions/workflows/testes.yml)

Skill do Claude Code que transforma o roteiro do informativo **Brooklin em Pauta** (IASD Brooklin)
nas telas de lower-third (PNG 1920×1080 transparente) usadas na transmissão.

## Como usar

1. **Instale a skill** — no Claude Code, peça:

   > Instale a skill deste repositório: https://github.com/DedeDuarte/BP-Telas

2. **Peça as telas** — cole o roteiro e peça:

   > Gere as telas deste roteiro: ...

   O Claude mostra uma tabela com título e texto de cada tela para você aprovar antes de gerar.

3. **Pegue as imagens** em `Downloads/Telas AAAA-MM-DD/`. Para salvar em outro lugar, é só dizer
   a pasta no pedido.

## Instalação (instruções para o Claude)

Ao receber o pedido do passo 1:

1. Clonar o repositório numa pasta temporária.
2. Copiar a pasta `.claude/skills/gerar-telas/` para a pasta de skills do usuário:
   - Windows: `%USERPROFILE%\.claude\skills\gerar-telas\`
   - Linux: `~/.claude/skills/gerar-telas/`

   Se já existir uma versão instalada, substituí-la (atualização).
3. Instalar as dependências:
   - Windows: `py -m pip install -r %USERPROFILE%\.claude\skills\gerar-telas\requirements.txt`
   - Linux: `python3 -m pip install -r ~/.claude/skills/gerar-telas/requirements.txt`
4. Apagar o clone temporário e avisar que a skill `gerar-telas` está disponível
   (pode ser preciso reiniciar o Claude Code).

## Requisitos

- Windows (principal) ou Linux
- Python 3.9+ e Pillow (`requirements.txt` dentro da skill)
- Internet na primeira execução (download da fonte Open Sans Bold)

## Estrutura

```
BP-Telas/
├── .claude/skills/gerar-telas/     ← a skill (é isto que é instalado)
│   ├── SKILL.md                    ← instruções principais (fluxo)
│   ├── requirements.txt
│   ├── scripts/                    ← render.py (gera as telas) e fonts.py (baixa a fonte)
│   ├── assets/                     ← logo e bloco de QR (modelo.png é só referência)
│   ├── references/                 ← especificação visual, regras de redação, formato do roteiro
│   └── examples/                   ← roteiro, JSON e telas reais de referência
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

Testes (também rodam no GitHub em Windows e Linux a cada push):

```
py -m unittest discover tests
```

## Próximos passos

- [ ] Gerar QR code específico por tela (ex.: link da comunidade do WhatsApp)

## Licença

[MIT](LICENSE) — inclui o código e as imagens do repositório (logo e telas de exemplo).
A fonte Open Sans não faz parte do repositório: é baixada do projeto oficial e usa a licença SIL OFL 1.1.
