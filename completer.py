#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shlex
from typing import List

from prompt_toolkit.completion import Completer
from prompt_toolkit.document import Document
from completions import sql_completions


class MyCustomCompleter(Completer):
    def get_completions(self, document: Document, complete_event):
        try:
            # line: str = document.current_line
            args: List[str] = shlex.split(document.current_line)
            if len(args) > 0:
                curr_word: str = document.get_word_under_cursor(WORD=True)
                # first_word: str = shlex.split(document.current_line)[0]
                # previous_word: str = shlex.split(document.current_line_before_cursor)[
                # 	len(shlex.split(document.current_line_before_cursor)) - 1]

                for i in sql_completions(document):
                    if i.text.startswith(curr_word.upper()) or i.text.startswith(curr_word):
                        yield i


        except (NameError, ValueError):
            pass
