#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os.path
from argparse import ArgumentParser
import re

parser = ArgumentParser()

parser.add_argument('-d',
                    '--database',
                    '--db',
                    dest='database',
                    metavar='PATH',
                    default='~/.sqlite')

args = parser.parse_args()

db_path = os.path.expanduser(args.database)

def _regex(string: str, pattern: str) -> bool:
    return bool(re.compile(pattern).fullmatch(string))


conn = sqlite3.connect(db_path)
conn.create_function("regex", 2, _regex)
curr = conn.cursor()
query = curr.execute

import pandas

pandas.reset_option('expand_frame_repr')
pandas.set_option('max_colwidth', 160)
pandas.set_option('max_rows', 9999)

from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

from completer import MyCustomCompleter
from styling import custom_style, SqlLexer, PygmentsLexer

# initialise variables
user_input = ""

# used for fish-like history completion
history = InMemoryHistory()

while user_input != 'exit':
    # offer suggestions from history from history
    try:
        user_input = prompt('SQLite >> ',
                            history=history,
                            multiline=False,
                            auto_suggest=AutoSuggestFromHistory(),
                            lexer=PygmentsLexer(SqlLexer),
                            style=custom_style,
                            completer=MyCustomCompleter())
    except (EOFError,KeyboardInterrupt) as e:
        break

    try:
        q = query(user_input)
        print(pandas.DataFrame(list(q)))

    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])


conn.commit()
curr.close()
conn.close()
