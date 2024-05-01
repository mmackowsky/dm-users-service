# DeviceMinder - Users Service

## Description
A service handling user creation, login, display, modification, and deletion from a PostgreSQL database. Upon registration, the application hashes the provided password, and during login attempts, it verifies it. Successful login ensures user authorization and access to the remaining services of the application.

## Technologies
- FastAPI
- Docker
- PostgreSQL
- Poetry
