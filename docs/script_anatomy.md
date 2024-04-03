# pyprototypr: Script Anatomy

**To Be Done**

## First, Middle and Last


## Basic Shapes


## Sets, Arrays and Grids


## Commands

### Page Commands

### Repeats


## Comments


## Drawing vs Creating


## The FEEDBACK Message


## Making Mistakes

It is, unfortunately, all too easy to make mistakes while writing scripts.

They are three main kinds of mistakes:

Supplying the script an **incorrect value**, for example, giving the location a
value of `3.0` when you meant to give it `0.3`; this kind of mistake can usually be
detected when you look at the PDF, although it may not be immediately obvious exactly
what has happened.

Supplying the script an **incorrect kind of value**, for example, giving the `y` location
a value of 'a' instead of a number. The script will stop at this point and give you
a feedback message.

Supplying the script a **property that does not exist**, for example, using `u=2.0`
when you meant to say `y=2.0` (which can happen because those two letters are located
right next to each other on a keyboard).  In this case, the script will
"fail silently" because properties that don't exist are simply ignored.
This kind of mistake is harder to spot, often because the default value will then be
used instead and it will seem as though the script is drawing something incorrectly.
