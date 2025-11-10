# PixelPath: Extrator de Documentos (Otimizado para Baixo Consumo)

Bem-vindo ao PixelPath! Este é um sistema leve e otimizado para extrair informações (texto e tabelas) de arquivos PDF, mesmo em computadores com pouca memória ou CPU, pois ele evita o uso de recursos pesados.

## ⚠️ Pré-requisitos (O que você precisa ter)

Antes de começar, certifique-se de que você tem o **Python** instalado no seu computador. Ele é o programa principal que roda este projeto.

Você também precisará de um **Prompt de Comando** (ou **Terminal**) para executar os comandos de instalação e inicialização.

---

## 🚀 Passo a Passo para Começar

Siga estas 4 etapas simples:

### Passo 1: Obter os Arquivos do Projeto

Se você executou este script (`create_project_full.py`), todos os arquivos e pastas (como `pixelpath/`) já foram criados.

### Passo 2: Instalar os Programas Auxiliares (Dependências)

Você precisa instalar as bibliotecas Python que o PixelPath usa para funcionar, incluindo agora as bibliotecas de exportação para planilha (`pandas` e `openpyxl`).

1.  Abra o seu **Prompt de Comando** (ou Terminal).
2.  Navegue até a pasta onde você salvou o arquivo `requirements.txt` e o diretório `pixelpath`.
3.  Execute o seguinte comando para instalar tudo:

    ```bash
    pip install -r requirements.txt
    ```
    *Aguarde a instalação terminar.*

### Passo 3: Ligar o Servidor da API

O PixelPath funciona como um serviço web local. Você precisa iniciá-lo.

1.  Ainda no seu Prompt de Comando, execute este comando para ligar a API:

    ```bash
    uvicorn pixelpath.api.main:app --host 0.0.0.0 --port 8000
    ```

2.  Se o servidor ligar corretamente, você verá mensagens indicando que ele está rodando no endereço `http://127.0.0.1:8000` (ou `http://0.0.0.0:8000`).

    **Importante:** Deixe esta janela do Prompt de Comando aberta. Se você fechá-la, o servidor desliga.

### Passo 4: Como Usar (Extrair um PDF)

Com o servidor ligado (Passo 3), você pode enviar um arquivo PDF para que ele seja processado.

**O endpoint agora aceita o formato de saída como parâmetro de consulta:**

* **URL:** `http://localhost:8000/extract?output_format=FORMATO`
* **FORMATO:**
    * `json` (Padrão: retorna o JSON estruturado)
    * `csv` (Retorna o arquivo CSV binário)
    * `xlsx` (Retorna o arquivo Excel binário)

**Exemplo usando `curl` para XLSX:**

```bash
curl -X POST "http://localhost:8000/extract?output_format=xlsx"      -H "accept: application/json"      -F "file=@/caminho/doc.pdf"      --output extraction_data.xlsx
```

**Exemplo usando `curl` para JSON (Estrutura):**

```bash
curl -X POST "http://localhost:8000/extract?output_format=json"      -F "file=@/caminho/doc.pdf"
```

---

## 💡 Notas de Otimização

Este sistema foi projetado para ser **muito leve** e funcionar bem em ambientes restritos:

* **Baixo Uso de CPU/Memória:** Ele renderiza as páginas em escala de cinza e usa a DPI mais baixa (150 DPI) para evitar que o uso de memória ultrapasse ~100 MB por página.
* **Sem Paralelismo:** O processamento é limitado a 1 thread (`1 thread`), minimizando a carga sobre a CPU.
* **Segurança (CORS):** Em produção (como no Render), o acesso é restrito apenas às URLs definidas na variável de ambiente `ALLOWED_ORIGINS`.
