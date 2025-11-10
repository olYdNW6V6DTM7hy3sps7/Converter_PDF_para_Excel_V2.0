from typing import List, Dict, Tuple
from .utils import inside

def build_page_schema(page_index: int, size: Tuple[int, int], lines: List[List[Dict]], tables: List[Dict]):
    W, H = size
    
    # linhas: texto por linha
    line_items = []
    for words in lines:
        if not words:
            continue
            
        # bbox da linha é união das palavras
        word_bboxes = [w["bbox"] for w in words]
        x1 = min(b[0] for b in word_bboxes)
        y1 = min(b[1] for b in word_bboxes)
        x2 = max(b[2] for b in word_bboxes)
        y2 = max(b[3] for b in word_bboxes)
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
