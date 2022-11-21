from typing import Optional
from pathfinding import run_alt
from file_handling import read_complete
from alt_preprocess import (
    ICELAND_LANDMARKS,
    load_preprocess,
    preprocess_and_save,
    SCANDINAVIA_LANDMARKS,
)
from utils import hour_min_sec_to_sec as seconds


def general_test(
    nodes, origin: int, destination: int, target_path_length: int, target_seconds: int
):
    global from_landmarks, to_landmarks
    distance, prev = run_alt(
        nodes, origin, to_landmarks, from_landmarks, destination, loading_bar=True
    )

    path_length, current = 2, destination
    while (current := prev[current] or origin) != origin:
        path_length += 1
    assert distance // 100 == target_seconds, f"{distance//100=}, {target_seconds}"
    assert path_length == target_path_length, f"{path_length=}, {target_path_length=}"


def test_zero_ten_thousand():
    general_test(nodes, 0, 10000, 128, seconds(1, 53, 9))


def test_ten_thousand_zero():
    general_test(nodes, 10000, 0, 128, seconds(1, 53, 9))


def test_500_100000():
    general_test(nodes, 500, 100000, 64, seconds(0, 5, 32))


def test_100000_50():
    general_test(nodes, 100000, 500, 70, seconds(0, 5, 41))


if __name__ == "__main__":
    global to_landmarks, from_landmarks

    # nodes, to_landmarks, from_landmarks = preprocess_and_save(
    #     "island_noder.txt",
    #     "island_kanter.txt",
    #     "island_interessepkt.txt",
    #     "island_preprocess.pickle",
    #     landmarks=ICELAND_LANDMARKS,
    #     loading_bar=True,
    # )
    nodes, to_landmarks, from_landmarks = load_preprocess("island_preprocess.pickle")
    _vars = vars().copy()
    for name, value in _vars.items():
        if name.startswith("test_"):
            print(name)
            try:
                value()
            except AssertionError as e:
                print("Exception!")
                print(str(e))
