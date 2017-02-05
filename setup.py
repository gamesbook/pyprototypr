from __future__ import print_function
from setuptools import setup
from setuptools.command.test import test as TestCommand
import io
import os
import sys


here = os.path.abspath(os.path.dirname(__file__))


class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


def get_version():
    import re
    VERSIONFILE = 'pyprototypr/_version.py'
    verstrline = open(VERSIONFILE, "rt").read()
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    mo = re.search(VSRE, verstrline, re.M)
    if mo:
        version_string = mo.group(1)
    else:
        raise RuntimeError('Unable to find version string in %s.' %
                           (VERSIONFILE,))
    return version_string


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as _file:
            buf.append(_file.read())
    return sep.join(buf)

VERSION = get_version()
LONG_DESCRIPTION = read('README.rst', 'CHANGES.txt')

setup(
    name='pyprototypr',
    version=VERSION,
    author='Derek Hohls',
    author_email='gamesbook@gmail.com',
    url='http://github.com/gamesbook/pyprototypr/',
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
    description='Python utility for designing and creating simple, regular,'
                '  graphic outputs',
    long_description=LONG_DESCRIPTION,
    packages=['pyprototypr'],
    include_package_data=True,
    test_suite='pyprototypr.test',
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 1 - Alpha',
        'Natural Language :: English',
        'Environment :: Desktop Environment',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Games/Entertainment :: Board Games',
        'Topic :: Multimedia :: Graphics :: Presentation'
        ],
    platforms='any',
    license='MIT License',
    extras_require={
        'testing': ['pytest'],
    }
)
