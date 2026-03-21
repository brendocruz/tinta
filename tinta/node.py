from weakref import ref, ReferenceType
from dataclasses import dataclass, field
from typing import Optional
from tinta.token import Position

@dataclass(eq=False)
class Node[T: 'Node']:
    """Base class for all nodes.

    Attributes:
        position (Position): The start location in the source code.
    """
    position: Position

    _parent_ref: Optional[ReferenceType[T]] = field(init=False,
                                                    repr=False,
                                                    default=None,
                                                    compare=False)

    @property
    def parent(self) -> T | None:
        if self._parent_ref:
            return self._parent_ref()
        return None

    @parent.setter
    def parent(self, value: Optional[T]) -> None:
        if value is None:
            self._parent_ref = None
        else:
            self._parent_ref = ref(value)

@dataclass(eq=False)
class IdentifierNode(Node):
    """A node for an identifier.

    Attributes:
        value (str): The name of the identifier
    """
    value: str

@dataclass(eq=False)
class StringLiteralNode(Node):
    """A node for a string literal.

    Attributes:
        value (str): The text context of the string, excluding delimiters.
    """
    value: str

@dataclass(eq=False)
class LabelNode(Node):
    """A node for a label.
    
    Attributes:
        name (IdentifierNode): The identifier naming the label.
    """
    name: IdentifierNode

@dataclass(eq=False)
class GroupLabelNode(LabelNode):
    """A node for a group label."""
    pass

@dataclass(eq=False)
class AnchorLabelNode(LabelNode):
    """A node for an anchor label."""
    pass

@dataclass(eq=False)
class LinkLabelNode(LabelNode):
    """A node for a link label."""
    pass

@dataclass(eq=False)
class StatementNode(Node['StatementWithBodyNode']):
    """A node for a statement"""
    pass

@dataclass(eq=False, kw_only=True)
class StatementWithBodyNode(StatementNode):
    """A node for a statement with a body attribute.

    Attributes:
        body (list[StatementNode]): The list of statements contained within the
            block.
    """
    body: list[StatementNode] = field(default_factory=list)

    # TODO: add docstring.
    def add(self, node: StatementNode):
        self.body.append(node)
        node.parent = self

    # TODO: add docstring.
    def remove(self, node: StatementNode):
        self.body.remove(node)
        node.parent = None

    # TODO: add docstring.
    def insert(self, index: int, node: StatementNode):
        self.body.insert(index, node)
        node.parent = self

@dataclass(eq=False)
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

@dataclass(eq=False)
class BlockNode(StatementWithBodyNode):
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

@dataclass(eq=False)
class ProgramNode(StatementWithBodyNode):
    """A node for a whole program."""
    pass

@dataclass(eq=False)
class SpacerNode(StatementNode):
    """A node for a text spacer."""
    pass
