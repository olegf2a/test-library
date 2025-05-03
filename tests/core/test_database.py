from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, AsyncSession


@pytest.mark.asyncio
async def test_session_success(db_manager):
    session_mock = AsyncMock(spec=AsyncSession)
    db_manager._sessionmaker = MagicMock(return_value=session_mock)

    async with db_manager.session() as session:
        assert session is session_mock

    session_mock.close.assert_awaited_once()


@pytest.mark.asyncio
async def test_session_uninitialized(db_manager):
    db_manager._sessionmaker = None

    with pytest.raises(Exception) as exc_info:
        async with db_manager.session():
            pass

    assert "not initialized" in str(exc_info.value)


@pytest.mark.asyncio
async def test_connect_success(db_manager):
    conn_mock = AsyncMock(spec=AsyncConnection)

    engine_mock = AsyncMock(spec=AsyncEngine)
    engine_mock.begin.return_value.__aenter__.return_value = conn_mock
    db_manager._engine = engine_mock

    async with db_manager.connect() as conn:
        assert conn is conn_mock

    engine_mock.begin.assert_called_once()
    conn_mock.rollback.assert_not_called()


@pytest.mark.asyncio
async def test_connect_uninitialized(db_manager):
    db_manager._engine = None

    with pytest.raises(Exception) as exc_info:
        async with db_manager.connect():
            pass

    assert "not initialized" in str(exc_info.value)


@pytest.mark.asyncio
async def test_close(db_manager):
    engine_mock = AsyncMock(spec=AsyncEngine)
    db_manager._engine = engine_mock
    db_manager._sessionmaker = MagicMock()

    await db_manager.close()

    engine_mock.dispose.assert_awaited_once()
    assert db_manager._engine is None
    assert db_manager._sessionmaker is None
