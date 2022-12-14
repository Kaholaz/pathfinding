from typing import TypeVar, cast
from utils import LoadingBarMocker, Node
from pathfinding import PathFinder
from file_handling import read_complete
import sys

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
    pathfinder: PathFinder, landmark: int, landmark_name: str
) -> list[float | int]:
    pathfinder.run_dijkstra(
        landmark, loading_desc=f"Calculating distances from {landmark_name}..."
    )
    return pathfinder.best_distances


def distances_from_landmarks(
    pathfinder: PathFinder, landmarks: dict[int, str]
) -> list[list[float | int]]:
    return [
        calculate_distances_from_landmark(pathfinder, landmark, landmark_name)
        for landmark, landmark_name in landmarks.items()
    ]


def preprocess(
    node_file: str,
    edges_file: str,
    place_file: str,
    landmarks: dict[int, str],
    loading_bar: bool = False,
) -> PathFinder:
    reverse_nodes = read_complete(
        node_file, edges_file, place_file, reverse=True, loading_bar=loading_bar
    )
    pathfinder = PathFinder(reverse_nodes, loading_bar)

    print("---Reversed nodes---")
    to_landmarks = distances_from_landmarks(pathfinder, landmarks)
    del reverse_nodes, pathfinder

    print("---Forwards nodes---")
    nodes = read_complete(node_file, edges_file, place_file, loading_bar=loading_bar)
    pathfinder = PathFinder(nodes, loading_bar)
    from_landmarks = distances_from_landmarks(pathfinder, landmarks)

    pathfinder.set_preprocess(to_landmarks, from_landmarks)
    return pathfinder


def save_preprocess(
    pathfinder: PathFinder,
    preprocess_file_name: str,
) -> PathFinder:
    number_of_landmarks = len(pathfinder.to_landmarks)
    number_of_nodes = len(pathfinder.to_landmarks[0])
    tab = "\t"
    with open(preprocess_file_name, "w") as f:
        f.write(f"{number_of_landmarks}\t{number_of_nodes}\n")
        for i in range(number_of_nodes):
            line = f"\
{tab.join(map(lambda l: str(l[i]), pathfinder.to_landmarks))}\t\
{tab.join(map(lambda l: str(l[i]), pathfinder.from_landmarks))}\n"
            f.write(line)
    return pathfinder


def load_preprocess(
    preprocess_file_name: str,
    loading_bar: bool = False,
) -> tuple[list[list[float | int]], list[list[float | int]]]:
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

        if loading_bar:
            from tqdm import tqdm  # type: ignore

            bar = tqdm(total=number_of_nodes, desc="Reading preprocess...")
        else:
            print("Reading preprocess...")
            bar = LoadingBarMocker()

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
            bar.update(1)

    bar.close()

    return to_landmarks, from_landmarks


def preprocess_and_save(
    node_file: str,
    edges_file: str,
    place_file: str,
    preprocess_file: str,
    landmarks: dict[int, str],
    loading_bar: bool,
) -> PathFinder:
    pathfinder = preprocess(node_file, edges_file, place_file, landmarks, loading_bar)
    return save_preprocess(pathfinder, preprocess_file)


if __name__ == "__main__":

    files = {
        "island": (
            "island_noder.txt",
            "island_kanter.txt",
            "island_interessepkt.txt",
            "island_preprocess.csv",
        ),
        "skandinavia": (
            "noder.txt",
            "kanter.txt",
            "interessepkt.txt",
            "preprocess.csv",
        ),
    }
    landmarks = {"island": ICELAND_LANDMARKS, "skandinavia": SCANDINAVIA_LANDMARKS}
    loading_bar = False

    try:
        chosen_files = files[sys.argv[1]]
        chosen_landmarks = landmarks[sys.argv[1]]
    except Exception:
        print("You must specify the map you want to process.")
        print(f"Choices: ({','.join(files.keys())})")
        sys.exit(1)

    pathfinder = preprocess_and_save(
        *chosen_files,
        landmarks=chosen_landmarks,
        loading_bar=loading_bar,
    )

    print("Reading file...")
    load_result = load_preprocess("island_preprocess.csv", loading_bar)
    assert pathfinder.to_landmarks, pathfinder.from_landmarks == load_result
