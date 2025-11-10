import os

# limitar threads via env antes de carregar libs pesadas
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")

from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response # Importação necessária para retornar o arquivo
from .schemas import ExtractOptions
from ..core.pipeline import process_pdf
from ..core.export import extract_tables_to_dataframe, export_to_format # Novo Import
import tempfile
import shutil
import uvicorn
import json # Necessário para dump de JSON

# --- Configuração CORS ---
CORS_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "*") 
ALLOWED_HOSTS = CORS_ORIGINS.split(",") if CORS_ORIGINS != "*" else ["*"]
if not ALLOWED_HOSTS and CORS_ORIGINS != "*":
    ALLOWED_HOSTS = []

app = FastAPI(title="PixelPath API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# -------------------------

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/extract")
def extract(
    file: UploadFile = File(...), 
    dpi: int = Query(150, ge=72, le=200), 
    max_pages: int = Query(50, ge=1, le=500),
    # Novo parâmetro de formato de saída, com JSON como padrão
    output_format: str = Query("json", description="Formato de saída: json, csv, ou xlsx") 
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Apenas arquivos PDF são suportados.")

    # Validação do formato
    if output_format not in ["json", "csv", "xlsx"]:
         raise HTTPException(400, "Formato de saída inválido. Use 'json', 'csv' ou 'xlsx'.")

    tmp_path = None
    try:
        # 1. Processamento do PDF (Cria o JSON estruturado)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name
            
        structured_data = process_pdf(tmp_path, dpi=int(dpi), max_pages=int(max_pages))

        # 2. Retorno do formato JSON padrão
        if output_format == "json":
            return structured_data

        # 3. Conversão e Retorno CSV/XLSX
        # A API precisa das libs pandas e openpyxl/xlsxwriter para funcionar em CSV/XLSX
        df = extract_tables_to_dataframe(structured_data)
        
        # Realiza a exportação e obtém o buffer binário
        buffer, media_type, filename = export_to_format(df, output_format)
        
        # Retorna o arquivo binário
        return Response(
            content=buffer.getvalue(),
            media_type=media_type,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except ValueError as ve:
         raise HTTPException(400, f"Erro de conversao: {ve}")
    except Exception as e:
        # Em produção, logar o erro é ideal
        print(f"Erro inesperado no processamento: {e}", file=sys.stderr)
        raise HTTPException(500, f"Erro no processamento: {e}")
        
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
