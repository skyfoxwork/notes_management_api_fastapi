# indent must be a tab not a space

# Specify that commands do not require reprocessing of the file
.PHONY: run test lint migrate upgrade downgrade

# Run FastAPI app
run:
	uvicorn src.main:app --reload

run-hp:
	uvicorn src.main:app --host 0.0.0.0 --port 8000

# Run test (pytest)
test:
	python3 -m pytest

# check code with flake8
lint:
	flake8

# install Python modules
install:
	pip install -r requirements.txt

# Run Alembic migrations
migrate:
	alembic revision --autogenerate

# upgrade database schemas
upgrade:
	alembic upgrade head

# Rollback of last meetings
downgrade:
	alembic downgrade -1

# Building and running Docker containers
docker-up:
	docker-compose up --build

docker-up-bg:
	docker-compose up --build -d

# Stopping containers
docker-down:
	docker-compose down
