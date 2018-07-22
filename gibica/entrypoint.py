"""Entrypoint of the interpreter."""

import click

from gibica.lexer import Lexer
from gibica.parser import Parser
from gibica.sementic import SymbolTableBuilder
from gibica.interpreter import Interpreter


#
# Main
#


@click.command()
@click.argument('filepath')
@click.option('--debug', 'in_debug_mode', is_flag=True, help='Run in debug mode.')
def main(filepath, in_debug_mode):
    """Gibica Interpreter."""

    with open(filepath) as file:

        try:

            # Lexical analysis
            lexer = Lexer(file.read())

            # Syntax analysis
            parser = Parser(lexer)
            tree = parser.parse()

            # Sementic analysis
            symtab_builder = SymbolTableBuilder(tree)
            symtab_builder.build()

            # Program evaluation
            interpreter = Interpreter(tree)
            interpreter.interpret()

            # Display internal variables if debug option is enabled
            if in_debug_mode:
                print(f"SYMBOL TABLE: {symtab_builder.table}")
                print(f"GLOBAL MEMORY: {interpreter.memory}")

        except Exception as gibica_exception:

            # Display the full trace if debug option is enabled
            if in_debug_mode:
                raise

            # In classic mode, just display the interpreter trace
            else:
                print(f"{gibica_exception.__class__.__name__}: {gibica_exception}")


if __name__ == '__main__':
    main()
