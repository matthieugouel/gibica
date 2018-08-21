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

test:
	@$(ENVRUN) py.test --cov=gibica --cov-report term-missing -vs --cov-fail-under=80

generate-doc:
	@$(ENVRUN) sphinx-apidoc -M -f -o docs gibica

doc: generate-doc
	@$(MAKE) html -C ./docs

build: docs
	@$(ENVRUN) python setup.py sdist bdist_wheel

upload-test: build
	@$(ENVRUN) twine upload --repository-url https://test.pypi.org/legacy/ dist/*

upload: build
	@$(ENVRUN) twine upload dist/*

clean-doc:
	@$(MAKE) clean -C ./docs > /dev/null

clean: clean-doc
	@rm -Rf dist build

.PHONY: install install-dev shell format lint mypy test doc
