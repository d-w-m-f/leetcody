import pytest

from data_structures.binsearchtree import (
    BaseNode,
    BinSearchTreeNode,
    BinSearchTree,
    ArrBinSearchTreeNode,
    ArrBinSearchTree,
)


class TestBaseNode:
    @pytest.mark.parametrize(
        "val_a, val_b, op, expected",
        [
            (10, 20, "__lt__", True),
            (20, 10, "__lt__", False),
            (10, 10, "__lt__", False),
            (10, 20, "__le__", True),
            (10, 10, "__le__", True),
            (20, 10, "__le__", False),
            (20, 10, "__gt__", True),
            (10, 20, "__gt__", False),
            (10, 10, "__gt__", False),
            (20, 10, "__ge__", True),
            (10, 10, "__ge__", True),
            (10, 20, "__ge__", False),
            (10, 10, "__eq__", True),
            (10, 20, "__eq__", False),
            (10, 20, "__ne__", True),
            (10, 10, "__ne__", False),
        ],
    )
    def test_node_comparisons(self, val_a, val_b, op, expected):
        node_a = BaseNode()
        node_a.value = val_a
        node_b = BaseNode()
        node_b.value = val_b

        comparison_method = getattr(node_a, op)
        assert comparison_method(node_b) == expected

    def test_repr(self):
        node = BaseNode()
        node.value = 42
        assert repr(node) == "Node(42)"


class TestBinSearchTree:
    def test_init_and_size(self):
        root = BinSearchTreeNode(50)
        tree = BinSearchTree(root=root)
        assert tree.root is root
        assert tree._size == 1

    def test_find_present_values(self, sample_bst):
        tree, values = sample_bst
        assert tree._size == len(values)
        for v in values:
            assert tree.find(v) is True

    @pytest.mark.parametrize("missing_value", [0, 25, 35, 45, 65, 75, 999, -10])
    def test_find_absent_values(self, sample_bst, missing_value):
        tree, _ = sample_bst
        assert tree.find(missing_value) is False

    def test_bst_structure_left_and_right_pointers(self):
        root = BinSearchTreeNode(50)
        tree = BinSearchTree(root=root)
        left_child = BinSearchTreeNode(30)
        right_child = BinSearchTreeNode(70)

        tree.add(left_child)
        tree.add(right_child)

        assert tree.root.left is left_child
        assert tree.root.right is right_child
        assert tree._size == 3

    def test_insert_duplicate_goes_left(self):
        root = BinSearchTreeNode(50)
        tree = BinSearchTree(root=root)
        dup = BinSearchTreeNode(50)
        tree.add(dup)

        # In implementation: new_node <= node_at branches to left
        assert tree.root.left is dup
        assert tree._size == 2
        assert tree.find(50) is True


class TestArrBinSearchTree:
    def test_init_and_root(self):
        root = ArrBinSearchTreeNode(50)
        tree = ArrBinSearchTree(root=root)
        assert tree._size == 1
        assert tree._tree[0] is root

    def test_add_places_nodes_at_correct_indices(self, sample_arr_bst):
        tree, indices = sample_arr_bst
        # Root is 50 at index 0
        # 30 <= 50 -> left child index (0*2)+1 = 1
        # 70 > 50  -> right child index (0*2)+2 = 2
        # 20 <= 30 -> left child of 1: (1*2)+1 = 3
        # 40 > 30  -> right child of 1: (1*2)+2 = 4
        assert indices == [1, 2, 3, 4]
        assert tree._tree[0].value == 50
        assert tree._tree[1].value == 30
        assert tree._tree[2].value == 70
        assert tree._tree[3].value == 20
        assert tree._tree[4].value == 40
        assert tree._size == 5

    def test_grow_size_on_skewed_insertions(self):
        root = ArrBinSearchTreeNode(10)
        tree = ArrBinSearchTree(root=root)
        initial_capacity = tree._capacity

        # Inserting strictly increasing elements doubles indices at each depth
        for val in [20, 30, 40, 50]:
            tree.add(ArrBinSearchTreeNode(val))

        assert tree._capacity > initial_capacity
        assert tree._size == 5

