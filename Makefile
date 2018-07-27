ENVRUN = pipenv run

install:
	@pipenv install --three

install-dev:
	@pipenv install --three --dev -e .

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
	@$(ENVRUN) sphinx-apidoc -M -f -o docs gibica

docs: generate-docs
	@$(MAKE) html -C ./docs

build: docs
	@$(ENVRUN) python setup.py sdist bdist_wheel

upload-test: build
	@$(ENVRUN) twine upload --repository-url https://test.pypi.org/legacy/ dist/*

upload: build
	@$(ENVRUN) twine upload dist/*

clean-docs:
	@$(MAKE) clean -C ./docs > /dev/null

clean: clean-docs
	@rm -Rf dist build

.PHONY: install install-dev shell format lint mypy tests docs
