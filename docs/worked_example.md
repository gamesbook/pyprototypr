# pyprototypr: A Worked Example of a Deck of Cards

This example assumes that you have set-up your computer with Python and have
tested to check that you can create a test file which generates a PDF. If not,
please first see the [Setting Up](setting_up.md) document.

> **Remember** when you create and edit your file, do **not** use a word processor
> such as "Word", "Pages" or "LibreOffice" - but a text file editor instead e.g.
> on Windows, use *NotePad* or *[NotePad++](https://notepad-plus-plus.org/)*;
> and on OS X, use *TextEdit*!


## A simple card deck example: Take 1

Open up a new text file with your text file editor and type the following, making
sure that each line starts **without** any blank spaces!
```python
from pyprototypr import *
Create()
Deck()
Save()
```

As can be seen there are four lines in the file:

*  *Line 1* - this tells Python to access the functionality in **pyprototypr**;
   every script you write must start with this
*  *Line 2* - `Create()` tells **pyprototypr**  to setup an output PDF file in
   which this design of will be saved.  Because no further information is given,
   the default values for sizes and colours will used, as well as the default page
   size, which is an A4 page. Every script you write will must have this as the next
   line.
*  *Line 3* - `Deck()` means that **pyprototypr** defines a deck with a default number
   of *9* cards, with each card having the same, default size (a "Poker" card size).
*  *Line 4* - `Save()` gives the go-ahead to create the output file on disc. Usually,
   every script you write will have this as the last line.

Now save the text file, for example, as `cards1.py`.  Then open a command-line
window (as described in [Setting Up](setting_up.md) ) and change to the
directory where the file is installed.

Type the following:
```
python cards1.py
```

An output PDF file should now have been created, in the same directory as your
`cards1.py` file, called `cards1.pdf`. If you open this in a PDF
reader program, you should see that it contains a set of 9 blank, poker-card
sized, rectangular outlines (which we term "cards") laid out in a grid
on an A4-sized page.


## A simple card deck example: Take 2

Open up a new text file with your text file editor and type in the following (again,
remember to start each line with **NO** any blank spaces):

```python
from pyprototypr import *

Create(pagesize=A3, filename="example2.pdf")
Deck()
Save()
```

You can see that the `Create()` instruction has now been expanded with a list of
new details appearing inside the brackets. These items are called *properties*
and each item is separated by a ",".  Each **property** is defined by a name,
followed by an "=" (equals) sign, and then a value of some kind.

In this case, the `pagesize` property has been set equal to a value of *A3*
(note, there are **no** *""* delimiters around the term *A3*), and a specific
file name has been chosen for the output PDF; in this case `example2.pdf`.

A blank line has been added before the `Create()` instruction. Adding blank
lines helps make your file more readable, but **pyprototypr** does *not* use or
require them.

Now save this new file, for example, as `cards2.py`. Open a command-line window and
change to the directory where the file has been saved.

Type the following:
```
python cards2.py
```

An output PDF file should now have been created in the same directory as your
`cards2.py` file - it will be called `example2.pdf`. It should contain a set
of 9 blank cards appearing near the bottom-left corner on one A3-sized page.


## A simple card deck example: Take 3

If you have followed the above examples, you will know how to create the cards
file, and how to create and display the output PDF file. This example will
therefore *only* show the text in the file you create, and discuss what the
resulting output should look like.

Create this text in a file called `cards3.py`:

```python
from pyprototypr import *

Create(filename='example3.pdf', offset=0.5)

# deck design: a "template" that all cards will use
Deck(
    cards=50,
    height=5,
    width=3.8,
    fill="#702EB0")

# create the output card file, using the card 'deck'
Save()
```

A `Deck()` instruction allows you to define the details for every card that will
appear in the deck, such as its height, width and the colour to fill it in.

Because there are many properties in it, the `Deck()` instruction has been split
over multiple lines to make it easier to read; but you need to make sure that such
a split happens directly after a comma, and **not** in the middle of a word or a
property setting.

When you split an instruction, make sure that there are one or more spaces at the
start of the continuation lines; its often helpful to start the next line indented
by four (4) spaces.

In this `Deck`, the number of cards has been set to 50. The size of the cards in
the deck have been changed to be 5cm high and 3.8cm wide.  The fill color is defined by
a **hexadecimal** value - this sets the red, green and blue parts that make up a
color; in this case we'd see it as a shade of "purple".

In this script, the lines shown starting with a **#** are called **comments** -
these will be ignored by **pyprototypr** but are included to provide some more
explanation as to what the next line, or lines, are doing.  You could also add
lines at the start of a script to help say what its purpose is.

The resulting `example3.pdf` will show two pages of small, blank, purple
cards, approximately 2 inches by 1.5 inches, with 25 cards per page, for a
total of 50 cards.

> Note that the **pyprototypr** will do the calculation for you on how many
> cards will fit on page to make up the total number of cards for the deck.


## A simple card deck example: Take 4

This example will only show the text in the file you create, and then discuss
the new kinds of details added to it, as well as what the resulting output should be.

Create this text in a file called `cards4.py`:

```python
from pyprototypr import *

# create the output card file and page details
Create(filename='example4.pdf', offset=0.5)

# create a deck design; use a white border instead of the default black
Deck(cards=25
     height=5,
     width=3.8,
     fill=skyblue,
     stroke=white)

# customize a single card (number 25) in the deck with some text
# the text is 1.9cm from the left of the card and 1cm from its lower edge
Card("25", text(text="25!", x=1.9, y=1.0))

# create a reference for a particular font; with it's face and size and colour
times = Font("Times New Roman", size=8, colour="red")

# create more text, and display it using the font defined by 'times' reference
mytext = text(text="I'm on cards 1-9", font=times, x=1.9)

# specify a range of cards that will contain 'mytext'
Card("1-9", mytext)

# save to file
Save()
```

For this deck we are are setting card colors by choosing their names from a
a set of pre-defined colors available in **pyprototypr** - these might be useful
if they match your needs.

A new instruction, called `Card()`, has been added.  As might be expected, this
specifies what will actually appear on a given card or cards apart from just the
color.  The number just after the `(` bracket is the card number or, if there are
multiple cards, then the first and last card number separated by a dash ("-").

In the line starting `Card("25"`, you can see that Card#25 will contain the text `25!`.

This script also shows the use of a **reference** - a reference is just a name,
followed by an "=" sign, and then an instruction of some kind.

You can see that the `times` reference is used when specifying the `mytext` reference.

You can also see that the `mytext` reference is used further on when specifying the
design for cards numbered #1 to #9 (`Card("1-9"`).

The resulting `example4.pdf` file will show a page of small, white-bordered,
light-blue cards - with the same text appearing on cards one to nine,
but with different text on card number 25 (twenty-five).

> **Note** the cards are displayed from the bottom-left upwards and then from left
> to right - that is why the first cards appear on the bottom rows and the last card
> is shown on the top-right.


## Continuing on ...

If you are interested in carrying on with design of card decks, then the section on
[Card Decks](card_decks.md) will be helpful for you (bear in mind that that section
assumes you are familiar with all the core concepts and program usage described in
the earlier sections of the documentation).

There are also card-related examples in the [Available Examples](available_examples.md)
section.
