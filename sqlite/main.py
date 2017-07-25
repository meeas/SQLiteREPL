#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from argparse import ArgumentParser, Namespace
import pandas
import os

pandas.reset_option('expand_frame_repr')
pandas.set_option('max_colwidth', 160)
pandas.set_option('max_rows', 9999)

parser: ArgumentParser = ArgumentParser()

parser.add_argument('-d',
                    '--database',
                    '--db',
                    dest='database',
                    metavar='PATH',
                    default='~/.sqlite')

args: Namespace = parser.parse_args()


def main():

    import sqlite3
    from sqlite3 import Connection, Cursor
    from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
    from prompt_toolkit.history import InMemoryHistory
    from prompt_toolkit.shortcuts import prompt
    from .completer import MyCustomCompleter
    from .styling import PygmentsLexer, SqlLexer, custom_style

    connection: Connection = sqlite3.connect(os.path.expanduser(args.database))

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
            with connection:
                print(pandas.DataFrame(list(connection.execute(user_input))))

        except (sqlite3.Error, sqlite3.IntegrityError) as e:
            print("An error occurred:", e.args[0])


if __name__ == "__main__":
    main()

# vim: ft=python
