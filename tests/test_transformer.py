from tinta.transformer import ASTTransformer
from tinta.token import Position
from tinta import node as n

def test_expand_whitespace__no_text_fragment__adds_no_spacers():
    # Arrange.
    position  = Position(-1, -1)
    node_root = n.ProgramNode(position)
    root_lv1a = n.BlockNode(position, n.IdentifierNode(position, 'LV-1A'))

    node_root.add(root_lv1a)

    # Act.
    transformer = ASTTransformer()
    transformer.expand_whitespace(node_root)

    # Assert.
    assert 1 == len(node_root.body)
    assert 0 == len(root_lv1a.body)

def test_expand_whitespace__single_text_fragment__adds_spacers():
    # Arrange.
    position  = Position(-1, -1)
    node_root = n.ProgramNode(position)
    root_lv1a = n.BlockNode(position, n.IdentifierNode(position,           'LV-1A'))
    lv1a_lv2a = n.TextFragmentNode(position, n.StringLiteralNode(position, 'LV-2A'))

    node_root.add(root_lv1a)
    root_lv1a.add(lv1a_lv2a)

    # Act.
    transformer = ASTTransformer()
    transformer.expand_whitespace(node_root)

    # Assert.
    assert 1 == len(node_root.body)
    assert 1 == len(root_lv1a.body)

def test_expand_whitespace__multiple_text_fragments__adds_spacers():
    # Arrange.
    position  = Position(-1, -1)
    node_root = n.ProgramNode(position)
    root_lv1a = n.BlockNode(position, n.IdentifierNode(position,           'LV-1A'))
    lv1a_lv2a = n.TextFragmentNode(position, n.StringLiteralNode(position, 'LV-2A'))
    lv1a_lv2b = n.TextFragmentNode(position, n.StringLiteralNode(position, 'LV-2B'))
    lv1a_lv2c = n.TextFragmentNode(position, n.StringLiteralNode(position, 'LV-2C'))

    node_root.add(root_lv1a)
    root_lv1a.add(lv1a_lv2a)
    root_lv1a.add(lv1a_lv2b)
    root_lv1a.add(lv1a_lv2c)

    # Act.
    transformer = ASTTransformer()
    transformer.expand_whitespace(node_root)

    # Assert.
    assert 1 == len(node_root.body)
    assert 5 == len(root_lv1a.body)

    assert n.TextFragmentNode == type(root_lv1a.body[0])
    assert n.SpacerNode       == type(root_lv1a.body[1])
    assert n.TextFragmentNode == type(root_lv1a.body[2])
    assert n.SpacerNode       == type(root_lv1a.body[3])
    assert n.TextFragmentNode == type(root_lv1a.body[4])

def test_expand_whitespace__multiple_text_fragments__adds_no_spacers():
    # Arrange.
    position  = Position(-1, -1)
    node_root = n.ProgramNode(position)
    root_lv1a = n.BlockNode(position, n.IdentifierNode(position,           'LV-1A'))
    lv1a_lv2a = n.TextFragmentNode(position, n.StringLiteralNode(position, 'LV-2A'))
    lv1a_lv2b = n.TextFragmentNode(position, n.StringLiteralNode(position, 'LV-2B'))
    lv1a_lv2c = n.TextFragmentNode(position, n.StringLiteralNode(position, 'LV-2C'))

    lv1a_lv2a.strip_right = True
    lv1a_lv2b.strip_left  = True
    lv1a_lv2b.strip_right = True
    lv1a_lv2c.strip_left  = True

    node_root.add(root_lv1a)
    root_lv1a.add(lv1a_lv2a)
    root_lv1a.add(lv1a_lv2b)
    root_lv1a.add(lv1a_lv2c)

    # Act.
    transformer = ASTTransformer()
    transformer.expand_whitespace(node_root)

    # Assert.
    assert 1 == len(node_root.body)
    assert 3 == len(root_lv1a.body)

    assert n.TextFragmentNode == type(root_lv1a.body[0])
    assert n.TextFragmentNode == type(root_lv1a.body[1])
    assert n.TextFragmentNode == type(root_lv1a.body[2])

def test_expand_whitespace__text_fragments_between_empty_blocks__adds_spacers():
    # Arrange.
    position  = Position(-1, -1)
    node_root = n.ProgramNode(position)
    root_lv1a = n.BlockNode(position, n.IdentifierNode(position,           'LV1A'))
    lv1a_lv2a = n.TextFragmentNode(position, n.StringLiteralNode(position, 'LV2A'))
    lv1a_lv2b = n.BlockNode(position, n.IdentifierNode(position,           'LV2B'))
    lv1a_lv2c = n.TextFragmentNode(position, n.StringLiteralNode(position, 'LV2C'))
    lv1a_lv2d = n.BlockNode(position, n.IdentifierNode(position,           'LV2D'))
    lv1a_lv2e = n.TextFragmentNode(position, n.StringLiteralNode(position, 'LV2E'))

    node_root.add(root_lv1a)
    root_lv1a.add(lv1a_lv2a)
    root_lv1a.add(lv1a_lv2b)
    root_lv1a.add(lv1a_lv2c)
    root_lv1a.add(lv1a_lv2d)
    root_lv1a.add(lv1a_lv2e)

    # Act.
    transformer = ASTTransformer()
    transformer.expand_whitespace(node_root)

    # Assert.
    assert 1 == len(node_root.body)
    assert 7 == len(root_lv1a.body)
    assert 0 == len(lv1a_lv2b.body)
    assert 0 == len(lv1a_lv2d.body)

    assert n.TextFragmentNode == type(root_lv1a.body[0])
    assert n.BlockNode        == type(root_lv1a.body[1])
    assert n.SpacerNode       == type(root_lv1a.body[2])
    assert n.TextFragmentNode == type(root_lv1a.body[3])
    assert n.BlockNode        == type(root_lv1a.body[4])
    assert n.SpacerNode       == type(root_lv1a.body[5])
    assert n.TextFragmentNode == type(root_lv1a.body[6])

def test_expand_whitespace__non_empty_block_before_text_fragment__adds_spacers():
    # Arrange.
    position  = Position(-1, -1)
    node_root = n.ProgramNode(position)
    root_lv1a = n.BlockNode(position, n.IdentifierNode(position,           'LV-1A'))
    lv1a_lv2a = n.BlockNode(position, n.IdentifierNode(position,           'LV-2A'))
    lv2a_lv3a = n.TextFragmentNode(position, n.StringLiteralNode(position, 'LV-3A'))
    lv1a_lv2b = n.TextFragmentNode(position, n.StringLiteralNode(position, 'LV-2B'))

    node_root.add(root_lv1a)
    root_lv1a.add(lv1a_lv2a)
    lv1a_lv2a.add(lv2a_lv3a)
    root_lv1a.add(lv1a_lv2b)

    # Act.
    transformer = ASTTransformer()
    transformer.expand_whitespace(node_root)

    # Assert.
    assert 1 == len(node_root.body)
    assert 3 == len(root_lv1a.body)
    assert 1 == len(lv1a_lv2a.body)

    assert n.BlockNode        == type(root_lv1a.body[0])
    assert n.SpacerNode       == type(root_lv1a.body[1])
    assert n.TextFragmentNode == type(root_lv1a.body[2])

def test_expand_whitespace__text_fragment_before_non_empty_block__adds_spacers():
    # Arrange.
    position  = Position(-1, -1)
    node_root = n.ProgramNode(position)
    root_lv1a = n.BlockNode(position, n.IdentifierNode(position,           'LV-1A'))
    lv1a_lv2a = n.TextFragmentNode(position, n.StringLiteralNode(position, 'LV-2A'))
    lv1a_lv2b = n.BlockNode(position, n.IdentifierNode(position,           'LV-2B'))
    lv2b_lv3a = n.TextFragmentNode(position, n.StringLiteralNode(position, 'LV-3A'))

    node_root.add(root_lv1a)
    root_lv1a.add(lv1a_lv2a)
    root_lv1a.add(lv1a_lv2b)
    lv1a_lv2b.add(lv2b_lv3a)

    # Act.
    transformer = ASTTransformer()
    transformer.expand_whitespace(node_root)

    # Assert.
    assert 1 == len(node_root.body)
    assert 3 == len(root_lv1a.body)
    assert 1 == len(lv1a_lv2b.body)

    assert n.TextFragmentNode == type(root_lv1a.body[0])
    assert n.SpacerNode       == type(root_lv1a.body[1])
    assert n.BlockNode        == type(root_lv1a.body[2])

def test_expand_whitespace__shallowly_nested_text_fragments__adds_spacers():
    # Arrange.
    position  = Position(-1, -1)
    node_root = n.ProgramNode(position)
    root_lv1a = n.BlockNode(position, n.IdentifierNode(position,           'LV-1A'))
    lv1a_lv2a = n.BlockNode(position, n.IdentifierNode(position,           'LV-1A'))
    lv2a_lv3a = n.TextFragmentNode(position, n.StringLiteralNode(position, 'LV-2A'))
    lv1a_lv2b = n.BlockNode(position, n.IdentifierNode(position,           'LV-2B'))
    lv2b_lv3a = n.TextFragmentNode(position, n.StringLiteralNode(position, 'LV-3A'))

    node_root.add(root_lv1a)
    root_lv1a.add(lv1a_lv2a)
    lv1a_lv2a.add(lv2a_lv3a)
    root_lv1a.add(lv1a_lv2b)
    lv1a_lv2b.add(lv2b_lv3a)

    # Act.
    transformer = ASTTransformer()
    transformer.expand_whitespace(node_root)

    # Assert.
    assert 1 == len(node_root.body)
    assert 3 == len(root_lv1a.body)
    assert 1 == len(lv1a_lv2a.body)
    assert 1 == len(lv1a_lv2b.body)

    assert n.BlockNode  == type(root_lv1a.body[0])
    assert n.SpacerNode == type(root_lv1a.body[1])
    assert n.BlockNode  == type(root_lv1a.body[2])

def test_expand_whitespace__text_fragment_before_deeply_nested_text_fragment__add_spacers():
    # Arrange.
    position  = Position(-1, -1)
    node_root = n.ProgramNode(position)
    root_lv1a = n.BlockNode(position, n.IdentifierNode(position,           'LV-1A'))
    lv1a_lv2a = n.TextFragmentNode(position, n.StringLiteralNode(position, 'LV-2A'))
    lv1a_lv2b = n.BlockNode(position, n.IdentifierNode(position,           'LV-2B'))
    lv2b_lv3a = n.BlockNode(position, n.IdentifierNode(position,           'LV-3A'))
    lv3a_lv4a = n.BlockNode(position, n.IdentifierNode(position,           'LV-4A'))
    lv4a_lv5a = n.BlockNode(position, n.IdentifierNode(position,           'LV-5A'))
    lv5a_lv6a = n.BlockNode(position, n.IdentifierNode(position,           'LV-6A'))
    lv6a_lv7a = n.TextFragmentNode(position, n.StringLiteralNode(position, 'LV-7A'))

    node_root.add(root_lv1a)
    root_lv1a.add(lv1a_lv2a)
    root_lv1a.add(lv1a_lv2b)
    lv1a_lv2b.add(lv2b_lv3a)
    lv2b_lv3a.add(lv3a_lv4a)
    lv3a_lv4a.add(lv4a_lv5a)
    lv4a_lv5a.add(lv5a_lv6a)
    lv5a_lv6a.add(lv6a_lv7a)

    # Act.
    transformer = ASTTransformer()
    transformer.expand_whitespace(node_root)

    # Assert.
    assert 1 == len(node_root.body)
    assert 3 == len(root_lv1a.body)
    assert 1 == len(lv1a_lv2b.body)
    assert 1 == len(lv2b_lv3a.body)
    assert 1 == len(lv3a_lv4a.body)
    assert 1 == len(lv4a_lv5a.body)
    assert 1 == len(lv5a_lv6a.body)

    assert n.TextFragmentNode == type(root_lv1a.body[0])
    assert n.SpacerNode       == type(root_lv1a.body[1])
    assert n.BlockNode        == type(root_lv1a.body[2])

def test_expand_whitespace__text_fragment_after_deeply_nested_text_fragment__add_spacers():
    # Arrange.
    position  = Position(-1, -1)
    node_root = n.ProgramNode(position)
    root_lv1a = n.BlockNode(position, n.IdentifierNode(position,           'LV-1A'))
    lv1a_lv2a = n.BlockNode(position, n.IdentifierNode(position,           'LV-2A'))
    lv2a_lv3a = n.BlockNode(position, n.IdentifierNode(position,           'LV-3A'))
    lv3a_lv4a = n.BlockNode(position, n.IdentifierNode(position,           'LV-4A'))
    lv4a_lv5a = n.BlockNode(position, n.IdentifierNode(position,           'LV-5A'))
    lv5a_lv6a = n.BlockNode(position, n.IdentifierNode(position,           'LV-6A'))
    lv6a_lv7a = n.TextFragmentNode(position, n.StringLiteralNode(position, 'LV-7A'))
    lv1a_lv2b = n.TextFragmentNode(position, n.StringLiteralNode(position, 'LV-2B'))

    node_root.add(root_lv1a)
    root_lv1a.add(lv1a_lv2a)
    root_lv1a.add(lv1a_lv2b)
    lv1a_lv2a.add(lv2a_lv3a)
    lv2a_lv3a.add(lv3a_lv4a)
    lv3a_lv4a.add(lv4a_lv5a)
    lv4a_lv5a.add(lv5a_lv6a)
    lv5a_lv6a.add(lv6a_lv7a)

    # Act.
    transformer = ASTTransformer()
    transformer.expand_whitespace(node_root)

    # Assert.
    assert 1 == len(node_root.body)
    assert 3 == len(root_lv1a.body)
    assert 1 == len(lv1a_lv2a.body)
    assert 1 == len(lv2a_lv3a.body)
    assert 1 == len(lv3a_lv4a.body)
    assert 1 == len(lv4a_lv5a.body)
    assert 1 == len(lv5a_lv6a.body)

    assert n.BlockNode        == type(root_lv1a.body[0])
    assert n.SpacerNode       == type(root_lv1a.body[1])
    assert n.TextFragmentNode == type(root_lv1a.body[2])

def test_expand_whitespace__orphan_text_fragment__adds_no_spacers():
    # Arrange.
    position  = Position(-1, -1)
    node_root = n.TextFragmentNode(position, n.StringLiteralNode(position, 'LV-7A'))

    # Act.
    transformer = ASTTransformer()
    transformer.expand_whitespace(node_root)

    # Assert.
    assert None is node_root.parent

def test_remove_empty_blocks__shallowly_nested_blocks__removes_blocks():
    # Arrange.
    position  = Position(-1, -1)
    node_root = n.ProgramNode(position)
    root_lv1a = n.BlockNode(position, n.IdentifierNode(position,           'LV-1A'))
    lv1a_lv2a = n.BlockNode(position, n.IdentifierNode(position,           'LV-2A'))
    lv1a_lv2b = n.TextFragmentNode(position, n.StringLiteralNode(position, 'LV-2B'))
    lv1a_lv2c = n.BlockNode(position, n.IdentifierNode(position,           'LV-2C'))
    lv1a_lv2d = n.TextFragmentNode(position, n.StringLiteralNode(position, 'LV-2D'))
    lv1a_lv2e = n.BlockNode(position, n.IdentifierNode(position,           'LV-2E'))

    node_root.add(root_lv1a)
    root_lv1a.add(lv1a_lv2a)
    root_lv1a.add(lv1a_lv2b)
    root_lv1a.add(lv1a_lv2c)
    root_lv1a.add(lv1a_lv2d)
    root_lv1a.add(lv1a_lv2e)

    # Act.
    transformer = ASTTransformer()
    transformer.remove_empty_blocks(node_root)

    # Assert.
    assert 1 == len(node_root.body)
    assert 2 == len(root_lv1a.body)

    assert n.TextFragmentNode == type(root_lv1a.body[0])
    assert n.TextFragmentNode == type(root_lv1a.body[1])

def test_remove_empty_blocks__deeply_nested_blocks__removes_blocks():
    # Arrange.
    position  = Position(-1, -1)
    node_root = n.ProgramNode(position)
    root_lv1a = n.BlockNode(position, n.IdentifierNode(position,           'LV-1A'))
    lv1a_lv2a = n.TextFragmentNode(position, n.StringLiteralNode(position, 'LV-2A'))
    lv1a_lv2b = n.BlockNode(position, n.IdentifierNode(position,           'LV-2B'))
    lv2b_lv3a = n.BlockNode(position, n.IdentifierNode(position,           'LV-3A'))
    lv3a_lv4a = n.BlockNode(position, n.IdentifierNode(position,           'LV-4A'))
    lv4a_lv5a = n.BlockNode(position, n.IdentifierNode(position,           'LV-5A'))
    lv5a_lv6a = n.BlockNode(position, n.IdentifierNode(position,           'LV-6A'))
    lv6a_lv7a = n.BlockNode(position, n.IdentifierNode(position,           'LV-7A'))

    node_root.add(root_lv1a)
    root_lv1a.add(lv1a_lv2a)
    root_lv1a.add(lv1a_lv2b)
    lv1a_lv2b.add(lv2b_lv3a)
    lv2b_lv3a.add(lv3a_lv4a)
    lv3a_lv4a.add(lv4a_lv5a)
    lv4a_lv5a.add(lv5a_lv6a)
    lv5a_lv6a.add(lv6a_lv7a)

    # Act.
    transformer = ASTTransformer()
    transformer.remove_empty_blocks(node_root)

    # Assert.
    assert 1 == len(node_root.body)
    assert 1 == len(root_lv1a.body)

    assert n.TextFragmentNode == type(root_lv1a.body[0])

def test_transform__adds_spaces_and_removes_empty_blocks():
    # Arrange.
    position  = Position(-1, -1)
    node_root = n.ProgramNode(position)
    root_lv1a = n.BlockNode(position, n.IdentifierNode(position,           'LV-1A'))
    lv1a_lv2a = n.TextFragmentNode(position, n.StringLiteralNode(position, 'LV-2A'))
    lv1a_lv2b = n.BlockNode(position, n.IdentifierNode(position,           'LV-2B'))
    lv1a_lv2c = n.BlockNode(position, n.IdentifierNode(position,           'LV-2C'))
    lv2c_lv3a = n.TextFragmentNode(position, n.StringLiteralNode(position, 'LV-3A'))

    node_root.add(root_lv1a)
    root_lv1a.add(lv1a_lv2a)
    root_lv1a.add(lv1a_lv2b)
    root_lv1a.add(lv1a_lv2c)
    lv1a_lv2c.add(lv2c_lv3a)

    # Act.
    transformer = ASTTransformer()
    transformer.transform(node_root)

    # Assert.
    assert 1 == len(node_root.body)
    assert 3 == len(root_lv1a.body)
    assert 1 == len(lv1a_lv2c.body)

    assert n.TextFragmentNode == type(root_lv1a.body[0])
    assert n.SpacerNode       == type(root_lv1a.body[1])
    assert n.BlockNode        == type(root_lv1a.body[2])
