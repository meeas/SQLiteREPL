#!/usr/bin/env python
# -*- coding: utf-8 -*-

import typing
from typing import Tuple, List, Callable, Iterable, Union
import sqlite3
from sqlite3 import Cursor, Connection
from pandas import DataFrame
import os
from logging.config import dictConfig
from os.path import expanduser
from json import load

dictConfig(load(open(expanduser('~/.python/logging.json'))))

Row = Tuple[Union[str, float, int, None], ...]

def connect(db_path: str) -> Tuple[Connection, Cursor, Callable]:

    db_path = os.path.expanduser(db_path)

    connection = sqlite3.connect(db_path)

    cursor = connection.cursor()

    return (connection, cursor, cursor.execute)


def close_connection(connection: Connection) -> bool:
    try:
        connection.commit()
        connection.close()
    except:
        print("Something went wrong.")
        return False


# performs the query quickly, saves the state and closes automatically
def quick_query(db_path: str, query_str: str) -> List[Row]:

    connection, cursor, query = connect(db_path)

    query(query_str)

    print(cursor.fetchall())

    close_connection(connection)


def create_table(rows: Iterable[Row], table_name: str, db_path: str, col_names: list, delete_existing=False) -> bool:

    connection, cursor, query = connect(db_path)

    DataFrame(rows, columns=col_names).to_sql(table_name, connection,
                                              if_exists='replace' if delete_existing else 'fail')

    close_connection(connection)
