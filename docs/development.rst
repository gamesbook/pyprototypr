===========
Development
===========

Coding
======

In general, follow the `Zen of Python <https://peps.python.org/pep-0020/>`_ ...

Note, however, that this project "breaks" a few normal conventions:

- Use of ``global`` variables in the ``proto.py`` file
- Extensive use of ``**kwargs**`` for the various shapes which means that a user 
  could pass in a key+value setting that simply gets ignored without raising an 
  error; this could be improved by creating numerous subclasses with a more 
  extensive inheritance framework, but...

Documentation
=============

Documents are written in reStructuredText. Some useful web resources:

- https://github.com/retext-project/retext - a reStructuredText editor
- https://github.com/pydanny/restructuredtext/blob/master/sphinx_tutorial.rst - Sphinx
- https://github.com/DevDungeon/reStructuredText-Documentation-Reference - guide
- https://docutils.sourceforge.io/docs/user/rst/quickstart.html - quick start
- https://docutils.sourceforge.io/docs/user/rst/quickref.html - detailed summary
- https://jwodder.github.io/kbits/posts/rst-hyperlinks/ - all about links
- https://docutils.sourceforge.io/docs/ref/rst/directives.html - directives
