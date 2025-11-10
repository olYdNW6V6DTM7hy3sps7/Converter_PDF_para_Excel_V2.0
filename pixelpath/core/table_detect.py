import cv2
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
    if len(xs_centers) == 0:
        return [] # Evita erro se não houver palavras
        
    widths = [w["bbox"][2] - w["bbox"][0] for w in word_items if w["bbox"][2] > w["bbox"][0]]
    heights = [w["bbox"][3] - w["bbox"][1] for w in word_items if w["bbox"][3] > w["bbox"][1]]
    
    med_w = max(8, int(np.median(widths))) if widths else 8
    med_h = max(8, int(np.median(heights))) if heights else 8
    
    # clusterização 1D barata por quantização
    def cluster_axis(vals, eps):
        if len(vals) == 0:
            return []
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
        if len(centers) == 0:
            return []
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
