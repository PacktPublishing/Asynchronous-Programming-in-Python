import time
import asyncio
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
async def test_print_docs():
    start_time = time.perf_counter()
    doc1 = concurrent_tasks.print_document("long", 3)
    doc2 = concurrent_tasks.print_document("short", 1)
    doc3 = concurrent_tasks.print_document("med", 2)
    await asyncio.gather(doc1, doc2, doc3)
    end_time = time.perf_counter()
    duration = end_time - start_time
    assert duration == pytest.approx(3.0, abs=0.1)

