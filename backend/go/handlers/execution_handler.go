package handlers

import (
	"encoding/json"
	"log"
	"net/http"
	"strconv"
	"strings"

	"chimera-go/models"
	"chimera-go/repositories"
)

type ExecutionHandler struct {
	repo *repositories.ExecutionRepository
}

// NewExecutionHandler creates a handler backed by the execution repository
func NewExecutionHandler(repo *repositories.ExecutionRepository) *ExecutionHandler {
	return &ExecutionHandler{
		repo: repo,
	}
}

// CreateExecution handles POST /executions
func (h *ExecutionHandler) CreateExecution(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var execution models.Execution

	if err := json.NewDecoder(r.Body).Decode(&execution); err != nil {
		http.Error(w, "invalid execution payload", http.StatusBadRequest)
		return
	}

	if execution.EndpointID == 0 {
		http.Error(w, "endpoint_id is required", http.StatusBadRequest)
		return
	}

	if err := h.repo.Create(r.Context(), &execution); err != nil {
		log.Println("execution persistence failed:", err)
		http.Error(w, "failed to persist execution", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusCreated)

	if err := json.NewEncoder(w).Encode(execution); err != nil {
		log.Println("failed to encode execution response:", err)
	}
}

// GetExecutionsByEndpoint handles GET /executions/endpoint/{endpoint_id}
func (h *ExecutionHandler) GetExecutionsByEndpoint(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
		return
	}

	endpointIDText := strings.TrimPrefix(r.URL.Path, "/executions/endpoint/")

	endpointID, err := strconv.Atoi(endpointIDText)
	if err != nil || endpointID <= 0 {
		http.Error(w, "invalid endpoint_id", http.StatusBadRequest)
		return
	}

	executions, err := h.repo.GetByEndpointID(r.Context(), endpointID)
	if err != nil {
		log.Println("execution history retrieval failed:", err)
		http.Error(w, "failed to retrieve execution history", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")

	if err := json.NewEncoder(w).Encode(executions); err != nil {
		log.Println("failed to encode execution history:", err)
	}
}
