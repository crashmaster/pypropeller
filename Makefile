PACKAGE := pypropeller

PYTHON3 := env python3

THIS_FILE := $(abspath $(lastword $(MAKEFILE_LIST)))
REPO_DIR := $(patsubst %/,%,$(dir $(THIS_FILE)))
TEST_DIR := $(REPO_DIR)/$(PACKAGE)/test
PACKAGE_DIR := $(REPO_DIR)/build

RUN_TESTS := PYTHONPATH=$(REPO_DIR)/pypropeller $(PYTHON3) $(TEST_DIR)/test_pypropeller.py

.PHONY: all test build

all: test

test:
	@$(RUN_TESTS)

build:
	@$(PYTHON3) setup.py --quiet sdist --dist-dir $(PACKAGE_DIR)
	@find $(PACKAGE_DIR) -name '*.tar.gz'
