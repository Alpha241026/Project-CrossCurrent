CREATE TABLE projects (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE endpoints (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    project_id INTEGER NOT NULL,

    name TEXT NOT NULL,
    method TEXT NOT NULL,
    url TEXT NOT NULL,
    description TEXT,

    params JSONB NOT NULL DEFAULT '{}'::jsonb,
    headers JSONB NOT NULL DEFAULT '{}'::jsonb,
    body JSONB,

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_endpoints_project
        FOREIGN KEY (project_id)
        REFERENCES projects(id)
        ON DELETE CASCADE,

    CONSTRAINT valid_endpoint_method
        CHECK (method IN ('GET', 'POST', 'PATCH', 'DELETE'))
);

CREATE TABLE executions (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    endpoint_id INTEGER NOT NULL,

    executed_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status_code INTEGER,
    response_time INTEGER,
    response_headers JSONB NOT NULL DEFAULT '{}'::jsonb,
    response_body JSONB,
    error_message TEXT,

    CONSTRAINT fk_executions_endpoint
        FOREIGN KEY (endpoint_id)
        REFERENCES endpoints(id)
        ON DELETE CASCADE
);