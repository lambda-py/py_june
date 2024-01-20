PHONY: isort
isort:
	isort .

.PHONY: isortcheck
isortcheck:
	@echo "Checking isort..."
	isort --diff --check-only .

.PHONY: black
black:
	black .

.PHONY: blackcheck
blackcheck:
	@echo "Checking black..."
	black --check .

.PHONY: pyformatcheck
pyformatcheck: isortcheck blackcheck

.PHONY: mypy
mypy:
	@echo "Checking mypy..."
	mypy .

.PHONY: lint
lint: pyformatcheck mypy

.PHONY: autofmt
autofmt: isort black

.PHONY: test
test:
	./scripts/test.sh

.PHONY: precommit
precommit: autofmt lint test

.PHONY: startdb
startdb:
	@echo "Starting postgres container..."
	@echo "Data will be stored in ./data"
	docker run --name postgres-container -e POSTGRES_PASSWORD=postgres -d -p 5432:5432 -v ./data:/var/lib/postgresql/data postgres:latest

.PHONY: setupdb
setupdb:
	@echo "Setting up database..."
	python manage.py migrate
	python manage.py loaddata categories.json

.PHONY: stopdb
stopdb:
	@echo "Stopping postgres container..."
	docker stop postgres-container
	docker rm postgres-container

.PHONY: dbshell
dbshell:
	@echo "Connecting to postgres container..."
	docker exec -it postgres-container psql -U postgres


