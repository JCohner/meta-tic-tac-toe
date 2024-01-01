SHELL:=/bin/bash
VERSION=0x03

.PHONY: gen_grpc
gen_grpc:
	@python3 -m grpc_tools.protoc -I. --python_out=. --pyi_out=. --grpc_python_out=. remote_calls/game.proto

.PHONY: run
run:
	@source bin/activate && python3 tictac/main.py

.PHONY: run_server
run_server:
	@source bin/activate &&python3 tictac/server.py

.PHONY: run_client
run_client:
	@source bin/activate &&python3 tictac/client.py

.PHONY: test
test:
	@pytest-3 tests/test_*.py

.PHONY: update_tictac
update_tictac:
	@cd tictac && pip install ..

# TODO
.PHONY: flake8
flake8:
	@python3 -m flake8 || true
