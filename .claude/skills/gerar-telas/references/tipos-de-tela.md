# Tela padrão e regras de redação

Existe **um único tipo de tela**: título na barra azul + corpo em texto azul + bloco QR
(ver [design-spec.md](design-spec.md)). Exemplos: os PNGs de `design/telas/` (só no repositório).

## Quais pontos do roteiro viram tela

**Todos.** O usuário já envia o roteiro limpo, só com os pontos que devem virar tela.
Exceção: se aparecer um ponto que claramente é só fala do locutor (abertura, encerramento,
"esta edição chegou ao fim"), sinalize-o na tabela de aprovação como "sem tela?" e pergunte.

## QR code

**Padrão:** o QR de visitante (`assets/qr-visitante.png`). Use-o em toda tela que não tenha link.

**QR personalizado:** quando o usuário passar um link para um ponto, a tela ganha um QR gerado
com esse link, o logo da igreja no centro e uma legenda. No JSON: `"qr": {"link": ..., "legenda": ...}`.

### De onde vêm os links

O usuário pode passar o link de duas formas:

- **Dentro do ponto** do roteiro (o link aparece no texto do item `3.`) → vale para o ponto 3.
- **No final do pedido**, indicando o número: `link do 3: https://...` (aceite variações como
  `link 3:`, `3 →`, `ponto 3: https://...`) → vale para o ponto 3 do roteiro.

Se um link não deixar claro a qual ponto pertence, **pergunte** — nunca adivinhe.
O número é sempre o do roteiro, não o da ordem das telas.

### Regras do link (obrigatórias)

- Use o link **exatamente** como o usuário escreveu: não encurte, não troque por bit.ly,
  não adicione parâmetros, não "corrija". O QR precisa apontar direto para o destino.
- O script só aceita `http://` ou `https://`. Se o usuário mandar sem (ex.: `chat.whatsapp.com/abc`),
  pergunte antes de completar com `https://`.
- Links muito longos (~100+ caracteres) geram QR ilegível e o script recusa: avise o usuário e
  peça um link mais curto **do próprio serviço** (ex.: o link curto oficial do Google Forms).

### Legenda

Texto curto abaixo do QR dizendo **o que acontece ao escanear**, no imperativo:
`ENTRE NA COMUNIDADE`, `FAÇA SUA INSCRIÇÃO`, `ASSISTA NO YOUTUBE`, `CONTRIBUA AQUI`.

- Até 2 linhas curtas (~20 caracteres por linha); o script reduz a fonte se precisar.
- Não repita o título da tela; não escreva o link.
- Com QR personalizado, o corpo pode dizer "leia o QR Code" — é coerente com a tela.
- Sem QR personalizado, o corpo **não** deve mandar ler QR (o da tela é o de visitante):
  use o telefone/contato no corpo.

## Redação

**Título** (barra azul)
- **Regra obrigatória:** pontos sobre o culto de domingo ou o culto de quarta têm título
  `CULTO DE DOMINGO` ou `CULTO DE QUARTA` — nunca o nome da série, do pregador ou da classe.
  O nome da série vai no corpo.
- Demais pontos: 1 a 4 palavras, nome do evento/ministério. Ex.: `ADOTE UM DESBRAVADOR`, `SECRETARIA`.

**Corpo** (texto azul)
- Até ~140 caracteres, para caber em 2 linhas sem reduzir demais a fonte.
  O script coloca em CAIXA ALTA, quebra as linhas e reduz a fonte (34 → 26 px) se precisar.
- Só o essencial: o quê + quando + onde/contato. Corte a narrativa do locutor.
- Horários no formato `10h`, `19h30`; telefones no formato `(11) 94914-7174`.
- **Regra obrigatória:** escreva sempre `pastor` por extenso — nunca `Pr.`, `pr.` ou `Pastor(a)`
  abreviado —, mesmo que o roteiro abrevie ou que o texto fique apertado (encurte outra parte).
- Pode terminar com chamada curta: `Esperamos você!`, `Participe!`, `Inscreva-se com a equipe do MIB!`.

**Português** (título, corpo e legenda do QR)
- **Regra obrigatória:** o roteiro pode ter erros. Na tela, o português tem de estar correto:
  concordância de gênero e número, acentuação, crase, ortografia e pontuação.
  Ex.: "a última campori" → "o último campori"; "as 19h" → "às 19h"; "tranferência" → "transferência".
- Corrija **sem mudar o sentido**: não troque nomes próprios, nomes de séries, datas, horários,
  números ou valores. Se não der para saber o que o roteiro quis dizer, pergunte.
- Não é preciso avisar cada correção ortográfica; a tabela de aprovação já mostra o texto final.

Exemplo — roteiro, ponto 2 (≈90 palavras) → corpo:
> AMANHÃ, ÀS 10H, O PASTOR JOSÉ ORLANDO ENCERRA A SÉRIE “CORAÇÃO E MENTE” COM A MENSAGEM “MENTE E CORAÇÃO SAUDÁVEIS”. ESPERAMOS VOCÊ!

Exemplo completo (roteiro → JSON): [examples/roteiros/2026-10-31.txt](../examples/roteiros/2026-10-31.txt)
→ [examples/roteiros/2026-10-31.json](../examples/roteiros/2026-10-31.json).
