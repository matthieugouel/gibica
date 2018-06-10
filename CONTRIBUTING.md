# Contributing

Thanks for contributing ! Here is some guidelines to make your life easier during the development process.

## Installation

Note : The use of a virtual environment is heavily recommended.

For development purposes, you can install the package in editable mode with the development requirements.

```
pip install -e . -r requirements-dev.txt
```

## Debug mode


You can launch Gibica in debug mode to see internal components.

```
gibica script.gbc --debug
```

## Syntax checking

You can check the syntax using flake8 :

```
flake8 gibica
```

You can also use tox :

```
tox -e lint
```

## Test coverage

You can run the coverage with the following command :

```
coverage run --source gibica -m py.test
```

You can also use tox :

```
tox -e test
```

## Type checking

You use annotation to do static type checking with mypy :

```
mypy gibica
```

You can also use tox :

```
tox -e type
```

## Documentation

The documentation of the project can be found under the directory `./doc/_build/html`.

To rebuild the configuration, you can use the makefile (or the make.bat for Windows users) :

```
cd docs/
make clean
sphinx-apidoc -F -P -o . ../gibica
make html
```

## Version bumping

To update the version of the project, just run the following command according to the nature of the change.

```
bumversion [ major | minor | patch ]
```
