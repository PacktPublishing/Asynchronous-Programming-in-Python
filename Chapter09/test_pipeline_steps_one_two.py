import pytest
import asyncio
from typing import List, Dict, Any

from pipeline_steps import stream_huggingface_etymology_data, group_records_by_term_id

@pytest.mark.asyncio
async def test_streaming_and_grouping_first_two_term_ids():
    data_stream = stream_huggingface_etymology_data("Nickmancol/mini_etymology")
    grouped_stream = group_records_by_term_id(data_stream)
    expected_term_ids = [
        "JFwk6_hjU8uJ5NHXEypjtQ", 
        "sMQjZAahXbqAUQv3cKiWzg" 
    ]
    received_groups = []
    group_count = 0
    async for term_id, records in grouped_stream:
        received_groups.append((term_id, records))
        group_count += 1
        if group_count >= len(expected_term_ids):
            break
    assert len(received_groups) == len(expected_term_ids)
    assert received_groups[0][0] == expected_term_ids[0]
    assert received_groups[1][0] == expected_term_ids[1]
    assert len(received_groups[0][1]) >= 6
    assert len(received_groups[1][1]) >= 1
