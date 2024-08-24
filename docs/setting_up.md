# pyprototypr: Setting Up

There are four parts to being able to use **pyprototypr**:

1. Install the correct version of Python
2. Install and set-up **pyprototypr**
3. Install a text editing program
4. Install a PDF viewer (e.g. *Adobe Acrobat*)

Its possible that you may already one or more already installed.


## Installing Python

**pyprototypr** requires a device e.g. laptop or desktop (but probably not a
smart phone) that already has the correct version of Python (version 3.11) installed.

If your device does not have Python installed, it can be obtained from http://www.python.org/download/.

A very detailed and useful guide to installing on Windows is at:
https://www.tomshardware.com/how-to/install-python-on-windows-10-and-11

This guide will also take you through installing
*[NotePad++](https://notepad-plus-plus.org/)* which is the
recommended Windows editor for creating **pyprototypr** scripts.

For MacOS, there is a helpful guide on working with Python from *pyLadies*; see:
http://www.pyladies.com/blog/Get-Your-Mac-Ready-for-Python-Programming/

### Test that Python is installed

In order to test that Python is installed, start a **command-line window**.
The way you do this depends on your operating system.

* For Windows users - go to "Start -> Run" (On Windows 7 to 10, press
  "WindowsKey+R" or use the search box at the bottom of the Start menu)

* For Mac OS X users - go to your Applications/Utilities folder and choose
  "Terminal".

* For Linux users; you should already know how to open a Terminal!!

When the command-line window appears, type::
```
python --version
```
You should see something like::
```
Python 3.11.5
```

The exact number after the "11" does not matter.

You can now close the command-line window.


## Installing **pyprototypr**

The simplest way to install **pyprototypr** itself is via::
```
pip install pyprototypr
```

The manual also provides alternate, more complex ways of installing, for
example, in a virtual environment.


## Other Software Installs

### PDF Viewer

You will also need a program that can display PDF files; for example,
*Adobe Acrobat* (cross-platform), or **evince** (Linux), or **Preview** (Mac),
or **foxit** (Windows). Most modern web browsers should also be able to open
and display PDF files.

### Core Fonts (optional)

For Linux users, it is recommended that you install Microsoft's Core Fonts -
see http://mscorefonts2.sourceforge.net/ - Ubuntu users can install these via::
```
sudo apt-get install ttf-mscorefonts-installer
```


## Checking if **pyprototypr** works

To now check that `pyprototypr` works, you should create a small test file.

Open your text editor and type (or copy and paste) the following:
```
from pyprototypr import *
Create()
Text(text="Hello World")
Save()
```
Save the file; call it something like *test.py*.  (The ".py" indicates its a
Python file - this is useful but not essential).

Now use Python to "run" this file.

By "run", its meant that you open a command-line window (see the section
**Test that Python is installed**), change to the directory in which the
test file was created, for example:
```
cd C:/
```

and then type:
```
python test.py
```

and press the *Enter* key. Note that you should replace `test.py` with the
actual name of the file you created.

There should now be a new file called `test.pdf` in the same directory.

You should be able to open and view this PDF file via your PDF viewer. It should
be a mostly blank page with the phrase *Hello World* at the bottom-left.
