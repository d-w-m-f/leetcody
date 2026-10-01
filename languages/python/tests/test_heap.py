import random
import pytest

from data_structures.heap import (
    Heap,
    calculate_heap_capacity_from,
    last_non_leaf,
)


class TestHeapHelpers:
    @pytest.mark.parametrize(
        "height, expected_capacity",
        [
            (0, 0),
            (1, 1),
            (2, 3),
            (3, 7),
            (4, 15),
            (5, 31),
        ],
    )
    def test_calculate_heap_capacity_from(self, height, expected_capacity):
        assert calculate_heap_capacity_from(heigth=height) == expected_capacity

    @pytest.mark.parametrize(
        "size, expected_last_non_leaf",
        [
            (0, None),
            (1, None),
            (2, 0),
            (3, 0),
            (4, 1),
            (5, 1),
            (6, 2),
            (7, 2),
            (8, 3),
            (9, 3),
        ],
    )
    def test_last_non_leaf(self, size, expected_last_non_leaf):
        assert last_non_leaf(size) == expected_last_non_leaf


class TestMinHeap:
    def test_initial_state(self, min_heap):
        assert min_heap.peek() == 25
        assert min_heap._size == 1
        assert min_heap.heap_type() == 'min'

    def test_peek_empty(self):
        heap = Heap(value=10, min_or_max='min')
        heap.pop()
        assert heap.peek() is None
        assert heap.pop() is None

    def test_insert_smaller_updates_root(self, min_heap):
        min_heap.insert(5)
        assert min_heap.peek() == 5
        assert min_heap._size == 2

    def test_insert_larger_keeps_root(self, min_heap):
        min_heap.insert(50)
        assert min_heap.peek() == 25
        assert min_heap._size == 2

    def test_popping_order(self, populated_min_heap):
        heap, all_values = populated_min_heap
        popped = []
        while heap._size > 0:
            popped.append(heap.pop())

        assert popped == sorted(all_values)

    @pytest.mark.parametrize(
        "numbers",
        [
            [-10, 0, -20, 5, -5],
            [7, 7, 7, 7],
            [100, 90, 80, 70, 60, 50, 40, 30, 20, 10],
        ],
    )
    def test_insert_various_sequences(self, numbers):
        heap = Heap(value=numbers[0], min_or_max='min')
        for n in numbers[1:]:
            heap.insert(n)

        popped = [heap.pop() for _ in range(len(numbers))]
        assert popped == sorted(numbers)

    def test_auto_resizing_up_and_down(self, min_heap):
        initial_capacity = min_heap._capacity
        # Insert 30 items to force capacity scale-up beyond initial 7
        for v in range(30, 0, -1):
            min_heap.insert(v)

        assert min_heap._capacity > initial_capacity
        assert min_heap.peek() == 1

        # Pop 28 items
        for _ in range(28):
            min_heap.pop()

        capacity_before_fit = min_heap._capacity
        min_heap.fit()
        assert min_heap._capacity < capacity_before_fit


class TestMaxHeap:
    def test_initial_state(self, max_heap):
        assert max_heap.peek() == 25
        assert max_heap.heap_type() == 'max'

    def test_insert_larger_updates_root(self, max_heap):
        max_heap.insert(100)
        assert max_heap.peek() == 100

    def test_insert_smaller_keeps_root(self, max_heap):
        max_heap.insert(5)
        assert max_heap.peek() == 25

    def test_popping_order(self, populated_max_heap):
        heap, all_values = populated_max_heap
        popped = []
        while heap._size > 0:
            popped.append(heap.pop())

        assert popped == sorted(all_values, reverse=True)


class TestHeapify:
    @pytest.mark.parametrize(
        "input_arr",
        [
            [],
            [42],
            [12, 11, 13, 5, 6, 7],
            [-5, 20, 0, -15, 8, 3, -1],
            [5, 5, 5, 5, 5],
        ],
    )
    def test_heapify_min(self, min_heap, input_arr):
        min_heap.heapify(input_arr)
        assert min_heap._size == len(input_arr)
        if input_arr:
            assert min_heap.peek() == min(input_arr)
            popped = [min_heap.pop() for _ in range(len(input_arr))]
            assert popped == sorted(input_arr)
        else:
            assert min_heap.peek() is None

    @pytest.mark.parametrize(
        "input_arr",
        [
            [],
            [42],
            [12, 11, 13, 5, 6, 7],
            [-5, 20, 0, -15, 8, 3, -1],
        ],
    )
    def test_heapify_max(self, max_heap, input_arr):
        max_heap.heapify(input_arr)
        assert max_heap._size == len(input_arr)
        if input_arr:
            assert max_heap.peek() == max(input_arr)
            popped = [max_heap.pop() for _ in range(len(input_arr))]
            assert popped == sorted(input_arr, reverse=True)
        else:
            assert max_heap.peek() is None

    def test_heapify_large_random_array(self, min_heap):
        data = list(range(100))
        random.seed(42)
        random.shuffle(data)

        min_heap.heapify(data)
        assert min_heap._size == 100

        # Verify underlying min-heap property for each parent
        for i in range(len(data)):
            left = 2 * i + 1
            right = 2 * i + 2
            if left < len(data):
                assert min_heap._heap_arr[i] <= min_heap._heap_arr[left]
            if right < len(data):
                assert min_heap._heap_arr[i] <= min_heap._heap_arr[right]

        popped = [min_heap.pop() for _ in range(100)]
        assert popped == sorted(data)
