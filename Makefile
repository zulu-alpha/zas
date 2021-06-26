build:
	@make build-lib-environment

build-lib-environment:
	@docker build -t lib.environment lib/environment/.

test-lib-environment:
	@docker run lib.environment pytest
