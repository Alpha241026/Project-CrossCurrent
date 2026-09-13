package main

import (
	"log"
	"net/http"

	"chimera-go/database"
	"chimera-go/handlers"
	"chimera-go/repositories"
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

	log.Println("Go execution service listening on :8080")

	if err := http.ListenAndServe(":8080", nil); err != nil {
		log.Fatal("Go execution service failed:", err)
	}
}
