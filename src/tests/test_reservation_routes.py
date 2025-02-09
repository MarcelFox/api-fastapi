import pytest


@pytest.mark.asyncio
async def test_post_reservation(client, random_hash, headers):
    reservation_body = {
        "user_name": "John Doe",
        "start_time": "2025-01-22T12:00:00",
        "end_time": "2025-01-22T13:00:00",
        "room_id": 1,
    }
    await client.post(
        "/rooms/", json={"name": "Sala 1", "capacity": 0, "location": "Andar 1"}
    )
    result = await client.post("/reservations/", json=reservation_body, headers=headers)
    assert result.status_code == 200

    reservation_exists = await client.post(
        "/reservations/", json=reservation_body, headers=headers
    )
    assert reservation_exists.status_code == 409
    assert reservation_exists.json()["detail"] == "Reservation already exists"

    wrong_time = await client.post(
        "/reservations/",
        json={
            **reservation_body,
            "start_time": reservation_body["end_time"],
            "end_time": reservation_body["start_time"],
        },
        headers=headers,
    )
    assert wrong_time.status_code == 406
    assert wrong_time.json()["detail"] == "Wrong time"

    unregistered_user = await client.post(
        "/reservations/",
        json={**reservation_body, "user_name": "John Carpenter"},
        headers=headers,
    )
    assert unregistered_user.status_code == 400
    assert unregistered_user.json()["detail"] == "Reservation user not registered"

    room_not_found = await client.post(
        "/reservations/", json={**reservation_body, "room_id": 10}, headers=headers
    )
    room_not_found.status_code == 404

    unauthorized = await client.post(
        "/reservations/", json={**reservation_body, "room_id": 10}
    )
    assert unauthorized.status_code == 401
    assert unauthorized.json()["detail"] == "Not authenticated"


@pytest.mark.asyncio
async def test_get_reservation(client, random_hash, headers):
    result = await client.get("/reservations/", headers=headers)
    assert result.status_code == 200


@pytest.mark.asyncio
async def test_delete_reservation(client, random_hash, headers):
    result = await client.delete("/reservations/1", headers=headers)
    assert result.status_code == 204
    unauthorized = await client.delete(
        "/reservations/1",
    )
    assert unauthorized.status_code == 401
    assert unauthorized.json()["detail"] == "Not authenticated"
