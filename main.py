#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import sqlite3
import sys
from argparse import ArgumentParser, Namespace

from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.layout.lexers import PygmentsLexer
from prompt_toolkit.shortcuts import prompt
from pygments.lexers.sql import SqlLexer

from completer import MyCustomCompleter
from db import SQLite
from styling import custom_style

parser = ArgumentParser()

parser.add_argument('-d',
                    '--database',
                    '--db',
                    dest='database',
                    metavar='PATH',
                    default='~/.sqlite')

parser.add_argument('-e',
                    '--script',
                    dest='script',
                    metavar='PATH')

args: Namespace = parser.parse_args()

db = SQLite(args.database)

if args.script:
    assert os.path.isfile(args.script), \
        f'{args.script} doesn\'t seem to exist.'

    db.execute_script(args.script)
    print(f'The script located at {args.script}')
    sys.exit()


# initialise variables
user_input: str = ""

# used for fish-like history completion,
# offer suggestions from history from history
history: InMemoryHistory = InMemoryHistory()

while user_input != 'exit':

    try:
        user_input: str = prompt('SQLite >> ',
                                 history=history,
                                 multiline=False,
                                 auto_suggest=AutoSuggestFromHistory(),
                                 lexer=PygmentsLexer(SqlLexer),
                                 style=custom_style,
                                 completer=MyCustomCompleter())
    except (EOFError, KeyboardInterrupt) as e:
        break

    try:
        db.query(user_input)
        db.pprint_results()


    except sqlite3.Error as e:
        print(f"The following error occurred: {e.args[0]}")

# on break commit
db.close_connection()
