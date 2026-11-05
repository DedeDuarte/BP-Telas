# Changelog

Todas as mudanças relevantes deste projeto são registradas aqui.
Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e versionamento
[SemVer](https://semver.org/lang/pt-BR/).

## [Não publicado]

### Adicionado

- QR code personalizado por tela: basta passar o link junto do ponto ou no fim do pedido
  (`link do 3: https://...`). O QR aponta direto para o link (sem site intermediário), tem o logo
  da igreja no centro e uma legenda curta abaixo, no mesmo lugar do QR de visitante.
- Links inválidos ou longos demais para um QR legível são recusados com aviso.
- Testes que leem o QR gerado (inclusive em 720p e 540p) e conferem o link caractere por caractere.

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

[Não publicado]: https://github.com/DedeDuarte/BP-Telas/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/DedeDuarte/BP-Telas/releases/tag/v0.1.0
