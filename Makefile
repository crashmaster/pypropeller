PACKAGE := pypropeller

PYTHON2 := env python2
PYTHON3 := env python3

THIS_FILE := $(abspath $(lastword $(MAKEFILE_LIST)))
REPO_DIR := $(patsubst %/,%,$(dir $(THIS_FILE)))
TEST_DIR := $(REPO_DIR)/$(PACKAGE)/test
PACKAGE_DIR := $(REPO_DIR)/build

RUN_TESTS_PY2 := PYTHONPATH=$(REPO_DIR)/pypropeller $(PYTHON2) $(TEST_DIR)/test_pypropeller.py
RUN_TESTS_PY3 := PYTHONPATH=$(REPO_DIR)/pypropeller $(PYTHON3) $(TEST_DIR)/test_pypropeller.py

.PHONY: all test2 test3 test build

all: test

test2:
	@echo "Smoke tests with Python2"
	@echo -e "------------------------\n"
	@$(RUN_TESTS_PY3)

test3:
	@echo "Smoke tests with Python3"
	@echo -e "------------------------\n"
	@$(RUN_TESTS_PY3)

test: test2 test3

build:
	@$(PYTHON3) setup.py --quiet sdist --dist-dir $(PACKAGE_DIR)
	@find $(PACKAGE_DIR) -name '*.tar.gz'
