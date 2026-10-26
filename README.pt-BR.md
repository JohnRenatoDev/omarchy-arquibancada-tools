# Arquibancada tools

[English](README.md) | [Português (Brasil)](README.pt-BR.md)

Artes-base, compositor de wallpapers, instalador opcional dos clubes e
verificações do [Arquibancada](https://github.com/JohnRenatoDev/omarchy-arquibancada-theme),
a coleção de temas Omarchy dos 20 clubes da Série A brasileira de 2026.

O tema pronto é distribuído em seu próprio repositório. Estas ferramentas usam
um checkout separado do tema. Gerar ou validar arquivos não ativa um tema no desktop.

## Instalar os temas dos clubes

Para instalar a variante padrão do Santos pelo Omarchy, siga as instruções do
[repositório do tema](https://github.com/JohnRenatoDev/omarchy-arquibancada-theme/blob/main/README.pt-BR.md#instalação).
O instalador opcional daqui adiciona as 20 variantes de um checkout local:

```bash
git clone https://github.com/JohnRenatoDev/omarchy-arquibancada-theme.git
git clone https://github.com/JohnRenatoDev/omarchy-arquibancada-tools.git
cd omarchy-arquibancada-tools
./install.sh --source ../omarchy-arquibancada-theme --link --menu
omarchy theme set flamengo
```

Mantenha o checkout do tema no lugar ao usar links. O checkout das ferramentas
fornece o instalador e os nomes dos clubes; os links apontam para o checkout do
tema. `--menu` acrescenta as entradas que faltam e faz backup do menu existente.
Repetir o comando preserva as entradas já criadas.

Use `--copy` no lugar de `--link` para criar uma cópia independente. Temas locais
armazenados como diretórios comuns são preservados, inclusive cópias criadas em
uma execução anterior. O instalador precisa de Bash e dos utilitários GNU de
arquivos; `--menu` também precisa de Python 3. Ele roda com seu usuário, sem `sudo`.

## Gerar e revisar

Você precisa de Python 3.11 ou mais recente, ImageMagick, `rsvg-convert` e das
fontes Anton, Oswald e JetBrains Mono. As artes revistas dos mascotes, os escudos
e as licenças das fontes ficam em `assets/`. A composição usa os arquivos salvos,
sem precisar de gerador de imagens, GPU ou token de API.

```bash
# Gerar todos os wallpapers e as prévias em um checkout separado.
nice -n 19 python3 src/build.py --output-dir ../omarchy-arquibancada-theme

# Atualizar só os pôsteres de mascotes e as prévias de um checkout completo.
nice -n 19 python3 src/build.py --output-dir ../omarchy-arquibancada-theme --mascotes-only

# Conferir a distribuição e as artes-base revistas.
nice -n 19 python3 scripts/validate.py --theme-dir ../omarchy-arquibancada-theme
nice -n 19 python3 -m unittest discover -s scripts -p 'test_*.py'
nice -n 19 python3 scripts/validate_badge_regions.py
```

Sem `--output-dir`, o build completo grava em `build/export/`, uma pasta ignorada
pelo Git. Um build parcial precisa de uma exportação completa para os clubes que
não serão gerados, pois ele atualiza a galeria conjunta. Os intermediários ficam
em `build/` neste repositório. Só os arquivos visuais finais vão para o checkout do tema.

O validador rejeita programas, arquivos executáveis, links simbólicos e workflows
em qualquer pasta da distribuição. Ele também confere as 20 paletas, exatamente
três wallpapers 4K por clube, o espelho do Santos na raiz e os hashes das artes e
dos símbolos das camisas revistos. Os testes do instalador usam diretórios
temporários de configuração e cache, sem alterar seu desktop.

Veja as [notas de desenvolvimento](docs/development.pt-BR.md), o
[brief das artes](docs/mascotes-brief.md) e as
[referências das camisas](https://github.com/JohnRenatoDev/omarchy-arquibancada-theme/blob/main/docs/uniformes-2026.md).

## Contribuir

Abra um PR aqui para mudanças no compositor, instalador, verificações ou
artes-base. Envie alterações nas paletas e nos wallpapers finais ao
[repositório do tema](https://github.com/JohnRenatoDev/omarchy-arquibancada-theme).
Inclua uma referência ou um comparativo visual ao propor mudanças nas imagens.

As ilustrações foram geradas com IA e revistas conforme a identidade de cada
clube. Nenhuma representa a preferência clubística do autor. A coleção foi feita
para a comunidade brasileira do Omarchy e os torcedores de todos os clubes incluídos.

## Direitos e créditos

O código e os scripts originais usam MIT. Nomes, escudos, mascotes e outras marcas
pertencem aos seus titulares. O projeto é independente, sem endosso dos clubes,
da ESPN ou do Omarchy. A MIT não concede direitos sobre esses materiais, inclusive
quando aparecem em imagens geradas por IA.

Anton, Oswald e Archivo Black vêm de Google Fonts sob SIL Open Font License 1.1,
com licenças incluídas em `assets/fonts/`. As URLs das fontes e as referências de
camisa acompanham os arquivos de entrada. Veja [LICENSE](LICENSE) e
[NOTICE.md](NOTICE.md).
