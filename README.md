# YDT

YDT é uma ferramenta simples e eficiente para baixar vídeos do YouTube em formato MP3 (somente áudio) ou MP4 (áudio e vídeo). Utilizando uma interface gráfica amigável desenvolvida com Flet, YDT facilita o gerenciamento de links de download e a seleção do formato desejado.

## Requisitos

Para executar o YDT, você precisará ter instalado em seu sistema:

- Python 3.7 ou superior;
- yt-dlp;
- Flet;
- pyperclip
- ffmpeg

## Instalação

Siga as instruções abaixo para instalar os requisitos necessários:

**1. Clone o repositório:**

`git clone https://github.com/GuiAgapito/ydt.git`
`cd YDT`

**2. Crie um ambiente virtual (opcional, mas recomendado):**

`python -m venv venv`
`source venv/bin/activate  # No Windows: venv\Scripts\activate`

**3. Instale as dependências:**

`pip install flet yt-dlp pyperclip`

**Windows:**
- `winget install "FFmpeg (Essentials Build)"`

**Linux:**
- `sudo apt install ffmpeg`

# Como usar:

**1. Adicionar Links:**

- Insira o link do vídeo do YouTube no campo "Link do vídeo" e clique em "Adicionar link".

**Selecionar Formato:**

- Escolha o formato desejado (MP3 ou MP4) na seção "Selecionar o formato do download".

**Iniciar Download:**

-Após adicionar todos os links e selecionar o formato, clique em "Iniciar download".

**Gerenciar Links:**

- Você pode remover links indesejados clicando no ícone de lixeira ao lado de cada link.
Para copiar um link para a área de transferência, clique no ícone de copiar ao lado do link.

**Limpar Lista:**

- Para limpar todos os links da lista, clique em "Limpar lista".
