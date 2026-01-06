import pytest
from pytest import mark, param
from tinta import node as n
from tinta.lexer import Lexer
from tinta.parser import Parser
from tinta.error import ParserError
from tinta.token import TokenKind, Position

parametrize = mark.parametrize

def test_peek_token_returns_current_token():
    stream = '{'
    lexer  = Lexer(stream)
    parser = Parser(lexer)

    expected = TokenKind.LEFT_BRACE
    observed = parser.peek_token().kind
    assert expected == observed

def test_pop_token_advances_lexer():
    stream = '{}'
    lexer  = Lexer(stream)
    parser = Parser(lexer)

    parser.pop_token()

    expected = TokenKind.RIGHT_BRACE
    observed = parser.peek_token().kind
    assert expected == observed

def test_next_token_return_current_token_and_advances_lexer():
    stream = '}{'
    lexer  = Lexer(stream)
    parser = Parser(lexer)

    expected = TokenKind.RIGHT_BRACE
    observed = parser.next_token().kind
    assert expected == observed

    expected = TokenKind.LEFT_BRACE
    observed = parser.next_token().kind
    assert expected == observed

    expected = TokenKind.EOF
    observed = parser.next_token().kind
    assert expected == observed

def test_expect_returns_expected_token():
    stream = '@'
    lexer  = Lexer(stream)
    parser = Parser(lexer)

    expected = TokenKind.AT_SIGN
    observed = parser.expect(TokenKind.AT_SIGN).kind
    assert expected == observed

def test_expect_raises_error_on_unexpected_token():
    stream = '#'
    lexer  = Lexer(stream)
    parser = Parser(lexer)

    with pytest.raises(ParserError):
        parser.expect(TokenKind.DOLLAR_SIGN)

def test_check_return_true_on_matching_kind():
    stream = '.'
    lexer  = Lexer(stream)
    parser = Parser(lexer)

    expected = True
    observed = parser.check(TokenKind.DOT)
    assert expected == observed

def test_check_return_false_on_unmatching_kind():
    stream = '$'
    lexer  = Lexer(stream)
    parser = Parser(lexer)

    expected = False
    observed = parser.check(TokenKind.AT_SIGN)
    assert expected == observed

def test_at_eof():
    stream = '#'
    lexer  = Lexer(stream)
    parser = Parser(lexer)

    expected = False
    observed = parser.at_eof()
    assert expected == observed

    parser.pop_token()

    expected = True
    observed = parser.at_eof()
    assert expected == observed

def test_parse_identifier_returns_node():
    stream = 'paragrafo'
    lexer  = Lexer(stream)
    parser = Parser(lexer)

    position = Position(1, 1)
    expected = n.IdentifierNode(position, 'paragrafo')
    observed = parser.parse_identifier()
    assert expected == observed

def test_parse_string_literal_returns_node():
    stream = '"rápido"'
    lexer  = Lexer(stream)
    parser = Parser(lexer)

    position = Position(1, 1)
    expected = n.StringLiteralNode(position, 'rápido')
    observed = parser.parse_string_literal()
    assert expected == observed

def test_parse_comment_returns_node():
    stream = '-- This is a comment.\n'
    lexer  = Lexer(stream)
    parser = Parser(lexer)

    position = Position(1, 1)
    expected = n.CommentNode(position, ' This is a comment.')
    observed = parser.parse_comment()
    assert expected == observed

def test_parse_text_fragment_returns_node_without_strip():
    stream = '"azul"'
    lexer  = Lexer(stream)
    parser = Parser(lexer)

    strip_left  = False
    strip_right = False
    position    = Position(1, 1)
    string_node = n.StringLiteralNode(position, 'azul')

    position = Position(1, 1)
    expected = n.TextFragmentNode(position, string_node, strip_left, strip_right)
    observed = parser.parse_text_fragment()
    assert expected == observed

def test_parse_text_fragment_returns_node_with_left_strip():
    stream = '*"azul"'
    lexer  = Lexer(stream)
    parser = Parser(lexer)

    strip_left  = True
    strip_right = False
    position    = Position(1, 2)
    string_node = n.StringLiteralNode(position, 'azul')

    position = Position(1, 1)
    expected = n.TextFragmentNode(position, string_node, strip_left, strip_right)
    observed = parser.parse_text_fragment()
    assert expected == observed
    assert observed.content.parent is observed

def test_parse_text_fragment_returns_node_with_right_strip():
    stream = '"azul"*'
    lexer  = Lexer(stream)
    parser = Parser(lexer)

    strip_left  = False
    strip_right = True
    position   = Position(1, 1)
    string_node = n.StringLiteralNode(position, 'azul')

    position = Position(1, 1)
    expected = n.TextFragmentNode(position, string_node, strip_left, strip_right)
    observed = parser.parse_text_fragment()
    assert expected == observed
    assert observed.content.parent is observed

def test_parse_text_fragment_returns_node_with_left_and_right_strip():
    stream = '*"azul"*'
    lexer  = Lexer(stream)
    parser = Parser(lexer)

    strip_left  = True
    strip_right = True
    position    = Position(1, 2)
    string_node = n.StringLiteralNode(position, 'azul')

    position = Position(1, 1)
    expected = n.TextFragmentNode(position, string_node, strip_left, strip_right)
    observed = parser.parse_text_fragment()
    assert expected == observed
    assert observed.content.parent is observed

def test_parse_group_label_returns_node():
    stream = '@group1'
    lexer  = Lexer(stream)
    parser = Parser(lexer)

    position = Position(1, 2)
    name     = n.IdentifierNode(position, 'group1')

    position = Position(1, 1)
    expected = n.GroupLabelNode(position, name)
    observed = parser.parse_group_label()
    assert expected == observed
    assert observed.name.parent is observed

def test_parse_anchor_label_returns_node():
    stream = '#group1'
    lexer  = Lexer(stream)
    parser = Parser(lexer)

    position = Position(1, 2)
    name     = n.IdentifierNode(position, 'group1')

    position = Position(1, 1)
    expected = n.AnchorLabelNode(position, name)
    observed = parser.parse_anchor_label()
    assert expected == observed
    assert observed.name.parent is observed

def test_parse_link_label_returns_node():
    stream = '$group1'
    lexer  = Lexer(stream)
    parser = Parser(lexer)

    position = Position(1, 2)
    name     = n.IdentifierNode(position, 'group1')

    position = Position(1, 1)
    expected = n.LinkLabelNode(position, name)
    observed = parser.parse_link_label()
    assert expected == observed
    assert observed.name.parent is observed

def test_parse_shorthand_block_body_returns_statements():
    stream = ': "o livro";'
    lexer  = Lexer(stream)
    parser = Parser(lexer)

    observed_body = parser.parse_shorthand_block_body()
    assert 1 == len(observed_body)

    observed_statement = observed_body[0]
    assert type(observed_statement) is n.TextFragmentNode

def test_parse_standard_block_body_returns_empty_body():
    stream = '{ }'
    lexer  = Lexer(stream)
    parser = Parser(lexer)

    observed_body = parser.parse_standard_block_body()
    assert 0 == len(observed_body)

def test_parse_standard_block_body_returns_multiple_statements():
    stream = ('{ -- Comment.\n'
              '"O céu"'
              'pred { }'
              '}')
    lexer  = Lexer(stream)
    parser = Parser(lexer)

    observed_body = parser.parse_standard_block_body()
    assert 3 == len(observed_body)

    observed_statement_1 = observed_body[0]
    assert type(observed_statement_1) is n.CommentNode

    observed_statement_2 = observed_body[1]
    assert type(observed_statement_2) is n.TextFragmentNode

    observed_statement_3 = observed_body[2]
    assert type(observed_statement_3) is n.BlockNode

def test_parse_block_body_returns_node_from_shorthand_syntax():
    stream = ': "Eles" ;'
    lexer  = Lexer(stream)
    parser = Parser(lexer)

    observed_body = parser.parse_block_body()
    assert 1 == len(observed_body)

    observed_statement = observed_body[0]
    assert type(observed_statement) is n.TextFragmentNode

def test_parse_block_body_returns_node_from_standard_syntax():
    stream = '{ "Eles" }'
    lexer  = Lexer(stream)
    parser = Parser(lexer)

    observed_body = parser.parse_block_body()
    assert 1 == len(observed_body)

    observed_statement = observed_body[0]
    assert type(observed_statement) is n.TextFragmentNode

def test_parse_block_returns_node_from_qualified_syntax():
    stream = 'x.y.z { "Eles" }'
    lexer  = Lexer(stream)
    parser = Parser(lexer)

    observed_x = parser.parse_block()
    assert type(observed_x) is n.BlockNode
    assert 'x' == observed_x.kind.value
    assert   1 == len(observed_x.body)

    observed_y = observed_x.body[0]
    assert type(observed_y) is n.BlockNode
    assert 'y' == observed_y.kind.value
    assert   1 == len(observed_y.body)

    observed_z = observed_y.body[0]
    assert type(observed_z) is n.BlockNode
    assert 'z' == observed_z.kind.value
    assert   1 == len(observed_z.body)
    assert type(observed_z.body[0]) is n.TextFragmentNode
    assert observed_z.body[0].parent is observed_z
    
def test_parse_block_returns_node_without_optional_labels():
    stream = 'pred { "falam" }'
    lexer  = Lexer(stream)
    parser = Parser(lexer)

    expected_type = 'pred'
    observed = parser.parse_block()
    assert type(observed) is n.BlockNode
    assert expected_type == observed.kind.value
    assert observed.kind.parent is observed

    assert observed.group is None
    assert observed.anchor is None
    assert observed.link is None

    assert 1 == len(observed.body)
    assert type(observed.body[0]) is n.TextFragmentNode
    assert observed.body[0].parent is observed
    
def test_parse_block_returns_node_with_all_optional_labels():
    stream = 'pred @group1 #ref1 $ref2 { "falam" }'
    lexer  = Lexer(stream)
    parser = Parser(lexer)

    expected_type = 'pred'
    observed = parser.parse_block()
    assert type(observed) is n.BlockNode
    assert expected_type == observed.kind.value
    assert observed.kind.parent is observed

    expected_group = 'group1'
    assert observed.group is not None
    assert expected_group == observed.group.name.value
    assert observed.group.parent is observed

    expected_anchor = 'ref1'
    assert observed.anchor is not None
    assert expected_anchor == observed.anchor.name.value
    assert observed.anchor.parent is observed

    expected_link = 'ref2'
    assert observed.link is not None
    assert expected_link == observed.link.name.value
    assert observed.link.parent is observed

    assert 1 == len(observed.body)
    assert type(observed.body[0]) is n.TextFragmentNode
    assert observed.body[0].parent is observed

@parametrize('stream,expected',
             [param('-- Comment.', n.CommentNode,      id='from_comment'),
              param('*"amarelo"*', n.TextFragmentNode, id='from_text_fragment_with_trim'),
              param('"amarelo"',   n.TextFragmentNode, id='from_text_fragment_without_trim'),
              param('pred {  }',   n.BlockNode,        id='from_block'),])
def test_parse_statement_returns_node(stream, expected):
    lexer  = Lexer(stream)
    parser = Parser(lexer)

    observed = type(parser.parse_statement())
    assert expected == observed

def test_parse_statement_raises_error_on_unexpected_token():
    stream = '@'
    lexer  = Lexer(stream)
    parser = Parser(lexer)

    with pytest.raises(ParserError):
        parser.parse_statement()

def test_parse_program_returns_node():
    stream = 'x { }'
    lexer  = Lexer(stream)
    parser = Parser(lexer)

    observed_program = parser.parse_program()
    assert type(observed_program) is n.ProgramNode
    assert 1 == len(observed_program.body)

    observed_block = observed_program.body[0]
    assert type(observed_block) is n.BlockNode
    assert observed_block.parent is observed_program

def test_parse_returns_program_node():
    stream = 'x { }'
    lexer  = Lexer(stream)
    parser = Parser(lexer)

    observed_program = parser.parse()
    assert type(observed_program) is n.ProgramNode
    assert 1 == len(observed_program.body)

    observed_block = observed_program.body[0]
    assert type(observed_block) is n.BlockNode
    assert observed_block.parent is observed_program
