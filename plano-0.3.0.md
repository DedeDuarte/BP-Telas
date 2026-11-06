# Plano — v0.3.0 (publicada) e próximos passos

> Documento de retomada. Escrito em 2026-11-05, logo após o release da v0.2.0, para que
> qualquer sessão futura (humana ou do Claude) consiga continuar sem o histórico do chat.
>
> **Status (2026-11-05, noite): a v0.3.0 foi publicada** (tag `v0.3.0` em `ef27918`, CI verde nos dois
> sistemas, `gerar-telas-0.3.0.zip` anexado). O que sobrou está em **Pendências para a v0.3.1**, no fim.

## Objetivo da v0.3.0

1. A skill funcionar também no **Claude App / claude.ai**, além do Claude Code.
2. A skill instalada ficar **leve** (hoje ~1,5 MB → meta ~100–400 KB).
3. Fechar as pendências de teste no **Windows**.

---

## Tarefas

> 2026-11-05 (noite): `description` encurtada para ≤200 caracteres (limite citado na ajuda do claude.ai),
> `$OUTPUT_DIR` suportado no render e tarefa 2 concluída (skill versionada: ~680 KB; logo 256 px).
> Ainda sem confirmação oficial de `/mnt/user-data/outputs` no claude.ai: validar no teste do app.

### 0. Antes de começar — pendências de validação

- [ ] **Teste no Windows** (combinado para sexta, 2026-11-06): instalar a skill pelo link do
      GitHub no Claude Code do Windows, rodar `tests/roteiros/2026-11-07-pegadinhas.txt` e conferir
      com o gabarito ao lado. Rodar `py -m unittest discover tests`.
      Anotar o resultado na seção "Histórico" do gabarito.
- [x] **Teste no Claude App** (2026-11-05): a redação/tabela acertou todas as pegadinhas; o render
      falhou porque o ambiente não tinha `segno` nem internet (download da fonte deu 403). Pillow 12.3.0
      já estava instalado. → resolvido embutindo fontes e segno (tarefa 1). Testar de novo com o ZIP novo.
- [x] **Testar de novo no Claude App** com um ZIP da skill atual (fontes e segno embutidos):
      funcionou; as telas foram geradas e entregues em um único ZIP. Depois desse teste, o ZIP de
      entrega perdeu a pasta interna (ver `96af1e8`): **refazer o teste com o ZIP do release**.
- [ ] Ler o QR das telas com o **celular de verdade** (o leitor dos testes é o zxing-cpp; celular
      é o que importa na transmissão).

### 1. Compatibilidade com Claude App / claude.ai

Contexto: no app, skills rodam num ambiente Linux isolado da Anthropic (code execution).
Não há pasta Downloads do usuário, a instalação é por **upload de ZIP** (Configurações →
Capacidades → Skills) e o acesso à internet/pip pode estar bloqueado.

- [x] **Confirmar na documentação oficial** como skills rodam no app (pesquisa de 2026-11-05):
      a rede depende do plano/configuração (Free/Pro/Max com pacotes liberados; Team/Enterprise
      desligada por padrão); o Pillow é pré-instalado, `segno` e fontes não constam (por isso foram
      embutidos); skills não sincronizam entre superfícies; ZIP com a pasta da skill na raiz e nome
      igual ao `name`; a ajuda cita `description` de até 200 caracteres. **Não confirmado:** o caminho
      `/mnt/user-data/outputs` (o render usa `$OUTPUT_DIR` primeiro, depois esse caminho).
- [x] **Embutir as fontes** Open Sans Bold e ExtraBold em `assets/fonts/` (hoje são baixadas e
      ignoradas pelo git). Incluir `OFL.txt` (licença SIL OFL 1.1 exige). Manter `fonts.py` só como
      fallback ou removê-lo. Atualizar `.gitignore`.
- [x] **Embutir o `segno`** (Python puro, licença BSD) em `scripts/vendor/` com a licença dele, ou
      confirmar que o app já o tem. Objetivo: o único requisito externo ser o Pillow.
- [x] **Detectar o ambiente** em `render.py`: se não houver pasta Downloads do usuário (ambiente do
      app), salvar na pasta de saída do ambiente. Documentar no `SKILL.md` como entregar os
      arquivos ao usuário nesse caso.
- [x] **Comandos no `SKILL.md`**: hoje mostram `py` (Windows) e `python3` (Linux). No app é sempre
      `python3`. Deixar claro.
- [x] **ZIP da skill em cada release**: anexar `gerar-telas-X.Y.Z.zip` aos releases do GitHub
      (manualmente ou com GitHub Actions disparado pela tag). README com o passo a passo de
      instalação/desinstalação no app.

### 2. Skill instalada mais leve

Medido em 2026-11-05 (pasta `.claude/skills/gerar-telas/`, ~1,5 MB):

| Arquivo | Tamanho | Ação |
|---|---|---|
| `assets/logo-qr.png` | 807 KB (1265×1243 px; vira ~70 px no QR) | Reduzir para ~512 px (~50 KB). Original em alta → `design/` |
| `examples/telas/*.png` (7) | 540 KB | Mover para `design/` (não são usadas pelo script) |
| `assets/modelo.png` | 98 KB | Mover para `design/` (referência histórica; o usuário quer manter) |

- [x] Criar `design/` na raiz (fora da skill = não é instalado) e mover os arquivos acima.
- [x] Reduzir `logo-qr.png` e **regerar `qr-visitante.png`** (`scripts/gerar_qr_visitante.py`).
      Conferir que os testes de leitura de QR continuam passando.
- [x] Atualizar referências a esses caminhos em `SKILL.md`, `references/*.md` e `README.md`.
- [x] Instalação com **`git clone --depth 1`** no README (evita baixar o histórico, que cresce a
      cada PNG alterado).

### 3. Release

- [x] CHANGELOG: mover "Não publicado" → `[0.3.0] - AAAA-MM-DD` + links de comparação no rodapé.
- [x] Se a forma de instalar mudar, aviso de atualização no topo da seção (como na 0.2.0).
- [x] Push → esperar CI verde (Windows e Linux) → `git tag -a v0.3.0` → `gh release create`.
- [x] Notas do release: novidades, aviso de atualização, limitações conhecidas.

### Pendências para a v0.3.1

- [ ] **Teste manual no Windows** (item da seção 0): instalar pelo link do GitHub, rodar o roteiro
      `pegadinhas`, conferir com o gabarito e anotar no "Histórico" do gabarito.
- [ ] **Refazer o teste no Claude App com o `gerar-telas-0.3.0.zip` do release**: conferir que o ZIP
      de entrega vem só com os PNGs na raiz e `extras/` (preview + JSON), e anotar o caminho que o
      `render.py` imprimiu (confirma `$OUTPUT_DIR` ou `/mnt/user-data/outputs`).
- [ ] **Ler o QR com um celular de verdade** (seção 0).
- [ ] Se algo falhar nos testes: corrigir, atualizar o CHANGELOG e publicar a v0.3.1 (o workflow
      `release-zip.yml` anexa o ZIP sozinho quando o release é publicado).

### Como publicar uma versão (aprendido na 0.3.0)

1. CHANGELOG fechado e CI verde na `main`.
2. `git tag -a vX.Y.Z -m "vX.Y.Z"` e `git push origin vX.Y.Z`.
3. `gh release create vX.Y.Z --title "vX.Y.Z" --notes-file <notas>` (esta versão do `gh` não tem
   `--verify-tag`). O workflow anexa `gerar-telas-X.Y.Z.zip`; conferir em Assets.
4. O "Source code" automático do GitHub não pode ser removido; tentou-se enxugá-lo com
   `.gitattributes` (`export-ignore`), mas a decisão final foi deixá-lo completo.

### Ideias para depois (fora da 0.3.0)

- Integração com o repositório `DedeDuarte/Pastas-Brooklin-Em-Pauta` (o comando `BP` do usuário
  no terminal do Windows, que cria a estrutura de pastas de cada edição).
- Script de instalação (o usuário dispensou na 0.2.0; reavaliar se a instalação pelo README falhar).

---

## Contexto importante

### O projeto

- Skill `gerar-telas` (em `.claude/skills/gerar-telas/`) que transforma o roteiro do informativo
  **Brooklin em Pauta** (IASD Brooklin) em telas PNG 1920×1080 transparentes (lower-thirds).
- Fluxo: roteiro → Claude redige título/corpo/QR → **usuário aprova a tabela** → JSON →
  `scripts/render.py` → PNGs em `Downloads/Telas AAAA-MM-DD/` (+ `telas.json` + `_preview.jpg`). No Claude App (sem Downloads)
  o render também gera `Telas AAAA-MM-DD.zip` (PNGs na raiz; preview e JSON em `extras/`).
- Repositório: https://github.com/DedeDuarte/BP-Telas (público, MIT, inclusive o logo — decisão
  do usuário). Releases: v0.1.0 e v0.2.0 (ambas em 2026-11-05).

### Preferências e regras do usuário

- Windows é prioridade, mas tem de funcionar no Linux.
- Commits: Conventional Commits, só título, sem body; breaking change com `!` + rodapé
  `BREAKING CHANGE:`. Um commit por mudança. (Tudo em `CLAUDE.md`.)
- O usuário envia o roteiro **já limpo** (sem abertura/encerramento) e não quer responder muitas
  perguntas. A skill só pergunta quando há ambiguidade real (ex.: link sem número claro).
- Regras de redação (em `references/tipos-de-tela.md`): títulos fixos `CULTO DE DOMINGO` /
  `CULTO DE QUARTA`; sempre "pastor" por extenso; ano atual salvo se outro estiver escrito;
  corrigir português do roteiro sem mudar o sentido; links usados exatamente como recebidos.
- Gosta do visual novo do QR (logo no centro, legenda em negrito) mais que do original.

### Decisões técnicas (e por quê)

- **Layout de texto BASIC forçado** (`render.fonte()`): o Pillow usa RAQM no Linux e BASIC no
  Windows, que medem texto diferente → telas diferentes entre sistemas. Descoberto pelo CI.
- **QR com correção de erro Q**: H deixava os quadradinhos pequenos; **M falhou** nos testes de
  leitura com o logo um pouco maior. Q é o equilíbrio. Logo num quadrado branco 1:1 (28% do código).
- **QR de visitante é arquivo fixo** (`assets/qr-visitante.png`), gerado por
  `scripts/gerar_qr_visitante.py`. Link: `https://typebot.co/my-typebot-a6oemdd`.
  Não editar o PNG à mão; um teste compara o PNG com o gerador (com tolerância de suavização).
- **Faixa branca do corpo e barra azul são desenhadas pelo código**; medidas em
  `references/design-spec.md` (extraídas dos PNGs originais).
- O QR original de visitante não era lido pelo zxing com a tela inteira (pouca margem branca);
  o novo é lido em 1080p/720p/540p.

### Ambiente de desenvolvimento (máquina Linux do usuário)

- `python3 -m venv` não funciona (falta `python3-venv`). Para testar QR localmente foi usado
  `pip install --target <pasta temporária> segno zxing-cpp` + `PYTHONPATH`.
- Testes: `python3 -m unittest discover tests` (sem `zxing-cpp` os testes de leitura são pulados).
- `roteiros/` e `saida/` são ignorados pelo git (rascunhos locais do usuário; há telas antigas
  em `saida/2026-10-23/` que **não** devem ser commitadas).

### Testes manuais

- `tests/roteiros/2026-11-07-pegadinhas.txt` + `.gabarito.md`: roteiro com pegadinhas só no texto
  (links limpos). Resultado em 2026-11-05: 15/16 (errou "da campori" → virou regra de português).
