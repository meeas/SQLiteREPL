#!/usr/bin/env python
# -*- coding: utf-8 -*-

import typing
from typing import Tuple, Any, List, Callable, Iterable, Union
import sqlite3
from sqlite3 import Cursor, Connection
import os
from copy import copy
from itertools import islice

Row = Tuple[Union[str, float, int, None, bytes], ...]


def connect(db_path: str) -> Tuple[Connection, Cursor, Callable]:

    db_path = os.path.expanduser(db_path)

    connection = sqlite3.connect(db_path)

    cursor = connection.cursor()

    return (connection, cursor, cursor.execute)


def close_connection(connection: Connection):
    connection.commit()
    connection.close()


# performs the query quickly, saves the state and closes automatically
def quick_query(db_path: str, query_str: str) -> List[Row]:

    connection, cursor, query = connect(db_path)

    query(query_str)

    print(cursor.fetchall())

    close_connection(connection)


def drop_table(db_path: str, table_name: str):
    try:
        quick_query(db_path, "DROP TABLE {};".format(table_name))
        print("Existing {} table deleted".format(table_name))
    except:
        print("An exception occured, it's likely that the table '{}' didn't exist.".format(table_name))


def __determine_len(iterable: Iterable) -> int:
    return len(list(islice(iter(copy(iterable)), 0, 1))[0])


def insert_rows(rows: Iterable[Row], table_name: str, db_path: str) -> bool:

    connection, cursor, query = connect(db_path)

    # temp string
    q = ""

    # add to it ?, for each item in each row
    for i in range(__determine_len(rows) - 1):
        q += "?,"
        query_str = "INSERT INTO {} VALUES ({} ?)".format(table_name ,q)

    try:
        for row in rows:
            query(query_str, row)
        close_connection(connection)
        return True
    except:
        return False


def wipe_table(db_path: str, table_name: str) -> bool:
    try:
        quick_query(db_path, "DELETE FROM {}".format(table_name))
        return True
    except:
        print("An error occured. The table might not exist.")
        return False



