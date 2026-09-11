package database

import (
	"database/sql"
	"os"

	"github.com/joho/godotenv"

	_ "github.com/jackc/pgx/v5/stdlib"
)

func GetConnection() (*sql.DB, error) {
	// load the existing Chimera database configuration
	if err := godotenv.Load("../python/.env"); err != nil {
		return nil, err
	}

	// build the PostgreSQL connection string from environment variables
	dsn := "host=" + os.Getenv("DB_HOST") +
		" port=" + os.Getenv("DB_PORT") +
		" dbname=" + os.Getenv("DB_NAME") +
		" user=" + os.Getenv("DB_USER") +
		" password=" + os.Getenv("DB_PASSWORD")

	// create the database handle without opening a connection yet
	return sql.Open("pgx", dsn)
}
