ENVRUN = pipenv run

install:
	@pipenv install

install-dev:
	@pipenv install --dev -e .

shell:
	@pipenv shell

format:
	@$(ENVRUN) black --py36 -l 88 -S gibica tests

lint:
	@$(ENVRUN) flake8 gibica tests

type:
	@$(ENVRUN) mypy gibica

test:
	@$(ENVRUN) py.test

.PHONY: install install-dev shell format lint mypy test
