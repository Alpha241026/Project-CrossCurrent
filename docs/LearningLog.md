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

___________________________________________________________________________________________________________