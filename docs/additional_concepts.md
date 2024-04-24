# pyprototypr: Additional Concepts

**To Be Done**

## Words, Numbers and Booleans


## Calculations


## Case-sensitivity


## Quotes

Using quotes inside a string of text can be tricky.

If you have a Text shape, for example, like this:
```
Text(x=1, y=1, text="Something interesting")
```

You can easily add single quotes:
```
Text(x=1, y=1, text="Something isn't interesting")
```

However, if you want to use double quotes in the string of text itself,
you'll need to change the outer ones to singles:
```
Text(x=1, y=1, text='Something "interesting"!')
```

What if you want to use single and double quotes in the string of text?
In this case, you'll need to add a special marker character before the quote
that matches the outer one:
```
Text(x=1, y=1, text='Something isn\'t "interesting"!')
```

## Properties and Short-cuts


## Lists

Lists are a particularly useful way to collate or group related items so that they
can be processed

You may be familiar with examples such as grocery lists or to-do lists. A list is
normally written as a series of items, each separated with a comma. For example,
apples, oranges, bananas and plums. A list can also be written vertically in the form
of a  series of bullets:

* first,
* second, and
* third.

A column in a spreadsheet can be thought of as such a vertical list.

Lists in **pyprototypr** are written in a similar way but they need to be identified by
wrapping them at their start and end by the use of brackets.

The brackets that are used are so-called square brackets - [ and ].  Items in the list
are separated by commas.

* If they are numbers then that's all you need: for example, [1, 3, 5, 7] - this
  list is a series of odd numbers.
* If they are words then each item must be wrapped in quotes: for for example,
  ['apples', 'oranges', 'bananas', 'plums'].

Note that there is **no** usage of the word "and" in these lists.

A list is normally given an assignment; for example:
```
groceries =  ['apples', 'oranges', 'bananas', 'plums']
```
This is so that the list can be referred to using this shorthand reference.  There
are examples of the use of lists of elsewhere in the documents and the coded examples.


## Errors

While **pyprototypr** will attempt to check the details of the script, its unlikely to
be able to catch every mistake; under the hood, Python will also report on errors,
for example:
```
    Arc(x=1, y=1, x=2, y1=3)
                  ^^^
SyntaxError: keyword argument repeated: x
```
It will attempt to identify the type and location of the error - a `SyntaxError` is
really a grammar error of same type - as well as what the cause might be. Here, you'd
need to change this to `x1` which is the intended property.

Another example:
```
    Rectangle(height=1.5, stroke=green, fill=bred)
                                             ^^^^
NameError: name 'bred' is not defined
```
In this case, the script uses the name of something - `bred` - which is unknown. It
could be a simple spelling mistake e.g. it should be `red` or possibly you'd meant to
define `bred` as special color before using it for the rectangle.
