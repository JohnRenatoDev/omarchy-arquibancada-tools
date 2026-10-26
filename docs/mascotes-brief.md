# Brief de geração — pôsteres dos mascotes

Use este brief para gerar os quatro wallpapers em um único modelo/provedor. A
referência visual é o pôster da orca do Santos anexado na conversa.

## Direção comum

- **Estilo:** cartoon cinematográfico semirrealista, arte de pôster esportivo de
  longa-metragem animado. Volumes anatômicos convincentes, musculatura esculpida,
  tecido com dobras/costuras, penas/barba/capa com textura, cel-shading em camadas,
  sombras profundas, highlights e rim light dramático. Não usar aparência de ícone,
  emoji, chibi, mascote flat ou desenho geométrico.
- **Câmera:** contraplongée ao nível do gramado, lente ampla com perspectiva
  controlada; personagem dominante, corpo inteiro visível, sem cortar cabeça, cauda,
  mãos, chuteiras ou bola.
- **Composição:** wallpaper horizontal 16:9 (2048×1152 ou maior); mascote ocupa a
  região centro-direita, espaço negativo escuro à esquerda para o layout do tema.
  Estádio lotado, bandeiras nas cores do clube, fumaça, refletores, gramado e
  partículas de terra iluminadas.
- **Identidade:** cores e uniforme oficiais de cada clube. Reservar no peito um patch
  simples, sem letras inventadas; aplicar o escudo oficial real na composição final.
- **Evitar:** moldura circular, escudos falsos, texto, números, marcas esportivas,
  mascotes duplicados, anatomia fundida, personagem cortado, água/oceano e aparência
  fotográfica pura. O resultado deve continuar claramente sendo uma ilustração cartoon.
- Gerar os quatro no mesmo modelo, proporção, número de passos e nível de detalhe.
  Manter a seed registrada para facilitar iterações.

## Prompt-base

```text
Premium cinematic animated-sports-poster illustration, semi-realistic 3D cartoon
mascot with convincing anatomy and sculpted volumes, intricate hand-painted
surface detail, layered cel shading, expressive determined face, crisp but painterly
contours, fine fabric seams and folds, dramatic chiaroscuro and strong rim lighting.
Ground-level extreme low-angle camera, wide controlled perspective. One single
full-body mascot dominates the center-right; keep the complete head, both feet,
tail, and one soccer ball inside frame. Leave dark uncluttered negative space in the
left quarter. Night football stadium packed with supporters, waving flags in the
club colours, atmospheric smoke, bright floodlights behind the hero, grass and
small flying turf in the foreground. Wide landscape 16:9 composition. No words,
letters, numbers, fake crest, sponsor, brand logo, circular frame, extra mascot,
extra animal, water, stretched anatomy, or cropped limbs. Make the subject a
beautiful, confident, powerful cartoon team mascot, not photorealistic and not flat.
```

## Variações por clube

### Santos — Baleia/Orca

```text
An imposing anthropomorphic killer-whale orca, unmistakable black dorsal head,
white eye patches, broad whale rostrum, white lower jaw, two powerful human-like
arms and legs, broad pectoral fins, curved tail visible behind. Fierce friendly
captain expression. Santos home kit: strict black-and-white vertical stripes, white
shorts, black socks and cleats. One cleat sole rests clearly on top of the foreground
soccer ball. Monochrome black, white and silver throughout.
```

### Corinthians — Mosqueteiro

```text
The Corinthians Musketeer, a confident athletic musketeer with expressive face,
curled moustache, broad feathered hat, flowing cape and raised slender rapier.
Strong human anatomy, not a generic knight. Corinthians kit details in black and
white, dark shorts, monochrome shield patch; one boot planted firmly on the ball.
Use only black, white, graphite and silver.
```

### Palmeiras — Periquito

```text
An athletic anthropomorphic green monk-parakeet mascot: unmistakable curved parrot
beak, bright expressive bird eyes, layered green feathers, long tail feathers and
wing-arms. Upright football-athlete stance, one boot on the ball. Palmeiras kit in
rich club green and white vertical stripes, white shorts and green socks. Green,
white and natural beak gold only.
```

### São Paulo — Santo Paulo

```text
Santo Paulo, an athletic cartoon apostle mascot with a mature expressive face,
short wavy hair and beard, subtle luminous halo, flowing white tunic and a strong
red stole with black-and-white trim. Saintly identity should read clearly without
looking like a generic wizard. São Paulo FC colours: red, white and black. One boot
rests on the ball; the chest patch stays blank for the real crest overlay.
```

## Entrega e composição

Salvar uma imagem aprovada por clube em `assets/mascotes-generated/` com nomes
`santos.png`, `corinthians.png`, `palmeiras.png` e `sao-paulo.png`. Revisar primeiro
uma folha 2×2. Só depois aplicar os escudos reais, compor a tipografia da família de
temas e converter para 3840×2160 sem deformar nem cortar o personagem. Atualizar
`4-caricatura.jpg`, `docs/mascotes-cartoon.png` e `docs/preview.png` juntos.

## Execução de 19/10/2026

Brief executado com a ferramenta integrada `image_gen`. O Santos foi gerado a partir
da imagem original anexada; os outros três foram gerados independentemente usando
a nova arte Santos como referência de linguagem, câmera e iluminação. Os prompts
realmente enviados estão em `assets/mascotes-generated/prompts.json`. A ferramenta
não expõe seed, passos ou versão do modelo; esses parâmetros não são declarados como
controlados. As fontes entregues têm 1672×941 e são compostas proporcionalmente em
3840×2160. Consulte `mascotes-status.md` para a revisão final e a captura aplicada.

## Expansão completa da Série A 2026

Os 16 clubes adicionais estão em `src/serie_a_2026.json`. A mesma direção foi
aplicada individualmente a cada um; prompts exatos e correções de enquadramento
estão em `assets/mascotes-generated/serie-a-2026-prompts.json`. O conjunto agora
contém 20 clubes e foi revisado e instalado. O terceiro wallpaper dos novos temas
é uma composição em duotone da arte gerada, sem alterar os quatro temas originais.

## Revisão de uniformes e seleção de três fundos — 19/10/2026

O pacote atual mantém `1-arte.jpg`, `2-escudo.jpg` e o pôster em `3-mascote.jpg`.
A quarta entrada e os mascotes antigos/duotone foram removidos. A camisa do Santo
Paulo foi editada com `image_gen`: branca com faixas horizontais vermelha e preta,
sem estola atravessando o peito. Halo, barba, corpo inteiro e bola foram mantidos.
Os símbolos exatos são aplicados pelo compositor, com posição, tamanho e rotação
individual por clube. Flamengo usa CRF, Cruzeiro cinco estrelas e Vasco a cruz.
A lista de estádios e suas fontes primárias está em `src/estadios.json` e
`docs/estadios.md`. Os trechos anteriores registram a entrega histórica de quatro
fundos; o formato atual tem três.

## Revisão 3 — camisas atuais e integração no tecido — 19/10/2026

A orientação atual substitui a sobreposição descrita nas etapas históricas acima.
Os 20 mascotes recebem edição individual com a foto da camisa de 2026 como
referência para posição anatômica, escala e versão do símbolo. O brasão é integrado
ao PNG, acompanhando a textura e a luz do tecido. O compositor fica responsável
somente pela imagem contida em 4K, pela tipografia e pelo escudo editorial.

São Paulo e Coritiba usam escudo central. Os outros clubes seguem a aplicação no
peitoral esquerdo de quem veste. Não acrescentar uma segunda aplicação SVG sobre
os PNGs revistos. Preservar sempre `1-arte.jpg` e `2-escudo.jpg` nesta revisão.
Fontes: `uniformes-2026.md`; prompts: `assets/mascotes-generated/uniformes-2026-prompts.json`.
