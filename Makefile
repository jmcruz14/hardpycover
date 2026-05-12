.PHONY: start-venv debug

VENV = .venv

start-venv:
	source $(VENV)/bin/activate && echo "Virtual environment started!"

debug: start-venv
	uv run main.py