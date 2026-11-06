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

## O projeto

Transforma o roteiro do **Brooklin em Pauta** (IASD Brooklin) em telas PNG transparentes. Funciona no
Claude Code (Windows e Linux) e no Claude App / claude.ai. Fluxo, formato e regras de redação estão no
[SKILL.md](.claude/skills/gerar-telas/SKILL.md) e em `references/`; versões em [CHANGELOG.md](CHANGELOG.md).

- O roteiro chega **já limpo** e o usuário não quer responder muitas perguntas: a skill só pergunta
  quando há ambiguidade real.
- `design/` guarda as telas e o modelo **originais**, para comparar com o que a skill gera. **Mantenha
  essas imagens** (decisão do usuário); o QR e algumas regras de texto mudaram depois delas.

## Decisões técnicas (e por quê)

- **Só o Pillow é requisito**: fontes (`assets/fonts/`) e `segno` (`scripts/vendor/`) vêm dentro da
  skill, porque o ambiente do app pode estar sem internet. Não troque por download nem pip.
- **Layout de texto BASIC forçado** (`render.fonte()`): o Pillow usa RAQM no Linux e BASIC no
  Windows, que medem texto diferente → telas diferentes entre sistemas.
- **Limites do claude.ai** (ajuda oficial): `description` do `SKILL.md` com até 200 caracteres; o ZIP
  precisa ter a pasta `gerar-telas/` na raiz. Pasta de saída no app: `$OUTPUT_DIR`, depois
  `/mnt/user-data/outputs` (este último ainda não confirmado na documentação oficial).
- **ZIP de entrega sem pasta interna**: o nome do ZIP já dá a pasta ao extrair (evita pasta dentro
  de pasta no "Extrair tudo" do Windows).

## Ambiente de desenvolvimento (máquina Linux do usuário)

- `python3 -m venv` não funciona (falta `python3-venv`). Para testar QR localmente:
  `pip install --target <pasta temporária> zxing-cpp` + `PYTHONPATH=<pasta>`. Sem `zxing-cpp`, os 2
  testes de leitura de QR são pulados (rode com ele antes de mexer em QR ou no logo).
- `roteiros/`, `saida/` e `dist/` são ignorados pelo git (rascunhos e ZIPs gerados).

## Publicar uma versão

1. CHANGELOG fechado (`[X.Y.Z] - data` + links de comparação no rodapé; aviso de atualização no topo
   se a forma de instalar mudar) e CI verde na `main` (Windows e Linux).
2. `git tag -a vX.Y.Z -m "vX.Y.Z"` e `git push origin vX.Y.Z`.
3. `gh release create vX.Y.Z --title "vX.Y.Z" --notes-file <notas>` (novidades, aviso de atualização,
   limitações conhecidas; o `gh` instalado não tem `--verify-tag`). O workflow `release-zip.yml`
   anexa `gerar-telas-X.Y.Z.zip`; conferir em Assets. O ZIP também sai local com `tools/gerar_zip.py`.
4. O "Source code" automático do GitHub não pode ser removido e fica completo de propósito.

## Pendências (v0.3.1)

- [ ] **Teste manual no Windows**: instalar pelo link do GitHub no Claude Code, rodar
      `tests/roteiros/2026-11-07-pegadinhas.txt`, conferir com o gabarito ao lado, rodar
      `py -m unittest discover tests` e anotar o resultado na seção "Histórico" do gabarito.
- [ ] **Refazer o teste no Claude App com o `gerar-telas-0.3.0.zip`**: conferir o ZIP de entrega
      (PNGs na raiz + `extras/`) e anotar o caminho que o `render.py` imprimiu.
- [ ] **Ler o QR com um celular de verdade** (os testes usam o `zxing-cpp`; o celular é o que importa
      na transmissão).
- Se algo falhar: corrigir, atualizar o CHANGELOG e publicar a v0.3.1.

## Planos futuros

Veja "Planos futuros" no [README.md](README.md). Ideias menores: integração com o repositório
`DedeDuarte/Pastas-Brooklin-Em-Pauta` (o comando `BP` do terminal do Windows, que cria as pastas de
cada edição) e um script de instalação (dispensado na 0.2.0; reavaliar se a instalação pelo README falhar).
