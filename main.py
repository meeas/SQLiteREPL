#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser, Namespace
from completer import MyCustomCompleter
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.shortcuts import prompt
from sqlite3 import Cursor, Connection
from styling import custom_style, SqlLexer, PygmentsLexer
from typing import Callable, Optional, Any, Tuple
import os.path
import pandas
from pandas import DataFrame
import re
import sqlite3

parser = ArgumentParser()

parser.add_argument('-d',
                    '--database',
                    '--db',
                    dest='database',
                    metavar='PATH',
                    default='~/.sqlite')

args: Namespace = parser.parse_args()

db_path: str = os.path.expanduser(args.database)


def _regex(string: str, pattern: str) -> bool:
	return bool(re.compile(pattern).fullmatch(string))


conn: Connection = sqlite3.connect(db_path)
conn.create_function("regex", 2, _regex)
curr: Cursor = conn.cursor()
query: Callable[[str, Optional[Tuple[Any, ...]]], None] = curr.execute

pandas.reset_option('expand_frame_repr')
pandas.set_option('max_colwidth', 160)
pandas.set_option('max_rows', 9999)

# initialise variables
user_input: str = ""

# used for fish-like history completion
history: InMemoryHistory = InMemoryHistory()

while user_input != 'exit':
	# offer suggestions from history from history
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
		q: str = query(user_input)
		print(DataFrame(list(q)))

	except sqlite3.Error as e:
		print("An error occurred:", e.args[0])

conn.commit()
curr.close()
conn.close()
