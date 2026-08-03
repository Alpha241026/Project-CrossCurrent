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