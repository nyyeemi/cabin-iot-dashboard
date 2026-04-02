# cabin-iot

Personal home automation system intended for cabin usage.

## Planned Architecture

```mermaid
flowchart LR
    B[ESP32 sensors] -->|HTTP POST| D
    C[future devices] -->|HTTP POST| D

    subgraph rpi [Raspberry Pi]
        D[Hub API]
        E[(SQLite buffer)]
        D <-->|offline| E
    end

    D -->|online| F[FastAPI Backend]
    F --> G[(PostgreSQL)]
    F --> H[Next.js dashboard]
```

## Stack

- **Backend** — FastAPI, SQLModel, PostgreSQL 
- **Frontend** — Next.js
- **Hub** — FastAPI on Raspberry Pi (planned), SQLite buffer for offline resilience
- **Device** — Arduino MKR WiFi 1010 + ENV shield, ESP32 (planned)

## Status
-  In progress
