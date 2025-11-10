import cv2
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
