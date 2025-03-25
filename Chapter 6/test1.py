import pytest
import pytest_asyncio
import concurrent_tasks

@pytest_asyncio.fixture
async def nobel_name():
    return "Gabriel García Márquez"

@pytest_asyncio.fixture
async def three_odds():
    return [False, True, False]

@pytest.mark.asyncio
async def test_get_nobel_name(nobel_name):
    result = await concurrent_tasks.get_nobel_name(659)
    assert result == nobel_name

@pytest.mark.asyncio
async def test_get_odds(three_odds):
    result = await concurrent_tasks.get_odds(3)
    assert result == three_odds
