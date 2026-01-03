from dataclasses import dataclass, field
from typing import Optional
from tinta.token import Position

@dataclass
class Node:
    """Base class for all nodes.

    Attributes:
        position (Position): The start location in the source code.
    """
    position: Position

@dataclass
class IdentifierNode(Node):
    """A node for an identifier.

    Attributes:
        value (str): The name of the identifier
    """
    value: str

@dataclass
class StringLiteralNode(Node):
    """A node for a string literal.

    Attributes:
        value (str): The text context of the string, excluding delimiters.
    """
    value: str

@dataclass
class LabelNode(Node):
    """A node for a label.
    
    Attributes:
        name (IdentifierNode): The identifier naming the label.
    """
    name: IdentifierNode

@dataclass
class GroupLabelNode(LabelNode):
    """A node for a group label."""
    pass

@dataclass
class AnchorLabelNode(LabelNode):
    """A node for an anchor label."""
    pass

@dataclass
class LinkLabelNode(LabelNode):
    """A node for a link label."""
    pass

@dataclass
class StatementNode(Node):
    """A node for a statement"""
    pass

@dataclass
class CommentNode(StatementNode):
    """A node for a comment.

    Attributes:
        content (str): The text content of the comment.
    """
    content: str

@dataclass
class TextFragmentNode(StatementNode):
    """A node for a text fragment.

    Attributes:
        content (StringLiteralNode): The string node containing the text.
        strip_left (bool): If `True`, leading whitespace is omitted.
        strip_right (bool): If `True`, trailing whitespace is omitted.
    """
    content:     StringLiteralNode
    strip_left:        bool = False
    strip_right:       bool = False

@dataclass
class BlockNode(StatementNode):
    """A node for a block.

    Attributes:
        kind (IdentifierNode): The type name of the block.
        group (Optional[GroupLabelNode]): The group associated with the block.
        anchor (Optional[AnchorLabelNode]): The anchor reference for the block.
        link (Optional[LinkLabelNode]): The link reference for the block.
        body (list[StatementNode]): The list of statements contained within the
            block.
    """
    kind:              IdentifierNode
    group:   Optional[GroupLabelNode] = None
    anchor: Optional[AnchorLabelNode] = None
    link:     Optional[LinkLabelNode] = None
    body:         list[StatementNode] = field(default_factory=list)

@dataclass
class ProgramNode(Node):
    """A node for a whole program.

    Attributes:
        body (list[StatementNode]): The list of statements that make up the
            program.
    """
    body: list[StatementNode] = field(default_factory=list)
