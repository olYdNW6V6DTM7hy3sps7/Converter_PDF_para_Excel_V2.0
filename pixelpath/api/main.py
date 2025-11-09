import os

# limitar threads via env antes de carregar libs pesadas
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")

from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from .schemas import ExtractOptions
from ..core.pipeline import process_pdf
import tempfile
import shutil
import uvicorn

app = FastAPI(title="PixelPath API", version="0.1.0")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/extract")
def extract(
    file: UploadFile = File(...), 
    dpi: int = Query(150, ge=72, le=200), 
    max_pages: int = Query(50, ge=1, le=500)
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Apenas arquivos PDF são suportados.")

    tmp_path = None
    try:
        # Salva o arquivo em um tempfile para ser lido pelo pymupdf
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name
            
        result = process_pdf(tmp_path, dpi=int(dpi), max_pages=int(max_pages))
        return result
        
    except Exception as e:
        # Em produção, você pode querer logar o erro completo
        raise HTTPException(500, f"Erro no processamento: {e}")
        
    finally:
        # Garante que o arquivo temporário seja deletado
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass

if __name__ == "__main__":
    # Comando de execução local sugerido: 
    # uvicorn pixelpath.api.main:app --host 0.0.0.0 --port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
