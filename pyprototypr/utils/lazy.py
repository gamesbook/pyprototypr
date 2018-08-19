#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Support classes
"""

DEBUG = False


class LazyEval(object):
    """Defer evaluation of a function.

    Usage:
        def foo(x):
            #print x
            return x

        random.choice((LazyEval(foo, "spam"), LazyEval(foo, "eggs")))()
        a = LazyEval(foo, "ham")
        a()   # execute it !
    """

    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.executed = False

    def __call__(self):
        return self.func(*self.args, **self.kwargs)

    def _exec(self):
        if not self.executed:
            self.value = self.func(*self.args, **self.kw)
            self.executed = True
        return self.value

    def __unicode__(self):
        return unicode(self._exec())

"""
def foo(x):
    #print x
    return x


a = LazyEval(foo, "spam")
a()   # execute it !

random.choice((LazyEval(foo, "spam"), LazyEval(foo, "eggs")))()
"""
