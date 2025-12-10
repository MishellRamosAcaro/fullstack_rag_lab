from typing import List

from pydantic import BaseModel, Field



class UploadResponse(BaseModel):
    uploaded: List[str] = Field(default_factory=list, description="Nombres de archivos aceptados")
    rejected: List[str] = Field(default_factory=list, description="Nombres de archivos rechazados")
    total_files: int = Field(..., description="Total de archivos almacenados")


class ProcessResponse(BaseModel):
    status: str = Field(..., description="Estado de la operación de procesado")
    chunks: int = Field(..., description="Número de chunks generados")


class RagQueryRequest(BaseModel):
    question: str = Field(..., description="Pregunta del operador")


class DocumentChunk(BaseModel):
    text: str
    source: str
    page: int | str


class RagQueryResponse(BaseModel):
    answer: str
    chunks: List[DocumentChunk]


class ResetResponse(BaseModel):
    status: str = Field(..., description="Estado del reseteo")
    files_cleared: int = Field(..., description="Cantidad de archivos eliminados")
    chunks_cleared: int = Field(..., description="Cantidad de chunks eliminados")
