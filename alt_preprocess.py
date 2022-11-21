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
    with open(preprocess_file_name, "wb") as f:
        pickle.dump((nodes, to_landmarks, from_landmarks), f, pickle.HIGHEST_PROTOCOL)
    return nodes, to_landmarks, from_landmarks


def load_preprocess(
    preprocess_file_name: str,
) -> tuple[list[Node], list[list[int]], list[list[int]]]:
    with open(preprocess_file_name, "rb") as f:
        return pickle.load(f)


def preprocess_and_save(
    node_file: str,
    edges_file: str,
    place_file: str,
    preprocess_file: str,
    landmarks: dict[int, str],
    loading_bar: bool,
) -> tuple[list[Node], list[list[int]], list[list[int]]]:
    nodes, to_landmarks, from_landmarks = preprocess(
        node_file, edges_file, place_file, landmarks, loading_bar
    )
    return save_preprocess(nodes, to_landmarks, from_landmarks, preprocess_file)


if __name__ == "__main__":
    pre_result = preprocess_and_save(
        "noder.txt",
        "kanter.txt",
        "interessepkt.txt",
        "preprocess.pickle",
        landmarks=SCANDINAVIA_LANDMARKS,
        loading_bar=True,
    )
    print("Unpickeling")
    load_preprocess("island_preprocess.pickle")
