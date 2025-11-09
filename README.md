PixelPath: Extrator de Documentos (Otimizado para Baixo Consumo)

Bem-vindo ao PixelPath! Este é um sistema leve e otimizado para extrair informações (texto e tabelas) de arquivos PDF, mesmo em computadores com pouca memória ou CPU, pois ele evita o uso de recursos pesados.

⚠️ Pré-requisitos (O que você precisa ter)

Antes de começar, certifique-se de que você tem o Python instalado no seu computador. Ele é o programa principal que roda este projeto.

Você também precisará de um Prompt de Comando (ou Terminal) para executar os comandos de instalação e inicialização.

🚀 Passo a Passo para Começar

Siga estas 4 etapas simples:

Passo 1: Obter os Arquivos do Projeto

Se você executou o script create_project.py, todos os arquivos e pastas (como pixelpath/) já foram criados. Se não, rode o create_project.py primeiro.

Passo 2: Instalar os Programas Auxiliares (Dependências)

Você precisa instalar as bibliotecas Python que o PixelPath usa para funcionar (como o FastAPI, para a API, e o OpenCV, para o processamento de imagens).

Abra o seu Prompt de Comando (ou Terminal).

Navegue até a pasta onde você salvou o arquivo requirements.txt e o diretório pixelpath.

Execute o seguinte comando para instalar tudo:

pip install -r requirements.txt


Aguarde a instalação terminar.

Passo 3: Ligar o Servidor da API

O PixelPath funciona como um serviço web local. Você precisa iniciá-lo.

Ainda no seu Prompt de Comando, execute este comando para ligar a API:

uvicorn pixelpath.api.main:app --host 0.0.0.0 --port 8000


Se o servidor ligar corretamente, você verá mensagens indicando que ele está rodando no endereço http://127.0.0.1:8000 (ou http://0.0.0.0:8000).

Importante: Deixe esta janela do Prompt de Comando aberta. Se você fechá-la, o servidor desliga.

Passo 4: Como Usar (Extrair um PDF)

Com o servidor ligado (Passo 3), você pode enviar um arquivo PDF para que ele seja processado.

Opção 1: Usando uma Ferramenta de Teste de API (Recomendado para Iniciantes)

Use ferramentas como Insomnia ou Postman para simular o upload do arquivo.

Método: POST

URL: http://localhost:8000/extract

Corpo da Requisição (Body):

Escolha a opção form-data (para enviar arquivos).

Adicione um campo chamado file e use-o para selecionar o seu arquivo PDF.

(Opcional) Adicione os campos dpi (qualidade, 72 a 200) e max_pages (limite de páginas a processar) para customizar a extração.

Opção 2: Usando o Comando curl (Mais técnico)

Se você tiver o curl instalado, pode testar diretamente no Prompt de Comando (substitua /caminho/doc.pdf pelo caminho real do seu arquivo):

curl -X POST "http://localhost:8000/extract?dpi=150&max_pages=50" -F "file=@/caminho/doc.pdf"


O resultado será exibido no seu Prompt de Comando como um grande texto em formato JSON contendo a estrutura de linhas e tabelas extraídas.

💡 Notas de Otimização

Este sistema foi projetado para ser muito leve e funcionar bem em ambientes restritos:

Baixo Uso de CPU/Memória: Ele renderiza as páginas em escala de cinza e usa a DPI mais baixa (150 DPI) para evitar que o uso de memória ultrapasse ~100 MB por página, muito abaixo do limite de 256 MB.

Sem Paralelismo: O processamento é limitado a 1 thread (1 thread), minimizando a carga sobre a CPU.

Sem Aprendizado de Máquina Pesado: Evita bibliotecas grandes como pandas ou sklearn. O agrupamento de texto e a detecção de tabelas usam heurísticas leves e rápidas.