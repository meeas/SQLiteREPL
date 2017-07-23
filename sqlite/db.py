
# NO DEPENDENCIES

"""High level, simple convenience wrapper for sqlite3 from the standard library.
"""

import os
import re
import sqlite3
from typing import Tuple, Union, Any


Row = Tuple[Union[str, float, int, None], ...]


def _regex(string: str, pattern: str) -> bool:
    return bool(re.compile(pattern).fullmatch(string))


class SQLite():
    def __init__(self, db_path='~/.sqlite'):
        self._location = os.path.expanduser(db_path)
        self._connection = sqlite3.connect(self._location)
        self._connection.create_function("regex", 2, _regex)
        self._cursor = self._connection.cursor()

    @property
    def location(self) -> str:
        return self._location


    def close_connection(self) -> bool:
        try:
            self.commit()
            self._connection.close()
            return True
        except:
            print("Something went wrong.")
            return False

    def commit(self):
        self._connection.commit()

    # performs the query quickly, saves the state automatically
    def query(self,
            query_str: str,
            pprint_results=True,
            data=None,
            commit=True):

        try:

            if data:
                self._cursor.execute(query_str, data)
            else:
                self._cursor.execute(query_str)

            if commit:
                self.commit()

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
