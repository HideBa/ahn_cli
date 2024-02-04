PACKAGE_DIR := ahn_cli

.PHONY: install
install:
	poetry install

.PHONY: update
update:
	poetry update

.PHONY: lint
lint:
	poetry run flake8 $(PACKAGE_DIR)

.PHONY: type
type:
	poetry run mypy $(PACKAGE_DIR)/**/*.py

.PHONY: format
format:
	poetry run black $(PACKAGE_DIR)/**/*.py

.PHONY: sort
sort:
	poetry run isort $(PACKAGE_DIR)/**/*.py

.PHONY: test
test:
	poetry run pytest $(PACKAGE_DIR)/**/*.py

.PHONY: check
check: lint type test	format sort

.PHONY: run
run:
	poetry run ahn_cli $(ARGS)
