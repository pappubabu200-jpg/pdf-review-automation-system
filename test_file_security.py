import pytest
from pathlib import Path
from src.api.utils import safe_join
from src.config import settings

def test_safe_join_inside():
    root = Path(settings.FILES_PATH).resolve()
    p = safe_join(root, 'job123', 'input.pdf')
    assert str(p).startswith(str(root))
