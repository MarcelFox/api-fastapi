import pytest

@pytest.mark.asyncio
async def test_get_rooms(client):
    good_for_reservation = await client.get("/rooms/1/availability?start_time=2025-01-22T14:00:00&end_time=2025-01-22T16:00:00")
    assert good_for_reservation.status_code == 200
    assert good_for_reservation.json()['message'] == "room available"

    wrong_time = await client.get("/rooms/1/availability?start_time=2025-01-22T18:00:00&end_time=2025-01-22T16:00:00")
    assert wrong_time.status_code == 406
    assert wrong_time.json()['detail'] == "Wrong time"