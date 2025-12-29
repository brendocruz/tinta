class LexerError(Exception):
    """
    Exception raised for errors during the lexical analysis.

    Attributes:
        message (`str`): Explanation of the error.
        line (`int`): Line number where the error occured.
        column (`int`): Column number where the error occured.
    """
    message: str
    line: int
    column: int

    def __init__(self, message: str, line: int, column: int):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f'{message} at line {line}, column {column}')
