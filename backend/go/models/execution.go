package models

import (
	"encoding/json"
	"time"
)

type Execution struct {
	ID              int             `json:"id"`
	EndpointID      int             `json:"endpoint_id"`
	ExecutedAt      time.Time       `json:"executed_at"`
	StatusCode      *int            `json:"status_code,omitempty"`
	ResponseTime    *int            `json:"response_time,omitempty"`
	ResponseHeaders json.RawMessage `json:"response_headers"`
	ResponseBody    json.RawMessage `json:"response_body"`
	ErrorMessage    *string         `json:"error_message,omitempty"`
}
