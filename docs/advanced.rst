==================
Advanced usage
==================

Grammar
--------

This is the current grammar of the Gibica language.

::

    program: (statement)*

    statement: function_declaration
             | variable_declaration
             | expression_statement
             | if_statement
             | while_statement
             | jump_statement

    function_declaration: 'def' ID parameters compound

    parameters: '(' logical_or_expr (',' logical_or_expr)* ')'

    function_body: '{' (statement)* '}'

    variable_declaration: 'let' assignment ';'

    expression_statement: assignment ';'

    assignment: logical_or_expr ['=' logical_or_expr]

    if_statement: 'if' logical_or_expr compound
                ('else' 'if' local_or_expr compound)*
                ['else' compound]

    while_statement: 'while' local_or_expr compound

    compound: '{' (statement)* '}'

    jump_statement: 'return' expression_statement

    logical_or_expr: logical_and_expr ('or' logical_and_expr)*

    logical_and_expr: logical_not_expr ('and' logical_not_expr)*

    logical_not_expr: 'not' logical_not_expr
                    | comparison

    comparison: expr (('==' | '!=' | '<=' | '>=' | '<' | '>') expr)*

    expr: term (('+' | '-') term)*

    term: atom (('*' | '/' | '//') atom)*

    call: ['mut'] ID ['(' parameters ')']

    atom: '+' atom
        | '-' atom
        | call
        | INT_NUMBER
        | FLOAT_NUMBER
        | '(' logical_or_expr ')'
        | TRUE
        | FALSE

Package content
---------------

.. include:: modules.rst
