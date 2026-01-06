from typing import Optional
from tinta.token import Token, TokenKind, Position
from tinta.lexer import Lexer
from tinta.error import ParserError
from tinta import node as n

class Parser:
    """A lexer for the Tinta language."""
    lexer:          Lexer
    _current_token: Token

    def __init__(self, lexer: Lexer):
        """Initializes the parser.

        Args:
            lexer (Lexer): The lexer instance to provide tokens.
        """
        self.lexer = lexer
        self._current_token = lexer.read_next_token()

    def peek_token(self) -> Token:
        """Returns the current token without consuming it.

        Returns:
            Token: The token currently pointed to by the parse.
        """
        return self._current_token

    def pop_token(self) -> None:
        """Consumes the current token."""
        self._current_token = self.lexer.read_next_token()

    def next_token(self) -> Token:
        """Returns the current token and consumes it.

        Returns:
            str: The consumed character.
        """
        current_token = self._current_token
        self.pop_token()
        return current_token

    def at_eof(self) -> bool:
        """Checks if the end of the token stream was reached.

        Returns:
            bool: `True` if the current token is EOF, `False` otherwise.
        """
        return self._current_token.kind == TokenKind.EOF

    def expect(self, kind: TokenKind) -> Token:
        """Ensures the current token matches the given type.

        If the token kinds match, the current token is consumed and returned.
        Otherwise, a ParserError is raised.

        Args:
            kind (TokenKind): The expect kind.

        Returns:
            TokenKind: The consumed token.

        Raises:
            ParserError: If the kinds do not match.
        """
        current_token = self.next_token()
        if current_token.kind != kind:
            message  = f'Expected `{kind}`, but found `{self._current_token.kind}'
            position = self._current_token.position
            raise ParserError(message, position)
        return current_token

    def check(self, kind: TokenKind) -> bool:
        """Checks if the current token matches the given kind.

        Args:
            kind (TokenKind): The kind to compare against.

        Returns:
            bool: `True` if the kinds match, `False` otherwise.
        """
        return self._current_token.kind == kind

    def parse_identifier(self) -> n.IdentifierNode:
        """Parses an identifier node from the input stream.

        Returns:
            IdentifierNode: The parsed identifier node.

        Raises:
            ParserError: If the next token is not an identifier.
        """
        token = self.expect(TokenKind.IDENTIFIER)
        return n.IdentifierNode(token.position, token.value)

    def parse_string_literal(self) -> n.StringLiteralNode:
        """Parses a string node from the input stream.

        Returns:
            StringLiteralNode: The parsed string node.

        Raises:
            ParserError: If the next token is not a string.
        """
        token = self.expect(TokenKind.STRING)
        return n.StringLiteralNode(token.position, token.value)

    def parse_comment(self) -> n.CommentNode:
        """Parses a comment node from the input stream.

        Returns:
            CommentNode: The parsed comment node.

        Raises:
            ParserError: If the next token is not a comment.
        """
        token = self.expect(TokenKind.COMMENT)
        return n.CommentNode(token.position, token.value)

    def parse_text_fragment(self) -> n.TextFragmentNode:
        """Parses a text fragment from the input stream.

        Returns:
            TextFragmentNode: The parsed text fragment node.

        Raises:
            ParserError: If the next tokens do not form a valid text fragment
            (e.g., encountering a token that is neither a string nor an 
            asterisk).
        """
        trim_left:  bool = False
        trim_right: bool = False

        position: Optional[Position] = None
        if self.check(TokenKind.ASTERISK):
            token = self.peek_token()
            position = token.position
            trim_left = True
            self.pop_token()

        string_node = self.parse_string_literal()
        if position is None:
            position = string_node.position

        if self.check(TokenKind.ASTERISK):
            trim_right = True
            self.pop_token()

        node = n.TextFragmentNode(position, string_node, trim_left, trim_right)
        string_node.parent = node
        return node

    def parse_group_label(self) -> n.GroupLabelNode:
        """Parses a group label from the input stream.

        Returns:
            GroupLabelNode: The parsed group label node.

        Raises:
            ParserError: If the next tokens do not form a valid group label
            (e.g., missing the leading symbol or the following identifier).
        """
        token     = self.expect(TokenKind.AT_SIGN)
        position  = token.position
        name_node = self.parse_identifier()

        group_node = n.GroupLabelNode(position, name_node)
        name_node.parent = group_node
        return group_node

    def parse_anchor_label(self) -> n.AnchorLabelNode:
        """Parses an anchor label from the input stream.

        Returns:
            AnchorLabelNode: The parsed anchor label node.

        Raises:
            ParserError: If the next tokens do not form a valid anchor label
            (e.g., missing the leading symbol or the following identifier).
        """
        token     = self.expect(TokenKind.HASH_SIGN)
        position  = token.position
        name_node = self.parse_identifier()

        anchor_node = n.AnchorLabelNode(position, name_node)
        name_node.parent = anchor_node
        return anchor_node

    def parse_link_label(self) -> n.LinkLabelNode:
        """Parses a link label from the input stream.

        Returns:
            LinkLabelNode: The parsed link label node.

        Raises:
            ParserError: If the next tokens do not form a valid link label
            (e.g., missing the leading symbol or the following identifier).
        """
        token     = self.expect(TokenKind.DOLLAR_SIGN)
        position  = token.position
        name_node = self.parse_identifier()

        link_node = n.LinkLabelNode(position, name_node)
        name_node.parent = link_node
        return link_node

    def parse_shorthand_block_body(self) -> list[n.StatementNode]:
        """Parses a shorthand block body from the input stream.

        Returns:
            list[StatementNode]: A list containing the single statement of 
            the shorthand block body.

        Raises:
            ParserError: If a valid shorthand block body cannot be formed 
            (e.g., missing the opening colon or the closing semicolon).
        """
        statements: list[n.StatementNode] = []
        self.expect(TokenKind.COLON)
        text_node = self.parse_text_fragment()
        statements.append(text_node)
        self.expect(TokenKind.SEMICOLON)
        return statements

    def parse_standard_block_body(self) -> list[n.StatementNode]:
        """Parses a standard block body from the input stream.

        Returns:
            list[StatementNode]: A list of statements parsed within the block
            braces.

        Raises:
            ParserError: If a valid standard block body cannot be formed
            (e.g., missing the opening or closing braces).
        """
        self.expect(TokenKind.LEFT_BRACE)
        statements: list[n.StatementNode] = []
        while not self.at_eof():
            if self.check(TokenKind.RIGHT_BRACE):
                break;
            statement_node = self.parse_statement()
            statements.append(statement_node)
        self.pop_token()
        return statements

    def parse_block_body(self) -> list[n.StatementNode]:
        """Parses a block body from the input stream.

        Returns:
            list[StatementNode]: A list of statements parsed within the block.

        Raises:
            ParserError: If a valid block body cannot be formed (e.g., missing 
            mandatory delimiters or containing invalid statements).
        """
        if self.check(TokenKind.COLON):
            return self.parse_shorthand_block_body()
        return self.parse_standard_block_body()

    def parse_block(self) -> n.BlockNode:
        """Parses a block from the input stream.

        Returns:
            BlockNode: The parsed block node.

        Raises:
            ParserError: If a valid block cannot be formed (e.g., missing the
            block type or containing an unclosed body).
        """
        block_type = self.parse_identifier()
        position   = block_type.position

        if self.check(TokenKind.DOT):
            self.pop_token()
            block_body = self.parse_block()
            block_node = n.BlockNode(position, block_type)
            block_node.body.append(block_body)
            return block_node

        block_node = n.BlockNode(position, kind=block_type)
        block_type.parent = block_node

        if self.check(TokenKind.AT_SIGN):
            group_label = self.parse_group_label()
            block_node.group = group_label
            group_label.parent = block_node

        if self.check(TokenKind.HASH_SIGN):
            anchor_label = self.parse_anchor_label()
            block_node.anchor = anchor_label
            anchor_label.parent = block_node

        if self.check(TokenKind.DOLLAR_SIGN):
            link_label = self.parse_link_label()
            block_node.link = link_label
            link_label.parent = block_node

        block_body = self.parse_block_body()
        for statement in block_body:
            statement.parent = block_node
        block_node.body = block_body

        return block_node

    def parse_statement(self) -> n.StatementNode:
        """Parses a statement from the input stream.

        Returns:
            StatementNode: The parsed statement node.

        Raises:
            ParserError: If the next tokens do not form a valid statement
            (e.g., containing unexpected tokens or syntax errors).
        """
        if self.check(TokenKind.COMMENT):
            return self.parse_comment()
        if self.check(TokenKind.STRING):
            return self.parse_text_fragment()
        if self.check(TokenKind.ASTERISK):
            return self.parse_text_fragment()
        if self.check(TokenKind.IDENTIFIER):
            return self.parse_block()

        token   = self.peek_token()
        message = f'Unexpected token `{token.kind}`'
        raise ParserError(message, token.position)

    def parse_program(self) -> n.ProgramNode:
        """Parses a program from the input stream.

        Returns:
            ProgramNode: The parsed program node.

        Raises:
            ParserError: If the input tokens do not form a valid program
            (e.g., containing unexpected tokens or syntax errors).
        """
        body: list[n.StatementNode] = []
        while not self.at_eof():
            statement = self.parse_statement()
            body.append(statement)

        position: Position = Position(0, 0)
        if len(body) > 0:
            position = body[0].position

        program_node = n.ProgramNode(position, body)
        for statement in body:
            statement.parent = program_node
        return program_node

    def parse(self) -> n.ProgramNode:
        """Parses the entire input stream.

        Returns:
            ProgramNode: The parsed root program node.

        Raises:
            ParserError: If the input tokens do not form a valid program
            (e.g., containing unexpected tokens or syntax errors).
        """
        return self.parse_program()
