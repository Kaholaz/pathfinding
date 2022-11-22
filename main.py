from alt_preprocess import load_preprocess
from pathfinding import PathFinder
from utils import Node, cs_to_hour_min_sec
import utils
from file_handling import read_complete

from timeit import default_timer as timer


DESTINATIONS = {
    "Oslo": 3430400,
    "Stockholm": 5046415,
    "Trondheim": 7425499,
    "Trondheim lufthavn, Værnes": 7172108,
    "Trondheim torg": 4546048,
    "Hemsedal": 3509663,
    "Tampere": 232073,
    "Stavanger": 4247796,
    "Kårvåg": 3292784,
    "Gjemnes": 7352330,
    "Ålesund": 2518780,
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
{"origin":>15} {origin_name:>20}
{"destination":>15} {destination_name:>20}
{"nodes in path":>15} {number_of_nodes:>20}
{"nodes evaluated":>15} {number_of_nodes_evaluated:>20}
{"duration":>15} {time_string:>20}
{"exec time":>15} {str(exec_time) + 's':>20}
"""
    )


def benchmark_dijkstra(pathfinder: PathFinder, origin_name: str, destination_name: str):
    origin = DESTINATIONS[origin_name]
    destination = DESTINATIONS[destination_name]

    start = timer()
    distance, path = pathfinder.run_dijkstra(origin, destination)
    end = timer()

    print_benchmark_results(
        distance,
        len(path),
        pathfinder.considered_nodes,
        origin_name,
        destination_name,
        end - start,
    )


def benchmark_alt(
    pathfinder: PathFinder,
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


def write_coordinates(nodes: list[Node], file_path: str):
    with open(file_path, "w") as f:
        for node in nodes:
            f.write(",".join(map(str, node.pos)) + "\n")


def export_path(
    pathfinder: PathFinder,
    origin_name: str,
    destination_name: str,
    export_file_path: str,
):
    origin = DESTINATIONS[origin_name]
    destination = DESTINATIONS[destination_name]

    distance, path = pathfinder.run_alt(origin, destination)

    write_coordinates(path, export_file_path)
    print("Path saved!")


if __name__ == "__main__":
    loading_bar = True
    nodes = read_complete(
        "noder.txt", "kanter.txt", "interessepkt.txt", loading_bar=loading_bar
    )
    pathfinder = PathFinder(nodes, loading_bar)

    benchmark_dijkstra(pathfinder, "Tampere", "Ålesund")
    benchmark_dijkstra(pathfinder, "Kårvåg", "Gjemnes")

    to_landmarks, from_landmarks = load_preprocess("preprocess.csv", loading_bar)
    pathfinder.set_preprocess(to_landmarks, from_landmarks)
    benchmark_alt(pathfinder, "Tampere", "Ålesund")
    benchmark_alt(pathfinder, "Kårvåg", "Gjemnes")

    export_path(pathfinder, "Oslo", "Trondheim", "oslo_trondheim.csv")

    charging_stations = pathfinder.closest_n_nodes(
        DESTINATIONS["Trondheim lufthavn, Værnes"], 8, utils.is_charging_station
    )
    write_coordinates(
        map(lambda n: pathfinder.nodes[n[0]], charging_stations),
        "charging_stations.csv",
    )

    drinking_places = pathfinder.closest_n_nodes(
        DESTINATIONS["Trondheim torg"], 8, utils.is_drinking_place
    )
    write_coordinates(
        map(lambda n: pathfinder.nodes[n[0]], drinking_places), "drinking_places.csv"
    )

    eating_places = pathfinder.closest_n_nodes(
        DESTINATIONS["Hemsedal"], 8, utils.is_eating_place
    )
    write_coordinates(
        map(lambda n: pathfinder.nodes[n[0]], charging_stations), "eating_places.csv"
    )
