import pytest
from data_structures.heap import Heap
from data_structures.binsearchtree import (
    BaseNode,
    BinSearchTreeNode,
    BinSearchTree,
    ArrBinSearchTreeNode,
    ArrBinSearchTree,
)


@pytest.fixture
def min_heap():
    """Provides a fresh min-heap with an initial root value of 25."""
    return Heap(value=25, min_or_max='min')


@pytest.fixture
def max_heap():
    """Provides a fresh max-heap with an initial root value of 25."""
    return Heap(value=25, min_or_max='max')


@pytest.fixture
def populated_min_heap(min_heap):
    """Provides a min-heap populated with multiple distinct elements."""
    values = [50, 30, 20, 15, 10, 8, 16]
    for v in values:
        min_heap.insert(v)
    return min_heap, [25] + values


@pytest.fixture
def populated_max_heap(max_heap):
    """Provides a max-heap populated with multiple distinct elements."""
    values = [10, 50, 20, 40, 30, 70, 5]
    for v in values:
        max_heap.insert(v)
    return max_heap, [25] + values


@pytest.fixture
def sample_bst():
    """Provides a populated pointer-based BST with root 50."""
    tree = BinSearchTree(BinSearchTreeNode(50))
    values = [30, 70, 20, 40, 60, 80]
    for v in values:
        tree.add(BinSearchTreeNode(v))
    return tree, [50] + values


@pytest.fixture
def sample_arr_bst():
    """Provides a populated array-based BST with root 50."""
    tree = ArrBinSearchTree(ArrBinSearchTreeNode(50))
    values = [30, 70, 20, 40]
    indices = []
    for v in values:
        idx = tree.add(ArrBinSearchTreeNode(v))
        indices.append(idx)
    return tree, indices

