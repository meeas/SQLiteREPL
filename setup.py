#!/usr/bin/env python3

"""
SQLite Clinet written in python3
"""

# Always prefer setuptools over distutils
import re
import sys
# To use a consistent encoding
from codecs import open
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(

    name='sqlite',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.2.0',

    description='SQLite Clinet written in python3',

    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/nl253/SQLiteREPL',

    # Author details
    author='Norbert Logiewa',

    author_email='norbertlogiewa96\@gmail.com',

    # Choose your license
    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Database :: Front-Ends',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='database sqllite3 sqlite clinet SQLite prompt-toolkit prompt_toolkit',

    packages=find_packages(),

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html

    install_requires=['prompt_toolkit', 'tabulate', 'pygments'],

    entry_points={
        'console_scripts': ['sqlite = sqlite.main:main']
        })
