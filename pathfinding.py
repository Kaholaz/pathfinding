from typing import Callable, Optional

from queue import PriorityQueue
from utils import LoadingBarMocker, Preprocess
from file_handling import read_complete
from utils import Node, is_gas_station

INFINITY = float("inf")


class DijkstraHeap:
    dist_heap: list[int]
    node_heap: list[int]
    in_heap: list[bool]
    heap_positions: list[int]


class PathFinder:
    nodes: list[Node]
    loading_bar: bool
    current_loading_bar: LoadingBarMocker

    origin: int
    destination: int
    considered_nodes: int
    best_distances: list[int]
    previous: list[int]
    visited: list[bool]
    heap: PriorityQueue

    to_landmarks: Preprocess
    from_landmarks: Preprocess

    def __init__(self, nodes: list[Node], loading_bar: bool = False) -> None:
        self.nodes = nodes
        self.loading_bar = loading_bar

    def reset_common(self):
        self.origin = None
        self.destination = None
        self.current_loading_bar = LoadingBarMocker()
        self.considered_nodes = 0
        self.best_distances = [INFINITY] * len(self.nodes)
        self.previous = [None] * len(self.nodes)
        self.visited = [False] * len(self.nodes)
        self.heap = PriorityQueue()

    def reset_preprocess(self):
        self.to_landmarks = [[0] * len(self.nodes)]
        self.from_landmarks = [[0] * len(self.nodes)]

    def set_preprocess(
        self,
        to_landmarks: list[list[float | int]],
        from_landmarks: list[list[float | int]],
    ):
        self.to_landmarks = to_landmarks
        self.from_landmarks = from_landmarks

    def find_next_considerations(
        self, target_predicate: Optional[Callable[[int], bool]] = None
    ):
        if target_predicate is None:
            if self.destination is not None:
                target_predicate = lambda i: i == self.destination
            else:
                target_predicate = lambda i: False

        if self.loading_bar:
            from tqdm import tqdm

            self.current_loading_bar = tqdm(
                total=len(self.nodes), desc=self.loading_desc
            )
        else:
            self.current_loading_bar = LoadingBarMocker()
            if self.loading_desc:
                print(self.loading_desc)

        while not self.heap.empty():
            heap_result = self.heap.get()
            current_distance, current_node = heap_result[-2:]

            if self.visited[current_node]:
                continue

            self.visited[current_node] = True
            if target_predicate(current_node):
                yield current_node, current_distance

            if self.loading_bar:
                self.current_loading_bar.update(1)
            self.considered_nodes += 1
            for target, cost in self.nodes[current_node].edges:
                if self.visited[target]:
                    continue
                yield current_node, target, cost + self.best_distances[current_node]

    def get_path(self, destination: int):

        current_node = destination
        reverse_path = [current_node]

        while (current_node := self.previous[current_node]) is not None:
            reverse_path.append(current_node)

        return list(map(lambda n: self.nodes[n], reverse_path[::-1]))

    def run_dijkstra(
        self,
        origin: int,
        destination: Optional[int] = None,
        loading_desc: str = "Running dijkstra...",
    ) -> tuple[Optional[int], Optional[list[Node]]]:
        self.reset_common()

        self.loading_desc = loading_desc
        self.best_distances[origin] = 0
        self.heap.put((0, origin))

        self.origin, self.destination = origin, destination
        self.loading_desc = loading_desc

        for consideration in self.find_next_considerations():
            if len(consideration) == 2:
                current_node, distance = consideration
                assert current_node == destination
                break
            else:
                current_node, target, distance = consideration

            if distance < self.best_distances[target]:
                self.best_distances[target] = distance
                self.previous[target] = current_node
                self.heap.put((distance, target))

        if self.loading_bar:
            self.current_loading_bar.close()

        if destination is None:
            return None, None
        else:
            return self.best_distances[destination], self.get_path(destination)

    def closest_n_nodes(
        self,
        origin: int,
        n: int,
        predicate: Callable[[Node], bool],
        loading_desc: str = "Finding n closest...",
    ) -> list[tuple[Node, int]]:
        self.reset_common()

        self.best_distances[origin] = 0
        self.heap.put((0, origin))

        self.origin = origin
        self.loading_desc = loading_desc
        found_nodes: list[Node] = list()

        for consideration in self.find_next_considerations(
            lambda n: predicate(self.nodes[n])
        ):
            if len(consideration) == 2:
                current_node, distance = consideration
                assert predicate(self.nodes[current_node])
                found_nodes.append((current_node, distance))
                if len(found_nodes) == n:
                    break
                continue
            else:
                current_node, target, distance = consideration

                if distance < self.best_distances[target]:
                    self.best_distances[target] = distance
                    self.previous[target] = current_node
                    self.heap.put((distance, target))

        if self.loading_bar:
            self.current_loading_bar.close()
        return found_nodes

    def run_alt(
        self,
        origin,
        destination,
        to_landmarks: Optional[Preprocess] = None,
        from_landmarks: Optional[Preprocess] = None,
        loading_desc: str = "Running alt...",
    ) -> tuple[float | int, list[Node]]:
        if to_landmarks is not None:
            self.to_landmarks = to_landmarks
        if from_landmarks is not None:
            self.from_landmarks = from_landmarks

        self.reset_common()

        self.best_distances[origin] = 0
        self.heap.put((0, origin))
        node_to_goal_estimate: list[float | int] = [INFINITY] * len(self.nodes)

        self.origin, self.destination = origin, destination
        self.loading_desc = loading_desc

        for consideration in self.find_next_considerations():
            if len(consideration) == 2:
                current_node, distance = consideration
                assert current_node == destination
                break
            else:
                current_node, target, distance = consideration

            # Calculate node to goal estimate
            if node_to_goal_estimate[target] is INFINITY:
                from_estimate = max(
                    from_landmark[destination] - from_landmark[target]
                    for from_landmark in self.from_landmarks
                )
                to_estimate = max(
                    to_landmark[target] - to_landmark[destination]
                    for to_landmark in self.to_landmarks
                )
                node_to_goal_estimate[target] = max(0, from_estimate, to_estimate)

            if distance < self.best_distances[target]:
                self.best_distances[target] = distance
                self.previous[target] = current_node
                self.heap.put(
                    (distance + node_to_goal_estimate[target], distance, target)
                )

        if self.loading_bar:
            self.current_loading_bar.close()
        return (self.best_distances[destination], self.get_path(destination))
