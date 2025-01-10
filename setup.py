"""
Setup for pyprototypr
"""
import ast
import io
import os
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


here = os.path.abspath(os.path.dirname(__file__))


class PyTest(TestCommand):
    """Wrapper for test runs."""

    def __init__(self):
        super(PyTest).__init__()
        self.test_args = None
        self.test_suite = None


    def finalize_options(self):
        """."""
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        """."""
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


def get_version():
    """."""
    try:
        version_file = 'pyprototypr/_version.py'
        with open(version_file, "rt") as vf:
            verstrline = vf.readlines()[0]
        _ver = verstrline.split('__version_info__ = ')
        version_tuple = ast.literal_eval(_ver[1])
        version_string = '.'.join(map(str, version_tuple))
        return version_string
    except Exception:
        raise RuntimeError(
            f'Unable to find version string in {version_file}.')


def read(*filenames, **kwargs):
    """."""
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as _file:
            buf.append(_file.read())
    return sep.join(buf)


VERSION = get_version()
LONG_DESCRIPTION = read('README.md', 'CHANGES.txt')

setup(
    name='pyprototypr',
    version=VERSION,
    author='Derek Hohls',
    author_email='gamesbook@gmail.com',
    url='http://github.com/gamesbook/pyprototypr/',
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
    description='Python utility for designing and creating simple, regular,'
                ' graphic outputs as PDF files',
    long_description=LONG_DESCRIPTION,
    packages=find_packages(exclude=['dist', 'build', 'docs', 'examples']),
    include_package_data=True,
        install_requires=[
            'reportlab', 'xlrd', 'bgg-api', 'svglib', 'lxml', 'Jinja2', 'pymupdf'],
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GPL License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Games/Entertainment :: Board Games',
        'Topic :: Multimedia :: Graphics :: Presentation'
        ],
    platforms='any',
    license='GPL 3.0 License',
)
