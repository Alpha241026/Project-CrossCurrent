package repositories

import (
	"context"
	"database/sql"

	"chimera-go/models"
)

type ExecutionRepository struct {
	db *sql.DB
}

// NewExecutionRepository creates a repository backed by the provided database connection
func NewExecutionRepository(db *sql.DB) *ExecutionRepository {
	return &ExecutionRepository{
		db: db,
	}
}

// create stores a new execution and returns the database-generated ID and timestamp
func (r *ExecutionRepository) Create(ctx context.Context, execution *models.Execution) error {
	query := `
		INSERT INTO executions (
			endpoint_id,
			status_code,
			response_time,
			response_headers,
			response_body,
			error_message
		)
		VALUES ($1, $2, $3, $4, $5, $6)
		RETURNING id, executed_at
	`

	return r.db.QueryRowContext(
		ctx,
		query,
		execution.EndpointID,
		execution.StatusCode,
		execution.ResponseTime,
		execution.ResponseHeaders,
		execution.ResponseBody,
		execution.ErrorMessage,
	).Scan(
		&execution.ID,
		&execution.ExecutedAt,
	)
}

// GetByID retrieves one execution by its ID
func (r *ExecutionRepository) GetByID(ctx context.Context, id int) (*models.Execution, error) {
	query := `
		SELECT
			id,
			endpoint_id,
			executed_at,
			status_code,
			response_time,
			response_headers,
			response_body,
			error_message
		FROM executions
		WHERE id = $1
	`

	var execution models.Execution

	err := r.db.QueryRowContext(ctx, query, id).Scan(
		&execution.ID,
		&execution.EndpointID,
		&execution.ExecutedAt,
		&execution.StatusCode,
		&execution.ResponseTime,
		&execution.ResponseHeaders,
		&execution.ResponseBody,
		&execution.ErrorMessage,
	)

	if err != nil {
		return nil, err
	}

	return &execution, nil
}

// GetByEndpointID retrieves all executions belonging to an endpoint
func (r *ExecutionRepository) GetByEndpointID(ctx context.Context, endpointID int) ([]models.Execution, error) {
	query := `
		SELECT
			id,
			endpoint_id,
			executed_at,
			status_code,
			response_time,
			response_headers,
			response_body,
			error_message
		FROM executions
		WHERE endpoint_id = $1
		ORDER BY executed_at DESC
	`

	rows, err := r.db.QueryContext(ctx, query, endpointID)
	if err != nil {
		return nil, err
	}

	defer rows.Close()

	//start with an empty slice so the API returns [] when no history exists
	executions := make([]models.Execution, 0)

	for rows.Next() {
		var execution models.Execution

		if err := rows.Scan(
			&execution.ID,
			&execution.EndpointID,
			&execution.ExecutedAt,
			&execution.StatusCode,
			&execution.ResponseTime,
			&execution.ResponseHeaders,
			&execution.ResponseBody,
			&execution.ErrorMessage,
		); err != nil {
			return nil, err
		}

		executions = append(executions, execution)
	}

	if err := rows.Err(); err != nil {
		return nil, err
	}

	return executions, nil
}
