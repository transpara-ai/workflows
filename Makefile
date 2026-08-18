.DEFAULT_GOAL := verify

PYTHON ?= python3

.PHONY: verify

verify:
	git diff --check
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) scripts/verify_tlc46_public_control_plane.py
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m unittest -v tests/test_tlc46_public_control_plane.py
