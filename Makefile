start:
	@docker-compose up

test:
	@docker-compose run --rm api1 pytest --cov --cov-report term-missing --cov-fail-under 90 --disable-pytest-warnings
