==================
Grammar
==================

This is the current grammar of the Gibica language.

::

    program: (statement)*

    statement: function_definition
             | declaration_statement
             | assignment_statement
             | expression_statement
             | if_statement
             | while_statement
             | jump_statement

    function_definition: DEF atom parameters compound

    parameters: LPAREN [variable] (COMMA variable)* RPAREN

    compound: LBRACKET (statement)* RBRACKET

    declaration_statement: LET assignment SEMI

    assignment_statement: assignment SEMI

    assignment: variable ASSIGN logical_or_expr

    variable: [MUT] atom

    atom: ID

    expression_statement: logical_or_expr SEMI

    if_statement: IF logical_or_expr compound
                (ELSE IF local_or_expr compound)*
                [ELSE compound]

    while_statement: WHILE local_or_expr compound

    jump_statement: RETURN expression_statement

    logical_or_expr: logical_and_expr (OR logical_and_expr)*

    logical_and_expr: logical_not_expr (AND logical_not_expr)*

    logical_not_expr: NOT logical_not_expr
                    | comparison

    comparison: expr ((EQ | NE | LE | GE | LT | GT) expr)*

    expr: term ((PLUS | MINUS) term)*

    term: factor ((MUL | DIV | INT_DIV) factor)*

    call: atom [LPAREN parameters RPAREN]

    factor: PLUS factor
          | MINUS factor
          | call
          | INT_NUMBER
          | FLOAT_NUMBER
          | LPAREN logical_or_expr RPAREN
          | TRUE
          | FALSE
