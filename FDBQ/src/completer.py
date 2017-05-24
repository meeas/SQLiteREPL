#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shlex
from prompt_toolkit.completion import Completer
from prompt_toolkit.document import Document
from completions import file_completions, sql_completions

class MyCustomCompleter(Completer):
    def get_completions(self, document: Document, complete_event):
        try:
            line = document.current_line
            args = shlex.split(document.current_line)
            if len(args) > 0:
                curr_word = document.get_word_under_cursor(WORD=True)
                first_word = shlex.split(document.current_line)[0]
                previous_word = shlex.split(document.current_line_before_cursor)[len(shlex.split(document.current_line_before_cursor)) - 1]

                for i in file_completions(document):
                    if i.text.startswith(curr_word):
                        yield i

                for i in sql_completions(document):
                    if i.text.startswith(curr_word.upper()) or i.text.startswith(curr_word):
                        yield i


        except (ValueError, NameError):
            pass
