==================
Grammar
==================

This is the current grammar of the Gibica language.

::

    program: (statement)*

    compound_statement: LBRACKET statement RBRACKET

    statement: declaration_statement
             | expression_statement
             | if_statement

    declaration_statement: LET assignment SEMI

    expression_statement: assignment SEMI

    assignment : variable ASSIGN logical_or_expr

    variable: [MUT] ID

    if_statement: IF logical_or_expr compound_statement
                (ELSE IF local_or_expr compound_statement)*
                [ELSE compound_statement]

    logical_or_expr: logical_and_expr (OR logical_and_expr)*

    logical_and_expr: logical_not_expr (AND logical_not_expr)*

    logical_not_expr: NOT logical_not_expr
                    | comparison

    comparison: expr ((EQ | NE | LE | GE | LT | GT) expr)*

    expr: term ((PLUS | MINUS) term)*

    term: factor ((MUL | DIV | INT_DIV) factor)*

    factor: PLUS factor
          | MINUS factor
          | INT_NUMBER
          | FLOAT_NUMBER
          | LPAREN logical_or_expr RPAREN
          | TRUE
          | FALSE
          | variable
