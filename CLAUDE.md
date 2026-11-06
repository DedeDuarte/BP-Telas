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

- Transforma o roteiro do informativo **Brooklin em Pauta** (IASD Brooklin) em telas PNG 1920×1080
  transparentes (lower-thirds). Funciona no Claude Code (Windows e Linux) e no Claude App / claude.ai.
- Fluxo: roteiro → Claude redige título/corpo/QR → **usuário aprova a tabela** → JSON →
  `scripts/render.py` → PNGs em `Downloads/Telas AAAA-MM-DD/` (+ `telas.json` + `_preview.jpg`).
  No Claude App (sem Downloads) o render também gera `Telas AAAA-MM-DD.zip` (PNGs na raiz; preview
  e JSON em `extras/`) e o Claude entrega só esse ZIP.
- Repositório: https://github.com/DedeDuarte/BP-Telas (público, MIT, inclusive o logo — decisão do
  usuário). Última versão: **v0.3.0** (2026-11-05). Histórico em [CHANGELOG.md](CHANGELOG.md).
- `design/` guarda as telas e o modelo **originais**, para comparar com o que a skill gera. Mantenha
  essas imagens no repositório (decisão do usuário); o visual do QR e algumas regras de texto mudaram
  depois delas ("Pr." virou "pastor", acento em "SÉRIE", logo no QR).

## Preferências do usuário

- O roteiro chega **já limpo** (sem abertura/encerramento). O usuário não quer responder muitas
  perguntas: a skill só pergunta quando há ambiguidade real (ex.: link sem número claro).
- Regras de redação em `references/tipos-de-tela.md`: títulos fixos `CULTO DE DOMINGO` /
  `CULTO DE QUARTA`; sempre "pastor" por extenso; ano atual salvo se outro estiver escrito;
  corrigir português do roteiro sem mudar o sentido; links usados exatamente como recebidos.
- Gosta do visual novo do QR (logo no centro, legenda em negrito) mais que do original.
- Mudanças pequenas podem ir direto na `main`; para juntar trabalho grande, prefere um PR (aceitar
  com merge commit ou rebase, nunca squash, para manter o histórico).

## Decisões técnicas (e por quê)

- **Layout de texto BASIC forçado** (`render.fonte()`): o Pillow usa RAQM no Linux e BASIC no
  Windows, que medem texto diferente → telas diferentes entre sistemas. Descoberto pelo CI.
- **QR com correção de erro Q**: H deixava os quadradinhos pequenos; **M falhou** nos testes de
  leitura com o logo um pouco maior. Logo num quadrado branco 1:1 (28% do código).
- **QR de visitante é arquivo fixo** (`assets/qr-visitante.png`), gerado por
  `scripts/gerar_qr_visitante.py` (link `https://typebot.co/my-typebot-a6oemdd`). Não editar o PNG
  à mão; um teste compara o PNG com o gerador.
- **Faixa branca do corpo e barra azul são desenhadas pelo código**; medidas em
  `references/design-spec.md`.
- **Só o Pillow é requisito**: fontes (`assets/fonts/`) e `segno` (`scripts/vendor/`) vêm dentro da
  skill, porque o ambiente do app pode estar sem internet. Não troque por download nem pip.
- **Limites do claude.ai** (ajuda oficial): `description` do `SKILL.md` com até 200 caracteres; o ZIP
  precisa ter a pasta `gerar-telas/` na raiz. O caminho de saída no app é `$OUTPUT_DIR`, depois
  `/mnt/user-data/outputs` (este último ainda não confirmado na documentação oficial).
- **ZIP de entrega sem pasta interna**: ao extrair, o nome do ZIP já dá a pasta (evita pasta dentro
  de pasta no "Extrair tudo" do Windows).

## Ambiente de desenvolvimento (máquina Linux do usuário)

- `python3 -m venv` não funciona (falta `python3-venv`). Para testar QR localmente:
  `pip install --target <pasta temporária> zxing-cpp` + `PYTHONPATH=<pasta>`. Sem `zxing-cpp`, os 2
  testes de leitura de QR são pulados (rode com ele antes de mexer em QR/logo).
- `roteiros/` e `saida/` são ignorados pelo git (rascunhos locais; as telas antigas em
  `saida/2026-10-23/` **não** devem ser commitadas). `dist/` (ZIPs gerados) também.
- O `gh` instalado não tem `--verify-tag`.

## Testes manuais

`tests/roteiros/2026-11-07-pegadinhas.txt` + `.gabarito.md`: roteiro com pegadinhas só no texto
(links limpos). Resultado em 2026-11-05: 15/16 (errou "da campori" → virou regra de português).

## Publicar uma versão

1. CHANGELOG fechado (`[X.Y.Z] - data` + links de comparação no rodapé; aviso de atualização no topo
   se a forma de instalar mudar) e CI verde na `main` (Windows e Linux).
2. `git tag -a vX.Y.Z -m "vX.Y.Z"` e `git push origin vX.Y.Z`.
3. `gh release create vX.Y.Z --title "vX.Y.Z" --notes-file <notas>` (novidades, aviso de atualização,
   limitações conhecidas). O workflow `release-zip.yml` anexa `gerar-telas-X.Y.Z.zip`; conferir em Assets.
4. O "Source code" automático do GitHub não pode ser removido; ele fica completo de propósito, já que
   o ZIP próprio cobre quem quer só a skill. Para gerar o ZIP localmente: `tools/gerar_zip.py`.

## Pendências (v0.3.1)

- [ ] **Teste manual no Windows**: instalar pelo link do GitHub no Claude Code, rodar o roteiro
      `pegadinhas`, conferir com o gabarito, rodar `py -m unittest discover tests` e anotar o resultado na seção
      "Histórico" do gabarito.
- [ ] **Refazer o teste no Claude App com o `gerar-telas-0.3.0.zip`**: conferir o ZIP de entrega
      (PNGs na raiz + `extras/`) e anotar o caminho que o `render.py` imprimiu.
- [ ] **Ler o QR com um celular de verdade** (os testes usam o `zxing-cpp`; o celular é o que importa
      na transmissão).
- Se algo falhar: corrigir, atualizar o CHANGELOG e publicar a v0.3.1.

## Planos futuros

Veja "Planos futuros" no [README.md](README.md). Ideias menores: integração com o repositório
`DedeDuarte/Pastas-Brooklin-Em-Pauta` (o comando `BP` do terminal do Windows, que cria as pastas de
cada edição) e um script de instalação (dispensado na 0.2.0; reavaliar se a instalação pelo README falhar).
