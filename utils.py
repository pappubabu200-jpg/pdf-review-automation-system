from fastapi import Header, HTTPException
from fastapi.security import APIKeyHeader
from src.config import settings
import logging
from pathlib import Path

logger = logging.getLogger("pdf_review")
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')

API_KEY = APIKeyHeader(name='x-secret', auto_error=False)

async def require_secret(x_secret: str = API_KEY):
    if x_secret != settings.X_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True

def safe_join(root: Path, *paths) -> Path:
    candidate = root.joinpath(*paths).resolve()
    if not str(candidate).startswith(str(root.resolve())):
        raise ValueError("Invalid path")
    return candidate
