# Documentação de Uso da API PixelPath (v0.1.0)

Esta documentação descreve como consumir o serviço PixelPath, que realiza o processamento de PDFs e retorna dados estruturados (JSON) ou arquivos de planilha (CSV/XLSX).

## 1. Endpoint Principal

O endpoint para processamento de documentos é o `/extract`.

| Método | Caminho | Descrição |
| :--- | :--- | :--- |
| **POST** | `/extract` | Processa um arquivo PDF enviado e retorna o resultado estruturado ou formatado. |

## 2. Parâmetros de Requisição

A requisição deve ser enviada como **`multipart/form-data`** e deve incluir um arquivo e parâmetros opcionais via *query string*.

### A. Campos (Multipart Form Data)

| Nome do Campo | Tipo | Obrigatório | Descrição |
| :--- | :--- | :--- | :--- |
| **`file`** | `File` | Sim | O arquivo PDF a ser processado. |

### B. Parâmetros de Consulta (Query Parameters)

| Nome do Parâmetro | Tipo | Padrão | Validação | Descrição |
| :--- | :--- | :--- | :--- | :--- |
| **`dpi`** | `int` | `150` | `72 <= dpi <= 200` | Resolução de renderização do PDF. Valores mais baixos economizam memória (padrão otimizado para baixo consumo). |
| **`max_pages`** | `int` | `50` | `1 <= pages <= 500` | Número máximo de páginas a serem processadas para evitar sobrecarga de memória. |
| **`output_format`** | `string` | `"json"` | `json`, `csv`, `xlsx` | Formato de saída desejado. Determina se a API retorna a estrutura JSON ou um arquivo binário de planilha. |

## 3. Tipos de Resposta (Baseado em `output_format`)

O tipo de resposta varia de acordo com o parâmetro `output_format`.

### 3.1. Resposta JSON (Padrão: `output_format=json`)

Retorna a estrutura completa do documento, incluindo metadados da página, lista de linhas de texto e uma lista de tabelas detectadas.

| Campo | Tipo | Descrição |
| :--- | :--- | :--- |
| **`meta`** | `object` | Metadados globais da extração. |
| **`pages`** | `array<object>` | Lista de resultados, um objeto por página processada. |
| **`pages[].lines`** | `array<object>` | Blocos de texto detectados e agrupados por linha. |
| **`pages[].tables`** | `array<object>` | Tabelas detectadas, com suas células estruturadas (prontas para exportação). |

### 3.2. Resposta de Arquivo (`output_format=csv` ou `output_format=xlsx`)

Se o formato for `csv` ou `xlsx`, a API retorna um arquivo binário para download.

| Parâmetro | `csv` | `xlsx` |
| :--- | :--- | :--- |
| **`Content-Type`** | `text/csv` | `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` |
| **Conteúdo** | Arquivo CSV (texto delimitado por vírgulas). | Arquivo XLSX (planilha Excel). |
| **Lógica** | O servidor extrai todas as células de todas as tabelas e concatena-as em uma única planilha (uma tabela por linha). | |

## 4. Exemplos de Uso (`curl`)

Assumindo que a API está rodando em `http://localhost:8000` e o arquivo PDF está em `/caminho/doc.pdf`.

### Exemplo A: Extração para JSON (Estrutura)

```bash
curl -X POST "http://localhost:8000/extract?dpi=150&output_format=json"      -F "file=@/caminho/doc.pdf"
# Resultado: Retorna um objeto JSON na saída padrão.
```

### Exemplo B: Extração para Planilha Excel (.xlsx)

```bash
curl -X POST "http://localhost:8000/extract?output_format=xlsx"      -H "accept: application/json"      -F "file=@/caminho/doc.pdf"      --output extraction_data.xlsx
# Resultado: Salva o arquivo binário como extraction_data.xlsx
```
