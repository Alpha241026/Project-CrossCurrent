package main

import (
	"log"
	"net/http"
	"os"

	"crosscurrent-go/database"
	"crosscurrent-go/handlers"
	"crosscurrent-go/repositories"
)

func main() {
	// create the database handle using CrossCurrent's existing configuration
	db, err := database.GetConnection()
	if err != nil {
		log.Fatal("database connection setup failed:", err)
	}

	defer db.Close()

	// verify that Go can reach the PostgreSQL server
	if err := db.Ping(); err != nil {
		log.Fatal("database ping failed:", err)
	}

	log.Println("Go → PostgreSQL connection successful.")

	executionRepo := repositories.NewExecutionRepository(db)
	executionHandler := handlers.NewExecutionHandler(executionRepo)

	http.HandleFunc("/executions", executionHandler.CreateExecution)
	http.HandleFunc("/executions/endpoint/", executionHandler.GetExecutionsByEndpoint)

	http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		w.Write([]byte(`{"status":"ok"}`))
	})

	port := os.Getenv("PORT")

	if port == "" {
		port = "8080"
	}

	log.Println("Go execution service listening on :" + port)

	if err := http.ListenAndServe(":"+port, nil); err != nil {
		log.Fatal("Go execution service failed:", err)
	}
}
