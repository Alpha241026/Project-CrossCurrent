# Architecture




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