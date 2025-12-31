from tinta.token import Position

class LexerError(Exception):
    """
    Exception raised for errors during the lexical analysis.

    Attributes:
        message: Explanation of the error.
        position: A `Position` object containing the line and column where the
            error occured.
    """
    message:  str
    position: Position

    def __init__(self, message: str, position: Position):
        self.message = message
        self.position = position
        super().__init__(f'{message} at line {position.line}, column {position.column}')
