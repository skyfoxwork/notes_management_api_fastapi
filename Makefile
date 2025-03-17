# indent must be a tab not a space

# Specify that commands do not require reprocessing of the file
.PHONY: run test lint migrate upgrade downgrade

# Run FastAPI app
run:
	uvicorn src.main:app --reload
# 	uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

# check code with flake8
lint:
	flake8

# install Python modules
install:
	pip install -r requirements.txt

# Run Alembic migrations
migrate:
	alembic revision --autogenerate
# 	alembic revision --autogenerate -m "New migration"

# upgrade database schemas
upgrade:
	alembic upgrade head
