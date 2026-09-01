.DEFAULT_GOAL := verify

PYTHON ?= python3

.PHONY: verify

verify:
	git diff --check
	git diff --cached --check
