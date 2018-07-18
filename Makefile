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

tests:
	@$(ENVRUN) py.test

generate-docs:
	@sphinx-apidoc -M -f -o docs gibica

clean-docs:
	@$(MAKE) clean -C ./docs

docs: generate-docs
	@$(MAKE) html -C ./docs

.PHONY: install install-dev shell format lint mypy tests docs
