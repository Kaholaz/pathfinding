from alt_preprocess import load_preprocess
from pathfinding import PathFinder
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
    number_of_nodes: int,
    number_of_nodes_evaluated: int,
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
{"nodes in path":>15}| {number_of_nodes:>30}
{"nodes evaluated":>15}| {number_of_nodes_evaluated:>30}
{"duration":>15}| {time_string:>30}
{"exec time":>15}| {str(exec_time) + 's':>30}
"""
    )


def benchmark_dijkstra(pathfinder: PathFinder, origin_name: str, destination_name: str):
    origin = DESTINATIONS[origin_name]
    destination = DESTINATIONS[destination_name]

    start = timer()
    distances, path = pathfinder.run_dijkstra(origin, destination)
    end = timer()

    print_benchmark_results(
        distances[destination],
        len(path),
        pathfinder.considered_nodes,
        origin_name,
        destination_name,
        end - start,
    )


def benchmark_alt(
    nodes: list[Node],
    origin_name: str,
    destination_name: str,
):
    origin = DESTINATIONS[origin_name]
    destination = DESTINATIONS[destination_name]

    start = timer()
    distance, path = pathfinder.run_alt(origin, destination)
    end = timer()

    print_benchmark_results(
        distance,
        len(path),
        pathfinder.considered_nodes,
        origin_name,
        destination_name,
        end - start,
    )


def export_path(
    pathfinder: PathFinder,
    origin_name: str,
    destination_name: str,
    export_file_path: str,
):
    origin = DESTINATIONS[origin_name]
    destination = DESTINATIONS[destination_name]

    distance, path = pathfinder.run_alt(nodes, origin, destination, loading_bar=True)

    with open(export_file_path, "w") as f:
        for node in path:
            f.write(",".join(map(str, node.pos)) + "\n")
    print("Path saved!")


if __name__ == "__main__":
    nodes = read_complete(
        "noder.txt", "kanter.txt", "interessepkt.txt", loading_bar=True
    )
    pathfinder = PathFinder(nodes, True)
    benchmark_dijkstra(pathfinder, "Tampere", "Stavanger")
    benchmark_dijkstra(pathfinder, "Trondheim torg", "Trondheim lufthavn, Værnes")
    benchmark_dijkstra(pathfinder, "Tampere", "Stavanger")

    to_landmarks, from_landmarks = load_preprocess("preprocess.csv")
    pathfinder.set_preprocess(to_landmarks, from_landmarks)
    benchmark_alt(pathfinder, "Trondheim torg", "Trondheim lufthavn, Værnes")
    benchmark_alt(pathfinder, "Tampere", "Stavanger")

    export_path(pathfinder, "Oslo", "Trondheim", "oslo_trondheim.csv")
