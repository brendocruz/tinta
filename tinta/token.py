from dataclasses import dataclass, field
from enum import Enum

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
    kind:  TokenKind
    value: str       = field(default_factory=str)
