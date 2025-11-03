from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from src.services import file_service
from src.api.utils import require_secret
from src.config import settings
import os
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post('/upload')
async def upload(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail='Only PDF files are accepted')

    contents = await file.read(16)
    await file.seek(0)
    if not contents.startswith(b'%PDF'):
        raise HTTPException(status_code=400, detail='Invalid PDF file')

    await file.seek(0, os.SEEK_END)
    size = await file.tell()
    await file.seek(0)
    max_bytes = settings.MAX_UPLOAD_MB * 1024 * 1024
    if size > max_bytes:
        raise HTTPException(status_code=413, detail='File too large')

    job_id = file_service.create_job_id()
    saved = await file_service.save_upload_file(job_id, 'input.pdf', file.file)

    status = {"job_id": job_id, "status": "uploaded", "artifacts": [{"name": "input.pdf", "url": f"{settings.BASE_URL}/files/{job_id}/input.pdf"}], "created_at": __import__('datetime').datetime.utcnow().isoformat(), "updated_at": None}
    file_service.save_status(job_id, status)

    try:
        file_service.register_artifact(job_id, 'input.pdf')
    except Exception:
        logger.exception('Failed to register artifact')

    return JSONResponse({"job_id": job_id, "status": "uploaded"}, status_code=201)

@router.post('/review/continue')
async def review_continue(job_id: str, authorized: bool = Depends(require_secret)):
    st = file_service.load_status(job_id)
    if not st:
        raise HTTPException(status_code=404, detail='Job not found')
    st['status'] = 'processing'
    st['attempts'] = st.get('attempts', 0) + 1
    st['updated_at'] = __import__('datetime').datetime.utcnow().isoformat()
    file_service.save_status(job_id, st)

    try:
        from src.services.n8n_service import trigger_analyze
        trigger_analyze(job_id, {"rerun": True})
    except Exception:
        logger.exception("Failed to call n8n")


    return {"job_id": job_id, "status": "processing"}
