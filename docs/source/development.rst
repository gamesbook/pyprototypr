===========
Development
===========

These notes are aimed at those who might be developing the code further,
or who want to use :doc:`protograf <index>` as part of other Python
projects.


Coding
======

In general, follow the `Zen of Python <https://peps.python.org/pep-0020/>`_ ...
but also try to follow the style of the code in the rest of the project.

Note, however, that this project "breaks" a few normal conventions:

- Use of ``global`` variables in the ``proto.py`` file
- Extensive use of ``**kwargs**`` for the various shapes which means that a user
  could pass in a key+value setting that simply gets ignored without raising an
  error; this could be improved by creating numerous subclasses with a more
  extensive inheritance framework, but these soon start getting tricky to
  juggle...
- Use of ``from protograf import *`` for running scripts; you could force a
  user to import only what they need but that makes it really tedious for them,
  and much harder to do if you're not a programmer;  if you are using it as
  part of another project, then of course you should follow the normal approach
  of only importing exactly what you need!


Documentation
=============

Documents are written in reStructuredText. Some helpful web resources:

- https://github.com/DevDungeon/reStructuredText-Documentation-Reference - guide
- https://docutils.sourceforge.io/docs/user/rst/quickstart.html - quick start
- https://docutils.sourceforge.io/docs/user/rst/quickref.html - detailed summary
- https://jwodder.github.io/kbits/posts/rst-hyperlinks/ - all about links
- https://docutils.sourceforge.io/docs/ref/rst/directives.html - directives

Some useful tools:

- https://github.com/retext-project/retext - a reStructuredText editor
- https://github.com/mgedmin/restview - a reStructuredText viewer in your browser
  (but currently does not support Sphinx directives)
