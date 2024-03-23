# pyprototypr: A Worked Example

This example assumes that you have set-up your computer with Python and have
tested to check that you can create a test file which generates a PDF.

If not, please first see the [Setting Up](setting_up.md) document.

> **Remember** to create your file do **not** use a word processor such as
> "Word", "Pages" or "LibreOffice" - but a text file editor instead e.g .
> on Windows, use *NotePad* or *NotePad++*; and on OS X, use *TextEdit*!


## A simple card deck example: Take 1

Open up a new text file with your text file editor and type the following, making 
sure that you start each line *without any blank spaces at the start.

```python

from pyprototypr.draw import *
Create()
Deck(cards=9)
Save()
```

`Create`_ tells **pyprototypr**  to define the output PDF file in which this
deck of 9 cards will be saved.  Because no further information is given,
the `defaults`_ for sizes and colours are used, as well as the default page
size of A4. `Deck`_ means that **pyprototypr** defines a deck of 9 cards, again
with default size. `Save`_ gives the go-ahead to create the resulting file.

Now save the text file, for example, as `cards1.py`.  Then open a command-line
window (see under `Testing that Python is installed`_) and change to the
directory where the file is installed. Type the following::
```
python cards1.py
```

An output PDF file should now have been created, in the same directory as your
`cards1.py` file, called `cards1.pdf`. If you open this in a PDF
reader program, you should see that it contains a set of 9 blank, poker-card
sized, rectangular outlines (which we are calling "cards") laid out in a grid
on an A4-sized page (*A4* being the default page size for **pyprototypr**).


## A simple card deck example: Take 2

Open up a new text file with your text file editor and type in the following (again,
remember to start each line *without any blank spaces):

```python
from pyprototypr.draw import *

Create(pagesize=A3, 
    filename="example2.pdf")
Deck(cards=9)
Save()
```

You can see that the `Create`_ instruction has now been expanded with new
`properties`_ (the items appearing in brackets). A *property* is just a name,
followed by an "=" sign, and then a value of some kind.

In this case, the `pagesize` property has been set to *A3* (note, there are **no** 
*""* delimiters around the term *A3*), and a specific file name has been chosen 
for the output PDF; in this case `example2.pdf`.

The `Create`_ instruction is split over multiple lines to make it easier to read;
but you need to make sure that the split happens directly after a comma,
and not in the middle of a word. Also make sure that there are one or spaces
at the start of those continuation lines; its often helpful to start the next
line indented by four (4) spaces.

A blank line has been added before the `Create`_ instruction. Adding blank
lines helps make your file more readable, but **pyprototypr** does not use or require them.

Now save this new file, for example, as `cards2.py`. 

Now open a command-line window (see `Testing that Python is installed`_) and 
change to the directory where the file is installed. Type the following:
```
    python cards2.py
```

An output PDF file should now have been created in the same directory as your
`cards2.py` file - it will be called `example2.pdf`. It should contain a set
of 9 blank cards appearing near the bottom corner on one A3-sized page.


## A simple card deck example: Take 3

If you have followed the above examples, you will know how to create the cards
file, and how to create and display the output PDF file. This example will
therefore *only* show the text in the file you create, and discuss what the
resulting output should look like.

Create this text in a file called `cards3.py`:

```python
from pyprototypr.draw import *

Create(filename='example3.pdf', offset=0.5)

# deck design - a "template" that all cards will use
Deck(
    cards=50,
    fill="#702EB0",
    height=5,
    width=3.8)

# create the output card file, using the card 'deck'
Save()
```

A `Deck`_ instruction allows you to define the details for every card that will
appear in the deck, such as its height, width and fill colour.

In this script, the lines starting with a **#** are `comments`_ and will
be ignored by **pyprototypr**. The comments are included to provide some more
explanation as to what the next line, or lines, are doing.

The resulting `example3.pdf` will show two pages of small, blank, purple
cards, approximately 2 inches by 1.5 inches, with 25 cards per page, for a
total of 50 cards.  

> Note that the **pyprototypr** will do the calculation for you on how many
> cards will fit on page to make up the total number of cards for the deck.


## A simple card deck example: Take 4

This example will only show the text in the file you create, and discusses what
the resulting output should be.

Create this text in a file called `cards4.py`:

```python

from pyprototypr.draw import *

# create the output card file
Create(filename='example4.pdf', offset=0.5)

# create a deck design
Deck(cards=25,
     fill=skyblue,
     stroke=white,
     height=5,
     width=3.8)

# create some text, with the default font, and centre it at a location
mytext = text(text="25!", point=(1.9,1.0))

# customize a single card (number 25) in the deck with 'mytext'
Card("25", mytext)

# specify a particular font; face and size and colour
times = Font("Times New Roman", size=8, colour="red")

# create more text, and display it using 'times' font
mytext2 = text(text="I'm on cards 1-10", font=times, x=1.9)

# specify a range of cards to contain 'mytext2'
Card("1-10", mytext2)

# save to file
Save()
```

This script also shows the use of a `reference`_: a reference is just
a name, followed by an "=" sign, and then an instruction.  You can see that the
*mydesign* reference is used further on when specifying the design for a
`Card`_; this requires a card number (or numbers) followed by the details of
what is required for the card - in this case, the text stored in *mydesign*.

The resulting `example4.pdf` file will show a page of small, white-bordered,
light-blue cards - with the same text appearing on cards one to ten,
but different text on card number 25 (twenty-five). 

> **Note** the cards are displayed from the bottom-left upwards;  that is why 
> the first cards appear on the bottom rows and the last card is on the top-right.

