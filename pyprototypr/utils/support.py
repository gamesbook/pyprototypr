# -*- coding: utf-8 -*-
"""
Support utilities for draw module
"""
# lib
import itertools
import sys
# third-party
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def feedback(item, stop=False, warn=False):
    """Placeholder for more complete feedback."""
    if warn:
        print('WARNING:: %s' % item)
    else:
        print('FEEDBACK:: %s' % item)
    if stop:
        print('FEEDBACK:: Could not continue with program.\n')
        #sys.exit()
        quit()


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
        for c in range(ord(start), ord(stop) + 1):
            yield chr(c)
    return list(gen())


def steps(start, end, step=1, REAL=True):
    """Return a list of numbers from start to end, at step intervals.

    Note:
        REAL is only used for doctest, to bypass sys.exist() problem

    Doc Test:

    >>> steps('a', 'b', REAL=False)
    FEEDBACK:: A start value of "a" is not a valid number
    >>> steps(1, 'b', REAL=False)
    FEEDBACK:: An end value of "b" is not a valid number
    >>> steps(1, 2, 'c', REAL=False)
    FEEDBACK:: A step value of "c" is not a valid number
    >>> steps(2, 1, REAL=False)
    FEEDBACK:: End value of "1" must be greater than start value of "2"
    >>> steps(1, 2, -1, REAL=False)
    FEEDBACK:: End value of "2" must be less than start value of "1"
    >>> steps(2, 1, 0, REAL=False)
    FEEDBACK:: An step value of "0" is not valid
    >>> steps(1, 3, REAL=False)
    [1, 2, 3]
    >>> steps(1, 3, 2, REAL=False)
    [1, 3]
    >>> steps(3, 1, -2, REAL=False)
    [3, 1]
    >>> steps(1, 5, 1.5, REAL=False)
    [1, 2.5, 4.0]
    """
    try:
        _start = float(start)
    except Exception:
        feedback(f'A start value of "{start}" is not a valid number', REAL)
        return
    try:
        _end = float(end)
    except Exception:
        feedback(f'An end value of "{end}" is not a valid number', REAL)
        return
    try:
        _step = float(step)
    except Exception:
        feedback(f'A step value of "{step}" is not a valid number', REAL)
        return
    if step == 0:
        feedback(f'An step value of "{step}" is not valid', REAL)
        return
    if end < start and step > 0:
        feedback(
            f'End value of "{end}" must be greater than start value of "{start}"', REAL)
        return
    if start < end and step < 0:
        feedback(
            f'End value of "{end}" must be less than start value of "{start}"', REAL)
        return

    result, current = [], start
    while True:
        result.append(current)
        current += step
        if current > end and step > 0:
            break
        if current < end and step < 0:
            break
    return result


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
        feedback(f'Unable to use a size of "{size}"', False, True)
        return []
    try:
        repeat = int(repeat)
    except (TypeError, AttributeError):
        feedback(f'Unable to use a repeat of "{repeat}"', False, True)
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
        feedback(f'Unable to create combinations from "{_object}"', False, True)
        return []


if __name__ == "__main__":
    import doctest
    doctest.testmod()
