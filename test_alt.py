from pathfinding import PathFinder
from file_handling import read_complete
from alt_preprocess import (
    ICELAND_LANDMARKS,
    load_preprocess,
    preprocess_and_save,
    SCANDINAVIA_LANDMARKS,
)
import os
from utils import hour_min_sec_to_sec as seconds


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


def test_karvag_gjemmnes():
    general_test(pathfinder, 3292784, 7352330, 329, seconds(0, 40, 46))


def test_gjemmnes_karvag():
    general_test(pathfinder, 7352330, 3292784, 329, seconds(0, 40, 46))


def test_trondheim_oslo():
    general_test(pathfinder, 7425499, 3430400, 1963, seconds(5, 53, 26))


def test_oslo_trondheim():
    general_test(pathfinder, 3430400, 7425499, 2013, seconds(5, 53, 19))


def test_jyva_karasjohk():
    general_test(pathfinder, 6748209, 2709967, 3283, seconds(11, 4, 52))


def test_karasjohk_jyva():
    general_test(pathfinder, 2709967, 6748209, 3336, seconds(11, 6, 7))


def test_stavanger_tampere():
    general_test(pathfinder, 4247796, 232073, 5316, seconds(19, 51, 8))


def test_tampere_stavanger():
    general_test(pathfinder, 232073, 4247796, 5258, seconds(19, 50, 33))


if __name__ == "__main__":
    global to_landmarks, from_landmarks
    node_file, edges_file, place_file, preprocess_file = (
        "noder.txt",
        "kanter.txt",
        "interessepkt.txt",
        "preprocess.csv",
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
