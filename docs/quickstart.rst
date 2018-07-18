==================
Getting Started
==================

Installation
------------

Gibica is still a very young project. Hence, It's still on an early stage of development and doesn't have a proper release on Pypi.
So, in order to install it, you must do it like a boss with the sources. Don't worry it's easy !

First, get the latest version of sources from Github.

.. code-block:: shell

    git clone https://github.com/matthieugouel/gibica gibica

Now get into the sources directory and install the project inside a virtual environment.
This project uses `pipenv` to manage as a package manager so you must install it first. Then just install it with *make*.

.. code-block:: shell

    make install

Finally enter in the virual environment.

.. code-block:: shell

    make shell

That's it ! Now you have everything to build and run your Gibica programs.

Hello, numbers !
----------------

For now Gibica doesn't understand strings so we cannot actually write the traditionnal "Hello, world!" program.
Nonetheless, we can write a first piece of code that display a number. Pretty much the same right ?!

::

    display(1);

Yes that's it. You can save that super fancy program in a file named `hello.gbc` and execute it with the following command :

::

    gibica hello.gbc

if **1** is printed on you screen, congratulation ! You just written your first Gibica program !
