import string
from tinta.error import LexerError
from tinta.token import TokenKind, Token

class Lexer:
    """A lexer for the Tinta language."""
    _stream: str
    _length: int
    _offset: int
    _line:   int
    _column: int

    symbols = ['.', '@', '#', '$', '*', ':', ';', '{', '}']

    def __init__(self, stream: str = ''):
        """Initializes the Lexer and sets its initial state.

        Args:
            stream (str): The input stream to be tokenized.
        """
        self._stream = stream
        self._length = len(stream)
        self._offset = 0
        self._line   = 1
        self._column = 1

    def is_ascii_letter(self, char: str) -> bool:
        """Checks if a character is an ASCII letter (`A-Z`, `a-z`).

        Args:
            char: The character to be checked.

        Returns:
            bool: `True` if the character is an ASCII letter, `False` otherwise.
        """
        return char != '' and char in string.ascii_letters

    def is_digit(self, char: str) -> bool:
        """Checks if a character is a digit (`0-9`).

        Args:
            char: The character to be checked.

        Returns:
            bool: `True` if the character is a digit, `False` otherwise.
        """
        return char.isdigit()

    def is_ascii_letter_or_underscore(self, char: str) -> bool:
        """Checks if a character is an ASCII letter or a digit (`A-Z`, `a-z`,
        `0-9`).

        Args:
            char: The character to be checked.

        Returns:
            bool: `True` if the character is an ASCII letter or a digit,
            `False` otherwise.
        """
        return self.is_ascii_letter(char) or char == '_'

    def is_ascii_letter_digit_or_underscore(self, char: str) -> bool:
        """Checks if a character is an ASCII letter, a digit or an underscore
        (`A-Z`, `a-z`, `0-9`, `_`).

        Args:
            char: The character to be checked.

        Returns:
            bool: `True` if the character is an ASCII letter, a digit or an
            underscore, `False` otherwise.
        """
        return self.is_ascii_letter_or_underscore(char) or self.is_digit(char)

    def is_ascii_letter_digit_underscore_or_hyphen(self, char: str) -> bool:
        """Checks if a character is an ASCII letter, a digit, an underscore or
        a hyphen (`A-Z`, `a-z`, `0-9`, `_`, `-`).

        Args:
            char: The character to be checked.

        Returns:
            bool: `True` if the character is an ASCII letter, a digit, an
            underscore or a hyphen, `False` otherwise.
        """
        return self.is_ascii_letter_digit_or_underscore(char) or char == '-'

    def at_eof(self) -> bool:
        """Checks if the end of the file was reached.

        Returns:
            bool: `True` if the end of the file was reached, `False` otherwise.
        """
        return self._offset >= self._length

    def get_offset(self) -> int:
        """Returns the current offset in the stream input.

        Returns:
            int: The current offset.
        """
        return self._offset

    def get_position(self) -> tuple[int, int]:
        """Returns the current position (i.e. line and column numbers) in the
        stream input.

        Returns:
            tuple[int, int]: A tuple containing the current line and the column,
            respectively, both starting from 1.
        """
        return (self._line, self._column)

    def peek_char(self) -> str:
        """Returns the character at the current offset without consuming it.

        Returns:
            str: The character at the current offset, or an empty string if
            the end of the file is reached.
        """
        if self._offset >= self._length:
            return ''
        return self._stream[self._offset]

    def peek2_char(self) -> str:
        """Returns the character immediately following the current offset
        without consuming it.

        Returns:
            str: The character at the next offset, or an empty string if it
            exceeds the file length.
        """
        if self._offset + 1 >= self._length:
            return ''
        return self._stream[self._offset + 1]

    def pop_char(self) -> None:
        """Consumes the character at the current offset and advances both the
        offset and stream position.
        """
        self._offset += 1
        self._column += 1

        if self._offset < self._length:
            if self._stream[self._offset] == '\n':
                self._line += 1
                self._column = 1

    def next_char(self) -> str:
        """Returns the character at the current offset and advances both the
        offset and the stream position.

        Returns:
            str: The consumed character.
        """
        if self._offset >= self._length:
            return ''

        char = self._stream[self._offset]
        self.pop_char()
        return char

    def skip_whitespace(self) -> None:
        """Consumes all whitespace characters from the current offset.

        Whitespace characters are spaces (` `), newlines (`\\n`), tabs (`\\t`)
        and carriage returns (`\\r`).
        """
        while not self.at_eof():
            lookahead = self.peek_char()
            if lookahead.isspace():
                self.pop_char()
                continue
            break

    def read_identifier(self) -> Token:
        """Scans and returns an identifier token.

        A identifier is a sequence of characters starting with an ASCII letter
        or underscore, followed by any combination of letters, digits,
        underscores or hyphens, and ending with a letter, underscore or digit.

        Returns:
            Token: A `Token` object of kind `IDENTIFIER` containing the
            identifier's value.

        Raises:
            LexerError:
                - If the identifier starts with a digit or hyphen.
                - If the identifier ends with a hyphen.
        """
        chars: list[str] = []

        next_char = self.next_char()
        if self.is_digit(next_char):
            message = f'Identifiers cannot start with a digit `{next_char}`'
            raise LexerError(message, self._line, self._column)
        if next_char == '-':
            message = f'Identifiers cannot start with a hyphen `{next_char}`'
            raise LexerError(message, self._line, self._column)

        chars.append(next_char)

        while not self.at_eof():
            lookahead1 = self.peek_char()
            if lookahead1 == '-':
                lookahead2 = self.peek2_char()
                if self.is_ascii_letter_digit_underscore_or_hyphen(lookahead2):
                    self.pop_char()
                    chars.append(lookahead1)
                else:
                    message = f'Identifiers cannot end with a hyphen `{lookahead1}`'
                    raise LexerError(message, self._line, self._column)
                continue
            if self.is_ascii_letter_digit_or_underscore(lookahead1):
                self.pop_char()
                chars.append(lookahead1)
                continue
            break

        token_value = ''.join(chars)
        return Token(TokenKind.IDENTIFIER, token_value)

    def read_escape_char(self) -> str:
        """Scans and returns the escaped character of an escape sequence.

        An escape sequence is a sequence of characters starting with a backslash
        (`\\`) and ending with one of the following characters:
            - `\\` for a literal backslash.
            - `n` for a newline character.
            - `r` for a return carriage character.
            - `t` for a tab character.

        Returns:
            str: The single escaped character.

        Raises:
            LexerError:
                - If the sequence does not start with a backslash.
                - If the sequence is unterminated (i.e., it reaches EOF before
                  finding the expected escape character).
                - If the sequence is not a valid escape sequence.
        """
        next_char = self.next_char()
        if next_char != '\\':
            message = f'Expected `\\`, but found `{next_char}'
            raise LexerError(message, self._line, self._column)

        if self.at_eof():
            message = 'Unterminated escape sequence at EOF'
            raise LexerError(message, self._line, self._column)

        next_char = self.next_char()
        if next_char == '\\':
            return '\\'
        if next_char == 'n':
            return '\n'
        if next_char == 't':
            return '\t'
        if next_char == 'r':
            return '\r'

        message = 'Invalid escape sequence `\\{next_char}`'
        raise LexerError(message, self._line, self._column)

    def read_string(self) -> Token:
        """Scans and returns a string literal token.

        A string is a sequence of characters starting with a double quote (`"`),
        followed by any combination of regular characters or escape sequences
        (starting with a backslash `\\`), and ending with a double quote.

        Returns:
            Token: A token object of kind `STRING` containing the literal's value.

        Raises:
            LexerError:
                - If the string doesn't start with the expected quote character.
                - If the string is unterminated (i.e., it reaches EOF before
                  finding the expected closing quote character).
                - If an invalid sequence is found.
        """
        chars: list[str] = []

        next_char = self.next_char()
        if next_char != '"':
            message = 'Expected `"`, but found `{next_char}`'
            raise LexerError(message, self._line, self._column)

        while not self.at_eof():
            lookahead = self.peek_char()
            if lookahead == '"':
                break
            if lookahead == '\\':
                next_char = self.read_escape_char()
                chars.append(next_char)
                continue
            self.pop_char()
            chars.append(lookahead)

        if self.at_eof():
            message = 'Unterminated string: expected `\"`, but found EOF'
            raise LexerError(message, self._line, self._column)

        self.pop_char()

        token_value = ''.join(chars)
        return Token(TokenKind.STRING, token_value)

    def read_comment(self) -> Token:
        """Scans and returns a comment token.

        A comment is a sequence of characters starting with two hyphens (`--`),
        followed by any combination of characters, and ending with a newline
        (`\\n`) or the end of the file (`EOF`).

        Returns:
            Token: a `Token` object of kind `COMMENT` containing the comment's
            value.

        Raises:
            LexerError: if the comment does not start with two hyphens.
        """
        chars: list[str] = []

        next_char = self.next_char()
        if next_char != '-':
            message = f'Expected `-`, but found `{next_char}'
            raise LexerError(message, self._line, self._column)

        next_char = self.next_char()
        if next_char != '-':
            message = f'Expected `-`, but found `{next_char}'
            raise LexerError(message, self._line, self._column)

        while not self.at_eof():
            next_char = self.next_char()
            if next_char == '\n':
                break
            chars.append(next_char)

        token_value = ''.join(chars)
        return Token(TokenKind.COMMENT, token_value)

    def read_symbol(self) -> Token:
        next_char = self.next_char()

        if next_char == '.':
            return Token(TokenKind.DOT)
        if next_char == '@':
            return Token(TokenKind.AT_SIGN)
        if next_char == '#':
            return Token(TokenKind.HASH_SIGN)
        if next_char == '$':
            return Token(TokenKind.DOLLAR_SIGN)
        if next_char == '*':
            return Token(TokenKind.ASTERISK)
        if next_char == ':':
            return Token(TokenKind.COLON)
        if next_char == ';':
            return Token(TokenKind.SEMICOLON)
        if next_char == '{':
            return Token(TokenKind.LEFT_BRACE)
        if next_char == '}':
            return Token(TokenKind.RIGHT_BRACE)

        message = f'Unexpected character `{next_char}`'
        raise LexerError(message, self._line, self._column)

    def read_next_token(self) -> Token:
        """Reads the stream and returns the next recognized token.

        Returns:
            Token: The next token object extracted from the input stream.
            Returns an EOF token when the end of the stream is reached.

        Raises:
            LexerError: If the input cannot be recognized as a valid token.
        """
        if self.at_eof():
            return Token(TokenKind.EOF)

        lookahead = self.peek_char()
        if self.is_ascii_letter_or_underscore(lookahead):
            return self.read_identifier()
        if lookahead == '-':
            return self.read_comment()
        if lookahead == '"':
            return self.read_string()
        if lookahead.isspace():
            self.skip_whitespace()
            return self.read_next_token()
        if lookahead in self.symbols:
            return self.read_symbol()

        message = f'Unexpected character `{lookahead}`'
        raise LexerError(message, self._line, self._column)
