"""Entrypoint of the interpreter."""

import click

from gibica.lexer import Lexer
from gibica.parser import Parser
from gibica.interpreter import Interpreter


#
# Main
#

def evaluate(raw):
    """Process the raw input."""

    # Lexical analysis
    lexer = Lexer(raw)

    # Syntax analysis
    parser = Parser(lexer)

    # Program evaluation
    intepreter = Interpreter(parser)

    # Return the output
    return intepreter.interpret()


@click.command()
@click.argument('filepath')
def main(filepath):
    """Gibica Interpreter."""

    if not filepath:

        # Live interpreter
        while True:

            # Get the raw input
            try:
                raw = input('>>> ')
            except EOFError:
                break

            if not raw:
                continue

            # Print the result
            print(evaluate(raw))

    else:

        # Evaluate the code provided as a file
        with open(filepath) as file:
            print(evaluate(file.read()))


if __name__ == '__main__':
    main()
