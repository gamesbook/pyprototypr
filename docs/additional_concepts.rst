===================
Additional Concepts
===================

This section assumes you are familiar with the concepts, terms and ideas
for **pyprototypr** as presented in `Basic Concepts <basic_concepts.rst>`_,
have looked through the `Core Shapes <core_shapes.rst>`_,
and that you have created one or two basic scripts on your own.

.. _table-of-contents:

Table of Contents
=================

-  `Names and Naming`_
-  `Strings (words and letters), Numbers and Booleans`_
-  `Calculations`_
-  `Case-sensitivity`_
-  `Quotes in Text`_
-  `Properties and Short-cuts`_
-  `Lists`_
-  `Errors`_

Names and Naming
================
`↑ <table-of-contents_>`_

Naming of things is supposed to be one of the harder aspects of programming!

If you work with the built-in commands and and their properties, the set
of names to use is already chosen for you. However, if you want to start
using some additional options, such as giving `Assigned names`_ to reuse
items in multiple places, then you need to be aware of the wider set of
so-called “reserved” names that are available as part of Python.

.. WARNING::
   If your assigned name is the same as a reserved name, then you’ll
   overwite it and your scripts may fail in very strange ways!

Basic built-in names include: False, None, True, and, as, assert, async,
await, break, class, continue, def, del, elif, else, except, finally,
for, from, global, if, import, in, is, lambda, nonlocal,
not, or, pass, raise, return, try, while, with, yield

Python also has a number of built-in functions, used to carry out common
operations.

Function names include: abs, aiter, all, anext, any, ascii, bin, bool,
breakpoint, bytearray, bytes, callable, chr, classmethod, compile,
complex, delattr, dict, dir, enumerate, eval, exec, filter, float,
format, frozenset, getattr, globals, hasattr, hash, help, hex, id,
input, int, isinstance, issubclass, iter, len, list, locals, map, max,
memoryview, min, next, object, oct, open, ord, pow, print, property,
range, repr, reversed, round, set, setattr, slice, sorted, staticmethod,
str, sum, super, tuple, type, vars, zip

If you’re interested in what all these functions do, there is a very
readable guide presented at:
https://www.mattlayman.com/blog/2024/layman-guide-python-built-in-functions/


Strings (words and letters), Numbers and Booleans
=================================================
`↑ <table-of-contents_>`_

**To Be Done**


Assigned Names
==============
`↑ <table-of-contents_>`_

**To Be Done**


Calculations
============
`↑ <table-of-contents_>`_

**To Be Done**


Case-sensitivity
================
`↑ <table-of-contents_>`_

**pyprototypr**, like Python, is case-sensitive - unlike some computer
languages (or, for example, file names that are used in Windows); so a
lowercase name is **NOT** the same as an uppercase version of it.

For example::

    Rectangle()

will create and draw a ``Rectangle`` shape on the page; but::

    area = rectangle()

will create a ``Rectangle`` shape, and store a reference to it in the
property called ``area`` (for use later on in the script) but will **not**
draw the Rectangle on the page.

Quotes in Text
==============
`↑ <table-of-contents_>`_

Using quotes inside a string of letters can be tricky.

If you have a Text shape, for example, like this::

   Text(x=1, y=1, text="Something interesting")

You can easily add single quotes for the text::

   Text(x=1, y=1, text="Something isn't interesting")

However, if you want to use double quotes inside the text, then you’ll
need to change the outer ones to singles::

   Text(x=1, y=1, text='Something "interesting"!')

What if you want to use single and double quotes in the text? In this
case, you’ll need to add a special marker character before the quote
that matches the outer one::

   Text(x=1, y=1, text='Something isn\'t "interesting"!')

Here the “" in front of the”’t” shows that the single quote is not the
end of the string, but simply a symbol that must be displayed.


Properties and Short-cuts
=========================
`↑ <table-of-contents_>`_

**To Be Done**


Lists
=====
`↑ <table-of-contents_>`_

Lists are a particularly useful way to collate, or group, related items
so that they can be processed together.

You may be familiar with examples such as grocery lists or to-do lists.
A list is normally written as a series of items, each separated with a
comma. For example; apples, oranges, bananas and plums. A list can also
be written vertically in the form of a number of bullets:

-  first,
-  second, and
-  third.

A column in a spreadsheet can be thought of as such a vertical list (but
you would not usually use an “and” in it!)

Lists in **pyprototypr** are written in a similar way but they need to
be identified by wrapping them at their start and end by the use of
*brackets*.

The brackets that are used are so-called **square brackets** - ``[`` and
``]``. Items in the list are separated by commas.

-  If they are numbers, then that’s all you need: for example, *[1, 3, 5,
   7]* - this list is a series of odd numbers.
-  If they are words, or strings of text then each item must be wrapped
   in quotes: for example, *['apples', 'oranges', 'bananas', 'plums']*
   or *["apples", "oranges", "bananas", "plums"]* (remember that quotes
   can be single or double but not a mix of both!)

..

   Note that there is **no** use of the word “and” in these lists!

A list is normally given an assignment to store it in memory for use by
the script; for example::

   groceries = ['apples', 'oranges', 'bananas', 'plums']

This is so that the list can be referred to in the script by using the
shorthand reference name (in this case ``groceries``). There are various
examples of the use of lists of elsewhere in these documents and also in
the script examples.

Errors
======
`↑ <table-of-contents_>`_

A situation that you will often encounter, especially as your script gets
longer and more complex, is the appearance of errors.

While **pyprototypr** will attempt to check many details of the script,
its very unlikely to be able to catch every mistake that might be made.

It will do some basic error checking as to whether correct values have
been assigned to properties; so::

    Rectangle(height="a")

will cause this error when the script is run::

    FEEDBACK:: The "a" is not a valid float number!
    FEEDBACK:: Could not continue with program.

because the ``height`` is meant to be a number, not a string.

In some cases, instructions will **not** cause an error, but they will simply
be ignored, for example::

    Rectangle(corner="a")

will still draw a ``Rectangle``; the meaning of ``corner`` is unknown so it will
simply be skipped.


Python-specific Errors
----------------------

“Under the hood” Python will itself also report on various errors, for example::

   Arc(x=1, y=1, x=2, y1=3)
                 ^^^
   SyntaxError: keyword argument repeated: x

Python attempts to identify the type and location of the error - a
``SyntaxError`` is just a grammar error of some type - as well as what
the cause *might* be. Here, it found that you have used the property ``x``
twice, so in this case you might need to change the second one to ``x1`` --
which  is probably the intended one::

   Arc(x=1, y=1, x1=2, y1=3)

Another example::

   Rectangle(height=1.5, stroke=green, fill=bred)
                                            ^^^^
   NameError: name 'bred' is not defined

In this case, the script uses the name of something - ``bred`` - which
is unknown. It could be a simple spelling mistake e.g. here it should be
``red`` *or* possibly you’d meant to assign the word ``bred`` to a particular
color before using it for the ``Rectangle``::

   bred = "#A0522D"
   Rectangle(height=1.5, stroke=green, fill=bred)

Another example::

   paper=A8 cards=9
            ^^
   SyntaxError: invalid syntax. Perhaps you forgot a comma?

Another ``SyntaxError`` where Python tries to assess what the cause
might be. Here, you’d need to add a “,” (comma) at the end of defining the
``paper=A8`` property as each property in the list must be comma-separated
(a space is not sufficient) as follows::

   paper=A8, cards=9
