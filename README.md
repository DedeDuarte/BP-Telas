# BP Telas — Brooklin em Pauta

Skill do Claude Code que transforma o roteiro do informativo **Brooklin em Pauta** (IASD Brooklin)
nas telas de lower-third (PNG 1920×1080 transparente) usadas na transmissão.

## Estrutura

```
BP_Telas/
├── .claude/skills/gerar-telas/     ← a skill
│   ├── SKILL.md                    ← instruções principais (fluxo)
│   ├── assets/                     ← modelo, logo e blocos de QR
│   ├── references/                 ← especificação visual, tipos de tela, formato do roteiro
│   └── examples/                   ← roteiro e telas reais de referência
├── roteiros/                       ← coloque aqui os roteiros novos (AAAA-MM-DD.txt)
└── saida/                          ← telas geradas, uma pasta por edição
```

## Uso

No Claude Code, dentro desta pasta:

```
/gerar-telas roteiros/2025-11-07.txt
```

ou simplesmente cole o roteiro e peça as telas.

## Próximos passos

- [x] Script de renderização (`scripts/render.py`) com Pillow, a partir de um JSON de telas
- [x] Download automático da fonte Open Sans Bold (`scripts/fonts.py`)
- [x] Validar a especificação comparando telas geradas com os exemplos
- [ ] Gerar QR code específico por tela (ex.: link da comunidade do WhatsApp)

## Requisitos

- Windows (principal) ou Linux
- Python 3.9+ com as dependências: `py -m pip install -r requirements.txt`
  (Linux: `python3 -m pip install -r requirements.txt`)
- Internet na primeira execução (download da fonte)

## Renderizar manualmente

Windows:

```
py .claude\skills\gerar-telas\scripts\render.py roteiros\2025-11-07.json
```

Linux:

```
python3 .claude/skills/gerar-telas/scripts/render.py roteiros/2025-11-07.json
```

## Testes

```
py -m unittest discover tests          # Windows
python3 -m unittest discover tests     # Linux
```
