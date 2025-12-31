from typing import NamedTuple
from dataclasses import dataclass, field
from enum import Enum

class Position(NamedTuple):
    line: int
    column: int

class TokenKind(Enum):
    STRING      = 'string'
    IDENTIFIER  = 'identifier'
    COMMENT     = 'comment'

    DOT         = '.'
    AT_SIGN     = '@'
    HASH_SIGN   = '#'
    DOLLAR_SIGN = '$'
    ASTERISK    = '*'
    COLON       = ':'
    SEMICOLON   = ';'
    LEFT_BRACE  = '{'
    RIGHT_BRACE = '}'

    EOF         = 'end of file'

@dataclass
class Token():
    position: Position
    kind:     TokenKind
    value:    str       = field(default_factory=str)
