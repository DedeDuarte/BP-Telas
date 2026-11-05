# BP Telas

Skill `gerar-telas` (em `.claude/skills/gerar-telas/`) que gera as telas do Brooklin em Pauta.
Veja o [README.md](README.md) para estrutura e uso.

## Plataformas

- **Windows é a prioridade**, mas tudo deve funcionar também no Linux.
- Use `pathlib`, nada de caminhos fixos com `/` ou `\`; leia e escreva arquivos com encoding explícito.
- Nos comandos documentados, mostre primeiro a versão Windows (`py ...`) e depois a Linux (`python3 ...`).

## Testes

Rode `python3 -m unittest discover tests` (Windows: `py -m unittest discover tests`) antes de cada commit
que mexa em `scripts/`.

## Commits

- **Após cada mudança, faça sempre um commit.** Uma mudança lógica por commit.
- Use [Conventional Commits](https://www.conventionalcommits.org/): `tipo(escopo opcional): descrição`.
  Tipos: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `style`, `perf`, `build`, `ci`.
- **Sem body**: só a linha de título, curta, em português, no imperativo, sem ponto final.
- **Breaking change**: marque com `!` após o tipo/escopo **e** adicione o rodapé `BREAKING CHANGE:`.
  É a única situação em que a mensagem tem mais de uma linha:

  ```
  feat(render)!: muda formato do JSON de entrada

  BREAKING CHANGE: campo "corpo" renomeado para "texto"
  ```

## Retomada

Antes de trabalhar na próxima versão, leia o plano e o contexto em [plano-0.3.0.md](plano-0.3.0.md).
