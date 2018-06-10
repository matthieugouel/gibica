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

    term: factor ((MUL | DIV | INT_DIV) factor)*

    factor: PLUS factor
          | MINUS factor
          | INT_NUMBER
          | FLOAT_NUMBER
          | LPAREN expr RPAREN
          | variable
