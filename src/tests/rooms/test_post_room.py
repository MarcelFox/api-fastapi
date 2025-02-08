"""Test rooms post module."""

import pytest

@pytest.mark.asyncio
async def test_post_rooms(client, random_hash):
    """test post method on '/rooms' route.

    Args:
        client (FastAPI): Api client fixture.
        random_hash: Random hash string fixture.
    """
    name = random_hash
    new_room = await client.post("/rooms/", json={
        "name": name,
        "capacity": 0,
        "location": "Andar 1"
    })
    assert new_room.status_code == 202
    existent_room = await client.post("/rooms/", json={
        "name": name,
        "capacity": 0,
        "location": "Andar 1"
    })
    assert existent_room.status_code == 201