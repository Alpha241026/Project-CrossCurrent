# Learning Log


# ------------------------------ DAY 1 / 2 ------------------------------


# Gap 1

## Topic
Vanilla JavaScript (DOM, Events, Fetch API)

## Reason
Required for the Pulse frontend to communicate with the backend and update the UI dynamically.

## Status
✅ Completed (Builder)

## Notes
Covered:
- DOM manipulation
- Event listeners
- Fetch API
- Basic async/await

_______________________________________________________________________________________


# Gap 2

## Topic
Go net/http fundamentals

## Reason
Pulse backend is written in Go. Needed to understand how HTTP requests are received, routed, processed and returned before building the real API.

## Status
✅ Completed (Builder)

## Notes
Covered:
- Handler functions
- ResponseWriter
- Request
- HandleFunc
- ListenAndServe
- JSON responses using json.NewEncoder
- Returning plain text vs JSON


____________________________________________________________________________________________________


# ------------------------------ DAY 3 / 4 / 5 ------------------------------


# Slice 1

## Topic
Project Management (Flask + Vanilla JS)

## Reason
Build the first complete end-to-end feature of Chimera by connecting the frontend with the backend using a layered architecture.

## Status
✅ Completed

## Notes

Covered:
- Flask layered architecture (Route → Controller → Service → Repository)
- GET and POST API endpoints
- Frontend-backend communication using Fetch API
- Dynamic project rendering using DOM manipulation
- Basic Flexbox layout for the sidebar
- Loading existing projects automatically on page load

Key Learnings:
- Refresh the UI from backend data instead of manually keeping it synchronized.
- `proList.innerHTML = ""` prevents duplicate rendering before rebuilding the list.
- `loadProjects()` should run after a successful POST and when the application first loads.

Common Bugs:
- Flask server not running (`ERR_CONNECTION_REFUSED`).
- Duplicate project rendering caused by not clearing the project list before re-rendering.
- Dependency wiring confusion between `app.py`, routes, controller and service during initial setup.

________________________________________________________________________________________________


# ------------------------------ DAY 6 / 7 ------------------------------

# Slice 2

## Topic

Request Execution Pipeline (Flask + Vanilla JS)

## Reason

Build the first complete request execution flow by routing API requests through the Pulse backend instead of contacting external APIs directly from the frontend.

## Status

✅ Completed

## Notes

Covered:

- Request Builder and Response Viewer frontend structure
- Sending request details from the frontend to the Flask backend
- Flask execution flow (Route → Controller → Service)
- External HTTP requests using Python's `requests` library
- GET and POST request execution
- Returning standardized JSON responses containing status and body

Key Learnings:

- The frontend sends request instructions to the backend instead of directly contacting external APIs.
- Routes handle URL mapping, controllers coordinate request and response flow, and services perform the actual HTTP execution.
- The backend returns the response status and body to the frontend for display.
- Request execution was tested independently with both GET and POST requests.

Common Bugs:

- Frontend initially contacted external APIs directly instead of routing requests through the backend.
- Incorrect indentation caused GET requests to return `null`.
- Confusion between Route, Controller and Service responsibilities during the initial backend implementation.
- Request body needed to be parsed from JSON before being sent to the backend.

____________________________________________________________________________________________________________

# ------------------------------ SLICE 3 ------------------------------

## Topic

Project & Endpoint Resource Management + Request Workflow

## Reason

Extend Chimera from basic project creation and request execution into a usable project-based API workspace by introducing reusable Endpoints, full resource CRUD, project selection and request-builder integration.

## Status

✅ Completed

## Notes

Covered:
- Endpoint domain modeling and Project → Endpoint ownership
- Full Project and Endpoint CRUD using Flask layered architecture
- In-memory repositories and dependency injection across services
- Project deletion cascading to child Endpoints
- Frontend project selection and nested Endpoint rendering
- Endpoint selection and loading saved configuration into the Request Builder
- Saving, updating and deleting Endpoints from the frontend
- Request execution expanded to GET, POST, PATCH and DELETE
- Handling empty/non-JSON HTTP responses
- Basic frontend validation and JSON body parsing

Key Learnings:
- Repositories handle storage operations while Services handle validation and cross-resource business logic.
- selectedProjectID and the complete selectedEndpoint object provide the frontend state needed for project-scoped operations and Request Builder population.
- Saved resource state should be refreshed from the backend after successful mutations.
- data-* attributes can connect dynamically rendered DOM elements to backend resource IDs.
- Empty request bodies should be represented as null rather than forcing JSON parsing.
- HTTP method support and route design must remain consistent across frontend, controllers, services and repositories.

Common Bugs:
- Repository update methods required both the resource ID and replacement object.
- Endpoint update/delete frontend routes initially did not match the backend's Endpoint-scoped routes.
- response.json() failed when backend errors returned HTML instead of JSON.
- Empty DELETE bodies caused JSON.parse("") failures.
- Endpoint lists initially rendered as a separate global section instead of nested under their Project.
- Request Builder fields were initially assigned in the wrong direction when loading a saved Endpoint.
- Frontend options code remained after the execution request configuration had already been rebuilt, causing an undefined-variable error for non-GET requests.

__________________________________________________________________________________________________________________________

# ------------------------------ SLICE 4 ------------------------------**

## Topic

Request Params & Headers + Dynamic Request Builder

## Reason

Extend the Request Builder so Endpoints can represent more complete HTTP request configurations through query parameters and custom headers.

## Status

✅ Completed

## Notes

Covered:

- Dynamic DOM generation for Params and Headers
- Key-value row creation and deletion using JavaScript
- Collecting Params and Headers into request data
- Persisting and restoring Params and Headers with Endpoints
- Updating request execution to include query parameters and custom headers
- Loading complete saved Endpoint configuration back into the Request Builder
- Basic responsive/flexible CSS layout for the expanded Request Builder

Key Learnings:

- Dynamic UI elements can be created and managed through reusable DOM functions.
- Params and Headers belong to the request configuration and should travel with the Endpoint.
- Saved configuration should reconstruct the same Request Builder state when an Endpoint is selected.
- Query parameters modify the outgoing URL, while headers belong to the HTTP request metadata.

Common Bugs:

- Params and Headers initially rendered as separate stacked inputs instead of compact key-value rows.
- Dynamically generated rows required their own event listeners for deletion.
- Saved Params and Headers initially needed explicit reconstruction when loading an Endpoint.
- Execution had to be updated so the newly stored Params and Headers actually reached the external API.

________________________________________________________________________________________________________________________


# ------------------------------ SLICE 5 ------------------------------

## Topic

PostgreSQL Persistence + JSONB + Database-backed Repositories

## Reason

Replace temporary in-memory storage with durable PostgreSQL persistence while preserving the existing layered architecture.

## Status

✅ Completed

## Notes

Covered:

- PostgreSQL connection using `psycopg`
- Environment-based database configuration with `.env`
- SQL schema design for Projects and Endpoints
- Identity-generated integer IDs
- PostgreSQL foreign keys and `ON DELETE CASCADE`
- Repository-based CRUD using SQL
- JSONB storage for Params, Headers and request Body
- Mapping database rows back into domain models
- Persisting Project and Endpoint descriptions

Key Learnings:

- A Repository abstraction allows persistence to change without redesigning higher application layers.
- Database-generated IDs and timestamps should come from the database rather than application code.
- JSON-shaped request configuration can be stored as JSONB without introducing unnecessary relational tables.
- Database constraints can enforce domain ownership rules such as Project → Endpoint cascading.
- PostgreSQL persistence makes backend state survive application restarts.

Common Bugs:

- PostgreSQL could not adapt Python dictionaries directly for JSONB parameters; `psycopg.types.json.Jsonb` was required.
- Database-generated IDs required removing the previous in-memory ID generation logic.
- Project deletion logic had to be aligned with the database's `ON DELETE CASCADE` behavior.
- Project descriptions were initially persisted but not displayed in the normal sidebar UI.

_________________________________________________________________________________________________________________________


# ------------------------------ SLICE 6 ------------------------------

## Topic

Executions + History (Go + PostgreSQL + Python Integration)

## Reason

Introduce persistent execution records and execution history while giving Go a meaningful backend responsibility without replacing the established Python execution layer.

## Status

✅ Completed

## Notes

Covered:

- Execution domain model and PostgreSQL persistence
- Go PostgreSQL connection using database/sql and pgx
- Go ExecutionRepository
- Creating executions with database-generated IDs and timestamps
- Retrieving executions by ID
- Retrieving endpoint execution history
- Go HTTP service for execution persistence and retrieval
- Python → Go execution result integration
- Frontend execution history and historical response inspection

Key Learnings:

- Go can be introduced as a specialized backend subsystem without rewriting existing Python functionality.
- database/sql provides a clean interface for PostgreSQL repositories through context-aware queries.
- INSERT ... RETURNING allows PostgreSQL-generated IDs and timestamps to be returned directly to Go.
- Execution is an immutable record of an Endpoint attempt.
- History is naturally represented as a view over an Endpoint's stored Executions rather than as a separate entity.
- A successful external API response should remain available even if secondary history persistence fails.

Common Bugs:

- Go PostgreSQL connection initially required dependency installation through a different network because of a local certificate issue.
- Execution test initially used an Endpoint ID that did not exist in the database, causing a foreign-key violation.
- Pointer fields printed memory addresses until their values were explicitly dereferenced during testing.
- Empty execution history initially returned null instead of an empty collection.
- The History UI initially conflicted with the existing workspace layout and required layout adjustment.

_________________________________________________________________________________________________________________________


# ------------------------------ SLICE 7 ------------------------------

## Topic

Finalization, Product Identity & V1 Polish

## Reason

Complete the transition from a functional engineering project into a coherent V1 product by refining its identity, frontend presentation and deployment readiness.

## Status

✅ Completed

## Notes

Covered:

- Final project naming and product identity
- CrossCurrent brand direction based on two independent currents crossing once
- Favicon design with small-size readability as the primary constraint
- Browser title and metadata considerations
- Frontend visual polish and consistency checks
- Final documentation review and architectural consistency
- V1 scope freeze and avoiding unnecessary last-minute refactoring

Key Learnings:

- A project name should reinforce the product's concept without needing to describe its implementation literally.
- A favicon is a small-scale interface asset and must be designed for clarity at 16px rather than simply shrinking a larger logo.
- Final polish should improve clarity and identity without destabilizing working functionality.
- Documentation should preserve the reasoning behind important engineering decisions rather than becoming a chronological list of every implementation change.
- Near the end of a project, scope discipline becomes as important as adding features.

Common Bugs:

- Final UI work can expose inconsistencies that were not visible while focusing primarily on functionality.
- Branding assets can become visually overcomplicated when designed for large displays instead of favicon-scale use.
- Last-minute cleanup can introduce unnecessary changes to already stable backend behavior.

________________________________________________________________________________________________________________________________