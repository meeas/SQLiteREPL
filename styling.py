
from prompt_toolkit.layout.lexers import PygmentsLexer
from prompt_toolkit.styles import style_from_pygments
from pygments.lexers import SqlLexer
from pygments.styles.tango import TangoStyle
from pygments.token import Token

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
