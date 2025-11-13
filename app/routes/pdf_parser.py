from fastapi import APIRouter
from app.services.pdf_pipeline import process_all_pdfs

router = APIRouter()

@router.post("/pdf-parser")
def pdf_parse():
    """
    Trigger the PDF parsing + DB storing pipeline.
    """
    result = process_all_pdfs()
    return result