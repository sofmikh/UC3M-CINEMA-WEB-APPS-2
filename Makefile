# Detect virtual environment directory (venv_mac or venv)
VENV ?= $(shell [ -d venv_mac ] && echo venv_mac || echo venv)
PYTHON  = $(VENV)/bin/python
PIP     = $(VENV)/bin/pip
FLASK   = $(VENV)/bin/flask
APP     = cinema

.PHONY: all install run clean clean-all help

## Default target: run the application
all: run

## Install dependencies in virtual environment
install:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

## Run the Flask development server in debug mode
run:
	$(PYTHON) -m flask --debug --app=$(APP) run

## Remove generated files (bytecode caches, local SQLite database)
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf instance/cinema.db
	rm -rf instance/
	@echo "Clean completed."

## Remove virtual environments and perform full cleanup
clean-all: clean
	rm -rf $(VENV) venv_mac venv .venv
	@echo "Virtual environments removed. Run 'make install' to recreate."

## Display available targets
help:
	@echo ""
	@echo "Available commands:"
	@echo "  make install    Create venv and install dependencies"
	@echo "  make run        Run Flask development server"
	@echo "  make clean      Remove Python cache and local database"
	@echo "  make clean-all  Remove all generated files and virtual environments"
	@echo ""
