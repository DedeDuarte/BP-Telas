# Changelog

Todas as mudanças relevantes deste projeto são registradas aqui.
Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e versionamento
[SemVer](https://semver.org/lang/pt-BR/).

## [Não publicado]

### Adicionado

- Funciona no Claude App / claude.ai: fontes Open Sans e o gerador de QR (`segno`) vêm dentro
  da skill, então nada é baixado nem instalado. O único requisito é o Pillow.
- Sem pasta Downloads (app, nuvem), as telas vão para a pasta de saída do ambiente e são
  entregues no chat.
- Instruções de instalação e remoção no Claude App (upload de ZIP).
- No app, as telas são entregues em um único `Telas AAAA-MM-DD.zip` (só os PNGs; `_preview.jpg` e `telas.json` em `extras/`); `--zip` força o ZIP em qualquer ambiente.

### Alterado

- Instalação pelo Claude Code clona só a versão atual (`git clone --depth 1`).

## [0.2.0] - 2026-11-05

> **Atualizando do 0.1.0:** reinstale a skill (peça ao Claude de novo com o link do repositório).
> A nova dependência `segno` é instalada junto; sem ela, telas com QR personalizado dão erro.

### Adicionado

- QR code personalizado por tela: basta passar o link junto do ponto ou no fim do pedido
  (`link do 3: https://...`). O QR aponta direto para o link (sem site intermediário), tem o logo
  da igreja no centro e uma legenda curta abaixo, no mesmo lugar do QR de visitante.
- Links inválidos ou longos demais para um QR legível são recusados com aviso.
- Testes que leem o QR gerado (inclusive em 720p e 540p) e conferem o link caractere por caractere.
- Regra de redação: sempre "pastor" por extenso, nunca "Pr.".
- Regra de redação: erros de português do roteiro são corrigidos nas telas, sem mudar o sentido.
- Roteiro de teste manual com gabarito em `tests/roteiros/`.

### Alterado

- QR de visitante refeito no mesmo modelo dos QR personalizados (logo no centro, legenda em
  negrito). Agora é lido também com a tela inteira e em resoluções reduzidas.
- QR com quadradinhos maiores, logo novo dentro de um quadrado branco e legenda em Open Sans
  ExtraBold, em uma linha quando couber.

### Corrigido

- Telas geradas no Windows e no Linux agora são idênticas (antes o texto podia ser medido
  de forma diferente e mudar quebras de linha e larguras).

## [0.1.0] - 2026-11-05

### Adicionado

- Skill `gerar-telas`: transforma cada ponto do roteiro do Brooklin em Pauta em uma tela PNG
  1920×1080 transparente, com aprovação dos textos antes de gerar.
- Renderizador (`render.py`): barra de título com largura proporcional ao texto, corpo em até
  2 linhas com redução automática da fonte, faixa branca, logo e QR de visitante.
- Download automático da fonte Open Sans Bold na primeira execução.
- Telas salvas em `Downloads/Telas AAAA-MM-DD/`, com `telas.json` e `_preview.jpg` de conferência.
- Regras de redação: títulos fixos `CULTO DE DOMINGO` / `CULTO DE QUARTA` e ano atual quando o
  roteiro não informa outro.
- Suporte a Windows (prioritário) e Linux, com testes automáticos nos dois sistemas.
- Licença MIT.

[Não publicado]: https://github.com/DedeDuarte/BP-Telas/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/DedeDuarte/BP-Telas/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/DedeDuarte/BP-Telas/releases/tag/v0.1.0
