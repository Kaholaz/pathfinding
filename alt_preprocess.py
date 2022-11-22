from typing import cast
from utils import Node
from pathfinding import run_dijkstra
from file_handling import read_complete
import pickle

ICELAND_LANDMARKS = {
    5129: "Keflavik",
    20567: "Tálknafjörður",
    17617: "Neskaupstaður",
}
SCANDINAVIA_LANDMARKS = {
    984009: "Hanko",
    3007953: "Nordkapp",
    2518780: "Ålesund",
    2383502: "Lindesnes",
    1246746: "Furusund",
    3551857: "Skagen",
}


def calculate_distances_from_landmark(
    nodes: list[Node], landmark: int, landmark_name: str, loading_bar: bool = False
) -> list[float | int]:
    distances, prev = run_dijkstra(
        nodes,
        landmark,
        loading_bar=loading_bar,
        loading_desc=f"Calculating distances from {landmark_name}...",
    )
    return distances


def distances_from_landmarks(
    nodes: list[Node], landmarks: dict[int, str], loading_bar: bool = False
) -> list[list[float | int]]:
    return [
        calculate_distances_from_landmark(
            nodes, landmark, landmark_name, loading_bar=loading_bar
        )
        for landmark, landmark_name in landmarks.items()
    ]


def preprocess(
    node_file: str,
    edges_file: str,
    place_file: str,
    landmarks: dict[int, str],
    loading_bar: bool = False,
) -> tuple[list[Node], list[list[float | int]], list[list[float | int]]]:
    reverse_nodes = read_complete(
        node_file, edges_file, place_file, reverse=True, loading_bar=loading_bar
    )

    print("---Reversed nodes---")
    to_landmarks = distances_from_landmarks(reverse_nodes, landmarks, loading_bar)
    del reverse_nodes

    print("---Forwards nodes---")
    nodes = read_complete(node_file, edges_file, place_file, loading_bar=loading_bar)
    from_landmarks = distances_from_landmarks(nodes, landmarks, loading_bar)

    return nodes, to_landmarks, from_landmarks


def save_preprocess(
    nodes: list[Node],
    to_landmarks: list[list[float | int]],
    from_landmarks: list[list[float | int]],
    preprocess_file_name: str,
):
    number_of_landmarks = len(to_landmarks)
    number_of_nodes = len(to_landmarks[0])
    tab = "\t"
    with open(preprocess_file_name, "w") as f:
        f.write(f"{number_of_landmarks}\t{number_of_nodes}\n")
        for i in range(number_of_nodes):
            line = f"\
{tab.join(map(lambda l: str(l[i]), to_landmarks))}\t\
{tab.join(map(lambda l: str(l[i]), from_landmarks))}\n"
            f.write(line)
    return nodes, to_landmarks, from_landmarks


def load_preprocess(
    preprocess_file_name: str,
    loading_bar: bool = False,
) -> tuple[list[list[float | int]], list[list[float | int]]]:
    if loading_bar:
        from tqdm import tqdm  # type: ignore

        with open(preprocess_file_name, "r") as f:
            fields = f.readline().split()
            number_of_landmarks = int(fields[0])
            number_of_nodes = int(fields[1])

            to_landmarks: list[list[int | float]] = cast(
                list[list[int | float]], [list()[:] for _ in range(number_of_landmarks)]
            )
            from_landmarks: list[list[int | float]] = cast(
                list[list[int | float]], [list()[:] for _ in range(number_of_landmarks)]
            )
            with tqdm(total=number_of_nodes, desc="Reading preprocess...") as bar:
                while line := f.readline():
                    fields = line.split()
                    for i, value in enumerate(
                        map(
                            lambda field: float("inf")
                            if field == "inf"
                            else int(field),
                            fields[:number_of_landmarks],
                        )
                    ):
                        to_landmarks[i].append(value)
                    for i, value in enumerate(
                        map(
                            lambda field: float("inf")
                            if field == "inf"
                            else int(field),
                            fields[number_of_landmarks:],
                        )
                    ):
                        from_landmarks[i].append(value)
                    bar.update(1)
    else:
        print("Reading preprocess...")
        to_landmarks, from_landmarks = list(), list()
        with open(preprocess_file_name, "r") as f:
            fields = f.readline().split()
            number_of_landmarks = int(fields[0])
            number_of_nodes = int(fields[1])
            while line := f.readline():
                fields = line.split()
                for i, value in enumerate(
                    map(
                        lambda field: float("inf") if field == "inf" else int(field),
                        fields[:number_of_landmarks],
                    )
                ):
                    to_landmarks[i].append(value)
                for i, value in enumerate(
                    map(
                        lambda field: float("inf") if field == "inf" else int(field),
                        fields[number_of_landmarks:],
                    )
                ):
                    from_landmarks[i].append(value)

    return to_landmarks, from_landmarks


def preprocess_and_save(
    node_file: str,
    edges_file: str,
    place_file: str,
    preprocess_file: str,
    landmarks: dict[int, str],
    loading_bar: bool,
) -> tuple[list[Node], list[list[float | int]], list[list[float | int]]]:
    nodes, to_landmarks, from_landmarks = preprocess(
        node_file, edges_file, place_file, landmarks, loading_bar
    )
    return save_preprocess(nodes, to_landmarks, from_landmarks, preprocess_file)


if __name__ == "__main__":
    pre_result = preprocess_and_save(
        "noder.txt",
        "kanter.txt",
        "interessepkt.txt",
        "preprocess.csv",
        landmarks=SCANDINAVIA_LANDMARKS,
        loading_bar=True,
    )
    print("Reading file...")
    load_preprocess("preprocess.csv", loading_bar=True)
