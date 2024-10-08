# pyprototypr: Additional Concepts

## Table of Contents

* [Names and Naming](#names )
* [Strings (words and letters), Numbers and Booleans](#strings)
* [Calculations](#calculations)
* [Case-sensitivity](#case)
* [Quotes in Text](#quotes)
* [Properties and Short-cuts](#short)
* [Lists](#lists)
* [Errors](#errors)


## Names and Naming <a name="names"></a>

Naming of things is supposed to be one of the harder aspects of programming.

If you work with the built-in commands and and their properties, the set of
names to use is already chosen for you. However, if you want to start using
some additional options, such as assigning [short-cut names](#short) to reuse
items in multiple places, then you need to be aware of the wider set of so-
called "reserved" names available as part of Python.  If your short-cut name
is the same as one of those, you'll overwite it and your scripts may fail in
strange ways!

> *NOTE* __pyprototypr__, like Python, is case-sensitive - unlike some computer
> languages or file names that are used in Windows); a lowercase name is *NOT*
> the same as an uppercase version of it!

Basic built-in names include: False, None, True, and, as, assert, async,
await, break, class, continue, def, del, elif, else, except, finally, for,
from, global, if, import, __import__, in, is, lambda, nonlocal,  not, or,
pass, raise, return, try, while, with, yield

Function names include: abs, aiter, all, anext, any, ascii, bin, bool,
breakpoint, bytearray, bytes, callable, chr, classmethod, compile, complex,
delattr, dict, dir, enumerate, eval, exec, filter, float, format, frozenset,
getattr, globals, hasattr, hash, help, hex, id, input, int, isinstance,
issubclass, iter, len, list, locals, map, max, memoryview, min, next, object,
oct, open, ord, pow, print, property, range, repr, reversed, round, set,
setattr, slice, sorted, staticmethod, str, sum, super, tuple, type, vars, zip

If you're interested in what all these functions do, there is a very readable
guide presented here:
 https://www.mattlayman.com/blog/2024/layman-guide-python-built-in-functions/


## Strings (words and letters), Numbers and Booleans  <a name="strings"></a>

**To Be Done**


## Calculations <a name="calculations"></a>

**To Be Done**


## Case-sensitivity  <a name="case"></a>

**To Be Done**


## Quotes in Text <a name="quotes"></a>

Using quotes inside a string of letters can be tricky.

If you have a Text shape, for example, like this:
```
Text(x=1, y=1, text="Something interesting")
```

You can easily add single quotes for the text:
```
Text(x=1, y=1, text="Something isn't interesting")
```

However, if you want to use double quotes inside the text, then
you'll need to change the outer ones to singles:
```
Text(x=1, y=1, text='Something "interesting"!')
```

What if you want to use single and double quotes in the text?
In this case, you'll need to add a special marker character before the quote
that matches the outer one:
```
Text(x=1, y=1, text='Something isn\'t "interesting"!')
```
Here the "\" in front of the "'t" shows that the single quote is not the end
of the string, but simply a symbol that must be displayed.


## Properties and Short-cuts  <a name="short"></a>

**To Be Done**


## Lists  <a name="lists"></a>

Lists are a particularly useful way to collate, or group, related items so
that they can be processed together.

You may be familiar with examples such as grocery lists or to-do lists.
A list is normally written as a series of items, each separated with a comma.
For example; apples, oranges, bananas and plums. A list can also be written
vertically in the form of a number of bullets:

* first,
* second, and
* third.

A column in a spreadsheet can be thought of as such a vertical list (but you
would not usually use an "and"!)

Lists in **pyprototypr** are written in a similar way but they need to be
identified by wrapping them at their start and end by the use of *brackets*.

The brackets that are used are so-called **square brackets** - `[` and `]`.
Items in the list are separated by commas.

* If they are numbers then that's all you need: for example, *[1, 3, 5, 7]* - this
  list is a series of odd numbers.
* If they are words, or strings of text then each item must be wrapped in quotes:
  for example, *['apples', 'oranges', 'bananas', 'plums']*  or
  *["apples", "oranges", "bananas", "plums"]* (remember that quotes can be single
  or double)

> Note that there is **no** usage of the word "and" in these lists!

A list is normally given an assignment to store it in memory for use by the
script; for example:
```
groceries = ['apples', 'oranges', 'bananas', 'plums']
```
This is so that the list can be referred to in the script by using the shorthand
reference name (in this case "groceries").  There are various examples of the
use of lists of elsewhere in these documents and also in the script examples.


## Errors  <a name="errors"></a>

While **pyprototypr** will attempt to check many details of the script, its
unlikely to be able to catch every mistake that might be made; "under the hood"
Python will itself also report on errors, for example:
```
    Arc(x=1, y=1, x=2, y1=3)
                  ^^^
SyntaxError: keyword argument repeated: x
```
It will attempt to identify the type and location of the error - a `SyntaxError`
is just a grammar error of some type - as well as what the cause *might* be.
Here, you'd need to change this to `x1` which would be the intended property.

Another example:
```
    Rectangle(height=1.5, stroke=green, fill=bred)
                                             ^^^^
NameError: name 'bred' is not defined
```
In this case, the script uses the name of something - `bred` - which is unknown.
It could be a simple spelling mistake e.g. it should be `red` or possibly you'd
meant to define `bred` as special color before using it for the Rectangle.

Another example:
```
    paper=A8 cards=9
             ^^
SyntaxError: invalid syntax. Perhaps you forgot a comma?
```
Another `SyntaxError` where Python tries to assess what the cause might be. Here,
you'd need to add "," (comma) at the end of property as each one must be
comma-separated (a space is not sufficient).
