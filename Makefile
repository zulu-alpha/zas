build:
	@make build-lib-environment

build-lib-environment:
	@docker buildx build -t lib.environment lib/environment/.

test-lib-environment:
	@docker run lib.environment pytest

pre-commit-lib-environment:
	@pre-commit run lib-environment-black -a
	@pre-commit run lib-environment-flake8 -a
	@pre-commit run lib-environment-mypy -a