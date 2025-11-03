import requests
from src.config import settings
import logging

logger = logging.getLogger(__name__)

def trigger_analyze(job_id: str, callback_payload: dict):
    url = settings.N8N_WEBHOOK_URL
    payload = {"job_id": job_id, **(callback_payload or {})}
    try:
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        logger.exception("n8n webhook call failed: %s", e)
        raise
