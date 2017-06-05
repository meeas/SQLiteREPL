#!/usr/bin/env python
# -*- coding: utf-8 -*-

# NO DEPENDENCIES

"""High level, simple convenience wrapper for sqlite3 from the standard library.
"""

import os
import re
import sqlite3
from typing import Tuple, Union

Row = Tuple[Union[str, float, int, None], ...]

def _regex(string: str, pattern: str) -> bool:
    return bool(re.compile(pattern).fullmatch(string))


class SQLite():
    def __init__(self, db_path='~/.sqlite'):
        self._db = os.path.expanduser(db_path)
        self._connection = sqlite3.connect(self._db)
        self._connection.create_function("regex", 2, _regex)
        self._cursor = self._connection.cursor()

    def close_connection(self) -> bool:
        try:
            self._connection.commit()
            self._connection.close()
            return True
        except:
            print("Something went wrong.")
            return False

    # performs the query quickly, saves the state automatically
    def query(self, query_str: str, data=None, pprint_results=True, commit=True):

        try:

            if data:
                self._cursor.execute(query_str, data)
            else:
                self._cursor.execute(query_str)

            if commit:
                self._connection.commit()

            if pprint_results:
                for row in self._cursor.fetchall():
                    if row:
                        print(row)
            return True

        except Exception as e:
            print(f"{e} occured.")
            return False

    @property
    def busy(self) -> bool:
        return self._connection.in_transaction
