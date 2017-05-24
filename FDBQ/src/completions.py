#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prompt_toolkit.document import Document
from prompt_toolkit.completion import Completion
from typing import List
import os
from glob import iglob
import itertools
# from main import curr

sql_commands = {
    'ABORT',
    'ACTION',
    'ADD',
    'AFTER',
    'ALL',
    'ALTER TABLE',
    'ALTER DATABASE',
    'AND',
    'ASC',
    'ANALYZE',
    'ATTACH DATABASE',
    'AUTOINCREMENT',
    'BEFORE',
    'BEGIN TRANSACTION',
    'BEGIN',
    'BETWEEN',
    'BY',
    'CASCADE',
    'CASE',
    'CAST',
    'CHECK',
    'COLLATE',
    'COLUMN',
    'COMMIT TRANSACTION',
    'CONFLICT',
    'CONSTRAINT',
    'CREATE INDEX',
    'CREATE TABLE',
    'CREATE TRIGGER',
    'CREATE VIEW',
    'CREATE VIRTUAL TABLE',
    'CROSS',
    'CURRENT_DATE',
    'CURRENT_TIME',
    'CURRENT_TIMESTAMP',
    'DATABASE',
    'DEFAULT',
    'DEFERRABLE',
    'DEFERRED',
    'DELETE',
    'DESC',
    'DETACH',
    'DISTINCT',
    'DROP INDEX',
    'DROP TABLE',
    'DROP TRIGGER',
    'DROP VIEW',
    'EACH',
    'ELSE',
    'END',
    'ESCAPE',
    'EXCEPT',
    'EXCLUSIVE',
    'EXISTS',
    'EXPLAIN',
    'FAIL',
    'FOR',
    'FOREIGN',
    'FROM',
    'FULL',
    'GROUP BY',
    'HAVING',
    'IF',
    'IGNORE',
    'IMMEDIATE',
    'IN',
    'INDEX',
    'INDEXED BY',
    'INITIALLY',
    'INNER',
    'INSERT INTO',
    'INSTEAD',
    'INTERSECT',
    'INTO',
    'IS',
    'ISNULL',
    'JOIN',
    'KEY',
    'LAST_INSERT_ROWID()',
    'LEFT',
    'LIKELIHOOD(',
    'LIKELY(',
    'LIMIT',
    'MATCH',
    'NATURAL',
    'NO',
    'NOT',
    'NOTNULL',
    'NULLIF(',
    'OF',
    'OFFSET',
    'ON CONFLICT',
    'ON',
    'OR',
    'ORDER BY',
    'OUTER',
    'PLAN',
    'PRAGMA',
    'PRIMARY',
    'PRINTF(',
    'QUERY',
    'QUOTE(',
    'RAISE',
    'RECURSIVE',
    'REFERENCES',
    'REGEXP',
    'REINDEX',
    'RELEASE SAVEPOINT',
    'RENAME',
    'RESTRICT',
    'RIGHT',
    'ROLLBACK',
    'ROW',
    'SAVEPOINT',
    'SELECT',
    'SET',
    'TABLE',
    'TEMP',
    'TEMPORARY',
    'THEN',
    'TO',
    'TRANSACTION',
    'TRIGGER',
    'UNION',
    'UNIQUE',
    'UPDATE',
    'USING',
    'VACUUM',
    'VALUES(',
    'VIEW',
    'VIRTUAL',
    'WHEN',
    'WHERE',
    'WITH',
    'WITHOUT'}

sql_tables = {'sqlite_master'}

sql_dtypes = {
    'TEXT',
    'INTEGER',
    'NULL',
    'BLOB',
    'REAL'
}

sql_numeric = {
    'NUMERIC'
    'DECIMAL(10,5)',
    'BOOLEAN',
    'DATE',
    'DATETIME'
}

sql_integer = {
    'INT',
    'MEDIUMINT',
    'SMALLINT',
    'BIGINT',
    'INT2',
    'INT8',
    'TINYINT',
    'UNSIGNED BIG INT'
}

sql_real = {
    'DOUBLE',
    'FLOAT',
    'DOUBLE PRECISION'
}

sql_text = {
    'CHARACTER(20)',
    'VARCHAR(255)',
    'VARYING CHARACTER(255)',
    'NCHAR(255)',
    'NATIVE CHARACTER(70)',
    'CLOB',
    'NVARCHAR(100)'
}

sql_functions = {
    'ABS(',
    'CHANGES(',
    'CHAR(',
    'COALESCE(',
    'GLOB(',
    'HEX(',
    'IFNULL(',
    'INSTR(',
    'LAST_INSERT_ROWID(',
    'LENGTH(',
    'LIKE(',
    'LIKELIHOOD(',
    'LIKELY(',
    'LOAD_EXTENSION(',
    'LOWER(',
    'LTRIM(',
    'MAX(',
    'MIN(',
    'NULLIF(',
    'PRINTF(',
    'QUOTE(',
    'RANDOM(',
    'RANDOMBLOB(',
    'REPLACE(',
    'ROUND(',
    'RTRIM(',
    'SOUNDEX(',
    'SQLITE_COMPILEOPTION_GET(',
    'SQLITE_COMPILEOPTION_USED(',
    'SQLITE_SOURCE_ID(',
    'SQLITE_VERSION()',
    'SUBSTR(',
    'TOTAL_CHANGES(',
    'TRIM(',
    'TYPEOF(',
    'UNICODE(',
    'UNLIKELY(',
    'UPPER(',
    'ZEROBLOB('}


def dir_completions(document: Document) -> List[Document]:
    nodes = itertools.chain(iglob('./*'), iglob('*'))
    dirs = filter(os.path.isdir, nodes)
    completions = [Completion(i, start_position=document.find_boundaries_of_current_word(WORD=True)[0], display_meta="dir") for i in dirs]
    return completions


def file_completions(document: Document) -> List[Completion]:
    nodes = itertools.chain(iglob('./*'), iglob('*'))
    files = filter(os.path.isfile, nodes)
    completions = [Completion(i, start_position=document.find_boundaries_of_current_word(WORD=True)[0], display_meta="file") for i in files]
    return completions


def sql_completions(document: Document) -> List[Completion]:
    commands = [Completion(i, start_position=document.find_boundaries_of_current_word(
        WORD=True)[0], display_meta="command") for i in sql_commands]
    tables = [Completion(i, start_position=document.find_boundaries_of_current_word(
        WORD=True)[0], display_meta="table") for i in sql_tables]
    functions = [Completion(i, start_position=document.find_boundaries_of_current_word(
        WORD=True)[0], display_meta="function") for i in sql_functions]
    dtypes = [Completion(i, start_position=document.find_boundaries_of_current_word(
        WORD=True)[0], display_meta="data type") for i in sql_dtypes]
    numeric = [Completion(i, start_position=document.find_boundaries_of_current_word(
        WORD=True)[0], display_meta="numeric (alias)") for i in sql_numeric]
    text = [Completion(i, start_position=document.find_boundaries_of_current_word(
        WORD=True)[0], display_meta="text (alias)") for i in sql_text]
    real = [Completion(i, start_position=document.find_boundaries_of_current_word(
        WORD=True)[0], display_meta="real (alias)") for i in sql_real]
    integer = [Completion(i, start_position=document.find_boundaries_of_current_word(
        WORD=True)[0], display_meta="integer (alias)") for i in sql_integer]
    return commands + tables + functions + integer + numeric + real + text + dtypes


