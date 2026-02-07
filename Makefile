.PHONY: setup run db-start db-stop db-shell clean install logs

# Setup: Install dependencies and start database
setup: install db-start
	@echo "Setup complete! Run 'make run' to start the backend."

# Install Python dependencies
install:
	cd backend && pip install -r requirements.txt

# Start PostgreSQL
db-start:
	docker-compose up -d db
	@echo "Waiting for PostgreSQL to be ready..."
	@sleep 3
	@echo "PostgreSQL is running on localhost:5432"

# Stop PostgreSQL
db-stop:
	docker-compose down

# Open PostgreSQL shell
db-shell:
	docker exec -it crm_postgres psql -U crmuser -d crm_db

# Start backend server
run:
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# View logs
logs:
	docker-compose logs -f db

# Clean up everything
clean:
	docker-compose down -v
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Start pgAdmin (database GUI)
pgadmin:
	docker-compose up -d pgadmin
	@echo "pgAdmin is running at http://localhost:5050"
	@echo "Email: admin@crm.local | Password: admin"
