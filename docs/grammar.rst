==================
Grammar
==================

This is the current grammar of the Gibica language.

::

    program: (statement SEMI)*

    statement: assignment_statement

    assignment_statement : variable ASSIGN expr

    variable: ID

    expr: term ((PLUS | MINUS) term)*

    factor:  factor ((MUL | DIV | INT_DIV) factor)*

    term: (PLUS | MINUS) INTEGER | INTEGER | LPAREN expr RPAREN
