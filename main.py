from alt_preprocess import load_preprocess
from pathfinding import run_alt, run_dijkstra
from utils import Node, cs_to_hour_min_sec
from file_handling import read_complete

from timeit import default_timer as timer


DESTINATIONS = {
    "Oslo": 3430400,
    "Stockholm": 5046415,
    "Trondheim": 7425499,
    "Trondheim lufthavn, Værnes": 7172108,
    "Trondheim torg": 4546048,
    "Hemseda": 3509663,
    "Tampere": 232073,
    "Stavanger": 4247796,
}


def print_benchmark_results(
    distance: float | int,
    previous_nodes: list[Node],
    origin_name: str,
    destination_name: str,
    exec_time: float,
):
    if isinstance(distance, int):
        time_string = "{}:{}:{}".format(*cs_to_hour_min_sec(distance))
    else:
        time_string = "Unreachable"
    print(
        f"""
{"origin":>15}| {origin_name:>30}
{"destination":>15}| {destination_name:>30}
{"path length":>15}| {len(previous_nodes):>30}
{"duration":>15}| {time_string:>30}
{"exec time":>15}| {str(exec_time) + 's':>30}
"""
    )


def benchmark_dijkstra(nodes: list[Node], origin_name: str, destination_name: str):
    origin = DESTINATIONS[origin_name]
    destination = DESTINATIONS[destination_name]

    start = timer()
    distances, previous = run_dijkstra(nodes, origin, destination, loading_bar=True)
    end = timer()

    current_node = previous[destination]
    assert current_node is not None

    previous_nodes_indexes = [current_node]
    while current_node is not None:
        previous_nodes_indexes.append(current_node)
        current_node = previous[current_node]
    previous_nodes = list(map(lambda n: nodes[n], previous_nodes_indexes))

    print_benchmark_results(
        distances[destination],
        previous_nodes,
        origin_name,
        destination_name,
        end - start,
    )


def benchmark_alt(
    nodes: list[Node],
    origin_name: str,
    destination_name: str,
    to_landmarks: list[list[float | int]],
    from_landmarks: list[list[float | int]],
):
    origin = DESTINATIONS[origin_name]
    destination = DESTINATIONS[destination_name]

    start = timer()
    distance, previous = run_alt(
        nodes, origin, to_landmarks, from_landmarks, destination, loading_bar=True
    )
    end = timer()

    current_node = previous[destination]
    assert current_node is not None

    previous_nodes_indexes = [current_node]
    while current_node is not None:
        previous_nodes_indexes.append(current_node)
        current_node = previous[current_node]
    previous_nodes = list(map(lambda n: nodes[n], previous_nodes_indexes))

    print_benchmark_results(
        distance,
        previous_nodes,
        origin_name,
        destination_name,
        end - start,
    )


def export_path(
    nodes: list[Node],
    origin_name: str,
    destination_name: str,
    to_landmarks: list[list[float | int]],
    from_landmarks: list[list[float | int]],
    export_file_path: str,
):
    origin = DESTINATIONS[origin_name]
    destination = DESTINATIONS[destination_name]

    start = timer()
    distance, previous = run_alt(
        nodes, origin, to_landmarks, from_landmarks, destination, loading_bar=True
    )
    end = timer()

    current_node = previous[destination]
    assert current_node is not None

    previous_nodes_indexes = [current_node]
    while current_node is not None:
        previous_nodes_indexes.append(current_node)
        current_node = previous[current_node]

    previous_nodes = list(map(lambda n: nodes[n], previous_nodes_indexes))
    tab = "\t"

    with open(export_file_path, "w") as f:
        for node in previous_nodes[::-1]:
            f.write(",".join(map(str, node.pos)) + "\n")
    print("Path saved!")


if __name__ == "__main__":
    nodes = read_complete(
        "noder.txt", "kanter.txt", "interessepkt.txt", loading_bar=True
    )
    benchmark_dijkstra(nodes, "Tampere", "Stavanger")
    benchmark_dijkstra(nodes, "Trondheim torg", "Trondheim lufthavn, Værnes")
    benchmark_dijkstra(nodes, "Tampere", "Stavanger")

    to_landmarks, from_landmarks = load_preprocess("preprocess.csv")
    benchmark_alt(
        nodes,
        "Trondheim torg",
        "Trondheim lufthavn, Værnes",
        to_landmarks,
        from_landmarks,
    )
    benchmark_alt(nodes, "Tampere", "Stavanger", to_landmarks, from_landmarks)

    export_path(
        nodes, "Oslo", "Trondheim", to_landmarks, from_landmarks, "oslo_trondheim.csv"
    )
