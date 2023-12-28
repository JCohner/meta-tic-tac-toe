SHELL:=/bin/bash
VERSION=0x03

FTPUSER ?=joshc

.PHONY: gen_grpc
gen_grpc:
	@python3 -m grpc_tools.protoc -I. --python_out=. --pyi_out=. --grpc_python_out=. remote_calls/game.proto

.PHONY: run
run:
	@python3 main.py

.PHONY: flake8
flake8:
	@python3 -m flake8 || true

.PHONY: test
test:
	@source bin/activate && pytest tests/Test*.py