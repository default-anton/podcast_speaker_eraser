PYTHON_FILES_DIR := ./src
PYTHON_FILES := main.py $(shell find $(PYTHON_FILES_DIR) -name "*.py")

# Define the commands for formatting
BLACK := black
ISORT := isort

.PHONY: format
format: black isort

.PHONY: black
black:
	$(BLACK) $(PYTHON_FILES)

.PHONY: isort
isort:
	$(ISORT) $(PYTHON_FILES)

.PHONY: check
check: check-black check-isort

.PHONY: check-black
check-black:
	$(BLACK) --check $(PYTHON_FILES)

.PHONY: check-isort
check-isort:
	$(ISORT) --check-only $(PYTHON_FILES)

.PHONY: help
help:
	@echo "Usage:"
	@echo "  make format      Format all Python files using black and isort"
	@echo "  make black       Format all Python files using black"
	@echo "  make isort       Format all Python files using isort"
	@echo "  make check       Check formatting of all Python files using black and isort"
	@echo "  make check-black Check formatting of all Python files using black"
	@echo "  make check-isort Check formatting of all Python files using isort"
