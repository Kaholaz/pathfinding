from typing import Optional

from utils import Node

INFINITY = float("inf")

class DijkstraHeap:
    dist_heap: list[int]
    node_heap: list[int]
    in_heap: list[bool]
    heap_positions: list[int]

    def __init__(self, number_of_nodes):
        self.dist_heap = list()
        self.node_heap = list()
        self.in_heap = [False] * number_of_nodes
        self.heap_positions = [0] * number_of_nodes

    def swap(self, a: int, b: int):
        node_a = self.node_heap[a]
        node_b = self.node_heap[b]

        self.heap_positions[node_a], self.heap_positions[node_b] = b, a
        self.dist_heap[a], self.dist_heap[b] = self.dist_heap[b], self.dist_heap[a]
        self.node_heap[a], self.node_heap[b] = self.node_heap[b], self.node_heap[a]

    def fix_heap(self, i: int):
        if i >= len(self):
            return

        value = self.dist_heap[i]
        while (left := i * 2 + 1) < len(self):
            right = left + 1

            min = left
            if right < len(self) and self.dist_heap[right] < self.dist_heap[min]:
                min = right

            if self.dist_heap[min] < value:
                self.swap(i, min)

            i = min

    def update_entry(self, node_number: int, dist: int):
        if self.in_heap[node_number]:
            i = self.heap_positions[node_number]
            self.dist_heap[i] = dist
        else:
            i = len(self.dist_heap)
            self.dist_heap.append(dist)
            self.node_heap.append(node_number)
            self.heap_positions[node_number] = i
            self.in_heap[node_number] = True

        while i > 0 and self.dist_heap[i] < self.dist_heap[(parent := (i - 1) // 2)]:
            self.swap(i, parent)
            i = parent

    def pop_heap(self) -> tuple[int, int]:
        """Returns the top node and dist as a tuple: (node, dist)"""
        last_i = len(self.dist_heap) - 1
        self.swap(last_i, 0)

        dist = self.dist_heap.pop()
        node = self.node_heap.pop()
        self.in_heap[node] = False

        self.fix_heap(0)
        return node, dist

    def __len__(self) -> int:
        return len(self.dist_heap)


def run_dijkstra(
    nodes: list[Node], origin: int, destination: Optional[int] = None, loading_bar: bool = False
) -> tuple[list[float], list[Optional[int]]]:
    number_of_nodes = len(nodes)
    best_distances: list[float | int] = [INFINITY] * number_of_nodes
    previous: list[Optional[int]] = [None] * number_of_nodes
    visited: list[bool] = [False] * number_of_nodes

    best_distances[origin] = 0
    heap: DijkstraHeap = DijkstraHeap(number_of_nodes)
    heap.update_entry(origin, 0)

    if loading_bar:
        from tqdm import trange # type: ignore
        _range = trange(len(nodes), desc="Finding paths...")
    else:
        print("Finding paths...")
        _range = range(len(nodes))

    for _ in _range:
        if len(heap) == 0:
            break

        current_node, current_dist = heap.pop_heap()

        for target, cost in nodes[current_node].edges:
            # No need to account for finished nodes, the cost will always be greater than current best.
            if visited[target]:
                continue

            if (new_dist := current_dist + cost) < best_distances[target]:
                best_distances[target] = new_dist
                previous[target] = current_node
                heap.update_entry(target, new_dist)
        
        if destination is not None and destination == current_node:
            break

    return best_distances, previous
