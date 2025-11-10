# Refinos leves para unir "ilhas" (pontos/acentos) a glifos próximos, sem tocar pixels
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
