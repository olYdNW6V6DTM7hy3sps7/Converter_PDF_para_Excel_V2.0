import cv2
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
