import pytest


@pytest.mark.asyncio
async def test_get_rooms(client):
    response = await client.get("/rooms/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_post_rooms(client, random_hash, headers):
    name = random_hash
    new_room = await client.post(
        "/rooms/",
        json={"name": name, "capacity": 0, "location": "Andar 1"},
        headers=headers,
    )
    assert new_room.status_code == 202
    existent_room = await client.post(
        "/rooms/",
        json={"name": name, "capacity": 0, "location": "Andar 1"},
        headers=headers,
    )
    assert existent_room.status_code == 201


@pytest.mark.asyncio
async def test_get_rooms_availability(client):
    good_for_reservation = await client.get(
        "/rooms/1/availability?start_time=2025-01-22T01:00:00&end_time=2025-01-22T02:00:00"
    )
    assert good_for_reservation.status_code == 200
    assert good_for_reservation.json()["message"] == "room available"

    wrong_time = await client.get(
        "/rooms/1/availability?start_time=2025-01-22T18:00:00&end_time=2025-01-22T16:00:00"
    )
    assert wrong_time.status_code == 406
    assert wrong_time.json()["detail"] == "Wrong time"


@pytest.mark.asyncio
async def test_get_room_reservations(client):
    no_reservation = await client.get("/rooms/999/reservation")
    assert no_reservation.status_code == 404
    assert no_reservation.json()["detail"] == "Reservations not found"
