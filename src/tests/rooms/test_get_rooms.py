import pytest

@pytest.mark.asyncio
async def test_get_rooms(client):
    response = await client.get("/rooms/")
    assert response.status_code == 200