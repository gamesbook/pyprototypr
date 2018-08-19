#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Support utilities for draw
"""
# lib
import itertools
import sys
# third-party
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def feedback(item, stop=False):
    """Placeholder for more complete feedback."""
    print 'FEEDBACK:: %s' % item
    if stop:
        sys.exit()


def base_fonts():
    """On Ubuntu: sudo apt-get install ttf-mscorefonts-installer"""
    fonts = [
        {'name': 'Ubuntu', 'file': 'Ubuntu-R.ttf'},
        {'name': 'Arial', 'file': 'Arial.ttf'},
        {'name': 'Verdana', 'file': 'Verdana.ttf'},
        {'name': 'Courier New', 'file': 'Courier_New.ttf'},
        {'name': 'Times New Roman', 'file': 'Times_New_Roman.ttf'},
        {'name': 'Trebuchet_MS', 'file': 'Trebuchet_MS.ttf'},
        {'name': 'Georgia', 'file': 'Georgia.ttf'},
        {'name': 'Webdings', 'file': 'Webdings.ttf'},
        #{'name': '', 'file': '.ttf'},
    ]
    for _font in fonts:
        try:
            pdfmetrics.registerFont(TTFont(_font['name'], _font['file']))
        except Exception as err:
            pass
            #log.error('Unable to register %s from %s (%s)', 
            #    _font['name'], _font['file'], err)


def numbers(*args):
    """Float range generator.

    'frange6' from http://code.activestate.com/recipes/\
                   66472-frange-a-range-function-with-float-increments/
    """
    start = 0.0
    step = 1.0
    l = len(args)
    if l == 1:
        end = args[0]
    elif l == 2:
        start, end = args
    elif l == 3:
        start, end, step = args
        if step == 0.0:
            raise ValueError("frange step must not be zero")
    else:
        raise TypeError("frange expects 1-3 arguments, got %d" % l)

    v = start
    while True:
        if (step > 0 and v >= end) or (step < 0 and v <= end):
            raise StopIteration
        yield v
        v += step


def letters(start='a', stop='z'):
    """Return list of characters between two."""
    def gen():
        for c in xrange(ord(start), ord(stop) + 1):
            yield chr(c)
    return list(gen())


def split(string, delim=' '):
    """Split a string on the delim."""
    return string.split(delim)


def combinations(_object, size=2, repeat=1, delimiter=','):
    """Create a list of combinations.

    Args:
        _object: list OR delimited string
        size: int
            how many items to take from list to create a combo
        repeat: int
            how many times to repeat item in original list
    """
    try:
        size = int(size)
    except (TypeError, AttributeError):
        feedback('Unable to use a size of "%s"' % size)
        return []
    try:
        repeat = int(repeat)
    except (TypeError, AttributeError):
        feedback('Unable to use a repeat of "%s"' % repeat)
        return []
    try:
        items = _object.split(delimiter)
    except AttributeError:
        items = _object
    try:
        for item in items:
            pass
        items = items*repeat
        combo = itertools.combinations(items, size)
        full_list = []
        while True:
            try:
                comb = next(combo)
                sub = [str(cmb) for cmb in comb]
                full_list.append(''.join(sub))
            except StopIteration:
                break
        new_list = list(set(full_list))
        new_list.sort()
        return new_list
    except (TypeError, AttributeError):
        feedback('Unable to create combinations from "%s"' % _object)
        return []
