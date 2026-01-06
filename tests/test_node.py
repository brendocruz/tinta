from tinta.node import Node
from tinta.token import Position

def test_node_parent_assignment_returns_correct_object():
    position    = Position(0, 0)
    node_parent = Node(position)
    node_child  = Node(position)
    node_child.parent = node_parent

    assert node_child.parent is node_parent

def test_node_parent_is_none_by_default():
    position = Position(0, 0)
    node     = Node(position)

    assert node.parent is None
