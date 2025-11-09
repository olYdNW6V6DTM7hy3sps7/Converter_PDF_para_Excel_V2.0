import pandas as pd
import io
from typing import Dict, Tuple

def extract_tables_to_dataframe(structured_data: Dict) -> pd.DataFrame:
    """
    Converte os dados estruturados do PixelPath (JSON) em um DataFrame Pandas,
    focando apenas nas celulas de texto das tabelas detectadas.
    """
    all_table_data = []

    for page in structured_data.get("pages", []):
        page_num = page.get("page", 0)
        
        for table in page.get("tables", []):
            table_rows = table.get("rows", [])
            
            # Extrai apenas o texto das células para uma lista de listas
            data = []
            for row in table_rows:
                cell_texts = [cell.get("text", "") for cell in row.get("cells", [])]
                data.append(cell_texts)

            if data:
                # Cria um DataFrame temporário para esta tabela
                df_temp = pd.DataFrame(data)
                
                # Adiciona coluna de metadados para saber a origem
                df_temp["_page"] = page_num
                df_temp["_table_index"] = len(all_table_data)
                
                all_table_data.append(df_temp)

    if not all_table_data:
        # Se não houver tabelas, retorna um DataFrame vazio com colunas padrão.
        return pd.DataFrame({"_status": ["Nenhuma tabela detectada."]})

    # Concatena todos os DataFrames de todas as tabelas e páginas
    final_df = pd.concat(all_table_data, ignore_index=True)
    return final_df.drop(columns=["_table_index"], errors='ignore')

    export_to_format(df: pd.DataFrame, file_format: str) -> Tuple[io.BytesIO, str, str]:
    """
    Converte o DataFrame para o formato de arquivo binario especificado (CSV ou XLSX).
    Retorna o buffer, o tipo de midia e o cabeçalho de download.
    """
    buffer = io.BytesIO()
    
    if file_format == "csv":
        # Usamos o buffer como se fosse um arquivo
        df.to_csv(buffer, index=False, encoding="utf-8")
        media_type = "text/csv"
        filename = "extraction_data.csv"
        
    elif file_format == "xlsx":
        # Pandas usa openpyxl/xlsxwriter para criar o arquivo XLSX
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Extracao_PDF")
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        filename = "extraction_data.xlsx"
        
    else:
        # Retorna o buffer vazio e um erro (nao deve acontecer com a validacao da API)
        raise ValueError(f"Formato de exportacao nao suportado: {file_format}")

    buffer.seek(0)
    return buffer, media_type, filename
