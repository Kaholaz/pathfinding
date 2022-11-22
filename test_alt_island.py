from pathfinding import PathFinder
from file_handling import read_complete
from alt_preprocess import (
    ICELAND_LANDMARKS,
    load_preprocess,
    preprocess_and_save,
    SCANDINAVIA_LANDMARKS,
)
from utils import hour_min_sec_to_sec as seconds
import os


def general_test(
    pathfinder: PathFinder,
    origin: int,
    destination: int,
    target_path_length: int,
    target_seconds: int,
):
    distance, path = pathfinder.run_alt(origin, destination)

    path_length = len(path)
    assert distance // 100 == target_seconds, f"{distance//100=}, {target_seconds}"
    assert path_length == target_path_length, f"{path_length=}, {target_path_length=}"


def test_zero_ten_thousand():
    general_test(pathfinder, 0, 10000, 128, seconds(1, 53, 9))


def test_ten_thousand_zero():
    general_test(pathfinder, 10000, 0, 128, seconds(1, 53, 9))


def test_500_100000():
    general_test(pathfinder, 500, 100000, 64, seconds(0, 5, 32))


def test_100000_500():
    general_test(pathfinder, 100000, 500, 70, seconds(0, 5, 41))


if __name__ == "__main__":
    global to_landmarks
    global from_landmarks

    node_file, edges_file, place_file, preprocess_file = (
        "island_noder.txt",
        "island_kanter.txt",
        "island_interessepkt.txt",
        "island_preprocess.csv",
    )
    loading_bar = True

    if not os.path.exists(preprocess_file):
        pathfinder = preprocess_and_save(
            node_file,
            edges_file,
            place_file,
            preprocess_file,
            landmarks=SCANDINAVIA_LANDMARKS,
            loading_bar=loading_bar,
        )
    else:
        nodes = read_complete(
            node_file, edges_file, place_file, loading_bar=loading_bar
        )
        pathfinder = PathFinder(nodes, loading_bar)
        to_landmarks, from_landmarks = load_preprocess(
            preprocess_file, loading_bar=loading_bar
        )
        pathfinder.set_preprocess(to_landmarks, from_landmarks)

    _vars = vars().copy()
    for name, value in _vars.items():
        if name.startswith("test_"):
            print(name)
            try:
                value()
            except AssertionError as e:
                print("Exception!")
                print(str(e))
