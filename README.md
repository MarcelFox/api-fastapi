# Reservation API

## Overview
The **Reservation API** is a RESTful service for managing room reservations. It allows users to create, retrieve, and delete reservations, register rooms, and check availability. Authentication is required for certain endpoints.

## API Information
- **Title:** Reservation API
- **Version:** 0.0.1
- **Description:** Room booking API.
- **Author:** [Marcel Fox](https://marcelfox.com/)
- **License:** [MIT](https://mit-license.org/)

## Local Development
**For information regarding how to run the application locally, visit the [development section](./docs/DEVELOPMENT.md)**

## Authentication
The API uses **OAuth2 Password Bearer Token** authentication for protected endpoints. Users must obtain a token via the `/token/` endpoint.

## Endpoints

### Health Check
- **GET /**
- **Description:** Check API health status.
- **Response:** `{ "message": "ok" }`

### Authentication
- **POST /token/**
- **Description:** Authenticate user and obtain an access token.
- **Request:** `application/x-www-form-urlencoded` (username & password required)
- **Response:** Access token

### Reservations
- **POST /reservations/**
  - **Description:** Create a new reservation.
  - **Authentication:** Required
  - **Request Body:** `{ "user_name": "John Doe", "start_time": "2025-01-22T14:00:00", "end_time": "2025-01-22T16:00:00", "room_id": 1 }`
  - **Response:** Reservation details

- **GET /reservations/**
  - **Description:** Retrieve a list of reservations.
  - **Query Parameters:** `skip` (default: 0), `limit` (default: 10)
  - **Response:** List of reservations

- **DELETE /reservations/{id}**
  - **Description:** Remove a reservation by ID.
  - **Authentication:** Required

### Rooms
- **GET /rooms/**
  - **Description:** Retrieve a list of registered rooms.
  - **Query Parameters:** `skip` (default: 0), `limit` (default: 10)
  - **Response:** List of rooms

- **POST /rooms/**
  - **Description:** Register a new room.
  - **Authentication:** Required
  - **Request Body:** `{ "name": "Conference Room", "capacity": 10, "location": "Floor 1" }`
  - **Response:** Room details

- **GET /rooms/{id}/availability**
  - **Description:** Check room availability for a specific time range.
  - **Query Parameters:** `start_time`, `end_time`
  - **Response:** Availability status

- **GET /rooms/{id}/reservation**
  - **Description:** List reservations for a specific room.
  - **Query Parameters:** `date` (optional), `skip` (default: 0), `limit` (default: 10)
  - **Response:** List of reservations for the room

## Error Handling
The API returns **422 Validation Error** for invalid requests. Errors include:
- Missing required fields
- Invalid data formats
- Unauthorized access

## License
This project is licensed under the [MIT License](https://mit-license.org/).

