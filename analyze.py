from fastapi import APIRouter, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from src.services import file_service, telegram_service
from src.config import settings
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

async def finalize_job(job_id: str, payload: dict):
    job_dir = file_service.job_dir(job_id)
    overlay_path = job_dir / 'overlay.pdf'
    excel_path = job_dir / 'output.xlsx'
    overlay_path.write_bytes(b'%PDF-1.4\n%placeholder overlay')
    excel_path.write_bytes(b'PK\x03\x04\n')
    file_service.register_artifact(job_id, 'overlay.pdf')
    file_service.register_artifact(job_id, 'output.xlsx')
    st = file_service.load_status(job_id) or {"job_id": job_id}
    st['status'] = 'completed'
    st['updated_at'] = __import__('datetime').datetime.utcnow().isoformat()
    file_service.save_status(job_id, st)
    return True

@router.post('/analyze')
async def analyze(request: Request, background_tasks: BackgroundTasks):
    payload = await request.json()
    job_id = payload.get('job_id')
    if not job_id:
        return JSONResponse({'ok': False, 'reason': 'job_id missing'}, status_code=400)
    background_tasks.add_task(finalize_job, job_id, payload)
    return JSONResponse({'ok': True}, status_code=200)
