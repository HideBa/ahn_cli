PACKAGE_DIR := pget

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
	poetry run mypy $(PACKAGE_DIR)

.PHONY: format
format:
	poetry run black $(PACKAGE_DIR)/**/*.py

.PHONY: sort
sort:
	poetry run isort $(PACKAGE_DIR)/**/*.py

.PHONY: test
test:
	poetry run pytest $(PACKAGE_DIR)


run-app:
	poetry run python $(PACKAGE_DIR)/server/app.py
