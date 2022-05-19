check-all:
	python -m black --check pdf_renderer config.py tests
	python -m pylint pdf_renderer config.py tests
	python -m flake8 pdf_renderer config.py
	@echo "\033[0;32m === Check is OK === \033[0m"

fix:
	python -m black pdf_renderer config.py tests

test-with-cov:
	pytest --cov pdf_renderer --cov-report html tests

test:
	pytest tests

test-docker:
	# Run tests in docker
	docker-compose run pdf_renderer_api pipenv run make test

test-docker:
	# Create .env for testing in Docker
	cp .env.example .env
