#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from argparse import ArgumentParser, Namespace

import pandas
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.shortcuts import prompt

from .completer import MyCustomCompleter
from .styling import PygmentsLexer, SqlLexer, custom_style

def initialise_pandas():

    pandas.reset_option('expand_frame_repr')
    pandas.set_option('max_colwidth', 160)
    pandas.set_option('max_rows', 9999)


def parse() -> Namespace:

    parser = ArgumentParser()

    parser.add_argument('-d',
                        '--database',
                        '--db',
                        dest='database',
                        metavar='PATH',
                        default='~/.sqlite')

    return parser.parse_args()


def main():

    initialise_pandas()

    args = parse()

    connection: Connection = sqlite3.connect(args.database)

    # initialise variables
    user_input: str = ""

    # used for fish-like history completion
    history: InMemoryHistory = InMemoryHistory()

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

        except (EOFError, KeyboardInterrupt) as e:
            break

        try:
            with connection:
                print(pandas.DataFrame(list(connection.execute(user_input))))

        except (sqlite3.Error, sqlite3.IntegrityError) as e:
            print("An error occurred:", e.args[0])


if __name__ == '__main__':
    main()

# vim: ft=python
