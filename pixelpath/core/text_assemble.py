import numpy as np
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
