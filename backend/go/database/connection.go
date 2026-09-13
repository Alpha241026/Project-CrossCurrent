package database

import (
	"database/sql"
	"os"

	"github.com/joho/godotenv"

	_ "github.com/jackc/pgx/v5/stdlib"
)

func GetConnection() (*sql.DB, error) {
	// Load local environment variables when running the project locally.
	// In production, Render provides environment variables directly.
	_ = godotenv.Load("../python/.env")

	databaseURL := os.Getenv("DATABASE_URL")

	if databaseURL != "" {
		return sql.Open("pgx", databaseURL)
	}

	dsn := "host=" + os.Getenv("DB_HOST") +
		" port=" + os.Getenv("DB_PORT") +
		" dbname=" + os.Getenv("DB_NAME") +
		" user=" + os.Getenv("DB_USER") +
		" password=" + os.Getenv("DB_PASSWORD")

	return sql.Open("pgx", dsn)
}
