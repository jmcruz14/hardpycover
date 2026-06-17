.PHONY: start-venv debug

VENV = .venv

ifneq (,$(wildcard .env))
	include .env
	export
endif

start-venv:
	source $(VENV)/bin/activate && echo "Virtual environment started!"

debug: start-venv
	uv run main.py

run-test:
	uv run pytest --cov=hardpycover . -vvv

update-schema:
	python3 -m sgqlc.introspection \
		--exclude-deprecated \
		--exclude-description \
		-H "Authorization: Bearer ${BEARER_TOKEN}" \
		https://api.hardcover.app/v1/graphql \
		hardcover_schema.json
	sgqlc-codegen schema hardcover_schema.json hardpycover/schema.py

