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