# Architecture


# ------------------------------ DAY 1 ------------------------------


## First Overall Layout Draft (d1.0) - a fixed three panel workspace


+---------------------------------------------------------------+
|                        Pulse                                  |
+---------------------------------------------------------------+

| Sidebar | Request Builder                 | Response Viewer   |
|         |                                 |                   |
|---------|---------------------------------|-------------------|
|         | GET | URL | Send                | Status            |
|         |---------------------------------|-------------------|
|Projects | Params                          | JSON              |
|         | Headers                         |                   |
|         | Auth                            |                   |
|Endpoints| Body                            |                   |
|         |                                 |                   |
|History  |                                 |                   |
|         |                                 |                   |
+---------+---------------------------------+-------------------+

____________________________________________________________________________________________


## Left Panel / Sidebar Draft (d1.1)


+--------------------------------+
|  🔍 Search Projects            |
|--------------------------------|
| + New Project                  |
|--------------------------------|
| 📁 Inventory API               |
|    ├── GET /products           |
|    ├── POST /products          |
|    └── DELETE /products        |
|                                |
| 📁 Auth API                    |
|    ├── POST /login             |
|    └── POST /register          |
+--------------------------------+

___________________________________________________________________________________________


## First Feature (Projects) Domain Modeling (d1.1.1)


Project   
          
↓         
          
Endpoint  
          
↓         
          
Execution 

___________________________________________________________________________________________


## Projects and its sub-objects' relationships


One Project
      │
      └────────────▶ Many Endpoints

______________________________________

One Endpoint
↓
Many Executions

______________________________________

Project A

    GET /users

Project B

    GET /users

_______________________________________

Project (1)

owns

Endpoints (many)

owns

Executions (many)

________________________________________


Domain Model


                  Pulse
                     │
                     │
             ┌───────▼────────┐
             │    Project      │
             └───────┬────────┘
                     │
             One Project
                owns many
                     │
             ┌───────▼────────┐
             │    Endpoint     │
             └───────┬────────┘
                     │
            One Endpoint
             has many
                     │
             ┌───────▼────────┐
             │   Execution     │
             └────────────────┘


_________________________________________________________________________________________


## Projects and its sub-objects' ER diagram (d1.1.1a)


┌──────────────────────────┐
│         PROJECT          │
├──────────────────────────┤
│ id                       │
│ name                     │
│ description              │
│ created_at               │
│ updated_at               │
└─────────────┬────────────┘
              │
              │ 1
              │
              │ owns
              │
              ▼
             ∞
┌──────────────────────────┐
│        ENDPOINT          │
├──────────────────────────┤
│ id                       │
│ project_id               │
│ method                   │
│ url                      │
│ description              │
│ headers                  │
│ query_params             │
│ request_body             │
│ created_at               │
│ updated_at               │
└─────────────┬────────────┘
              │
              │ 1
              │
              │ executed many times
              │
              ▼
             ∞
┌──────────────────────────┐
│       EXECUTION          │
├──────────────────────────┤
│ id                       │
│ endpoint_id              │
│ executed_at              │
│ status_code              │
│ response_time_ms         │
│ response_headers         │
│ response_body            │
│ error_message            │
└──────────────────────────┘


__________________________________________________________________________________________


## Projects and its sub-objects' API Design (d1.1.1b)


POST   /projects

GET    /projects

GET    /projects/{id}

PATCH  /projects/{id}

DELETE /projects/{id}

_____________________________________

Endpoints

POST   /projects/{id}/endpoints

GET    /projects/{id}/endpoints

PATCH  /endpoints/{id}

DELETE /endpoints/{id}

_____________________________________

Executions

POST   /endpoints/{id}/execute

GET    /endpoints/{id}/executions

___________________________________________________________________________________________


## Overall folder and sub-folders setup (d1.0a)


pulse/

│
├── backend/
│
│   ├── python/
│   │
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
│
│   ├── css/
│   ├── js/
│   ├── assets/
│   └── index.html
│
├── docs/
│
├── README.md
│
└── .env

___________________________________________________________________________________________


## Starting setup (d1.0b)


Project-Chimera/

│
├── docs/
│
│   ├── Architecture.md
│   ├── DecisionLog.md
│   ├── Journal.md
│   ├── Roadmap.md
│   └── Resources.md
│
├── assets/
│   ├── diagrams/
│   └── sketches/
│
├── backend/
│
├── frontend/
│
├── .gitignore
│
├── README.md
│
└── LICENSE (later)

____________________________________________________________________________________________


# Final Setup (d1.0c....for no starting confusion)


pulse/

├── README.md
├── .gitignore
│
├── docs/
│   ├── Architecture.md
│   ├── DecisionLog.md
│   └── Resources.md
│
├── assets/
│   ├── diagrams/
│   └── sketches/
│
├── frontend/
│   ├── index.html
│   ├── css/
│   ├── js/
│   └── assets/
│
└── backend/
    │
    ├── python/
    │   ├── app.py
    │   ├── requirements.txt
    │   ├── .env
    │   │
    │   ├── config/
    │   ├── routes/
    │   ├── controllers/
    │   ├── services/
    │   ├── models/
    │   ├── database/
    │   └── utils/
    │
    └── go/
        ├── go.mod
        ├── repository/
        ├── json/
        └── utils/

__________________________________________________________________________________________________


# Version 1 Milestones

1. Bootstrap
2. Projects
3. Endpoints
4. Executions
5. Polish & Deployment

___________________________________________________________________________________________________



# Current Implemented Flow (Slice 1 - d1.1.2)


Browser

↓

JavaScript (Fetch API)

↓

Flask Routes

↓

Controllers

↓

Services

↓

Repositories

↓

Models

↓

In-memory Storage

↓

HTTP Response

↓

JavaScript

↓

DOM Rendering

_______________________________________________________________________________________________________


# Current Implemented Flow (Slice 2 - d1.1.3)

Browser

↓

JavaScript (Fetch API)

↓

POST /execute

↓

Flask Route

↓

Controller

↓

Execution Service

↓

External HTTP API

↓

Execution Service

↓

Controller

↓

HTTP Response

↓

JavaScript

↓

Response Viewer

_________________________________________________________________________________________________________


## Slice 2 Execution Responsibility

Frontend

Collects request details and sends them to the backend.

↓

Route

Maps `/execute` to the execution controller.

↓

Controller

Extracts request data and coordinates execution.

↓

Service

Performs the external HTTP request and returns the status and response body.

↓

Response Viewer

Displays the execution result.

__________________________________________________________________________________________________


# ------------------------------ SLICE 3 ------------------------------

## Slice 3 — Resource Management + Request Execution Integration

Slice 3 connects the project/endpoint resource layer with the request execution workflow.

The implemented responsibility is now:

Project
   ↓
Endpoint
   ↓
Request Configuration
   ↓
Request Execution
   ↓
Status + Response


Slice 3 covers:

Project CRUD
Endpoint CRUD
Project → Endpoint ownership
Frontend project/endpoint selection
Request-builder population from saved endpoints
Request execution
Response display
Basic frontend validation

_________________________________________________

## Slice 3 Backend Layer Architecture

The backend now consistently follows the layered architecture:

HTTP Request
     ↓
Route
     ↓
Controller
     ↓
Service
     ↓
Repository
     ↓
In-memory Storage

The response travels back through the same layers:

In-memory Storage
     ↓
Repository
     ↓
Service
     ↓
Controller
     ↓
HTTP Response
     ↓
Frontend


## Route

Defines the HTTP endpoint and forwards the request to the appropriate controller.

## Controller

Handles HTTP-specific concerns:

reading JSON request bodies
extracting route parameters
calling the service layer
converting domain objects to JSON
returning HTTP responses/status codes

## Service

Contains business logic and validation.

## Repository

Handles access to the current in-memory storage.

## Model

Represents the domain object.

____________________________________________________

## Slice 3 Project CRUD

Projects now have complete CRUD support:

POST   /projects
GET    /projects
PATCH  /projects/{id}
DELETE /projects/{id}

The flow is :

Frontend
   ↓
Project Route
   ↓
ProjectController
   ↓
ProjectService
   ↓
ProjectRepository
   ↓
In-memory Project List

ProjectService receives both the ProjectRepository and EndpointRepository.

This allows project deletion to enforce the parent-child relationship:

Delete Project
      ↓
Validate Project exists
      ↓
Delete all Endpoints belonging to Project
      ↓
Delete Project

___________________________________________________

## Slice 3 Endpoint CRUD

Endpoints now have complete resource management:

POST   /projects/{project_id}/endpoints
GET    /projects/{project_id}/endpoints
GET    /endpoints/{endpoint_id}
PATCH  /endpoints/{endpoint_id}
DELETE /endpoints/{endpoint_id}

The endpoint belongs to a project through: project_id

Endpoint creation therefore verifies that its parent project exists.

The currently implemented endpoint structure is:

Endpoint
├── id
├── project_id
├── name
├── method
├── url
└── body

Currently supported HTTP methods are:

GET
POST
PATCH
DELETE

The service layer validates endpoint name, URL, HTTP method and parent-project existence where applicable.

_______________________________________________________________

## Slice 3 Repository Architecture

The current repositories use in-memory Python lists:

ProjectRepository
    └── projects[]

EndpointRepository
    └── endpoints[]

Repositories expose CRUD operations to the service layer while hiding the underlying storage implementation.

This preserves the existing architecture for the eventual transition to PostgreSQL.

EndpointRepository additionally supports filtering endpoints by their parent project and deleting all endpoints belonging to a project.

________________________________________________________________

## Slice 3 Frontend Resource Hierarchy

The frontend now mirrors the backend project → endpoint relationship.

Instead of a separate global endpoint section:

Projects

Project A

Endpoints
   └── Endpoint A

the endpoint list is dynamically nested underneath its project:

Projects

Project A
   ├── Endpoint A
   └── Endpoint B

Project B
   └── Endpoint C

When a project is selected:

Its backend ID is stored in selectedProjectID.
Its endpoints are fetched from the backend.
Previously displayed endpoint lists are removed.
A new endpoint list is created.
The endpoint list is attached beneath the selected project.

______________________________________________________________

## Slice 3 Frontend State

The frontend maintains:

let selectedProjectID = null;
let selectedEndpoint = null;

selectedProjectID: 
Stores the ID of the currently selected project and is used for project-scoped endpoint operations.

selectedEndpoint: 
Stores the complete endpoint object currently selected.

Keeping the complete endpoint object avoids maintaining separate state variables for every endpoint property.

______________________________________________________________

## Slice 3 Endpoint → Request Builder Flow

Selecting an endpoint follows:

Endpoint selected
      ↓
selectedEndpoint = endpoint object
      ↓
loadEndpointIntoBuilder()
      ↓
Method
URL
Body

The endpoint body receives special handling:

endpoint.body == null
        ↓
empty textarea

endpoint.body exists
        ↓
JSON.stringify(endpoint.body, null, 2)
        ↓
formatted JSON in textarea

This keeps the backend's null representation for an absent body separate from the frontend's empty editing field.

___________________________________________________________

## Slice 3 Endpoint Creation Flow

Saving an endpoint from the frontend follows:

Select Project
      ↓
Enter Endpoint Name
      ↓
Configure Method / URL / Body
      ↓
Validate
      ↓
Parse JSON Body
      ↓
POST /projects/{project_id}/endpoints
      ↓
EndpointService
      ↓
EndpointRepository
      ↓
Refresh selected project's endpoint list

An endpoint cannot be saved without:

a selected project
an endpoint name
a URL
valid JSON when a body is supplied

____________________________________________________________

## Slice 3 Request Execution Integration

Saving an endpoint and executing a request remain separate operations.

A saved endpoint can populate the request builder, after which the user can modify the configuration before executing it.

Select Endpoint
      ↓
Load Endpoint Configuration
      ↓
Modify Request Configuration if required
      ↓
Send
      ↓
POST /execute
      ↓
Execution Controller
      ↓
Execution Service
      ↓
External HTTP API
      ↓
Status + Response Body
      ↓
Response Viewer

The request builder therefore represents the current request configuration, while the saved endpoint represents the persisted resource configuration currently held by the backend.

_____________________________________________________________

## Slice 3 Project + Endpoint CRUD Scope

The frontend/backend resource layer now supports:

Projects
├── Create
├── Read/List
├── Update
└── Delete

Endpoints
├── Create
├── Read/List
├── Read by ID
├── Update
└── Delete

Updating an endpoint preserves its existing project_id, preventing an ordinary endpoint update from accidentally changing its parent project.

Deleting a project also deletes its child endpoints.

_____________________________________________________________

# ------------------------------ SLICE 4 ------------------------------

## Slice 4 — Request Parameters + Headers

Slice 4 extends Endpoint configuration to include query parameters and HTTP headers.

The Endpoint structure now includes:

Endpoint
├── id
├── project_id
├── name
├── method
├── url
├── params
├── headers
└── body

The Request Builder now provides dynamic editors for both Params and Headers.

Each row contains:

Key | Value | Delete

Users can add or remove rows dynamically.

_____________________________________________________________

## Slice 4 Request Configuration Flow

Select Endpoint
      ↓
Load Endpoint Configuration
      ↓
Method / URL / Params / Headers / Body
      ↓
Modify if required
      ↓
Save or Send

Saved endpoints reconstruct their Params and Headers when loaded into the Request Builder.

_____________________________________________________________

## Slice 4 Execution Integration

Params and Headers are collected by the frontend and included in the existing execution payload.

The execution pipeline remains:

Frontend
   ↓
POST /execute
   ↓
Execution Controller
   ↓
Execution Service
   ↓
External HTTP API

The execution layer now uses the configured query parameters and headers when making the outbound request.

Slice 4 does not introduce a new execution architecture; it extends the existing request configuration flow. 

________________________________________________________________


# ------------------------------ SLICE 5 ------------------------------

## Slice 5 — PostgreSQL Persistence

Slice 5 replaces the in-memory Project and Endpoint repositories with PostgreSQL persistence while keeping the existing layered architecture unchanged.

Current flow:

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

_____________________________________________________________

### Persistence Model

PostgreSQL now owns:

- Project and Endpoint IDs through identity columns
- created_at / updated_at timestamps
- Project → Endpoint ownership through a foreign key
- cascading Endpoint deletion when a Project is deleted

Endpoint `params`, `headers`, and `body` are stored as JSONB.

_______________________________________________________________

### Resource Metadata

Projects and Endpoints now support optional descriptions.

Descriptions are persisted alongside the resource and exposed in the frontend.

_______________________________________________________________

### Architecture Boundary

The PostgreSQL migration changes the repository implementation, not the responsibility of the surrounding layers.

The Service layer continues to handle validation and business logic, while the Repository handles database access and mapping between database rows and domain models.

This preserves the layered architecture while making resource state persistent across application restarts.

_______________________________________________________________