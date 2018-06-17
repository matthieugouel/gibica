==================
Grammar
==================

This is the current grammar of the Gibica language.

::

    program: (statement)*

    statement: declaration_statement
             | expression_statement

    declaration_statement: var_type assignment SEMI

    var_type: INT
            | FLOAT
            | BOOL

    expression_statement: assignment SEMI

    assignment : variable ASSIGN comparison

    variable: [ MUT ] ID

    comparison: expr ((EQ | LE | GE | LT | GT) expr)*

    expr: term ((PLUS | MINUS) term)*

    term: factor ((MUL | DIV | INT_DIV) factor)*

    factor: PLUS factor
          | MINUS factor
          | INT_NUMBER
          | FLOAT_NUMBER
          | LPAREN expr RPAREN
          | TRUE
          | FALSE
          | variable
