from pydantic import BaseModel, Field

class ExtractOptions(BaseModel):
    dpi: int = Field(default=150, ge=72, le=200)
    max_pages: int = Field(default=50, ge=1, le=500)
