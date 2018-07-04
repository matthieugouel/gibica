# Gibica

[![Build Status](https://travis-ci.org/matthieugouel/gibica.svg?branch=master)](https://travis-ci.org/matthieugouel/gibica)
[![Coverage Status](https://img.shields.io/coveralls/github/matthieugouel/gibica.svg)](https://coveralls.io/github/matthieugouel/gibica?branch=master)
[![license](https://img.shields.io/github/license/matthieugouel/gibica.svg)](https://github.com/matthieugouel/gibica/blob/master/LICENSE)
[![Documentation Status](https://readthedocs.org/projects/gibica/badge/?version=latest)](http://gibica.readthedocs.io/en/latest/?badge=latest)

> Interprète ? Interprète ? Cuillère ! -- King of Burgundy (Kaamelott).

## Installation

You can install the package from sources after cloning the project and navigating into the project directory.

This project uses `pipenv` as a package manager.

```
pipenv install
```

Then activate the project's virtualenv with the following command.

```
pipenv shell
```

## Usage

After have installed the software, you can run it as a CLI program with your Gibica script file as an argument.

```
gibica script.gbc
```

For more information, you can display the help.

```
gibica --help
```

## Contributing

See [CONTRIBUTING](CONTRIBUTING.md) for more information about how to contribute to this project.

## Credits

This project was initially born by the reading of the amazing series of articles [Let’s Build A Simple Interpreter](https://ruslanspivak.com/lsbasi-part1/) written by Ruslan Spivak.
