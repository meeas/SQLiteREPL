#!/usr/bin/env python
# -*- coding: utf-8 -*-

# NO DEPENDENCIES

"""High level, simple convenience wrapper for sqlite3 from the standard library.
"""

import os
import re
import sqlite3
from copy import copy
from itertools import islice
from typing import Tuple, Union, Iterable, Optional, Any

import pandas
from pandas import DataFrame, Series

pandas.reset_option('expand_frame_repr')
pandas.set_option('max_colwidth', int(os.get_terminal_size()[0] * 4 / 10))
pandas.set_option('max_rows', os.get_terminal_size()[1] * 2)

SQLiteDataType = Union[str, float, int, None, dict, set]
Row = Tuple[SQLiteDataType, ...]

for t in [dict, set, tuple, DataFrame, Series]:
    sqlite3.register_adapter(t, str)

# Helper functions
def _regex(string: str, pattern: str) -> bool:
    return bool(re.compile(pattern).fullmatch(string))


def validate_row(*data) -> Optional[bool]:
    """
    Test input befor performing queries such as inserion.
    For example,
    >>> # Valid input
    >>> sample_input: Row = (11, "somthing", None, 211.22)
    >>> validate_row(sample_input)
    True
    >>> # Now invalid input
    >>> sample_input: Tuple[Series, Series, Series, Series] = (Series([]), Series([]), Series([]), Series([]))
    >>> validate_row(sample_input)
    False
    """
    for datum in data:
        if type(datum) not in [str, float, None, int, dict, set]:
            print('SQLite only works with floats, ints, strings and None.')
            raise sqlite3.Error
    return True


def _determine_format(sample_row: Row) -> str:
    """
    Enables to add data to a table without using the (?, ?, ?, ... ) notation.
    It outputs the (?, ?, ?, ... ) with as many quesionmarks as are needed to insert.
    To do that it takes as a parameter a row and creates it's copy.
    Using it's length is creates a string with approparate format.

    For example,

    >>> row: Row = (1, None, 'Something', 'Someone')
    >>> _determine_format(row)
    '(?, ?, ?, ?)'
    """
    head: str = "("
    tail: str = ""
    middle: str = "?)"
    # because the last question mark is provided only iterate until n-1
    for _ in range(len(copy(sample_row)) - 1):
        middle += "?, "
    return head + middle + tail


class SQLite:
    def __init__(self, db_path='~/.sqlite'):
        # path to the database, expand just in case
        self._db = os.path.expandvars(os.path.expanduser(db_path))
        self._connection = sqlite3.connect(self._db)
        # add regexp to SQLite (not available normally)
        self._connection.create_function("regex", 2, _regex)
        self._cursor = self._connection.cursor()

    def close_connection(self):
        self._connection.commit()
        self._connection.close()

    # performs the query quickly, saves the state automatically
    def query(self, query_str: str, data: Row = None, pprint_results=True, commit=True):
        if data:
            if validate_row(data):
                self._cursor.execute(query_str, data)
            else:
                print("Bad data type. Aborting.")
                raise sqlite3.Error
        else:
            self._cursor.execute(query_str)

        if commit:
            self.commit()

        if pprint_results:
            self.pprint_results()

    def pprint_results(self):
        results = self._cursor.fetchall()
        if all(map(bool, results)):
            df = DataFrame(results)
            if len(df) > 0:
                print(df)

    @property
    def busy(self) -> bool:
        return self._connection.in_transaction

    def create_table(self, table_name, commit=True,
                     delete_existing=True):
        """
        Convenience method to create a table with a given name,
        optionally you can specify that an existing table with the same name would be deleted.
        """
        try:
            self.query(f"CREATE TABLE {table_name}", commit=commit)
        except sqlite3.Error:
            if delete_existing:
                self.drop_table(table_name=table_name, commit=commit)
                self.create_table(table_name, commit, delete_existing=False)
            else:
                raise sqlite3.Error

    def drop_table(self,
                   table_name: str,
                   commit=True):
        self.query(f"DROP TABLE {table_name}", commit=commit)

    def insert(self, row: Row, table_name: str, commit: bool = True):
        """
        Insert a single row into a table.
        """
        self.query(f"INSERT INTO {table_name} VALUES {_determine_format(row)}",
                   data=row, commit=commit)

    def insert_many(self, rows: Iterable[Row], table_name: str,
                    commit: bool = True):
        """
        Add many rows to a specified table.
        Commit only after all rows have been successfully added,
        check that they are all of the same length.
        Use insert() as a helper method.
        """
        len_first: int = len(list(islice(copy(rows), 0, 1)))
        # make sure all rows are of the same size
        # do this by comparing to the length of the first one
        assert all(map(lambda row: len(row) == len_first, copy(rows))), \
            "Rows have different sizes."

        self._cursor.executemany(
            f"INSERT INTO {table_name} VALUES {_determine_format(islice(rows ,0 , 1))}",
            rows)

        if commit:
            self.commit()

    def clear_table(self, table_name: str, commit=True):
        self.query(f"DELETE FROM {table_name}", commit=commit)

    def rollback(self):
        self._connection.rollback()

    def execute_script(self, script_path: Union[bytes, str],
                       commit: bool = True):
        """
        Execute an SQL script from a text file.
        You need to specify the path.
        """
        assert os.path.isfile(script_path), \
            "The path doesn't point to an existing file."
        with open(os.path.expanduser(script_path), encoding="utf-8") as f:
            text: str = f.read()

        self._cursor.executescript(text)

        if commit:
            self.commit()

    def commit(self):
        self._connection.commit()
