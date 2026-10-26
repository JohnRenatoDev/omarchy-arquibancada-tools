# Artes e desenvolvimento

[README](https://github.com/JohnRenatoDev/omarchy-arquibancada-theme/blob/main/docs/../README.pt-BR.md) | [English](development.md) | [Português (Brasil)](development.pt-BR.md)

Os caminhos abaixo são relativos à raiz do repositório.

## Três wallpapers por clube

Os nomes dos estádios foram conferidos em fontes primárias em 19/10/2026.
[docs/estadios.md](https://github.com/JohnRenatoDev/omarchy-arquibancada-theme/blob/main/docs/estadios.md) reúne as referências e as observações sobre
mandos temporários. Palmeiras usa Nubank Parque; São Paulo usa MorumBIS. As
legendas de Palmeiras, São Paulo, Bahia e Mirassol têm os nomes atualizados.

Os 20 uniformes foram revistos com fotografias das camisas de 2026, registradas em
[docs/uniformes-2026.md](https://github.com/JohnRenatoDev/omarchy-arquibancada-theme/blob/main/docs/uniformes-2026.md). A revisão de 20/10 usa os arquivos
originais dos brasões projetados sobre a superfície de cada camisa, acompanhando
a perspectiva e a curvatura do peitoral, com luz e trama de tecido. Letras e
estrelas conservam o desenho original. Posição, escala e folgas foram revistas
em todos os clubes. São Paulo e Coritiba usam escudo central; os demais seguem
o peitoral esquerdo de quem veste. Flamengo usa CRF, Cruzeiro as cinco estrelas
e Vasco a cruz dentro da faixa branca. A composição ao redor mantém o escudo
completo do clube.

O Saci do Internacional mantém sua única perna apoiada no gramado e segura a bola
no braço. Athletico usa Fura-Cão; Botafogo usa Bira; Bahia usa Homem de Aço;
Fluminense usa Guerreiro. Leões, aves e personagens humanos têm uniforme, anatomia
e cores próprios. As camisas seguem fotografias dos modelos atuais, e os símbolos
usam os arquivos originais separados. Não foram adicionados patrocinadores.

## Arquivos e prévias

- `<output-dir>/themes/<slug>/`: paleta, três JPEGs, prévia e arquivos extras do Omarchy.
- `assets/mascotes-generated/<slug>.png`: 20 artes-base independentes.
- `assets/mascotes-generated/prompts.json`: prompts dos quatro primeiros clubes.
- `assets/mascotes-generated/serie-a-2026-prompts.json`: prompts dos outros 16 e
  correções de enquadramento de Atlético-MG, Chapecoense, Cruzeiro e Fluminense.
- `assets/mascotes-generated/uniformes-2026-prompts.json`: prompts e referências
  das 20 edições de camisa feitas com a ferramenta integrada `image_gen`.
- `assets/crests/serie-a-2026-sources.json`: URLs dos 16 escudos adicionados.
- `assets/kit-badges/`: variantes dos símbolos de camisa, com fontes em `sources.json`.
- `src/badge_surface.py`: projeção do símbolo original sobre a superfície da camisa.
- `src/mascotes-layout.json`: modelo de camisa, posição anatômica, fontes e hashes
  da arte e do símbolo de cada clube, com os quatro pontos da superfície da camisa
  e sua curvatura para projetar o desenho original conforme a pose.
- [Camisas atuais e referências da revisão](https://github.com/JohnRenatoDev/omarchy-arquibancada-theme/blob/main/docs/uniformes-2026.md).
- [Estádios e fontes oficiais](https://github.com/JohnRenatoDev/omarchy-arquibancada-theme/blob/main/docs/estadios.md).
- [Revisão ampliada das camisas](https://github.com/JohnRenatoDev/omarchy-arquibancada-theme/blob/main/docs/uniformes-revisao.jpg).
- [Prévia dos 20 pôsteres](https://github.com/JohnRenatoDev/omarchy-arquibancada-theme/blob/main/docs/mascotes-cartoon.png).
- [Catálogo dos 60 wallpapers](https://github.com/JohnRenatoDev/omarchy-arquibancada-theme/blob/main/docs/preview.png), com uma linha por clube e três colunas.
- [Status e revisão](https://github.com/JohnRenatoDev/omarchy-arquibancada-theme/blob/main/docs/mascotes-status.md).
- [Verificação de integridade](https://github.com/JohnRenatoDev/omarchy-arquibancada-theme/blob/main/docs/serie-a-2026-verificacao.json).
- [Fontes das identidades](https://github.com/JohnRenatoDev/omarchy-arquibancada-theme/blob/main/docs/serie-a-2026-fontes.md).

## Geração por IA e resolução

As ilustrações foram geradas com a ferramenta integrada `image_gen`, usando a arte
Santos aprovada como referência comum de estilo, câmera e iluminação. O serviço
não expõe seed, número de passos ou versão interna do modelo. Os PNGs nativos têm
1672×941; os JPEGs 3840×2160 são ampliações proporcionais com a imagem inteira
contida no quadro. Não são gerações nativas em 4K.

A tipografia e os escudos da composição são montados separadamente em resolução
final. Os emblemas das camisas também usam os arquivos originais em uma camada
separada. As bases PNG em `assets/mascotes-generated/` contêm o tecido sem brasão;
o compositor produz o wallpaper final.

## Reproduzir o build

Você precisa de Python 3, ImageMagick, `rsvg-convert` e das fontes Anton, Oswald e
JetBrains Mono. As artes geradas fazem parte do pacote, então o build dispensa
gerador de imagens, GPU ou token. A falta de uma arte gera um erro, sem retorno
a SVG simplificado.

```bash
nice -n 19 python3 src/build.py --output-dir ../omarchy-arquibancada-theme --mascotes-only  # só pôsteres e previews dos 20
nice -n 19 python3 src/build.py --output-dir ../omarchy-arquibancada-theme flamengo gremio    # todos os wallpapers desses clubes
nice -n 19 python3 src/build.py --output-dir ../omarchy-arquibancada-theme  # pacote completo
```

`src/teams.py` mantém os dados dos quatro clubes originais e carrega os demais de
`src/serie_a_2026.json`. Para acrescentar um clube, inclua seus dados, escudo real
e uma arte de mascote própria, gerada e revisada. Não basta mudar a cor do mascote
de outro clube.

As folhas de prévias usam miniaturas intermediárias para evitar carregar os 60
wallpapers 4K ao mesmo tempo na memória. As exportações preservam a textura
pintada das ilustrações, sem adicionar ruído sintético pesado.

## Repositórios de ferramentas e temas

Este repositório guarda os programas, as imagens-base revistas e as fontes.
O [repositório do tema](https://github.com/JohnRenatoDev/omarchy-arquibancada-theme) guarda as paletas, os wallpapers e as prévias
finais. O build grava esses resultados em `--output-dir`; os intermediários ficam
na pasta ignorada `build/` das ferramentas. O destino padrão é `build/export`.
Um build parcial precisa de uma exportação completa existente para montar a galeria.

A raiz do tema é a variante do Santos. Os 20 clubes ficam em
`<output-dir>/themes/<slug>/`. Gerar os arquivos não instala nem ativa um tema.

Para validar um checkout separado:

```bash
nice -n 19 python3 scripts/validate.py --theme-dir ../omarchy-arquibancada-theme
nice -n 19 python3 -m unittest discover -s scripts -p 'test_*.py'
nice -n 19 python3 scripts/validate_badge_regions.py
```

`install.sh --source <checkout-do-tema>` instala a distribuição separada. A opção
`--menu` precisa de Python 3. O modo de links acompanha mudanças no checkout do
tema. O modo de cópia cria uma versão independente; uma nova execução preserva
uma cópia existente. Os testes usam caminhos temporários explícitos para
configuração e cache, sem alterar o perfil real do usuário.
