from typing import Optional
from tinta import node as n

class ASTTransformer:
    """AST transformer for the Tinta language.

    This class normalizes the AST received from the parser and prepares it
    for the generator by injecting spacer nodes and pruning empty blocks.
    """
    def __init__(self) -> None:
        pass

    def _find_first_text_child(self, node: n.BlockNode) -> Optional[n.TextFragmentNode]:
        for child_node in node.body:
            if type(child_node) is n.TextFragmentNode:
                return child_node
            if type(child_node) is n.BlockNode:
                return self._find_first_text_child(child_node)

    def _find_last_text_child(self, node: n.BlockNode) -> Optional[n.TextFragmentNode]:
        for child_node in reversed(node.body):
            if type(child_node) is n.TextFragmentNode:
                return child_node
            if type(child_node) is n.BlockNode:
                return self._find_last_text_child(child_node)

    def _find_following_text_node(self, node: n.StatementNode) -> Optional[n.TextFragmentNode]:
        if node.parent is None:
            return None

        index = node.parent.body.index(node)
        if index == len(node.parent.body) - 1:
            return self._find_following_text_node(node.parent)

        next_node = node.parent.body[index + 1]
        if type(next_node) is n.TextFragmentNode:
            return next_node
        assert type(next_node) is n.BlockNode
        if len(next_node.body) == 0:
            return self._find_following_text_node(next_node)
        return self._find_first_text_child(next_node)

    def _find_preceding_text_node(self, node: n.StatementNode) -> Optional[n.TextFragmentNode]:
        if node.parent is None:
            return None

        index = node.parent.body.index(node)
        if index == 0:
            return self._find_preceding_text_node(node.parent)

        previous_node = node.parent.body[index - 1]
        if type(previous_node) is n.TextFragmentNode:
            return previous_node
        assert type(previous_node) is n.BlockNode
        if len(previous_node.body) == 0:
            return self._find_preceding_text_node(previous_node)
        return self._find_last_text_child(previous_node)

    def _adjust_slot_right(self, left_node: n.TextFragmentNode) -> None:
        right_node = self._find_following_text_node(left_node)
        if right_node is None:
            left_node.strip_right = True
        elif not left_node.strip_right and not right_node.strip_left:
            left_node.strip_right = True

    def _adjust_slot_left(self, right_node: n.TextFragmentNode) -> None:
        left_node = self._find_preceding_text_node(right_node)
        if left_node is None:
            right_node.strip_left = True
        # elif not left_node.strip_right and not right_node.strip_left:
        #     left_node.strip_right = True

    def _adjust_slots(self, node: n.Node) -> None:
        if isinstance(node, n.StatementWithBodyNode):
            for child_node in node.body:
                self._adjust_slots(child_node)
        if isinstance(node, n.TextFragmentNode):
            self._adjust_slot_left(node)
            self._adjust_slot_right(node)

    def _find_spacer_slot_left(self, node: n.StatementNode) -> n.StatementNode:
        assert node.parent is not None
        if node.parent.body[0] != node:
            return node
        return self._find_spacer_slot_left(node.parent)

    def _inject_spacer_left(self, node: n.TextFragmentNode) -> None:
        if node.strip_left:
            return
        left_node = self._find_spacer_slot_left(node)
        assert left_node.parent is not None
        index = left_node.parent.body.index(left_node)

        target_node = left_node.parent.body[index]
        spacer_node = n.SpacerNode(target_node.position)
        left_node.parent.insert(index, spacer_node)

    def _inject_spacers(self, node: n.Node) -> None:
        if not isinstance(node, n.StatementWithBodyNode):
            return

        for child_node in node.body[:]:
            if isinstance(child_node, n.TextFragmentNode):
                self._inject_spacer_left(child_node)
            elif isinstance(child_node, n.StatementWithBodyNode):
                self._inject_spacers(child_node)

    def expand_whitespace(self, node: n.StatementWithBodyNode) -> None:
        """Recursively converts implicit spacing into SpacerNodes.

        Args:
            node (Node): The node whose body will be processed.
        """
        self._adjust_slots(node)
        self._inject_spacers(node)

    def remove_empty_blocks(self, node: n.StatementWithBodyNode) -> None:
        """Recursively prunes empty blocks nodes from the given node's body.

        Args:
            node (StatementWithBodyNode): The node whose body will be pruned.
        """
        for child_node in node.body[:]:
            if not isinstance(child_node, n.StatementWithBodyNode):
                continue
            if len(child_node.body) != 0:
                self.remove_empty_blocks(child_node)
            if len(child_node.body) == 0:
                node.remove(child_node)

    def transform(self, node: n.ProgramNode) -> None:
        """Executes the transformation pipeline on the program's AST.

        Args:
            node (ProgramNode): The root node of the AST.
        """
        self.remove_empty_blocks(node)
        self.expand_whitespace(node)
