import os
import tempfile
from unittest.mock import AsyncMock

import pytest
from fastapi import UploadFile
from httpx import ASGITransport, AsyncClient
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import DatabaseSessionManager
from app.main import app


@pytest.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture
def fake_db_session():
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def db_manager():
    url = URL.create(
        drivername="sqlite+aiosqlite",
        database=":memory:",
    )
    return DatabaseSessionManager(url)


@pytest.fixture
def upload_file():
    created_files = []

    def _create(content=b"Hello", filename="testfile.txt"):
        tmp_file = tempfile.NamedTemporaryFile(delete=False)
        tmp_file.write(content)
        tmp_file.seek(0)

        created_files.append(tmp_file.name)

        return UploadFile(filename=filename, file=open(tmp_file.name, "rb"))

    yield _create

    # Cleanup created files after test
    for path in created_files:
        try:
            os.remove(path)
        except FileNotFoundError:
            pass
