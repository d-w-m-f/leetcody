import math
from typing import Literal


def calculate_heap_capacity_from(heigth: int) -> int:
    return 2 ** heigth - 1

def last_non_leaf(size: int) -> int | None:
    if size == 1:
        return None

    height_non_leafs = math.floor(math.sqrt(size)) - 1
    return calculate_heap_capacity_from(heigth=height_non_leafs)

class Heap:
    HEAP_T = Literal['min', 'max']
    REDIMENTION_SCALE = Literal['up', 'down']
    HEAP_MIN_HEIGHT = 3

    def __init__(self, value, min_or_max: HEAP_T = 'min'):
        self._heap_t = min_or_max
        self._size = 0
        self._heigth = self.HEAP_MIN_HEIGHT
        self._capacity = calculate_heap_capacity_from(heigth=self._heigth)

        # Initializes heap root
        self._heap_arr = [None for i in range(self._capacity)]
        self._heap_arr[0] = value
        self._size = self._size + 1

    def peek(self):
        """
        Returns min or max, according to the heap type
        
        If heap is empty, returns 'None'

        Time complexity: O(1)
        """
        if self._size == 0:
            return None
        return self._heap_arr[0]


    def insert(self, new_value) -> None:
        """
        Inserts a new value into the heap. 

        Time complexity: O(lg(n))
        n := height of the heap
        """
        self._check_resizing()

        inserting_at = self._size-1
        self._heap_arr[inserting_at] = new_value
        self._size = self._size + 1

        self._heapify_up(at=inserting_at)

    def pop(self):
        """
        Remove the value at the root node and returns it. 
        Performs heapify operations to keep structural integrity.

        Time complexity: O(lg(n))
        n := height of the heap
        """
        if self._size == 0:
            return

        # Switch root and last element in-place
        self._switch_nodes_inplace(at_1 = 0, at_2=self._size-1)

        # Erases last element (now older root) and decrement size
        self._heap_arr[self._size-1] = None
        self._size = self._size - 1

        # Heapify_down from the root
        self._heapify_down(at=0)

    def heapify(self, arr):
        """
        Receives an array of elements and constructs a heap representation of its elements.
        Consuming the array whole does have the benefit of running on linear time, 
        in opposition of n.lg(n) if we were inserting elements one by one.
        
        NOTE: This action is destructive on the current data held by the Heap, meaning that it
        will become a representation of the array, and forget all previous information.

        TIme complexity: O(n)
        n := length of the array.
        """
        self._heigth = math.ceil(math.sqrt(len(arr)))
        self._capacity = calculate_heap_capacity_from(heigth=self._heigth)

        self._heap_arr = [None for i in range(self._capacity)]
        for i in range(len(arr)):
            self._heap_arr[i] = arr[i]

        last_non_leaf_idx = last_non_leaf(size=self._size)
        for node_idx in range(start=last_non_leaf_idx, stop=1, step=-1):
            self.heapify_up(node_idx)

    def fit(self):
        """
        Scales down resizable array, if fitting.
        Applies the criteria only when 
        """

        should_scale_down = self._size <= calculate_heap_capacity_from(heigth=self._heigth-2)
        """ Why 'should_scale_down' follows this rule
            
            For heigth -> capacity of our resizable arr, we have:
            3 -> 7
            4 -> 15
            5 -> 31
            6 -> 63
            ...

            Suppose the heigth is at N, we consider the heap is sufficiently empty for resizing if
            scaling its heigth by 1 (thus its capacity in half) still leaves roughtly 50% empty spots.
            
            So, when size <= calculate_heap_capacity_from(height-2).
        """

        if should_scale_down:
            self._redimention(scale='down')

    def heap_type(self) -> str:
        return self._heap_t


    def _heapify_up(self, at: int):
        if self._is_leaf_node(at=at):
            return

        next_at = self._ensure_heap_property(at=at)
        if next_at is not None:
            self._heapify_up(at=next_at)


    def _heapify_down(self, at: int):
        if self._is_leaf_node(at=at):
            return

        next_at = self._ensure_heap_property(at=at)
        if next_at is not None:
            self._heapify_down(at=next_at)

    def _redimention(self, scale: REDIMENTION_SCALE = 'up'):
        """
        Applies scalign rules for our Heap's resizable array.
        """
        def scale_up():
            self._heigth = self._heigth + 1
            self._capacity = calculate_heap_capacity_from(heigth=self._heigth)
            new_arr_buffer = [None for i in range(self._capacity)]
            for i in range(len(self._heap_arr)):
                new_arr_buffer[i] = self._heap_arr[i]

        def scale_down():
            self._heigth = max(self.HEAP_MIN_HEIGHT, self._heigth - 1)
            self._capacity = calculate_heap_capacity_from(heigth=self._heigth)
            new_arr_buffer = [None for i in range(self._capacity)]
            for i in range(len(new_arr_buffer)):
                new_arr_buffer[i] = self._heap_arr[i]


        if scale == 'up':
            scale_up()
        else:
            scale_down()

    def _is_leaf_node(self, at: int) -> bool:
        left_idx = 2*at + 1
        right_idx = 2*at + 2

        if left_idx > self._capacity:
            return True
        if self._heap_arr[left_idx] == None and self._heap_arr[right_idx] == None:
            return True

        return False

    def _ensure_heap_property(self, at: int) -> int | None:
        def ensure_min_heap_structure(at: int) -> int | None:
            left_idx = 2*at + 1
            right_idx = 2*at + 2

            if (
                self._heap_arr[at] <= self._heap_arr[left_idx] and 
                self._heap_arr[at] <= self._heap_arr[right_idx]
            ):
                return None

            if self._heap_arr[left_idx] <= self._heap_arr[right_idx]:
                 self._switch_nodes_inplace(at_1=at, at_2=left_idx)
                 return left_idx

            self._switch_nodes_inplace(at_1=at, at_2=right_idx)
            return right_idx

        
        def ensure_max_heap_structure(at: int) -> int | None:
            left_idx = 2*at + 1
            right_idx = 2*at + 2

            if (
                self._heap_arr[at] >= self._heap_arr[left_idx] and 
                self._heap_arr[at] >= self._heap_arr[right_idx]
            ):
                return None

            if self._heap_arr[left_idx] >= self._heap_arr[right_idx]:
                self._switch_nodes_inplace(at_1=at, at_2=left_idx)
                return left_idx

            self._switch_nodes_inplace(at_1=at, at_2=right_idx)
            return right_idx
        
        if self._heap_t == 'min':
            return ensure_min_heap_structure(at=at)
        return ensure_max_heap_structure(at=at)

    def _switch_nodes_inplace(self, at_1: int, at_2: int):
        aux = self._heap_arr[at_1]
        self._heap_arr[at_1] = self._heap_arr[at_2]
        self._heap_arr[at_2] = aux
        