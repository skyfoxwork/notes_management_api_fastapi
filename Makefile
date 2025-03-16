# indent must be a tab not a space

# Specify that commands do not require reprocessing of the file
.PHONY: run test lint migrate upgrade downgrade

# Run FastAPI app
run:
	uvicorn src.main:app --reload

# check code with flake8
lint:
	flake8

# install Python modules
install:
	pip install -r requirements.txt
