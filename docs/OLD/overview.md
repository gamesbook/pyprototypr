# pyprototypr: Overview

## Introduction

The aim of **pyprototypr** is to provide a general purpose program that allows
you to design simple and reproducible graphics that can be used for prototyping the
elements or components of a project such as the creation of a board game; including
the board, the tiles, the cards and so on.

> **pyprototypr** is *NOT* a full-blown graphics editor - like the Adobe
> Photoshop, GIMP, or Inkscape packages - or a desktop publishing tool - like
> Scribus, InDesign, or Xpress - which allow sophisticated creation of complex
> graphics and text layouts - and it does not  attempt in **any** way to replicate
> their functionality!


## How do I use it?

In general, what you do is type a set of instructions into a file on your computer,
save that file, and then use Python to create your output - a PDF or PNG file -
containing the results of those instructions; hopefully the design you intended!

As your design changes and evolves, you add or change instructions and recreate
the output.


## How does it work?

**pyprototypr** is written in Python; the reason being that this is a relatively
easy to use programming language that is often used for scripting or automating
routines - both by itself and as part of larger programs. Python has access to
numerous libraries that help avoid having to develop code from scratch.

> Python is not a speedy language, but its still fast enough to use for **pyprototypr**

**pyprototypr** is designed such that you *don't* need to know how to program in
Python in order to use it; but if you *are* a Python programmer then you can
certainly treat this as you would any other library and add in your own additional
Python code or logic to your scripts for your own purpose.


## Who might want to use **pyprototypr** ?

**pyprototypr** is useful for anyone that needs to work on a design in an
incremental fashion, tweaking and changing as they go along. Doing this with
a regular graphics package can sometimes be tedious; especially when common
changes need to be made across many elements.

Simple designs that make use of regular-shaped symbols or fonts are
straightforward to implement in **pyprototypr**; but more complex pictures or
background images should be made, as usual, in a regular graphics design package
and then added into from your script by a link to the image file.

**pyprototypr** also supports access of data in text files ("CSV") and Excel
documents; this can help separate out the design and layout from the content -
the text and numbers - that appears in the design.


## How do I get started?

Its suggested that you first get everything [set-up](setting_up.md) and tested.
Then read through the [basic concepts](basic_concepts.md) before trying out a
[worked example](worked_example.py). After that, browse through the sections
listed in the [index](index.md).
