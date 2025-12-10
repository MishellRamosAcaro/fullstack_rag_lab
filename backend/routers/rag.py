from functools import lru_cache
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from config import get_settings
from schemas import (
    ProcessResponse,
    RagQueryRequest,
    RagQueryResponse,
    ResetResponse,
    UploadResponse,
)
from services.rag_service import RAGService

router = APIRouter(prefix="/rag", tags=["rag"])


@lru_cache()
def get_rag_service() -> RAGService:
    settings = get_settings()
    return RAGService(settings)


@router.post("/upload", response_model=UploadResponse)
async def upload_files(
    files: List[UploadFile] = File(...),
    service: RAGService = Depends(get_rag_service),
) -> UploadResponse:
    accepted, rejected, total = await service.store_files(files)
    return UploadResponse(uploaded=accepted, rejected=rejected, total_files=total)


@router.post("/process", response_model=ProcessResponse)
def process_documents(service: RAGService = Depends(get_rag_service)) -> ProcessResponse:
    chunks = service.process_documents()
    return ProcessResponse(status="processed", chunks=chunks)


@router.post("/query", response_model=RagQueryResponse)
def query_rag(request: RagQueryRequest, service: RAGService = Depends(get_rag_service)) -> RagQueryResponse:
    try:
        answer, chunks = service.query(request.question)
        return RagQueryResponse(answer=answer, chunks=chunks)
    except HTTPException:
        raise
    except Exception as exc:  # pragma: no cover - defensive against unexpected errors
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.delete("/reset", response_model=ResetResponse)
def reset_documents(service: RAGService = Depends(get_rag_service)) -> ResetResponse:
    files_cleared, chunks_cleared = service.reset()
    return ResetResponse(status="reset", files_cleared=files_cleared, chunks_cleared=chunks_cleared)
