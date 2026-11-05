# Changelog

Todas as mudanças relevantes deste projeto são registradas aqui.
Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e versionamento
[SemVer](https://semver.org/lang/pt-BR/).

## [Não publicado]

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
