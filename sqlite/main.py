#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from argparse import ArgumentParser, Namespace
import os
import tabulate

parser: ArgumentParser = ArgumentParser()

parser.add_argument('database',
                    help='path to database',
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

    while True:

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

        if user_input.lower() == '.quit' or user_input.lower() == 'exit':
            break
        elif user_input.lower() == '.tables':
            user_input = 'select name from sqlite_master where type = "table";'

        try:
            with connection:
                print(tabulate.tabulate(list(connection.execute(user_input)), tablefmt="orgtbl"))

        except (sqlite3.Error, sqlite3.IntegrityError) as e:
            print("An error occurred:", e.args[0])


if __name__ == "__main__":
    main()

# vim: ft=python
