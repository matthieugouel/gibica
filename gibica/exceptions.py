"""Exceptions module."""


class LexicalError(Exception):
    """Lexical error."""

    pass


class SyntaxError(Exception):
    """Syntax error."""

    pass


class SementicError(Exception):
    """Sementic error."""

    pass


class ObjectError(Exception):
    """Object error."""

    pass


class TypeError(Exception):
    """Type error."""

    pass


class InterpreterError(Exception):
    """Interpreter error."""

    pass
