"""Entrypoint of the interpreter."""

import click

from gibica.lexer import Lexer
from gibica.parser import Parser
from gibica.interpreter import Interpreter


#
# Main
#


@click.command()
@click.argument(
    'filepath'
)
@click.option(
    '--debug',
    'in_debug_mode',
    is_flag=True,
    help='Run in debug mode.'
)
def main(filepath, in_debug_mode):
    """Gibica Interpreter."""

    with open(filepath) as file:

        # Lexical analysis instantiation
        lexer = Lexer(file.read())

        # Syntax analysis instantiation
        parser = Parser(lexer)

        # Interpreter instantiation
        interpreter = Interpreter(parser)

        # Program evaluation
        result = interpreter.interpret()

        # Display the output if it's an evaluation
        if result:
            click.echo(result)

        # Display internal variables if debug option enabled
        if in_debug_mode:
            click.echo(f'GLOBAL_SCOPE: {interpreter.GLOBAL_SCOPE}')


if __name__ == '__main__':
    main()
