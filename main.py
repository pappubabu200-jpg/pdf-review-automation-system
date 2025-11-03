from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from src.api import review_router, analyze_router
from src.config import settings
from pathlib import Path
from src.api.utils import safe_join
import uvicorn

app = FastAPI(title='PDF Review System')

app.include_router(review_router, prefix='')
app.include_router(analyze_router, prefix='')

FILES_ROOT = Path(settings.FILES_PATH).resolve()

@app.get('/files/{job_id}/{filename}')
async def serve_file(job_id: str, filename: str):
    try:
        p = safe_join(FILES_ROOT, job_id, filename)
    except ValueError:
        raise HTTPException(status_code=400, detail='Invalid path')
    if not p.exists():
        raise HTTPException(status_code=404, detail='Not found')
    return FileResponse(path=p, filename=filename)

if __name__ == '__main__':
    uvicorn.run('src.main:app', host='0.0.0.0', port=8000, reload=True)
