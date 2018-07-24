# Contributing

Thanks for contributing ! Here is some guidelines to make your life easier during the development process.

## Installation

First you need to download the sources of the project from Github.

```
git clone https://github.com/matthieugouel/gibica
```

For development purposes, you can install the package in editable mode with the development requirements. Note: this project uses `pipenv` as a package manager.

```
make install-dev
```

Then, enter in the virual environment.

```
make shell
```

## Debug mode


You can launch Gibica in debug mode to see internal components.

```
gibica script.gbc --debug
```

## Syntax checking

You can check the syntax using flake8 :

```
make lint
```

## Type checking

If you used annotations to do static Python type checking with mypy :

```
make type
```

## Test coverage

You can run the coverage with the following command :

```
make tests
```

## Documentation

The documentation of the project can be found under the directory `./doc/_build/html`.

To rebuild the configuration, you can use the following command :

```
make docs
```

## Version bumping

To update the version of the project, just run the following command according to the nature of the change.

```
bumpversion [ major | minor | patch ]
```
