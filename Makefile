ENVRUN = pipenv run

build:
	@$(ENVRUN) python setup.py sdist bdist_wheel

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
	@sphinx-apidoc -M -f -o docs gibica

clean-docs:
	@$(MAKE) clean -C ./docs

docs: generate-docs
	@$(MAKE) html -C ./docs

upload-test: build
	@$(ENVRUN) twine upload --repository-url https://test.pypi.org/legacy/ dist/*

upload: build
	@$(ENVRUN) twine upload dist/*

clean:
	@rm -Rf dist build

.PHONY: install install-dev shell format lint mypy tests docs
