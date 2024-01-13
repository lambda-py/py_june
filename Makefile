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
