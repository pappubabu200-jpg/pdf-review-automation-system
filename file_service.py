import os
import json
from pathlib import Path
import aiofiles
from uuid import uuid4
from src.config import settings

FILES_ROOT = Path(settings.FILES_PATH)

PDF_SIGNATURE = b"%PDF-"

async def save_upload_file(job_id: str, filename: str, file_stream) -> Path:
    job_dir = FILES_ROOT / job_id
    job_dir.mkdir(parents=True, exist_ok=True)
    dest = job_dir / filename
    async with aiofiles.open(dest, 'wb') as out:
        while True:
            chunk = await file_stream.read(1024*64)
            if not chunk:
                break
            await out.write(chunk)
    return dest

async def validate_pdf_stream(stream) -> bool:
    head = await stream.read(8)
    await stream.seek(0)
    return head.startswith(PDF_SIGNATURE)

def create_job_id() -> str:
    return uuid4().hex

def job_dir(job_id: str) -> Path:
    return FILES_ROOT / job_id

def status_path(job_id: str) -> Path:
    return job_dir(job_id) / 'status.json'

def load_status(job_id: str):
    p = status_path(job_id)
    if not p.exists():
        return None
    with open(p, 'r') as f:
        return json.load(f)

def save_status(job_id: str, status: dict):
    p = status_path(job_id)
    with open(p, 'w') as f:
        json.dump(status, f, default=str, indent=2)

def register_artifact(job_id: str, filename: str):
    st = load_status(job_id) or {"job_id": job_id, "status": "queued", "artifacts": [], "created_at": None, "updated_at": None}
    artifact_url = f"{settings.BASE_URL}/files/{job_id}/{filename}"
    st.setdefault('artifacts', []).append({"name": filename, "url": artifact_url})
    st['updated_at'] = __import__('datetime').datetime.utcnow().isoformat()
    save_status(job_id, st)
