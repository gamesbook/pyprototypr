#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utility functions for pyprototypr
"""
# lib
import csv
import collections
from itertools import zip_longest
import math
import os
import sys
import xlrd
# local
from pyprototypr.utils.support import numbers, feedback


DEBUG = False


def load_data(datasource=None, **kwargs):
    """
    Load data from a 'tabular' source (CSV, XLS) into a dict
    """
    dataset = {}
    #print "tools_21: Load data from a 'tabular' source (CSV, XLS)", datasource
    if datasource:
        filename, file_ext = os.path.splitext(datasource)
        if file_ext.lower() == '.csv':
            headers = kwargs.get('headers', None)
            selected = kwargs.get('selected', None)
            dataset = open_csv(datasource, headers=headers, selected=selected)
        elif file_ext.lower() == '.xls':
            headers = kwargs.get('headers', None)
            selected = kwargs.get('selected', None)
            sheet = kwargs.get('sheet', 0)
            sheetname = kwargs.get('sheetname', None)
            dataset = open_xls(datasource, sheet=sheet, sheetname=sheetname,
                               headers=headers, selected=selected)
        else:
            feedback('Unable to process a file %s of type "%s"' %
                     (filename, file_ext))
    return dataset


def grouper(n, iterable, fillvalue=None):
    """group and return sets

    See:
        http://stackoverflow.com/questions/2990121/~
        how-do-i-loop-through-a-python-list-by-twos
    """
    #grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
    #grouper(3, [1,3,2,4,5,7,6,8,0], None) --> 1 3 2   4 5 7   6 8 0
    # use: for item1, item2 in grouper(3, l):
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)


def boolean_join(items):
    """Create a result from boolean concatenation

    >>> items = [True, '+', False]
    >>> boolean_join(items)
    False
    >>> items = [True, '|', False]
    >>> boolean_join(items)
    True
    >>> items = [True, None]
    >>> boolean_join(items)
    True
    """
    if not items or len(items) == 0:
        return None
    expr = ''
    for item in items:
        if item == '&' or item == 'and' or item == '+':
            expr += ' and '
        elif item == '|' or item == 'or':
            expr += ' or '
        elif item is not None:
            expr += '%s' % item
        else:
            pass  # ignore nones
    try:
        result = eval(expr)
    except NameError:
        return None
    return result


def query_construct(string):
    """
    Split a query string into a list of lists.

    string: str
        boolean-type expression which can be evaluated to return a True
        e.g.1 'name`=`fred' filters item for dataset['name'] == 'fred'
        e.g.2 name`fred is a shortcut for the equals expression!
        e.g.3 'name`=`fred`&`height`<`6' filters item for:
            dataset['name'] == 'fred' and dataset['height'] < 6.0
    """
    result = []
    if string:
        items = string.split('`')
        if len(items) == 2:
            items.insert(1, '=')
        for item1, item2, item3, item4 in grouper(4, items):
            result.append([item1, item2, item3, item4])
        return result
    return [(None, None, None)]


def tuple_split(string):
    """
    Split a string into a list of tuple values

    from utils.tools import tuple_split
    print tuple_split('')
    #[]
    print tuple_split('3')
    #[3]
    print tuple_split('3,4')
    #[(3, 4)]
    print tuple_split('3,5 6,1 4,2')
    #[(3, 5), (6, 1), (4, 2)]
    """
    values = []
    if string:
        try:
            _string_list = string.strip(' ').replace(';', ',').split(' ')
            for _str in _string_list:
                items = _str.split(',')
                _items = [float(itm) for itm in items]
                values.append(tuple(_items))
            return values
        except:
            return values
    else:
        return values


def sequence_split(string):
    """
    Split a string into a list of individual values

    import tools
    print tools.sequence_split('')
    #[]
    print tools.sequence_split('3')
    #[3]
    print tools.sequence_split('3,4,5')
    #[3, 4, 5]
    print tools.sequence_split('3-5,6,1-4')
    #[1, 2, 3, 4, 5, 6]
    """
    values = []
    if string:
        try:
            _string = string.replace(' ', '').replace('"', '').\
                replace("'", '').replace(';', ',')
        except:
            return values
    else:
        return values
    try:
        values.append(int(_string))
        return values
    except:
        _strings = _string.split(',')
        #log.debug('strings:%s', _strings)
        for item in _strings:
            if '-' in item:
                _strs = item.split('-')
                seq_range = list(range(int(_strs[0]), int(_strs[1]) + 1))
                values = values + seq_range
            else:
                values.append(int(item))
    return list(set(values))  # unique


def splitq(seq, sep=None, pairs=("()", "[]", "{}"), quote='"\''):
    """Split seq by sep but considering parts inside pairs or quoted as
       unbreakable pairs have different start and end value, quote have same
       symbol in beginning and end.

    Use itertools.islice if you want only part of splits

    Source:
        https://www.daniweb.com/programming/software-development/code/426990/\
        split-string-except-inside-brackets-or-quotes
    """
    if not seq:
        yield []
    else:
        lsep = len(sep) if sep is not None else 1
        lpair, rpair = zip(*pairs)
        pairs = dict(pairs)
        start = index = 0
        while 0 <= index < len(seq):
            c = seq[index]
            if (sep and seq[index:].startswith(sep)) or \
                    (sep is None and c.isspace()):
                yield seq[start:index]
                #pass multiple separators as single one
                if sep is None:
                    index = len(seq) - len(seq[index:].lstrip())
                else:
                    while sep and seq[index:].startswith(sep):
                        index = index + lsep
                start = index
            elif c in quote:
                index += 1
                p, index = index, seq.find(c, index) + 1
                if not index:
                    raise IndexError(
                        'Unmatched quote %r\n%i:%s' % (c, p, seq[:p]))
            elif c in lpair:
                nesting = 1
                while True:
                    index += 1
                    p, index = index, seq.find(pairs[c], index)
                    if index < 0:
                        raise IndexError(
                            'Did not find end of pair for %r: %r\n%i:%s' %
                            (c, pairs[c], p, seq[:p]))
                    nesting += '{lpair}({inner})'.format(
                        lpair=c, inner=splitq(seq[p:index].count(c) - 2))
                    if not nesting:
                        break
            else:
                index += 1
        if seq[start:]:
            yield seq[start:]


def open_csv(filename, headers=None, selected=None):
    """Read data from CSV file into a list of dictionaries

    Supply:

      * headers is a list of strings to use instead of the first row
      * selected is a list of desired rows e.g. [2,4,7]
    """
    dict_list = []
    try:
        _filename = os.path.normpath(filename)
        if headers:
            reader = csv.DictReader(open(_filename), fieldnames=headers)
        else:
            reader = csv.DictReader(open(_filename))
        for key, item in enumerate(reader):
            if not selected:
                dict_list.append(item)
            else:
                if key + 1 in selected:
                    dict_list.append(item)
    except IOError:
        feedback('Unable to find or open "%s"' % filename)
    return dict_list


def open_xls(filename, sheet=0, sheetname=None, headers=None, selected=None):
    """Read data from XLS file into a list of dictionaries

    Supply:

      * sheet to select a sheet number (otherwise first is used)
      * sheetname to select a sheet by name (otherwise first is used)
      * headers is a list of strings to use instead of the first row
      * selected is a list of desired rows e.g. [2,4,7]
    """
    dict_list = []
    try:
        _filename = os.path.normpath(filename)
        book = xlrd.open_workbook(_filename)
        if sheet:
            sheet = sheet - 1
            sheet = book.sheet_by_index(sheet)
        elif sheetname:
            sheet = book.sheet_by_name(sheetname)
        else:
            sheet = book.sheet_by_index(0)
        start = 1
        if not headers:
            keys = [sheet.cell(0, col_index).value \
                    for col_index in xrange(sheet.ncols)]
        else:
            start = 0
            keys = headers
        if len(keys) < sheet.ncols:
            feedback(
                'Too few headers supplied for the existing columns in "%s"' %
                filename)
        else:
            dict_list = []
            for row_index in xrange(start, sheet.nrows):
                item = {keys[col_index]: sheet.cell(row_index, col_index).value
                        for col_index in xrange(sheet.ncols)}
                if not selected:
                    dict_list.append(item)
                else:
                    if row_index + 1 in selected:
                        dict_list.append(item)
    except IOError:
        feedback('Unable to find or open "%s"' % filename)
    except IndexError:
        feedback('Unable to open sheet "%s"' % (sheet or sheetname))
    except xlrd.biffh.XLRDError:
        feedback('Unable to open sheet "%s"' % sheetname)
    return dict_list


def flatten(lst):
    """Flatten nested lists into a single list of lists."""
    try:
        for ele in lst:
            if isinstance(ele, collections.Iterable) and \
                    not isinstance(ele, basestring):
                for sub in flatten(ele):
                    yield sub
            else:
                yield ele
    except TypeError:
        yield lst


def comparer(val, operator, target):
    """target could be list?? - split a string by , or ~

    assert comparer(None, None, None) == True

    assert comparer("1", '*', "1") == False

    assert comparer("1", None, "1") == True
    assert comparer("a", None, "a") == True
    assert comparer("True", None, "True") == True
    assert comparer("False", None, "False") == True

    assert comparer("1", '<', "1.1") == True
    assert comparer("a", '<', "aa") == True
    assert comparer("True", '<', "True") == False
    assert comparer("False", '<', "False") == False

    assert comparer("1", '~', "1.1") == False
    assert comparer("a", '~', "aa") == True
    assert comparer("True", '~', "True") == False
    assert comparer("False", '~', "False") == False

    assert comparer("1", '~', [1,2,3]) == True
    """

    def to_length(val, target):
        """Get length of object."""
        try:
            val = len(val)
        except:
            pass
        try:
            target = len(target)
        except:
            pass
        return val, target

    if target == 'T' or target == 'True':
        target = True
    if target == 'F' or target == 'False':
        target = False
    if val == 'T' or val == 'True':
        val = True
    if val == 'F' or val == 'False':
        val = False

    if not operator:
        operator = '='
    if operator in ['<', '<=', '>', '>=']:
        val, target = to_length(val, target)

    try:
        val = float(val)
    except:
        pass
    try:
        target = float(target)
    except:
        pass
    if operator == '=':
        if val == target:
            return True
    elif operator == '~' or operator == 'in':
        try:
            if val in target:
                return True
        except TypeError:
            pass
    elif operator == '!=':
        if val != target:
            return True
    elif operator == '<':
        if val < target:
            return True
    elif operator == '>':
        if val > target:
            return True
    elif operator == '>=':
        if val >= target:
            return True
    elif operator == '<=':
        if val <= target:
            return True
    else:
        feedback("Unknown operator: %s (%s and %s)" % (operator, val, target))
    return False


def polygon_vertices(sides, radius, starting_angle, center):
    """Calculate array of points for a polygon's vertices.

    Args:
    * sides: integer
        number of sides
    * starting_angle: float
        this is effectively the "rotation"
    * center: tuple of (x,y) values
    """
    try:
        sides = int(sides)
        if sides < 3:
            sides = 3
    except ValueError:
        feedback("Polygon's sides must be an integer of 3 or more.")
        return []
    points = []
    step = 360.0 / sides
    rotate = starting_angle  # this is effectively the "rotation"
    for rotate in numbers(starting_angle, 360, step):  # go in a full circle
        points.append(degrees_to_xy(rotate, radius, center))
    return points


def color_to_hex(name):
    """Convert a named ReportLab color (Color class) to a hexadecimal string"""
    _tuple = (int(name.red*255), int(name.green*255), int(name.blue*255))
    _string = '#%02x%02x%02x' % _tuple
    return _string.upper()


def degrees_to_xy(degrees, radius, origin):
    """Calculates a point that is at an angle from the origin;
    0 is to the right.

    Args:
    *  origin: tuple of (x,y) values

    Returns:
     *  (x,y) tuple
    """
    radians = degrees * math.pi / 180.0
    x_o = math.cos(radians) * radius + origin[0]
    y_o = math.sin(-radians) * radius + origin[1]
    return (x_o, y_o)
