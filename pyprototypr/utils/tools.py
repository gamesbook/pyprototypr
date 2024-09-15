# -*- coding: utf-8 -*-
"""
General purpose utility functions for pyprototypr
"""
# lib
from collections import namedtuple
import cmath
import csv
import collections
from itertools import zip_longest
import logging
import math
import os
import pathlib
import string
import sys
import xlrd
# third party
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
# local
from pyprototypr.utils.support import numbers, feedback

log = logging.getLogger(__name__)
DEBUG = False


def script_path():
    """Get the path for a script being called from command line."""
    fname = os.path.abspath(sys.argv[0])
    if fname:
        return pathlib.Path(fname).resolve().parent


def load_data(datasource=None, **kwargs):
    """
    Load data from a 'tabular' source (CSV, XLS) into a dict
    """
    dataset = {}
    log.debug("Load data from a 'tabular' source (CSV, XLS) %s", datasource)
    if datasource:
        filename, file_ext = os.path.splitext(datasource)
        if file_ext.lower() == ".csv":
            headers = kwargs.get("headers", None)
            selected = kwargs.get("selected", None)
            dataset = open_csv(datasource, headers=headers, selected=selected)
        elif file_ext.lower() == ".xls":
            headers = kwargs.get("headers", None)
            selected = kwargs.get("selected", None)
            sheet = kwargs.get("sheet", 0)
            sheetname = kwargs.get("sheetname", None)
            dataset = open_xls(
                datasource,
                sheet=sheet,
                sheetname=sheetname,
                headers=headers,
                selected=selected,
            )
        else:
            feedback('Unable to process a file %s of type "%s"' % (filename, file_ext))
    return dataset


def grouper(n, iterable, fillvalue=None):
    """group and return sets

    See:
        http://stackoverflow.com/questions/2990121/~
        how-do-i-loop-through-a-python-list-by-twos

    Use:
        for item1, item2, item3 in grouper(3, 'ABCDEFG', 'x'):

    >>> list(grouper(3, 'ABCDEFG', 'x'))
    [('A', 'B', 'C'), ('D', 'E', 'F'), ('G', 'x', 'x')]
    """

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
    expr = ""
    for item in items:
        if item == "&" or item == "and" or item == "+":
            expr += " and "
        elif item == "|" or item == "or":
            expr += " or "
        elif item is not None:
            expr += "%s" % item
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
        items = string.split("`")
        if len(items) == 2:
            items.insert(1, "=")
        for item1, item2, item3, item4 in grouper(4, items):
            result.append([item1, item2, item3, item4])
        return result
    return [(None, None, None)]


def as_int(value, label, maximum=None, minimum=None) -> int:
    """Set a value to an int; or stop if an invalid value

    >>> as_int(value='3', label='N')
    3

    # below cannot be tested because of sys.exit() in feedback()
    # >>> as_int(value='3', label='N', minimum=4)
    # FEEDBACK:: z is
    # >>> as_int(value='3', label='N', maximum=2)
    # FEEDBACK:: z is
    # >>> as_int(value='z', label='N')
    # FEEDBACK:: z is not a valid N integer!
    # >>> as_int(value='3.1', label='N')
    # FEEDBACK:: 3.1 is not a valid N integer!
    """
    _label = f" for {label}" if label else ' of'
    try:
        the_value = int(value)
        if minimum and the_value < minimum:
            feedback(
                f"The value{_label} integer is less than the minimum of {minimum}!",
                True)
        if maximum and the_value > maximum:
            feedback(
                f"The value{_label} integer is more than the maximum of {maximum}!",
                True)
        return the_value
    except (ValueError, Exception):
        feedback(f"The {value}{label} is not a valid integer!", True)


def as_float(value, label, maximum=None, minimum=None) -> int:
    """Set a value to an float; or stop if an invalid value

    >>> as_float(value='3', label='N')
    3

    # below cannot be tested because of sys.exit() in feedback()
    # >>> as_float(value='3', label='N', minimum=4)
    # FEEDBACK:: z is
    # >>> as_float(value='3', label='N', maximum=2)
    # FEEDBACK:: z is
    # >>> as_float(value='z', label='N')
    # FEEDBACK:: z is not a valid N integer!
    # >>> as_float(value='3.1', label='N')
    # FEEDBACK:: The value of 3.1 for N is not a valid integer!
    """
    _label = f" for {label}" if label else ' of'
    try:
        the_value = float(value)
        if minimum and the_value < minimum:
            feedback(
                f"The {value}{_label} float is less than the minimum of {minimum}!",
                True)
        if maximum and the_value > maximum:
            feedback(
                f"The {value}{_label} float is more than the maximum of {maximum}!",
                True)
        return the_value
    except (ValueError, Exception):
        feedback(f"The {value}{label} is not a valid float!", True)


def tuple_split(string):
    """
    Split a string into a list of tuple values

    >>> print(tuple_split(''))
    []
    >>> print(tuple_split('3'))
    [(3.0,)]
    >>> print(tuple_split('3,4'))
    [(3.0, 4.0)]
    >>> print(tuple_split('3,5 6,1 4,2'))
    [(3.0, 5.0), (6.0, 1.0), (4.0, 2.0)]
    """
    values = []
    if string:
        try:
            _string_list = string.strip(" ").replace(";", ",").split(" ")
            for _str in _string_list:
                items = _str.split(",")
                _items = [float(itm) for itm in items]
                values.append(tuple(_items))
            return values
        except Exception:
            return values
    else:
        return values


def sequence_split(string):
    """
    Split a string into a list of individual values

    >>> sequence_split('')
    []
    >>> sequence_split('3')
    [3]
    >>> sequence_split('3,4,5')
    [3, 4, 5]
    >>> sequence_split('3-5,6,1-4')
    [1, 2, 3, 4, 5, 6]
    """
    values = []
    if string:
        try:
            _string = (
                string.replace(" ", "")
                .replace('"', "")
                .replace("'", "")
                .replace(";", ",")
            )
        except Exception:
            return values
    else:
        return values
    try:
        values.append(int(_string))
        return values
    except Exception:
        _strings = _string.split(",")
        # log.debug('strings:%s', _strings)
        for item in _strings:
            if "-" in item:
                _strs = item.split("-")
                seq_range = list(range(int(_strs[0]), int(_strs[1]) + 1))
                values = values + seq_range
            else:
                values.append(int(item))
    return list(set(values))  # unique


def splitq(seq, sep=None, pairs=("()", "[]", "{}"), quote="\"'"):
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
        lpair, _ = zip(*pairs)
        pairs = dict(pairs)
        start = index = 0
        while 0 <= index < len(seq):
            c = seq[index]
            if (sep and seq[index:].startswith(sep)) or (sep is None and c.isspace()):
                yield seq[start:index]
                # pass multiple separators as single one
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
                    raise IndexError("Unmatched quote %r\n%i:%s" % (c, p, seq[:p]))
            elif c in lpair:
                nesting = 1
                while True:
                    index += 1
                    p, index = index, seq.find(pairs[c], index)
                    if index < 0:
                        raise IndexError(
                            "Did not find end of pair for %r: %r\n%i:%s"
                            % (c, pairs[c], p, seq[:p])
                        )
                    nesting += "{lpair}({inner})".format(
                        lpair=c, inner=splitq(seq[p:index].count(c) - 2)
                    )
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
    if not filename:
        feedback("A valid CSV filename must be supplied!")

    dict_list = []
    _file_with_path = None
    norm_filename = os.path.normpath(filename)
    if not os.path.exists(norm_filename):
        filepath = script_path()
        _file_with_path = os.path.join(filepath, norm_filename)
        if not os.path.exists(_file_with_path):
            feedback(f'Unable to find CSV "{filename}", including in {filepath}')

    try:
        csv_filename = _file_with_path or norm_filename
        if headers:
            reader = csv.DictReader(open(csv_filename), fieldnames=headers)
        else:
            reader = csv.DictReader(open(csv_filename))
        for key, item in enumerate(reader):
            if not selected:
                dict_list.append(item)
            else:
                if key + 1 in selected:
                    dict_list.append(item)
    except IOError:
        feedback('Unable to find or open CSV "%s"' % csv_filename)
    return dict_list


def open_xls(filename, sheet=0, sheetname=None, headers=None, selected=None):
    """Read data from XLS file into a list of dictionaries

    Supply:

      * sheet to select a sheet number (otherwise first is used)
      * sheetname to select a sheet by name (otherwise first is used)
      * headers is a list of strings to use instead of the first row
      * selected is a list of desired rows e.g. [2,4,7]
    """
    def cleaned(value):
        if isinstance(value, float):
            if float(value) == float(int(value)):
                return int(value)
        # if isinstance(value, str):
        #     return value.encode('utf8')
        return value

    if not filename:
        feedback("A valid Excel filename must be supplied!")

    dict_list = []

    _file_with_path = None
    norm_filename = os.path.normpath(filename)
    if not os.path.exists(norm_filename):
        filepath = script_path()
        _file_with_path = os.path.join(filepath, norm_filename)
        if not os.path.exists(_file_with_path):
            feedback(f'Unable to find "{filename}", including in {filepath}')

    try:
        excel_filename = _file_with_path or norm_filename
        book = xlrd.open_workbook(excel_filename)
        if sheet:
            sheet = sheet - 1
            sheet = book.sheet_by_index(sheet)
        elif sheetname:
            sheet = book.sheet_by_name(sheetname)
        else:
            sheet = book.sheet_by_index(0)
        start = 1
        if not headers:
            keys = [sheet.cell(0, col_index).value for col_index in range(sheet.ncols)]
        else:
            start = 0
            keys = headers
        if len(keys) < sheet.ncols:
            feedback(
                'Too few headers supplied for the existing columns in "%s"' % filename
            )
        else:
            dict_list = []
            for row_index in range(start, sheet.nrows):
                item = {
                    keys[col_index]: cleaned(sheet.cell(row_index, col_index).value)
                    for col_index in range(sheet.ncols)
                }
                if not selected:
                    dict_list.append(item)
                else:
                    if row_index + 1 in selected:
                        dict_list.append(item)
    except IOError:
        feedback('Unable to find or open Excel "%s"' % excel_filename)
    except IndexError:
        feedback('Unable to open sheet "%s"' % (sheet or sheetname))
    except xlrd.biffh.XLRDError:
        feedback('Unable to open sheet "%s"' % sheetname)
    return dict_list


def flatten(lst):
    """Flatten nested lists into a single list of lists.

    >>> list(flatten([[1, 2], [3,4, [5,6]]]))
    [1, 2, 3, 4, 5, 6]
    """
    try:
        for ele in lst:
            if isinstance(ele, collections.abc.Iterable) and not isinstance(ele, str):
                for sub in flatten(ele):
                    yield sub
            else:
                yield ele
    except TypeError:
        yield lst


def comparer(val, operator, target):
    """target could be list?? - split a string by , or ~

    >>> comparer(None, None, None)
    True
    >>> comparer("1", '*', "1")
    FEEDBACK:: Unknown operator: * (1.0 and 1.0)
    False
    >>> comparer("1", None, "1")
    True
    >>> comparer("a", None, "a")
    True
    >>> comparer("True", None, "True")
    True
    >>> comparer("False", None, "False")
    True
    >>> comparer("1", '<', "1.1")
    True
    >>> comparer("a", '<', "aa")
    True
    >>> comparer("True", '<', "True")
    False
    >>> comparer("False", '<', "False")
    False
    >>> comparer("1", '~', "1.1")
    False
    >>> comparer("a", '~', "aa")
    True
    >>> comparer("True", '~', "True")
    False
    >>> comparer("False", '~', "False")
    False
    >>> comparer("1", '~', [1,2,3])
    True
    """

    def to_length(val, target):
        """Get length of object."""
        try:
            val = len(val)
        except Exception:
            pass
        try:
            target = len(target)
        except Exception:
            pass
        return val, target

    if target == "T" or target == "True":
        target = True
    if target == "F" or target == "False":
        target = False
    if val == "T" or val == "True":
        val = True
    if val == "F" or val == "False":
        val = False

    if not operator:
        operator = "="
    if operator in ["<", "<=", ">", ">="]:
        val, target = to_length(val, target)

    try:
        val = float(val)
    except Exception:
        pass
    try:
        target = float(target)
    except Exception:
        pass
    if operator == "=":
        if val == target:
            return True
    elif operator == "~" or operator == "in":
        try:
            if val in target:
                return True
        except TypeError:
            pass
    elif operator == "!=":
        if val != target:
            return True
    elif operator == "<":
        if val < target:
            return True
    elif operator == ">":
        if val > target:
            return True
    elif operator == ">=":
        if val >= target:
            return True
    elif operator == "<=":
        if val <= target:
            return True
    else:
        feedback("Unknown operator: %s (%s and %s)" % (operator, val, target))
    return False


def color_to_hex(name):
    """Convert a named ReportLab color (Color class) to a hexadecimal string"""
    _tuple = (int(name.red * 255), int(name.green * 255), int(name.blue * 255))
    _string = "#%02x%02x%02x" % _tuple
    return _string.upper()


def alpha_column(num: int, lower: bool = False) -> string:
    """Convert a number to a letter-based notation

    Notes:
        * Encountered on a WarpWar map; numbers below 26 appear sequentially as
          a, b, c, etc, numbers above 26 appear sequentially as aa, bb, cc, etc; if
          above 52 then appear sequentially as aaa, bbb, ccc etc. Add more letters for
          each multiple of 26.
    """
    if lower:
        return string.ascii_lowercase[divmod(num - 1, 26)[1] % 26] * (divmod(num - 1, 26)[0] + 1)
    else:
        return string.ascii_uppercase[divmod(num - 1, 26)[1] % 26] * (divmod(num - 1, 26)[0] + 1)


def sheet_column(num: int, lower: bool = False) -> string:
    """Convert a spreadsheet number to a column letter

    Ref:
        https://stackoverflow.com/questions/23861680/
    """

    def converter(num, lower):
        if lower:
            return (
                ""
                if num == 0
                else converter((num - 1) // 26, lower)
                + string.ascii_lowercase[(num - 1) % 26]
            )
        else:
            return (
                ""
                if num == 0
                else converter((num - 1) // 26, lower)
                + string.ascii_uppercase[(num - 1) % 26]
            )

    return converter(num, lower)


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


if __name__ == "__main__":
    import doctest
    doctest.testmod()
