.DEFAULT_GOAL := help
SHELL = bash


.PHONY: help
help: ## show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: install
install: ## install dependencies
	poetry install --with local
	poetry run pre-commit install

.PHONY: isort
isort:
	poetry run isort . ${OPTIONS}

.PHONY: black
black:
	poetry run black . ${OPTIONS}

.PHONY: flake8
flake8:
	poetry run flake8 . ${OPTIONS}

.PHONY: lint
lint: isort black flake8 ## lint code
