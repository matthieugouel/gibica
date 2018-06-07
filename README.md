# Gibica

[![Build Status](https://travis-ci.org/matthieugouel/gibica.svg?branch=master)](https://travis-ci.org/matthieugouel/gibica)
[![Coverage Status](https://img.shields.io/coveralls/github/matthieugouel/gibica.svg)](https://coveralls.io/github/matthieugouel/gibica?branch=master)
[![license](https://img.shields.io/github/license/matthieugouel/gibica.svg)](https://github.com/matthieugouel/gibica/blob/master/LICENSE)
[![Documentation Status](https://readthedocs.org/projects/gibica/badge/?version=latest)](http://gibica.readthedocs.io/en/latest/?badge=latest)

> Interprète ? Interprète ? Cuillère ! -- King of Burgundy (Kaamelott).

## Installation

Note : The use of a virtual environment is heavily recommended.

If you want to install the package :

```bash
pip install .
```

For development purposes, you can install the package in editable mode with the dev requirements.

```bash
pip install -e . -r requirements-dev.txt
```

## Syntax checking

You can check the syntax using flake8 :

```bash
flake8 gibica
```

You can also use tox :

```bash
tox -e lint
```

## Test coverage

You can run the coverage with the following command :

```bash
coverage run --source gibica -m py.test
```

You can also use tox :

```bash
tox -e test
```

## Type checking

You use annotation to do static type checking with mypy :

```bash
mypy gibica
```

You can also use tox :

```
tox -e type
```

## Documentation

The documentation of the project can be found under the directory `./doc/_build/html`.

To rebuild the configuration, you can use the makefile (or the make.bat for Windows users) :

```bash
$ cd docs/
$ make clean
$ sphinx-apidoc -F -P -o . ../gibica
$ make html
```

## Version bumping

When you are satisfied with your code and you want to bump a version, just run the command :

```bash
bumversion [ major | minor | patch ]
```
