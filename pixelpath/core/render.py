import fitz
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
