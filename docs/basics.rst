==================
Main features
==================

Overview
--------

* Like many programming languages, Gibica impose the semicolon at the end of expressions.

::

    print(1);

* You can write comments in your programs. Comments are code that will be ignored during the interpretation.
  To do that, just put the character **#** before your comment.

::

    # This is a comment !

    print(1); # Here is an other.

Variable and mutability
-----------------------

Gibica uses the dynamic type feature from Python so you don't have to declare explicitly the type of your variables.
Let's declare a first variable with an integer number.

::

    let integer = 1;


By default, all Gibica variables are *immutables*. Yes it seems tough but in fact it protects from many surprises.

I admit that not be able to use mutability on variables can be very unconveniant, so it's possible to explicitly enable the mutabily of a variable at the declaration with the keyword **mut**.

::

    let mut interger = 1;
    integer = integer + 1;

There is currently three implicit types in the Gibica implementation.

**Integer type**

::

    let integer = 10;

**FLoat type**

::

    let float = 1.0;

**Boolean type**

::

    let boolean1 = true;
    let boolean2 = false;


Control flow
------------

For now Gibica provides two types of control flows.

**conditional statement**

::

    let mut result = 0;
    let i = 5;
    if i <= 4 {
        result = 1;
    } else if i == 5  {
        result = 2;
    }
    else {
        result = 3;
    }


**loop statement**

::

    let i = 0;
    while i < 5 {
        i = i + 1;
    }

Functions
---------

Here is a basic example of a function declaration.

::

    def add(a, b) {
        return a + b;
    }

    let result = add(1, 1);


Moreover, you can specify the mutability nature of a parameter.

::

    def increment(mut n) {
        n = n + 1;
        return n;
    }

    let result = increment(1);
