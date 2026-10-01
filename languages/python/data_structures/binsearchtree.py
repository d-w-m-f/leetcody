class BaseNode:
    value = 0

    def __repr__(self):
            return f"Node({self.value})"
    
    def __ge__(self, other):
            return self.value >= other.value
    
    def __gt__(self, other):
        return self.value > other.value

    def __le__(self, other):
        return self.value <= other.value

    def __lt__(self, other):
        return self.value < other.value

    def __eq__(self, other):
        if other is None or not hasattr(other, 'value'):
            return False
        return self.value == other.value
    
    def __ne__(self, other):
        return not self.__eq__(other)


class BinSearchTreeNode(BaseNode):
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None



class BinSearchTree:
    def __init__(self, root: BinSearchTreeNode):
        self.root = root
        self._size = 1

    def add(self, node: BinSearchTreeNode) -> int | None:
        def recursive_add(node_at: BinSearchTreeNode, new_node: BinSearchTreeNode):
            if new_node <= node_at:
                if node_at.left is None:
                    node_at.left = new_node
                    return
                return recursive_add(node_at=node_at.left, new_node=new_node)

            if node_at.right is None:
                node_at.right = new_node
                return
            recursive_add(node_at=node_at.right, new_node=new_node)

        recursive_add(node_at=self.root, new_node=node)
        self._size = self._size + 1


    def find(self, value) -> bool:
        def recursive_find(node_at: BinSearchTreeNode, value: BinSearchTreeNode):
            if node_at is None:
                return False
            if node_at == value:
                return True
            if value < node_at:
                return recursive_find(node_at=node_at.left, value=value)
            return recursive_find(node_at=node_at.right, value=value)

        node_value = BinSearchTreeNode(value=value)
        return recursive_find(node_at=self.root, value=node_value)

    def delete(self, value):
        pass

class ArrBinSearchTreeNode(BaseNode):
    def __init__(self, value):
        self.value = value


class ArrBinSearchTree:
    def __init__(self, root: ArrBinSearchTreeNode):
        self._size = 0
        self._capacity = 8
        self._tree = [None for i in range(self._capacity)]
        self.add(root)

    def _is_full(self) -> bool:
        return self._size == self._capacity


    def add(self, node: ArrBinSearchTreeNode):
        def recursive_add(node, at):
            while at >= self._capacity:
                self._grow_size()

            lookup_node = self._tree[at]
            if lookup_node is None:
                self._tree[at] = node
                return at
            
            if node <= lookup_node:
                return recursive_add(node, (at*2)+1) 
            return recursive_add(node, (at*2)+2)

        if self._size == 0:
            return self._add_root(node)
        
        added_at = recursive_add(node=node, at=0)
        self._size = self._size + 1
        if self._is_full():
            self._grow_size()
        return added_at
    
    def _grow_size(self):
        tree_bffr = [None for i in range(2*self._capacity)]
        for i in range(len(self._tree)):
            tree_bffr[i] = self._tree[i]

        self._capacity = 2*self._capacity
        self._tree = tree_bffr

    def _add_root(self, node: ArrBinSearchTreeNode):
        self._tree[0] = node
        self._size = 1
        return 0

    def delete(self):
        pass

    def shrink_size(self):
        pass