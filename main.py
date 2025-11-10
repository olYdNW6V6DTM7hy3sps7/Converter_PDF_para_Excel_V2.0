# -*- coding: utf-8 -*-
import os
import sys

def create_project_structure():
    """
    Cria a estrutura de pastas e salva todos os arquivos do projeto PixelPath
    com o conteúdo especificado, incluindo arquivos Python e de documentação.
    """

    # --- Conteúdo dos Arquivos de Documentação ---

    readme_content = """# PixelPath: Extrator de Documentos (Otimizado para Baixo Consumo)

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
curl -X POST "http://localhost:8000/extract?output_format=xlsx" \
     -H "accept: application/json" \
     -F "file=@/caminho/doc.pdf" \
     --output extraction_data.xlsx
```

**Exemplo usando `curl` para JSON (Estrutura):**

```bash
curl -X POST "http://localhost:8000/extract?output_format=json" \
     -F "file=@/caminho/doc.pdf"
```

---

## 💡 Notas de Otimização

Este sistema foi projetado para ser **muito leve** e funcionar bem em ambientes restritos:

* **Baixo Uso de CPU/Memória:** Ele renderiza as páginas em escala de cinza e usa a DPI mais baixa (150 DPI) para evitar que o uso de memória ultrapasse ~100 MB por página.
* **Sem Paralelismo:** O processamento é limitado a 1 thread (`1 thread`), minimizando a carga sobre a CPU.
* **Segurança (CORS):** Em produção (como no Render), o acesso é restrito apenas às URLs definidas na variável de ambiente `ALLOWED_ORIGINS`.
"""

    github_guide_content = """# Guia Simples: Sincronizando seu Projeto com o GitHub

Este guia ensinará como usar o **Git** (uma ferramenta de controle de versão) para conectar sua pasta local (onde está o `PixelPath`) a um repositório online no **GitHub**.

## ⚠️ 0. Pré-requisitos

1.  **Conta no GitHub:** Você precisa ter uma conta gratuita no [GitHub](https://github.com/).
2.  **Git Instalado:** Você precisa instalar o programa **Git** no seu computador. (Procure por "Download Git" no Google.)
3.  **Terminal/Prompt de Comando:** Você fará tudo usando a linha de comando.

## 🚀 1ª Parte: Configurando o Repositório

### Passo 1.1: Criar um Repositório Vazio no GitHub

1.  Acesse o seu GitHub e clique no botão **"New"** (Novo) para criar um novo repositório.
2.  Dê um nome ao seu projeto (ex: `PixelPath-Otimizado`).
3.  Mantenha a opção **"Public"** (Público) ou **"Private"** (Privado) como preferir.
4.  **Muito Importante:** Deixe todas as outras caixas (README, gitignore, license) **DESMARCADAS**. O repositório deve estar **completamente vazio**.
5.  Clique em **"Create repository"** (Criar repositório).

### Passo 1.2: Copiar o Link do Repositório

Após a criação, o GitHub mostrará uma página com instruções. Procure e copie o link que termina em `.git`.

Exemplo: `https://github.com/SeuUsuario/PixelPath-Otimizado.git`

## 💻 2ª Parte: Conectando sua Pasta Local

Abra o seu **Terminal/Prompt de Comando** e navegue até a pasta principal do seu projeto PixelPath (aquela que contém o `create_project_full.py`, o `requirements.txt` e a pasta `pixelpath/`).

### Passo 2.1: Inicializar o Git

Este comando diz ao seu computador para começar a rastrear a pasta como um projeto Git.

```bash
git init
```

### Passo 2.2: Adicionar Todos os Arquivos

Este comando prepara todos os arquivos e pastas para serem enviados ao GitHub.

```bash
git add .
```

### Passo 2.3: Registrar a Primeira Versão (Commit)

O "commit" é como tirar uma foto do estado atual dos seus arquivos. Você precisa dar uma mensagem descrevendo o que foi feito.

```bash
git commit -m "Primeiro commit do projeto PixelPath otimizado"
```

### Passo 2.4: Conectar ao GitHub

Este comando usa o link que você copiou no Passo 1.2 e nomeia a conexão como `origin`.

```bash
git remote add origin SEU_LINK_DO_REPOSITÓRIO
# Exemplo: git remote add origin [https://github.com/SeuUsuario/PixelPath-Otimizado.git](https://github.com/SeuUsuario/PixelPath-Otimizado.git)
```

### Passo 2.5: Enviar para o GitHub (Push)

Este é o comando final que envia seus arquivos locais para o servidor do GitHub.

```bash
git push -u origin main
```
*Se for a primeira vez, pode ser que o Terminal peça seu nome de usuário e senha do GitHub.*

**Pronto!** Seus arquivos agora estão no GitHub!

## 🔄 3ª Parte: Atualizando o Repositório (Sincronizando)

Sempre que você fizer mudanças nos arquivos (como no `README.md` ou nos códigos Python) e quiser salvar essas mudanças no GitHub, siga estes três passos:

1.  **Adicionar:** Prepare as novas alterações para o registro.

    ```bash
    git add .
    ```

2.  **Registrar (Commit):** Crie a nova "foto" das alterações, com uma mensagem descritiva (ex: "Atualizei a lógica do CCL").

    ```bash
    git commit -m "Descreva aqui suas alterações"
    ```

3.  **Enviar (Push):** Envie as alterações registradas para o GitHub.

    ```bash
    git push
    ```
"""

    requirements_content = """fastapi>=0.110
uvicorn[standard]>=0.22
pymupdf>=1.23
numpy>=1.24
opencv-python-headless>=4.8
python-multipart>=0.0.9
pandas>=2.0 # Adicionado para exportação para CSV/XLSX
openpyxl>=3.0 # Adicionado para suporte a XLSX
"""

    # --- Conteúdo dos Arquivos Python ---

    init_content = """__version__ = "0.1.0"
"""

    schemas_content = """from pydantic import BaseModel, Field

class ExtractOptions(BaseModel):
    dpi: int = Field(default=150, ge=72, le=200)
    max_pages: int = Field(default=50, ge=1, le=500)
"""

    utils_content = """from typing import Tuple

BBox = Tuple[int, int, int, int]  # (x1,y1,x2,y2)

def iou(a: BBox, b: BBox) -> float:
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    
    ix1, iy1 = max(ax1, bx1), max(ay1, by1)
    ix2, iy2 = min(ax2, bx2), min(ay2, by2)
    
    iw, ih = max(0, ix2 - ix1), max(0, iy2 - iy1)
    inter = iw * ih
    
    if inter == 0:
        return 0.0
        
    a_area = max(0, ax2 - ax1) * max(0, ay2 - ay1)
    b_area = max(0, bx2 - bx1) * max(0, by2 - by1)
    union = a_area + b_area - inter
    
    return inter / union if union > 0 else 0.0

def inside(a: BBox, b: BBox) -> bool:
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    return ax1 >= bx1 and ay1 >= by1 and ax2 <= bx2 and ay2 <= by2

def merge_boxes(a: BBox, b: BBox) -> BBox:
    return (min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3]))

def expand_box(b: BBox, margin: int) -> BBox:
    return (b[0] - margin, b[1] - margin, b[2] + margin, b[3] + margin)
"""

    render_content = """import fitz
import numpy as np

def open_doc(path: str):
    return fitz.open(path)

def page_count(doc) -> int:
    return doc.page_count

def render_page_gray(doc, page_index: int, dpi: int = 150):
    page = doc.load_page(page_index)
    zoom = dpi / 72.0
    mat = fitz.Matrix(zoom, zoom)
    
    # grayscale para economizar memória
    pix = page.get_pixmap(matrix=mat, colorspace=fitz.csGRAY, alpha=False)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w)
    return img  # uint8 grayscale

def get_words_scaled(doc, page_index: int, dpi: int):
    page = doc.load_page(page_index)
    scale = dpi / 72.0
    # retorna lista de (x1,y1,x2,y2,text) em pixels da imagem renderizada
    words = []
    for w in page.get_text("words"):
        # w = [x0, y0, x1, y1, word, block_no, line_no, word_no]
        if len(w) < 5:
            continue
        x0, y0, x1, y1, text = w[:5]
        words.append((int(x0 * scale), int(y0 * scale), int(x1 * scale), int(y1 * scale), str(text)))
    return words
"""

    preprocess_content = """import cv2
import numpy as np

def binarize_gray(gray: np.ndarray) -> np.ndarray:
    # desfoque leve para ruídos finos, preservando traços
    g = cv2.medianBlur(gray, 3)
    
    # threshold adaptativo robusto a iluminação irregular
    bin_img = cv2.adaptiveThreshold(
        g, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 35, 11
    )
    
    # foreground como 255 (texto), background 0
    # se ficou invertido, invertemos
    if np.mean(bin_img) < 127:
        bin_img = 255 - bin_img
        
    return bin_img
"""

    ccl_content = """import cv2
import numpy as np

# Retorna caixas, centros, áreas (sem manter a matriz de rótulos para economizar memória)
def extract_components(bin_img: np.ndarray):
    # bin_img: 0/255, foreground=255
    num, labels, stats, centroids = cv2.connectedComponentsWithStats(bin_img, connectivity=8)
    
    # stats colunas: [x, y, w, h, area]
    # ignorar background (índice 0)
    boxes = []
    centers = []
    areas = []
    
    # Estatísticas cruas
    raw_areas = stats[1:, 4]
    if raw_areas.size == 0:
        return np.empty((0, 4), dtype=np.int32), np.empty((0, 2), dtype=np.float32), np.empty((0,), dtype=np.int32)

    # thresholds automáticos
    p1 = np.percentile(raw_areas, 5)
    p99 = np.percentile(raw_areas, 99)
    min_area = max(10, int(p1))
    max_area = int(max(p99, min_area + 1))

    for i in range(1, num):
        x, y, w, h, a = stats[i]
        
        if a < min_area or a > max_area or w < 1 or h < 1:
            continue
            
        boxes.append((int(x), int(y), int(x + w), int(y + h)))
        cx, cy = centroids[i]
        centers.append((float(cx), float(cy)))
        areas.append(int(a))
        
    # liberar memória cedo
    del labels
    
    return (
        np.array(boxes, dtype=np.int32),
        np.array(centers, dtype=np.float32),
        np.array(areas, dtype=np.int32),
    )
"""

    pathfinder_content = """# Refinos leves para unir "ilhas" (pontos/acentos) a glifos próximos, sem tocar pixels
# Implementa uma união por proximidade geométrica, baixo custo (sem visitar pixel-a-pixel globalmente)
import numpy as np
from .utils import merge_boxes

def refine_merge_islands(boxes: np.ndarray, centers: np.ndarray, areas: np.ndarray):
    if boxes.shape[0] == 0:
        return boxes, centers, areas

    # estimativas
    med_w = np.median(boxes[:, 2] - boxes[:, 0])
    med_h = np.median(boxes[:, 3] - boxes[:, 1])
    med_area = np.median(areas)
    
    # consideramos "ilhas" componentes muito pequenos
    island_thr = max(5, int(0.2 * med_area))
    is_island = areas <= island_thr
    
    # índice simples: ordenar por x centro
    order = np.argsort(centers[:, 0])
    boxes_o = boxes[order]
    centers_o = centers[order]
    areas_o = areas[order]
    
    merged = np.zeros(len(order), dtype=np.int8)
    new_boxes = []
    new_centers = []
    new_areas = []
    
    i = 0
    while i < len(order):
        if merged[i]:
            i += 1
            continue
            
        base_box = boxes_o[i]
        base_center = centers_o[i]
        base_area = areas_o[i]
        cluster_indices = [i]
        
        # janela de busca local em X
        j = i + 1
        max_dx = med_w * 1.2
        while j < len(order) and (centers_o[j][0] - base_center[0]) <= max_dx:
            # proximidade vertical e tamanho razoável
            dy = abs(centers_o[j][1] - base_center[1])
            if dy <= med_h * 1.2:
                # se um é ilha e o outro não, ou ambos muito próximos, agrega
                if is_island[order[j]] or is_island[order[i]]:
                    cluster_indices.append(j)
            j += 1
            
        # mesclar se houver ilhas próximas
        if len(cluster_indices) > 1:
            mb = base_box
            total_area = 0
            sum_cx = 0.0
            sum_cy = 0.0
            
            for k in cluster_indices:
                merged[k] = 1
                mb = merge_boxes(mb, boxes_o[k])
                total_area += int(areas_o[k])
                sum_cx += centers_o[k][0]
                sum_cy += centers_o[k][1]
                
            new_boxes.append(mb)
            new_centers.append((sum_cx/len(cluster_indices), sum_cy/len(cluster_indices)))
            new_areas.append(total_area)
        else:
            merged[i] = 1
            new_boxes.append(tuple(map(int, base_box)))
            new_centers.append((float(base_center[0]), float(base_center[1])))
            new_areas.append(int(base_area))
            
        i += 1
        
    return (
        np.array(new_boxes, dtype=np.int32),
        np.array(new_centers, dtype=np.float32),
        np.array(new_areas, dtype=np.int32),
    )
"""

    text_assemble_content = """import numpy as np
from typing import List, Dict, Tuple
from .utils import merge_boxes

def assemble_lines_and_words(boxes: np.ndarray, centers: np.ndarray):
    n = boxes.shape[0]
    if n == 0:
        return []  # sem linhas
        
    heights = boxes[:, 3] - boxes[:, 1]
    widths = boxes[:, 2] - boxes[:, 0]
    med_h = max(1, int(np.median(heights)))
    med_w = max(1, int(np.median(widths)))
    
    # agrupar por linha: ordenar por y centro e juntar por limiar
    idx = np.argsort(centers[:, 1])
    lines = []
    current = [idx[0]]
    
    for k in idx[1:]:
        if abs(centers[k, 1] - centers[current[-1], 1]) <= med_h * 0.6:
            current.append(k)
        else:
            lines.append(current)
            current = [k]
            
    if current:
        lines.append(current)
        
    # dentro de cada linha, ordenar por x e agrupar em palavras por gap
    all_lines = []
    gap_thr = max(2, int(med_w * 0.6))
    
    for ln in lines:
        xs = sorted(ln, key=lambda i: boxes[i, 0])
        words = []
        if not xs:
            all_lines.append([])
            continue

        wb = tuple(boxes[xs[0]])
        for i in range(1, len(xs)):
            prev = xs[i - 1]
            cur = xs[i]
            gap = boxes[cur, 0] - boxes[prev, 2]
            
            if gap > gap_thr:
                words.append({"bbox": wb, "text": ""})
                wb = tuple(boxes[cur])
            else:
                wb = merge_boxes(wb, tuple(boxes[cur]))

        words.append({"bbox": wb, "text": ""})
        all_lines.append(words)
        
    return all_lines

def map_text_to_words(lines: List[List[Dict]], mu_words: List[Tuple[int,int,int,int,str]]):
    if not mu_words:
        return lines

    # índice simples por x inicial para reduzir comparações
    mu_words_sorted = sorted(mu_words, key=lambda w: w[0])
    xs = [w[0] for w in mu_words_sorted]
    import bisect
    
    for words in lines:
        for w in words:
            x1, y1, x2, y2 = w["bbox"]
            
            # janela de candidatos por x
            left = bisect.bisect_left(xs, x1 - 10)
            right = bisect.bisect_right(xs, x2 + 10)
            
            best_iou = 0.0
            best_text = ""
            
            for j in range(left, min(right, len(mu_words_sorted))):
                bx1, by1, bx2, by2, txt = mu_words_sorted[j]
                
                # iou rápido
                ix1, iy1 = max(x1, bx1), max(y1, by1)
                ix2, iy2 = min(x2, bx2), min(y2, by2)
                iw, ih = max(0, ix2 - ix1), max(0, iy2 - iy1)
                inter = iw * ih
                
                if inter == 0:
                    continue
                    
                a_area = (x2 - x1) * (y2 - y1)
                b_area = (bx2 - bx1) * (by2 - by1)
                union = a_area + b_area - inter
                iou = inter / union if union > 0 else 0.0
                
                if iou > best_iou:
                    best_iou = iou
                    best_text = txt
                    
            if best_iou >= 0.35:  # tolerante a pequenas diferenças
                w["text"] = best_text
                
    return lines
"""

    table_detect_content = """import cv2
import numpy as np
from typing import List, Dict, Tuple
from .utils import inside

def detect_ruled_tables(bin_img: np.ndarray):
    h, w = bin_img.shape
    inv = 255 - bin_img
    
    # kernels proporcionais ao tamanho da página, baratos
    hk = max(10, w // 40)
    vk = max(10, h // 40)
    
    horiz_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (hk, 1))
    vert_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, vk))
    
    h_lines = cv2.morphologyEx(inv, cv2.MORPH_OPEN, horiz_kernel, iterations=1)
    v_lines = cv2.morphologyEx(inv, cv2.MORPH_OPEN, vert_kernel, iterations=1)
    
    # binariza linhas
    _, h_bin = cv2.threshold(h_lines, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    _, v_bin = cv2.threshold(v_lines, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    
    # contornos finos
    contours_h, _ = cv2.findContours(h_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_v, _ = cv2.findContours(v_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    xs = []
    ys = []
    
    for c in contours_h:
        x, y, ww, hh = cv2.boundingRect(c)
        if ww > max(30, w // 8) and hh < max(5, h // 200):
            ys.append(y + hh // 2)
            
    for c in contours_v:
        x, y, ww, hh = cv2.boundingRect(c)
        if hh > max(30, h // 8) and ww < max(5, w // 200):
            xs.append(x + ww // 2)
            
    xs = sorted(set(xs))
    ys = sorted(set(ys))
    
    if len(xs) < 2 or len(ys) < 2:
        return []

    # células a partir de interseções adjacentes
    tables = []
    x_edges = xs
    y_edges = ys
    
    # construir células entre bordas consecutivas
    cells = []
    for r in range(len(y_edges) - 1):
        row_cells = []
        y1, y2 = y_edges[r], y_edges[r + 1]
        if y2 - y1 < 8:  # linha muito estreita
            continue
            
        for c in range(len(x_edges) - 1):
            x1, x2 = x_edges[c], x_edges[c + 1]
            if x2 - x1 < 8:
                continue
            row_cells.append((x1, y1, x2, y2))
            
        if row_cells:
            cells.append(row_cells)
            
    if cells:
        tables.append({"bbox": (0, 0, w, h), "grid": cells})
        
    return tables

def detect_gridless_tables_from_words(lines: List[List[Dict]], page_bbox: Tuple[int, int]):
    # Agrupar colunas e linhas por histogramas simples dos centros dos words
    xs_centers = []
    ys_centers = []
    word_items = []
    
    for l in lines:
        for w in l:
            x1, y1, x2, y2 = w["bbox"]
            xs_centers.append((x1 + x2) // 2)
            ys_centers.append((y1 + y2) // 2)
            word_items.append(w)
            
    if not xs_centers:
        return []

    xs_centers = np.array(xs_centers)
    ys_centers = np.array(ys_centers)
    
    # estimativas
    widths = [w["bbox"][2] - w["bbox"][0] for w in word_items]
    heights = [w["bbox"][3] - w["bbox"][1] for w in word_items]
    med_w = max(8, int(np.median(widths)))
    med_h = max(8, int(np.median(heights)))
    
    # clusterização 1D barata por quantização
    def cluster_axis(vals, eps):
        vals_sorted = np.sort(vals)
        centers = []
        cur_grp = [vals_sorted[0]]
        
        for v in vals_sorted[1:]:
            if abs(v - cur_grp[-1]) <= eps:
                cur_grp.append(v)
            else:
                centers.append(int(np.mean(cur_grp)))
                cur_grp = [v]
                
        if cur_grp:
            centers.append(int(np.mean(cur_grp)))
            
        return centers

    col_centers = cluster_axis(xs_centers, eps=int(med_w * 1.0))
    row_centers = cluster_axis(ys_centers, eps=int(med_h * 0.9))
    
    if len(col_centers) < 2 or len(row_centers) < 2:
        return []

    # limites entre centros adjacentes
    def edges_from_centers(centers, max_val):
        centers = sorted(centers)
        edges = []
        
        # borda antes do primeiro
        first_gap = max(4, (centers[1] - centers[0]) // 2) if len(centers) > 1 else 10
        edges.append(max(0, centers[0] - first_gap))
        
        for i in range(len(centers) - 1):
            edges.append((centers[i] + centers[i + 1]) // 2)
            
        # borda após o último
        last_gap = max(4, (centers[-1] - centers[-2]) // 2) if len(centers) > 1 else 10
        edges.append(min(max_val, centers[-1] + last_gap))
        
        return edges

    W, H = page_bbox
    x_edges = edges_from_centers(col_centers, W)
    y_edges = edges_from_centers(row_centers, H)

    cells = []
    for r in range(len(y_edges) - 1):
        row_cells = []
        for c in range(len(x_edges) - 1):
            x1, x2 = x_edges[c], x_edges[c + 1]
            y1, y2 = y_edges[r], y_edges[r + 1]
            row_cells.append((x1, y1, x2, y2))
            
        if row_cells:
            cells.append(row_cells)
            
    return [{"bbox": (0, 0, W, H), "grid": cells}]
"""

    schema_content = """from typing import List, Dict, Tuple
from .utils import inside

def build_page_schema(page_index: int, size: Tuple[int, int], lines: List[List[Dict]], tables: List[Dict]):
    W, H = size
    
    # linhas: texto por linha
    line_items = []
    for words in lines:
        if not words:
            continue
            
        # bbox da linha é união das palavras
        x1 = min(w["bbox"][0] for w in words)
        y1 = min(w["bbox"][1] for w in words)
        x2 = max(w["bbox"][2] for w in words)
        y2 = max(w["bbox"][3] for w in words)
        text = " ".join([w["text"] for w in words if w["text"]])
        
        line_items.append({
            "bbox": {"x1": int(x1), "y1": int(y1), "x2": int(x2), "y2": int(y2)},
            "text": text,
            "words": [
                {"bbox": {"x1": int(w["bbox"][0]), "y1": int(w["bbox"][1]), "x2": int(w["bbox"][2]), "y2": int(w["bbox"][3])}, "text": w["text"]}
                for w in words
            ]
        })
        
    # Tabelas: preencher células com textos das palavras contidas
    table_items = []
    for t in tables:
        cells_out = []
        grid = t.get("grid", [])
        
        for row in grid:
            row_cells = []
            for cell in row:
                cx1, cy1, cx2, cy2 = cell
                
                # textos das palavras dentro
                texts = []
                for words in lines:
                    for w in words:
                        bx1, by1, bx2, by2 = w["bbox"]
                        
                        # Simplificação: verifica se o bbox da palavra está totalmente dentro do bbox da célula
                        if bx1 >= cx1 and by1 >= cy1 and bx2 <= cx2 and by2 <= cy2:
                            if w["text"]:
                                texts.append(w["text"])
                                
                row_cells.append({
                    "bbox": {"x1": int(cx1), "y1": int(cy1), "x2": int(cx2), "y2": int(cy2)},
                    "text": " ".join(texts).strip(),
                    "colspan": 1,
                    "rowspan": 1
                })
            cells_out.append({"cells": row_cells})
            
        table_items.append({
            "page": page_index + 1,
            "bbox": {"x1": 0, "y1": 0, "x2": int(W), "y2": int(H)},
            "rows": cells_out
        })
        
    return {
        "page": page_index + 1,
        "bbox": {"x1": 0, "y1": 0, "x2": int(W), "y2": int(H)},
        "lines": line_items,
        "tables": table_items
    }
"""

    pipeline_content = """import os
import gc
import cv2
import numpy as np
from typing import Dict

# limitar threads para baixo uso de CPU
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")

try:
    cv2.setNumThreads(1)
except Exception:
    pass

from .render import open_doc, page_count, render_page_gray, get_words_scaled
from .preprocess import binarize_gray
from .ccl import extract_components
from .pathfinder import refine_merge_islands
from .text_assemble import assemble_lines_and_words, map_text_to_words
from .table_detect import detect_ruled_tables, detect_gridless_tables_from_words
from .schema import build_page_schema

def process_pdf(path: str, dpi: int = 150, max_pages: int = 50) -> Dict:
    doc = open_doc(path)
    n = min(page_count(doc), max_pages)
    pages_out = []
    
    for i in range(n):
        # 1. Renderização e pré-processamento
        gray = render_page_gray(doc, i, dpi=dpi)
        bin_img = binarize_gray(gray)
        
        # 2. Extração de Componentes Conexos (CCL)
        boxes, centers, areas = extract_components(bin_img)
        
        # 3. Refino (união de ilhas/acentos)
        boxes, centers, areas = refine_merge_islands(boxes, centers, areas)
        
        # 4. Agrupamento de texto
        lines = assemble_lines_and_words(boxes, centers)
        
        # 5. Mapeamento de texto (da camada de texto do PDF)
        mu_words = get_words_scaled(doc, i, dpi=dpi)
        lines = map_text_to_words(lines, mu_words)
        
        # 6. Detecção de tabelas
        ruled = detect_ruled_tables(bin_img)
        if ruled:
            tables = ruled
        else:
            H, W = bin_img.shape
            tables = detect_gridless_tables_from_words(lines, (W, H))
            
        # 7. Construção do esquema de saída
        page_schema = build_page_schema(i, (bin_img.shape[1], bin_img.shape[0]), lines, tables)
        pages_out.append(page_schema)
        
        # liberar memória cedo (processamento por página)
        del gray, bin_img, boxes, centers, areas, lines, mu_words, ruled, tables
        gc.collect()
        
    return {"meta": {"dpi": dpi, "units": "px"}, "pages": pages_out}
"""

    export_content = """import pandas as pd
import io
from typing import Dict, Tuple

def extract_tables_to_dataframe(structured_data: Dict) -> pd.DataFrame:
    \"\"\"
    Converte os dados estruturados do PixelPath (JSON) em um DataFrame Pandas,
    focando apenas nas celulas de texto das tabelas detectadas.
    \"\"\"
    all_table_data = []

    for page in structured_data.get("pages", []):
        page_num = page.get("page", 0)
        
        for table in page.get("tables", []):
            table_rows = table.get("rows", [])
            
            # Extrai apenas o texto das células para uma lista de listas
            data = []
            for row in table_rows:
                cell_texts = [cell.get("text", "") for cell in row.get("cells", [])]
                data.append(cell_texts)

            if data:
                # Cria um DataFrame temporário para esta tabela
                df_temp = pd.DataFrame(data)
                
                # Adiciona coluna de metadados para saber a origem
                df_temp["_page"] = page_num
                df_temp["_table_index"] = len(all_table_data)
                
                all_table_data.append(df_temp)

    if not all_table_data:
        # Se não houver tabelas, retorna um DataFrame vazio com colunas padrão.
        return pd.DataFrame({"_status": ["Nenhuma tabela detectada."]})

        # Concatena todos os DataFrames de todas as tabelas e páginas
        final_df = pd.concat(all_table_data, ignore_index=True)
        return final_df.drop(columns=["_table_index"], errors='ignore')

    def export_to_format(df: pd.DataFrame, file_format: str) -> Tuple[io.BytesIO, str, str]:
        \"\"\"
        Converte o DataFrame para o formato de arquivo binario especificado (CSV ou XLSX).
        Retorna o buffer, o tipo de midia e o cabeçalho de download.
        \"\"\"
        buffer = io.BytesIO()
        
        if file_format == "csv":
            # Usamos o buffer como se fosse um arquivo
            df.to_csv(buffer, index=False, encoding="utf-8")
            media_type = "text/csv"
            filename = "extraction_data.csv"
            
        elif file_format == "xlsx":
            # Pandas usa openpyxl/xlsxwriter para criar o arquivo XLSX
            with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="Extracao_PDF")
            media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            filename = "extraction_data.xlsx"
            
        else:
            # Retorna o buffer vazio e um erro (nao deve acontecer com a validacao da API)
            raise ValueError(f"Formato de exportacao nao suportado: {file_format}")
    
        buffer.seek(0)
        return buffer, media_type, filename
    """

    # Conteúdo do arquivo main.py com o middleware CORS e Exportação
    main_content = """import os

# limitar threads via env antes de carregar libs pesadas
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")

from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response # Importação necessária para retornar o arquivo
from .schemas import ExtractOptions
from ..core.pipeline import process_pdf
from ..core.export import extract_tables_to_dataframe, export_to_format # Novo Import
import tempfile
import shutil
import uvicorn
import json # Necessário para dump de JSON

# --- Configuração CORS ---
CORS_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "*") 
ALLOWED_HOSTS = CORS_ORIGINS.split(",") if CORS_ORIGINS != "*" else ["*"]
if not ALLOWED_HOSTS and CORS_ORIGINS != "*":
    ALLOWED_HOSTS = []

app = FastAPI(title="PixelPath API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# -------------------------

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/extract")
def extract(
    file: UploadFile = File(...), 
    dpi: int = Query(150, ge=72, le=200), 
    max_pages: int = Query(50, ge=1, le=500),
    # Novo parâmetro de formato de saída, com JSON como padrão
    output_format: str = Query("json", description="Formato de saída: json, csv, ou xlsx") 
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Apenas arquivos PDF são suportados.")

    # Validação do formato
    if output_format not in ["json", "csv", "xlsx"]:
         raise HTTPException(400, "Formato de saída inválido. Use 'json', 'csv' ou 'xlsx'.")

    tmp_path = None
    try:
        # 1. Processamento do PDF (Cria o JSON estruturado)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name
            
        structured_data = process_pdf(tmp_path, dpi=int(dpi), max_pages=int(max_pages))

        # 2. Retorno do formato JSON padrão
        if output_format == "json":
            return structured_data

        # 3. Conversão e Retorno CSV/XLSX
        # A API precisa das libs pandas e openpyxl/xlsxwriter para funcionar em CSV/XLSX
        df = extract_tables_to_dataframe(structured_data)
        
        # Realiza a exportação e obtém o buffer binário
        buffer, media_type, filename = export_to_format(df, output_format)
        
        # Retorna o arquivo binário
        return Response(
            content=buffer.getvalue(),
            media_type=media_type,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except ValueError as ve:
         raise HTTPException(400, f"Erro de conversao: {ve}")
    except Exception as e:
        raise HTTPException(500, f"Erro no processamento: {e}")
        
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""
    
    # Mapeamento de caminhos e conteúdos (incluindo documentação e o main.py atualizado)
    file_map = {
        "requirements.txt": requirements_content,
        "README.md": readme_content,
        "GUIA_GITHUB.md": github_guide_content,
        "pixelpath/__init__.py": init_content,
        "pixelpath/api/main.py": main_content,
        "pixelpath/api/schemas.py": schemas_content,
        "pixelpath/core/export.py": export_content, # Novo arquivo
        "pixelpath/core/pipeline.py": pipeline_content,
        "pixelpath/core/render.py": render_content,
        "pixelpath/core/preprocess.py": preprocess_content,
        "pixelpath/core/ccl.py": ccl_content,
        "pixelpath/core/pathfinder.py": pathfinder_content,
        "pixelpath/core/text_assemble.py": text_assemble_content,
        "pixelpath/core/table_detect.py": table_detect_content,
        "pixelpath/core/schema.py": schema_content,
        "pixelpath/core/utils.py": utils_content,
    }

    print("Criando a estrutura do projeto PixelPath...")
    
    # Cria as pastas necessárias
    os.makedirs("pixelpath/api", exist_ok=True)
    os.makedirs("pixelpath/core", exist_ok=True)
    
    # Salva os arquivos
    for path, content in file_map.items():
        try:
            # Garante que as novas linhas sejam tratadas corretamente em diferentes sistemas operacionais
            # Ao ler o conteúdo de uma string, a reescrita com 'w' é suficiente.
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  [SUCESSO] Arquivo criado/atualizado: {path}")
        except Exception as e:
            print(f"  [ERRO] Falha ao criar {path}: {e}")

if __name__ == "__main__":
    create_project_structure()
    print("\nEstrutura do projeto PixelPath criada com sucesso!")

    print("\n--- Próximos Passos ---")
    print("1. Instale as dependências: pip install -r requirements.txt")
    print("2. Para iniciar localmente: python -m uvicorn pixelpath.api.main:app --host 0.0.0.0 --port 8000")