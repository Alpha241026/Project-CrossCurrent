# Decision Log


# ------------------------------ DAY 1/2 ------------------------------


- ## D001 : Pulse Version 1 will use a fixed three-panel workspace.

Sidebar

↓

Request Builder

↓

Response Viewer

______________________________________________________________________________________________________

- ## D002 : For Version 1, Pulse has three primary domain entities:

📁 Project

A container for organizing related API work.

Examples:

Inventory API
Weather API
Auth Service
🌐 Endpoint

A reusable API definition belonging to a Project.

It stores things like:

Method
URL
Headers
Body
Query parameters

Notice I said stores, not executes.

▶ Execution

A single attempt to execute an Endpoint.

It records:

Timestamp
Status code
Response body
Headers
Duration
Success/failure

A Response does not exist independently.

History is simply a filtered or grouped view of Executions.

_____________________________________________________________________________________________________

- ## D003 : Ownership

Project

owns

Endpoints

owns

Executions

______________________________________________________________________________________________________

- ## D004 : Version 1 Deletion

Hard delete.

Not because it's "better."

Because it's appropriate.

We'll literally write in our roadmap:

"Soft delete intentionally postponed."

That's not a limitation.

That's scope management.

______________________________________________________________________________________________________

- ## D005 : Version 1 uses Integer IDs instead of UUIDs.

Reason:
- Easier debugging
- Easier learning
- Easier to explain
- Sufficient for a local developer tool

Future:
UUIDs remain a future enhancement.

______________________________________________________________________________________________________

- ## D006 : Sidebar Interaction

Decision:

A single click on an Endpoint loads it into the Request Builder.

No separate "Open" button.

Why?
1. Matches user expectations
2. No destructive action
3. Fewer clicks

________________________________________________________________________________________________________

- ## D007 : History is NOT a first-class entity.

Reason:
History is simply a view over Executions.

Alternative:
Separate History table.

Rejected because:
It duplicates data and adds unnecessary complexity.

_______________________________________________________________________________________________________

- ## D008 : Every new feature must pass the Version 1 Filter.

Questions:

Does it improve learning?

Does it improve clarity?

Does it keep architecture simple?

Does it reduce friction?

If not, postpone.

_______________________________________________________________________________________________________

- ## D09 : Layered Architecture

backend/

models/
    Project

↓

repositories/
    ProjectRepository

↓

services/
    ProjectService

↓

controllers/
    ProjectController

↓

routes/
    project_routes

↓

app.py


___________________________________________________________________________________________________


# ------------------------------ DAY 3 / 4 / 5 ------------------------------


- ## D010 : Project data will initially be stored in an in-memory repository.

Reason:
Allows validation of the layered architecture before introducing PostgreSQL.

Future:
Replace the repository storage with a real database without changing the frontend or higher backend layers.

______________________________________________________________________________________________________


- ## D011 : The frontend will always refresh its state from the backend after successful operations.

Reason:
The backend remains the single source of truth.

Alternative:
Manually append newly created projects to the sidebar.

Rejected because:
It risks frontend and backend state becoming inconsistent.

______________________________________________________________________________________________________


- ## D012 : Slice 1 will use Vanilla JavaScript Fetch API for backend communication.

Reason:
Keeps the frontend lightweight while reinforcing HTTP fundamentals before introducing any frontend framework.

Future:
The communication layer can later be migrated to React or another framework without changing the backend API.

______________________________________________________________________________________________________


# ------------------------------ DAY 6 / 7 ------------------------------

- ## D013 : Request execution will be routed through the Pulse backend.

Decision:

The frontend will send request details to the backend instead of contacting external APIs directly.

Reason:

Keeps request execution behind the backend boundary and allows Pulse to later handle execution-related features such as history, logging and authentication centrally.

___________________________________________________________________________________________________

- ## D014 : Version 1 will use a single `/execute` endpoint for request execution.

Decision:

The frontend sends:

Method
URL
Body

to:

POST /execute

The backend then performs the actual external HTTP request.

Reason:

Keeps the frontend execution logic simple while providing a single entry point for request execution.

_____________________________________________________________________________________________________

- ## D015 : External HTTP communication belongs in the Service layer.

Decision:

The execution Service will use Python's `requests` library to perform external API calls.

Reason:

The Route handles URL mapping.

The Controller handles request/response coordination.

The Service handles the actual execution logic.

This keeps the layered architecture consistent.

_____________________________________________________________________________________________________

- ## D016 : Execution responses will be returned in a standardized format.

Decision:

The backend will return:

{
    status,
    body
}

Reason:

The frontend only needs the HTTP status and response body to display the result in the Response Viewer.

___________________________________________________________________________________________________

- ## D017 : Version 1 execution initially supports GET and POST requests.

Reason:

Sufficient for validating the complete request execution pipeline before expanding support to additional HTTP methods.

Future:

PUT, PATCH, DELETE and additional request features remain part of future slices.

_________________________________________________________________________________________________

# ------------------------------ SLICE 3 ------------------------------

- ## D018 : Endpoint execution support expanded to GET, POST, PATCH and DELETE.

Decision:

Version 1 execution now supports:

GET
POST
PATCH
DELETE

Reason:

The frontend already exposes these request methods and supporting them keeps the request builder and execution layer consistent.

________________________________________________________________________________________________

- ## D019 : Project deletion will cascade to its Endpoints.

Decision:

Deleting a Project also deletes all Endpoints belonging to it.

Reason:

Endpoints are owned by Projects in Version 1 and have no independent purpose without their parent Project.

Implementation:

The ProjectService coordinates deletion through both repositories.

_______________________________________________________________________________________________

- ## D020 : Endpoint update/delete routes will use Endpoint-scoped IDs.

Decision:

Creation/listing remain project-scoped:

POST /projects/{project_id}/endpoints
GET  /projects/{project_id}/endpoints

Individual Endpoint operations use:

GET    /endpoints/{endpoint_id}
PATCH  /endpoints/{endpoint_id}
DELETE /endpoints/{endpoint_id}

Reason:

An Endpoint already contains its project_id; individual operations target the Endpoint directly.

________________________________________________________________________________________________

- ## D021 : Frontend selection state will track the active Project and Endpoint.

Decision:

The frontend maintains:

selectedProjectID
selectedEndpoint

Reason:

The selected Project determines the Endpoint scope, while the complete selected Endpoint object is reused to populate the Request Builder without an unnecessary second lookup.

_________________________________________________________________________________________________

- ## D022 : Endpoints will be rendered as nested children of Projects.

Decision:

Endpoint lists appear inside their selected Project rather than as a separate global sidebar section.

Reason:

Keeps the UI consistent with the Project → Endpoint ownership model.

__________________________________________________________________________________________________

- ## D023 : The Request Builder will also serve as the Endpoint editing surface.

Decision:

Selecting an Endpoint loads its saved configuration into the existing Request Builder.

Updating an Endpoint reuses the same builder rather than introducing a separate edit form.

Reason:

Avoids duplicate UI and keeps Endpoint management centered around the actual request configuration.

____________________________________________________________________________________________________

- ## D024 : Endpoint creation will reuse the current Request Builder configuration.

Decision:

Saving an Endpoint sends:

name
method
url
body

under the currently selected Project.

Reason:

Avoids maintaining a second request-configuration form and keeps saved Endpoints directly connected to executable requests.

_______________________________________________________________________________________________________

- ## D025 : Request bodies will be represented as null when empty.

Decision:

Empty request bodies are sent/stored as null.

Frontend textareas display null bodies as empty fields, while existing JSON bodies are formatted for editing.

Reason:

Keeps the backend representation explicit without displaying the literal null to users.

_________________________________________________________________________________________________________

- ## D026 : Request execution must tolerate non-JSON responses.

Decision:

Execution will attempt JSON parsing but fall back to raw response text when a response cannot be parsed as JSON.

Reason:

External APIs may return empty or plain-text responses, including successful 204 No Content responses.

_________________________________________________________________________________________________________

- ## D027 : Slice 3 remains in-memory.

Decision:

Projects and Endpoints continue using in-memory repositories.

Reason:

Slice 3 focuses on resource management and workflow integration; durable persistence remains a later architectural step.

__________________________________________________________________________________________________________

# ------------------------------ SLICE 4 ------------------------------

- ## D028 : Params and Headers will use dynamic key-value rows.

Decision:

Users can add or remove Params and Headers dynamically from the Request Builder.

Each row contains:

Key | Value | Delete

Reason:

Keeps request configuration flexible without requiring a fixed number of fields.

__________________________________________________________________________________________________________

- ## D029 : Params and Headers will share the same row-generation pattern.

Decision:

Params and Headers use separate row-creation functions but follow the same DOM structure and interaction pattern.

Reason:

Keeps the frontend implementation consistent while preserving clear separation between query parameters and HTTP headers.

_________________________________________________________________________________________________________

- ## D030 : Saved Params and Headers will be reconstructed in the Request Builder.

Decision:

Selecting a saved Endpoint restores its stored Params and Headers into dynamically generated rows.

Reason:

The Request Builder should represent the complete saved Endpoint configuration rather than only its method, URL and body.

________________________________________________________________________________________________________

- ## D031 : The Request Builder remains the single request-configuration surface.

Decision:

Params and Headers are configured, edited and reviewed directly inside the existing Request Builder.

Reason:

Avoids introducing separate configuration screens and keeps Endpoint editing centered around the executable request.

_______________________________________________________________________________________________________

# ------------------------------ SLICE 5 ------------------------------

- ## D032 : Project and Endpoint persistence will move from in-memory storage to PostgreSQL.

Decision:

The Repository layer will use PostgreSQL as the persistent storage backend.

Reason:

The resource model is stable enough to introduce durable persistence without changing the surrounding layered architecture.

The frontend, Controllers and Services remain independent of the storage implementation.

______________________________________________________________________________________________________

- ## D033 : PostgreSQL will generate Project and Endpoint IDs.

Decision:

Use PostgreSQL identity columns for integer IDs instead of generating IDs in application code.

Reason:

The database is responsible for persistent identity generation, while integer IDs remain simple and sufficient for Version 1.

______________________________________________________________________________________________________

- ## D034 : Endpoint request configuration will use PostgreSQL JSONB.

Decision:

Params, Headers and request Body will be stored as JSONB fields.

Reason:

These structures are naturally key-value / JSON-shaped and do not require separate relational tables for Version 1.

This keeps the schema simple while preserving the complete Endpoint configuration.

________________________________________________________________________________________________________

- ## D035 : Project deletion cascading will be enforced by PostgreSQL.

Decision:

The Project → Endpoint relationship uses a foreign key with `ON DELETE CASCADE`.

Reason:

Endpoint ownership is already defined at the domain level, so the database should enforce the same invariant when a Project is deleted.

This replaces the earlier application-level cascade implementation.

________________________________________________________________________________________________________

- ## D036 : Python and Go remain permanent backend technologies.

Decision:

The PostgreSQL migration does not trigger a rewrite of existing Python responsibilities into Go.

Python continues handling the established API, resource management and application coordination.

Go will be assigned meaningful new backend responsibilities in later slices rather than being used merely to replace existing Python code.

Reason:

Technology choice should follow responsibility and learning value, not an arbitrary language quota.

__________________________________________________________________________________________________________

# ------------------------------ SLICE 6 ------------------------------

## D037 : Execution history will be persisted through a dedicated Go subsystem.

Decision:

Go will own persistence and retrieval of Execution records through a small HTTP service.

Reason:

This gives Go a meaningful backend responsibility without rewriting the established Python execution layer.

__________________________________________________________________________________________________________

## D038 : Python will continue performing outbound HTTP requests.

Decision:

The existing Python ExecutionService continues to use requests for external API communication.

After execution, Python sends the resulting Execution record to Go for persistence.

Reason:

The existing execution path is already established and working. Go is introduced as new functionality rather than as a rewrite target.

__________________________________________________________________________________________________________

## D039 : Execution history will be associated directly with Endpoints.

Decision:

Each Execution stores endpoint_id and belongs to one Endpoint.

Reason:

An Endpoint can be executed multiple times, making Execution the natural immutable record of each attempt.

__________________________________________________________________________________________________________

## D040 : History will remain a view over Executions.

Decision:

History is not introduced as a separate database entity.

Reason:

History represents previously recorded Executions and does not require duplicated data.

__________________________________________________________________________________________________________

## D041 : History persistence failure will not hide a successful API response.

Decision:

If the external request succeeds but the Go history service is unavailable, the frontend still receives the external API result.

Reason:

Execution is the primary operation; history is supporting functionality in V1.

__________________________________________________________________________________________________________