from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Artifact(BaseModel):
    name: str
    url: str

class JobStatus(BaseModel):
    job_id: str
    status: str = Field("queued", description="queued | processing | completed | failed")
    artifacts: List[Artifact] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime]
    attempts: int = 0
    message: Optional[str]
