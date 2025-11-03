from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_review_continue_not_found():
    res = client.post('/review/continue', params={'job_id': 'nonexist'}, headers={'x-secret': 'wrong'})
    assert res.status_code in (401, 404)
