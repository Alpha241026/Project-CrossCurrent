# CrossCurrent

A developer-focused API workspace for organizing, configuring, executing, and inspecting HTTP requests.

CrossCurrent provides a single workspace for managing Projects and reusable Endpoints, building HTTP requests, executing them through a backend-controlled execution boundary, inspecting responses, and reviewing persistent execution history.

The project is built as a learning-focused full-stack system with deliberate separation between application logic, request execution, persistence, and frontend presentation.

---

## Overview

CrossCurrent is built around a simple workflow:

```text
Project
   ↓
Endpoint
   ↓
Configure Request
   ↓
Execute
   ↓
Inspect Response
   ↓
Review History
```

A **Project** organizes related API work.

An **Endpoint** represents a reusable HTTP request definition containing:

- HTTP method
- URL
- Query parameters
- Headers
- Request body

An Endpoint stores request configuration but does not execute the request itself.

Each execution produces an immutable **Execution** record containing information such as:

- Status code
- Response time
- Execution timestamp
- Response headers
- Response body
- Error information

History is represented as a view over an Endpoint's stored Executions rather than as a separate domain entity.

---

## Features

### Project Management

- Create, view, update, and delete Projects
- Store optional Project descriptions
- Organize related Endpoints under each Project

### Endpoint Management

- Create reusable Endpoints
- View, update, and delete Endpoints
- Store optional Endpoint descriptions
- Associate Endpoints with their owning Project

### Request Builder

Configure requests directly inside the workspace:

- HTTP method
- URL
- Query parameters
- Custom headers
- Request body

Params and Headers use dynamic key-value editors.

Selecting an Endpoint reconstructs its saved request configuration inside the Request Builder.

### Request Execution

CrossCurrent sends execution instructions from the frontend to the backend rather than allowing the browser to contact external APIs directly.

Supported request methods:

- GET
- POST
- PATCH
- DELETE

The backend performs the outbound HTTP request and returns the resulting response to the frontend.

### Response Viewer

Inspect the result of an executed request, including:

- HTTP status
- Response body
- Response information

### Execution History

Each Endpoint can have multiple recorded Executions.

The History panel provides:

- Status code
- Response time
- Execution timestamp
- Saved response body

Selecting a historical execution displays its saved response again in the Response Viewer.

History can also be refreshed independently.

### Persistent Storage

PostgreSQL is the source of truth for persistent:

- Projects
- Endpoints
- Executions

Endpoint request configuration such as Params, Headers, and Body is stored using PostgreSQL `JSONB`.

Project → Endpoint ownership is enforced through database relationships, including cascading Endpoint deletion when a Project is deleted.

---

## Architecture

CrossCurrent uses a layered Python backend together with a dedicated Go subsystem for execution-history persistence and retrieval.

```text
                         ┌──────────────────────┐
                         │    CrossCurrent UI   │
                         │    HTML / CSS / JS   │
                         └──────────┬───────────┘
                                    │
                                  Fetch
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     Flask Backend    │
                         │                      │
                         │ Routes               │
                         │ Controllers          │
                         │ Services             │
                         │ Repositories         │
                         │ Models               │
                         └──────────┬───────────┘
                                    │
                    ┌───────────────┴────────────────┐
                    │                                │
                    ▼                                ▼
             Resource Management              Request Execution
                    │                                │
                    ▼                                ▼
               PostgreSQL                    External HTTP API
                    │
                    ▼
             Project / Endpoint
                Persistence

                    Execution Result
                           │
                           ▼
                    Go Execution Service
                           │
                           ▼
                    Execution Repository
                           │
                           ▼
                       PostgreSQL
```

### Backend Layering

The Python backend follows:

```text
Route
  ↓
Controller
  ↓
Service
  ↓
Repository
  ↓
Model / PostgreSQL
```

Each layer has a defined responsibility.

**Routes**

- Map HTTP methods and URLs
- Organize Flask Blueprints
- Connect incoming requests to controllers

**Controllers**

- Read incoming HTTP request data
- Extract JSON fields
- Coordinate Service calls
- Convert results into HTTP/JSON responses

**Services**

- Perform validation
- Apply business rules
- Check resource existence
- Construct domain objects
- Coordinate repository operations

**Repositories**

- Handle persistence operations
- Communicate with PostgreSQL
- Map database rows to domain models

This keeps storage and implementation details from leaking into higher application layers.

---

## Request Execution

The main execution path is:

```text
Frontend
   ↓
POST /execute
   ↓
Flask Route
   ↓
Execution Controller
   ↓
Execution Service
   ↓
External HTTP API
   ↓
Execution Result
   ├──────────────→ Frontend
   │                  ↓
   │             Response Viewer
   │
   └──────────────→ Go Execution Service
                      ↓
                Execution Repository
                      ↓
                  PostgreSQL
```

Python remains responsible for performing the outbound HTTP request.

Go owns the execution-history persistence and retrieval subsystem.

This gives Go a meaningful backend responsibility without rewriting the established Python application and execution layers.

A successful external API response remains available to the user even if secondary history persistence fails.

---

## Domain Model

```text
Project
   │
   │ owns
   ▼
Endpoint
   │
   │ can be executed many times
   ▼
Execution
```

### Project

A Project is a container for related API work.

### Endpoint

An Endpoint is a reusable API request definition belonging to a Project.

```text
Endpoint
├── id
├── project_id
├── name
├── method
├── url
├── params
├── headers
└── body
```

Params and Headers are configuration belonging to the Endpoint rather than independent top-level resources.

### Execution

An Execution represents one attempt to execute an Endpoint.

```text
Execution
├── id
├── endpoint_id
├── executed_at
├── status_code
├── response_time
├── response_headers
├── response_body
└── error_message
```

Executions are immutable records.

History is a view over these stored Executions.

---

## API

### Projects

```text
POST   /projects
GET    /projects
PATCH  /projects/{id}
DELETE /projects/{id}
```

### Endpoints

```text
POST   /projects/{project_id}/endpoints
GET    /projects/{project_id}/endpoints
GET    /endpoints/{endpoint_id}
PATCH  /endpoints/{endpoint_id}
DELETE /endpoints/{endpoint_id}
```

### Request Execution

```text
POST   /execute
```

The execution endpoint accepts request instructions from the frontend and performs the external HTTP request through the backend execution layer.

### Execution History

The Go execution-history service exposes:

```text
POST /executions
GET  /executions/endpoint/{endpoint_id}
```

The first stores a completed execution record.

The second retrieves execution history for an Endpoint, newest first.

---

## Frontend

The frontend intentionally uses no frontend framework.

```text
frontend/
├── index.html
├── css/
│   └── style.css
├── js/
│   └── main.js
└── assets/
```

The UI is organized as a three-panel workspace:

```text
┌────────────┬──────────────────────┬──────────────────────┐
│  Sidebar   │   Request Builder    │   Response Viewer    │
│            │                      │                      │
│ Projects   │ Method               │ Status               │
│   └─ Endpt │ URL                  │ Response             │
│            │ Params               │                      │
│            │ Headers              │                      │
│            │ Body                 │                      │
└────────────┴──────────────────────┴──────────────────────┘
```

### Sidebar

- Projects
- Nested Endpoints
- Project CRUD controls

Selecting an Endpoint loads its saved configuration into the Request Builder.

### Request Builder

- Method selection
- URL input
- Endpoint name
- Dynamic Params editor
- Dynamic Headers editor
- Request body

### Response Viewer

Displays results from the backend execution flow and saved historical responses.

---

## Persistence

PostgreSQL replaced the original in-memory repository implementation while preserving the existing application architecture.

```text
Frontend
   ↓
Route
   ↓
Controller
   ↓
Service
   ↓
Repository
   ↓
PostgreSQL
```

PostgreSQL owns:

- Project and Endpoint IDs
- Execution IDs
- Creation and update timestamps
- Project → Endpoint relationships
- Execution records
- Endpoint request configuration

Endpoint Params, Headers, and Body are stored as `JSONB`.

Database-generated IDs and timestamps are used instead of generating them inside application code.

Project deletion uses `ON DELETE CASCADE` to remove associated Endpoints.

---

## Go Subsystem

Go is used as a specialized backend subsystem rather than replacing the entire Python backend.

Its current responsibility is execution-history persistence and retrieval.

```text
Go
├── HTTP service
├── PostgreSQL connection
├── ExecutionRepository
├── Execution persistence
└── Execution history retrieval
```

The Go subsystem uses:

- `net/http`
- `database/sql`
- `encoding/json`
- `pgx`

The Python and Go responsibilities are deliberately separated:

```text
Python / Flask
├── Projects
├── Endpoints
├── Params / Headers
├── Application logic
├── CRUD
├── Request execution
└── Execution coordination

Go
├── Execution persistence
└── Execution history retrieval
```

---

## Technology Stack

| Layer | Technologies |
|---|---|
| Frontend | HTML, CSS, Vanilla JavaScript, Fetch API, DOM APIs |
| Backend | Python, Flask, `requests` |
| Go subsystem | Go, `net/http`, `database/sql`, `encoding/json`, `pgx` |
| Database | PostgreSQL, SQL, JSONB |
| Architecture | Layered architecture, Repository pattern |

---

## Project Structure

```text
CrossCurrent/
│
├── backend/
│   ├── python/
│   │   ├── config/
│   │   ├── controllers/
│   │   ├── services/
│   │   ├── repositories/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── database/
│   │   ├── utils/
│   │   ├── app.py
│   │   └── requirements.txt
│   │
│   └── go/
│       ├── repository/
│       ├── utils/
│       ├── json/
│       └── ...
│
├── frontend/
│   ├── css/
│   ├── js/
│   ├── assets/
│   └── index.html
│
├── docs/
│   ├── Architecture.md
│   ├── DecisionLog.md
│   ├── LearningLog.md
│   └── Resources.md
│
├── .gitignore
└── README.md
```

The project structure follows the same separation of concerns used by the application architecture.

---

## Development Approach

CrossCurrent was developed incrementally using **Foundation → Vertical Slice Development**.

Each major capability was taken through its relevant backend, persistence, frontend, and testing work before moving to the next slice.

```text
Foundation
   ↓
Projects
   ↓
Endpoints
   ↓
Request Execution
   ↓
Params + Headers
   ↓
PostgreSQL Persistence
   ↓
Execution History
   ↓
UI Polish
```

This approach kept the system functional throughout development and made architectural changes easier to isolate.

---

## Design Principles

### Separation of Concerns

Each backend layer has a defined responsibility.

### Backend as Source of Truth

The frontend refreshes its displayed state from backend data after successful operations.

### Domain Ownership

```text
Project
   ↓
Endpoint
   ↓
Execution
```

Projects own Endpoints, Endpoints contain request configuration, and Executions represent attempts to execute those Endpoints.

### Execution Separation

An Endpoint stores a request definition. It does not execute itself.

### Repository Abstraction

Persistence is isolated behind repositories so storage implementation can change without redesigning higher layers.

### Deliberate Scope

Features that add complexity without improving the current V1 learning objectives are postponed rather than prematurely integrated.

---

## Documentation

The project keeps its engineering documentation separate from the README.

| Document | Purpose |
|---|---|
| [`Architecture.md`](docs/Architecture.md) | System architecture and technical structure |
| [`DecisionLog.md`](docs/DecisionLog.md) | Important engineering decisions and their reasoning |
| [`LearningLog.md`](docs/LearningLog.md) | Concepts learned and problems encountered during development |
| [`Resources.md`](docs/Resources.md) | Documentation and references used during development |

The README describes the finished system.

The documentation preserves the reasoning and learning behind it.

---

## V1 Scope

CrossCurrent V1 focuses on the core API-workspace experience:

- Project management
- Endpoint management
- Request configuration
- Query parameters
- Custom headers
- Request bodies
- HTTP request execution
- Response inspection
- PostgreSQL persistence
- Execution records
- Execution history
- Historical response inspection

---

## Status

**Version 1 — Core system complete**

CrossCurrent provides a functional developer workspace spanning:

```text
Frontend
   ↓
Python / Flask
   ↓
PostgreSQL
   ↕
Go Execution History Service
```

The project is structured as both a usable V1 application and a practical exploration of layered backend architecture, persistence, HTTP execution, and multi-language backend integration.
