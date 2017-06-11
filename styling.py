#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygments.token import Token
from prompt_toolkit.styles import style_from_pygments
from pygments.styles.tango import TangoStyle

custom_style = style_from_pygments(TangoStyle, {
    Token.Comment:   '#888888 bold',
    Token.Name:   '#888888 bold',
    Token.Operator:   '#888888 bold',
    Token.Generic:   '#888888 bold',
    Token.Other:   '#888888 bold',
    Token.Number:   '#ff9900 bold',
    Token.Literal:   '#888888 bold',
    Token.String:   '#00cc00 bold',
    Token.Keyword:   '#ff00ff bold'})
