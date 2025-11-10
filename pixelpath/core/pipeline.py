import os
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
        if gray.size == 0:
            print(f"Aviso: Página {i} resultou em imagem vazia.")
            continue
        
        bin_img = binarize_gray(gray)
        
        # 2. Extração de Componentes Conexos (CCL)
        boxes, centers, areas = extract_components(bin_img)
        
        # 3. Refino (união de ilhas/acentos)
        if boxes.shape[0] > 0:
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
