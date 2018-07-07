==================
Grammar
==================

This is the current grammar of the Gibica language.

::

    program: (statement)*

    statement: function_declaration
             | variable_declaration
             | expression_statement
             | if_statement
             | while_statement
             | jump_statement

    function_declaration: DEF ID parameters compound

    parameters: LPAREN [[MUT] ID] (COMMA [MUT] ID)* RPAREN

    function_body: LBRACKET (statement)* RBRACKET

    variable_declaration: LET assignment SEMI

    expression_statement: assignment SEMI

    assignment: logical_or_expr [ASSIGN logical_or_expr]

    if_statement: IF logical_or_expr compound
                (ELSE IF local_or_expr compound)*
                [ELSE compound]

    while_statement: WHILE local_or_expr compound

    compound: LBRACKET (statement)* RBRACKET

    jump_statement: RETURN expression_statement

    logical_or_expr: logical_and_expr (OR logical_and_expr)*

    logical_and_expr: logical_not_expr (AND logical_not_expr)*

    logical_not_expr: NOT logical_not_expr
                    | comparison

    comparison: expr ((EQ | NE | LE | GE | LT | GT) expr)*

    expr: term ((PLUS | MINUS) term)*

    term: atom ((MUL | DIV | INT_DIV) atom)*

    call: [MUT] ID [LPAREN parameters RPAREN]

    atom: PLUS atom
        | MINUS atom
        | call
        | INT_NUMBER
        | FLOAT_NUMBER
        | LPAREN logical_or_expr RPAREN
        | TRUE
        | FALSE
