from typing import Tuple

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
