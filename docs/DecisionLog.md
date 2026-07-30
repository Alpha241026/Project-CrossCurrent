# Decision Log



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

- ## D008 : History is NOT a first-class entity.

Reason:
History is simply a view over Executions.

Alternative:
Separate History table.

Rejected because:
It duplicates data and adds unnecessary complexity.

_______________________________________________________________________________________________________

- ## D009 : Every new feature must pass the Version 1 Filter.

Questions:

Does it improve learning?

Does it improve clarity?

Does it keep architecture simple?

Does it reduce friction?

If not, postpone.

_______________________________________________________________________________________________________

- ## D010 : Layered Architecture