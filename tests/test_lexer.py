import pytest
from pytest import param, mark
from tinta.lexer import Lexer
from tinta.error import LexerError
from tinta.token import Token, TokenKind

parametrize = mark.parametrize

chars = ['a', 'Z', 'é', '1', '_', '-', ':', '']
ids   = ['lowercase_alpha',
         'uppercase_alpha',
         'accented_alpha',
         'digit',
         'underscore',
         'hyphen',
         'punctuation',
         'empty_string']

expecteds = [True, True, False, False, False, False, False, False]
@parametrize('character,expected', zip(chars, expecteds), ids=ids)
def test_is_ascii_letter(character, expected):
    lexer    = Lexer()
    observed = lexer.is_ascii_letter(character)
    assert expected == observed

expecteds = [False, False, False, True, False, False, False, False]
@parametrize('character,expected', zip(chars, expecteds), ids=ids)
def test_is_digit(character, expected):
    lexer    = Lexer()
    observed = lexer.is_digit(character)
    assert expected == observed

expecteds = [True, True, False, False, True, False, False, False]
@parametrize('character,expected', zip(chars, expecteds), ids=ids)
def test_is_ascii_letter_or_underscore(character, expected):
    lexer    = Lexer()
    observed = lexer.is_ascii_letter_or_underscore(character)
    assert expected == observed

expecteds = [True, True, False, True, True, False, False, False]
@parametrize('character,expected', zip(chars, expecteds), ids=ids)
def test_is_ascii_letter_digit_or_underscore(character, expected):
    lexer    = Lexer()
    observed = lexer.is_ascii_letter_digit_or_underscore(character)
    assert expected == observed

expecteds = [True, True, False, True, True, True, False, False]
@parametrize('character,expected', zip(chars, expecteds), ids=ids)
def test_is_ascii_letter_digit_underscore_or_hyphen(character, expected):
    lexer    = Lexer()
    observed = lexer.is_ascii_letter_digit_underscore_or_hyphen(character)
    assert expected == observed

def test_at_eof_returns_false_until_reaches_stream_end():
    lexer = Lexer('ab')

    expected = False
    observed = lexer.at_eof()
    assert expected == observed

    lexer.pop_char()
    expected = False
    observed = lexer.at_eof()
    assert expected == observed

    lexer.pop_char()
    expected = True
    observed = lexer.at_eof()
    assert expected == observed

    lexer.pop_char()
    expected = True
    observed = lexer.at_eof()
    assert expected == observed

def test_next_char_returns_character_at_current_offset():
    stream = 'html'
    lexer  = Lexer(stream)

    expected = 'h'
    observed = lexer.next_char()
    assert expected == observed

    expected = 't'
    observed = lexer.next_char()
    assert expected == observed

    expected = 'm'
    observed = lexer.next_char()
    assert expected == observed

    expected = 'l'
    observed = lexer.next_char()
    assert expected == observed

    expected = ''
    observed = lexer.next_char()
    assert expected == observed

    expected = ''
    observed = lexer.next_char()
    assert expected == observed

def test_pop_char_advances_stream_offset_and_position():
    stream = 'ab\ncd\nef'
    lexer  = Lexer(stream)

    expected = [(1, 1), 0]
    observed = [lexer.get_position(), lexer.get_offset()]
    assert expected == observed

    lexer.pop_char()
    expected = [(1, 2), 1]
    observed = [lexer.get_position(), lexer.get_offset()]
    assert expected == observed

    lexer.pop_char()
    expected = [(2, 1), 2]
    observed = [lexer.get_position(), lexer.get_offset()]
    assert expected == observed

    lexer.pop_char()
    expected = [(2, 2), 3]
    observed = [lexer.get_position(), lexer.get_offset()]
    assert expected == observed

    lexer.pop_char()
    expected = [(2, 3), 4]
    observed = [lexer.get_position(), lexer.get_offset()]
    assert expected == observed

    lexer.pop_char()
    expected = [(3, 1), 5]
    observed = [lexer.get_position(), lexer.get_offset()]
    assert expected == observed

    lexer.pop_char()
    expected = [(3, 2), 6]
    observed = [lexer.get_position(), lexer.get_offset()]
    assert expected == observed

    lexer.pop_char()
    expected = [(3, 3), 7]
    observed = [lexer.get_position(), lexer.get_offset()]
    assert expected == observed

    lexer.pop_char()
    expected = [(3, 4), 8]
    observed = [lexer.get_position(), lexer.get_offset()]
    assert expected == observed

def test_peek_char_returns_character_at_stream_start():
    stream = 'xml'
    lexer  = Lexer(stream)

    expected = 'x'
    observed = lexer.peek_char()
    assert expected == observed
    observed = lexer.peek_char()
    assert expected == observed
    observed = lexer.peek_char()
    assert expected == observed

def test_peek_char_returns_character_at_stream_end():
    stream = 'xml'
    lexer  = Lexer(stream)

    lexer.pop_char()
    lexer.pop_char()
    lexer.pop_char()

    expected = ''
    observed = lexer.peek_char()
    assert expected == observed
    observed = lexer.peek_char()
    assert expected == observed
    observed = lexer.peek_char()
    assert expected == observed

def test_peek2_char_returns_second_character_at_stream_start():
    stream = 'xml'
    lexer  = Lexer(stream)

    expected = 'm'
    observed = lexer.peek2_char()
    assert expected == observed
    observed = lexer.peek2_char()
    assert expected == observed
    observed = lexer.peek2_char()
    assert expected == observed

def test_peek2_char_returns_second_character_at_stream_end():
    stream = 'xml'
    lexer  = Lexer(stream)

    lexer.pop_char()
    lexer.pop_char()
    lexer.pop_char()

    expected = ''
    observed = lexer.peek2_char()
    assert expected == observed
    observed = lexer.peek2_char()
    assert expected == observed
    observed = lexer.peek2_char()
    assert expected == observed

def test_skip_whitespace_consumes_stream_of_mixed_whitespaces():
    stream = ' \t\n\ra\r\n\t '
    lexer  = Lexer(stream)

    lexer.skip_whitespace()
    lexer.pop_char()
    lexer.skip_whitespace()

    expected = True
    observed = lexer.at_eof()
    assert expected == observed

def test_read_identifier_returns_token_at_stream_boundary():
    stream = 'verbo@'
    lexer  = Lexer(stream)

    expected = Token(TokenKind.IDENTIFIER, 'verbo')
    observed = lexer.read_identifier()
    assert expected == observed

@parametrize('stream',
             [param('predicado',         id='from_stream_of_letters_only'),
              param('objeto-direto-a',   id='from_stream_including_hyphen'),
              param('_sujeito_simples_', id='from_stream_including_underscore'),
              param('o1adjunto1',        id='from_stream_including_digits'),])
def test_read_identifier_returns_token(stream):
    lexer    = Lexer(stream)
    expected = Token(TokenKind.IDENTIFIER, stream)
    observed = lexer.read_identifier()
    assert expected == observed

@parametrize('stream',
             [param('nucleo-',  id='on_stream_ending_with_hyphen'),
              param('-nucleo',  id='on_stream_starting_with_hyphen'),
              param('1sujeito', id='on_stream_starting_with_digit'),])
def test_read_identifier_raises_error(stream):
    lexer = Lexer(stream)
    with pytest.raises(LexerError):
        lexer.read_identifier()

@parametrize('stream,expected',
             [param('.', TokenKind.DOT,         id='from_stream_of_dot'),
              param('@', TokenKind.AT_SIGN,     id='from_stream_of_at_sign'),
              param('#', TokenKind.HASH_SIGN,   id='from_stream_of_hash_sign'),
              param('$', TokenKind.DOLLAR_SIGN, id='from_stream_of_dollar_sign'),
              param('*', TokenKind.ASTERISK,    id='from_stream_of_asterisk'),
              param(':', TokenKind.COLON,       id='from_stream_of_colon'),
              param(';', TokenKind.SEMICOLON,   id='from_stream_of_semicolon'),
              param('{', TokenKind.LEFT_BRACE,  id='from_stream_of_left_brace'),
              param('}', TokenKind.RIGHT_BRACE, id='from_stream_of_right_brace'),])
def test_read_symbol_returns_token(stream, expected):
    lexer    = Lexer(stream)
    expected = Token(expected)
    observed = lexer.read_symbol()
    assert expected == observed

def test_read_symbol_raises_error_on_invalid_character():
    stream = '?'
    lexer  = Lexer(stream)

    with pytest.raises(LexerError):
        lexer.read_symbol()

@parametrize('stream,expected',
             [param('\\n', '\n',  id='from_slash_n'),
              param('\\t', '\t',  id='from_slash_t'),
              param('\\r', '\r',  id='from_slash_r'),
              param('\\\\', '\\', id='from_slashes'),])
def test_read_escape_sequence_returns_resoveld_character(stream, expected):
    lexer    = Lexer(stream)
    observed = lexer.read_escape_char()
    assert expected == observed

def test_read_escape_sequence_raises_error_on_invalid_escape_character():
    stream = '\\z'
    lexer  = Lexer(stream)

    with pytest.raises(LexerError):
        lexer.read_escape_char()

def test_read_escape_sequence_raises_error_on_unterminated_sequence():
    stream = '\\'
    lexer  = Lexer(stream)

    with pytest.raises(LexerError):
        lexer.read_escape_char()

def test_read_escape_sequence_raises_error_on_missing_backslash():
    stream = 'x'
    lexer  = Lexer(stream)

    with pytest.raises(LexerError):
        lexer.read_escape_char()

def test_read_string_returns_token_without_escape_sequence():
    stream = '"Amor é fogo"'
    lexer  = Lexer(stream)

    expected = Token(TokenKind.STRING, 'Amor é fogo')
    observed = lexer.read_string()
    assert expected == observed

def test_read_string_returns_token_with_escape_sequence():
    stream = '"Amor\\té fogo\\n"'
    lexer  = Lexer(stream)

    expected = Token(TokenKind.STRING, 'Amor\té fogo\n')
    observed = lexer.read_string()
    assert expected == observed

def test_read_string_raises_error_on_missing_opening_quote():
    stream = 'Amor é fogo"'
    lexer  = Lexer(stream)

    with pytest.raises(LexerError):
        lexer.read_string()

def test_read_string_raises_error_on_missing_closing_quote():
    stream = '"Amor é fogo'
    lexer  = Lexer(stream)

    with pytest.raises(LexerError):
        lexer.read_string()

def test_read_comment_returns_token_at_eof():
    stream = '-- This is a comment.'
    lexer  = Lexer(stream)

    expected = Token(TokenKind.COMMENT, ' This is a comment.')
    observed = lexer.read_comment()
    assert expected == observed

def test_read_comment_returns_token_terminated_by_newline():
    stream = '-- This is a comment.\n'
    lexer  = Lexer(stream)

    expected = Token(TokenKind.COMMENT, ' This is a comment.')
    observed = lexer.read_comment()
    assert expected == observed

def test_read_comment_raises_error_on_missing_first_hyphen():
    stream = 'This is a comment.'
    lexer  = Lexer(stream)

    with pytest.raises(LexerError):
        lexer.read_comment()

def test_read_comment_missing_second_hyphen():
    stream = '- This is a comment.'
    lexer  = Lexer(stream)

    with pytest.raises(LexerError):
        lexer.read_comment()

def test_read_next_token_returns_expected_token_kinds():
    stream = ('-- This is a comment.\n' 'sujeito: "Eu";')
    lexer  = Lexer(stream)

    expected = Token(TokenKind.COMMENT, ' This is a comment.')
    observed = lexer.read_next_token()
    assert expected == observed

    expected = Token(TokenKind.IDENTIFIER, 'sujeito')
    observed = lexer.read_next_token()
    assert expected == observed

    expected = Token(TokenKind.COLON)
    observed = lexer.read_next_token()
    assert expected == observed

    expected = Token(TokenKind.STRING, 'Eu')
    observed = lexer.read_next_token()
    assert expected == observed

    expected = Token(TokenKind.SEMICOLON)
    observed = lexer.read_next_token()
    assert expected == observed

    expected = Token(TokenKind.EOF)
    observed = lexer.read_next_token()
    assert expected == observed

def test_read_next_token_raises_error_on_invalid_chararcter():
    stream = '?'
    lexer  = Lexer(stream)

    with pytest.raises(LexerError):
        lexer.read_next_token()
