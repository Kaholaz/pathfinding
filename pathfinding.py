from typing import Optional

from queue import PriorityQueue
from utils import Node

INFINITY = float("inf")


class DijkstraHeap:
    dist_heap: list[int]
    node_heap: list[int]
    in_heap: list[bool]
    heap_positions: list[int]


class ListMocker:
    def __getitem__(self, item: int):
        return 0


def run_dijkstra(
    nodes: list[Node],
    origin: int,
    destination: Optional[int] = None,
    loading_bar: bool = False,
    loading_desc="Running dijkstra...",
) -> tuple[list[float], list[Optional[int]]]:
    return run_alt(
        nodes,
        origin,
        (ListMocker(),),
        (ListMocker(),),
        destination,
        loading_bar,
        loading_desc,
    )


def run_alt(
    nodes: list[Node],
    origin: int,
    to_landmarks: list[list[int]],
    from_landmarks: list[list[int]],
    destination: Optional[int] = None,
    loading_bar: bool = False,
    loading_desc: str = "Running alt...",
) -> tuple[list[float], list[Optional[int]]]:
    number_of_nodes = len(nodes)

    # Initializing return lists
    best_distances: list[float | int] = [INFINITY] * number_of_nodes
    previous: list[Optional[int]] = [None] * number_of_nodes

    # Initializing variables
    node_to_goal_estimate: list[Optional[int]]
    if destination is not None:
        node_to_goal_estimate = [None] * number_of_nodes
    else:
        node_to_goal_estimate = [0] * number_of_nodes
    start_to_goal_through_node_estimate: list[int | float] = [
        INFINITY
    ] * number_of_nodes

    visited: list[bool] = [False] * number_of_nodes

    # Finding estimate for origin
    from_estimate = max(
        from_landmark[destination] - from_landmark[origin]
        for from_landmark in from_landmarks
    )
    to_estimate = max(
        to_landmark[origin] - to_landmark[destination] for to_landmark in to_landmarks
    )
    node_to_goal_estimate[origin] = max(0, from_estimate, to_estimate)

    # Setting initializing heap
    best_distances[origin] = 0
    heap = PriorityQueue()
    heap.put((node_to_goal_estimate[origin], 0, origin))

    if loading_bar:
        from tqdm import tqdm  # type: ignore

        # Running pathfinder
        with tqdm(total=len(nodes), desc=loading_desc) as bar:
            while not heap.empty():
                _, current_dist, current_node = heap.get()
                if visited[current_node]:
                    continue
                best_distances[current_node] = current_dist

                bar.update(1)
                visited[current_node] = True
                for target, cost in nodes[current_node].edges:
                    # No need to account for finished nodes, the cost will always be greater than current best.
                    if visited[target]:
                        continue

                    new_dist = current_dist + cost
                    if node_to_goal_estimate[target] is None:
                        from_estimate = max(
                            from_landmark[destination] - from_landmark[target]
                            for from_landmark in from_landmarks
                        )
                        to_estimate = max(
                            to_landmark[target] - to_landmark[destination]
                            for to_landmark in to_landmarks
                        )
                        node_to_goal_estimate[target] = max(
                            0, from_estimate, to_estimate
                        )
                    new_start_to_goal_estimate = (
                        new_dist + node_to_goal_estimate[target]
                    )
                    if (
                        new_start_to_goal_estimate
                        < start_to_goal_through_node_estimate[target]
                    ):
                        start_to_goal_through_node_estimate[
                            target
                        ] = new_start_to_goal_estimate
                        previous[target] = current_node
                        heap.put(
                            (
                                node_to_goal_estimate,
                                new_dist,
                                target,
                            )
                        )

                if destination is not None and destination == current_node:
                    break
    else:
        print(loading_desc)
        while not heap.empty():
            _, current_dist, current_node = heap.get()
            if visited[current_node]:
                continue
            best_distances[current_node] = current_dist

            bar.update(1)
            visited[current_node] = True
            for target, cost in nodes[current_node].edges:
                # No need to account for finished nodes, the cost will always be greater than current best.
                if visited[target]:
                    continue

                new_dist = current_dist + cost
                if node_to_goal_estimate[target] is None:
                    from_estimate = max(
                        from_landmark[destination] - from_landmark[target]
                        for from_landmark in from_landmarks
                    )
                    to_estimate = max(
                        to_landmark[target] - to_landmark[destination]
                        for to_landmark in to_landmarks
                    )
                    node_to_goal_estimate[target] = max(0, from_estimate, to_estimate)
                new_start_to_goal_estimate = new_dist + node_to_goal_estimate[target]
                if (
                    new_start_to_goal_estimate
                    < start_to_goal_through_node_estimate[target]
                ):
                    start_to_goal_through_node_estimate[
                        target
                    ] = new_start_to_goal_estimate
                    previous[target] = current_node
                    heap.put(
                        (
                            node_to_goal_estimate,
                            new_dist,
                            target,
                        )
                    )

            if destination is not None and destination == current_node:
                break

    return best_distances, previous
