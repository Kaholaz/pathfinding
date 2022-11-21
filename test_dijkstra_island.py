from pathfinding import run_dijkstra
from file_handling import read_complete
from utils import hour_min_sec_to_sec as seconds


def general_test(nodes, origin, destination, target_path_length, target_seconds):
    distances, prev = run_dijkstra(nodes, origin, destination, True)

    path_length, current = 2, destination
    while (current := prev[current]) != origin:
        path_length += 1
    assert (
        distances[destination] // 100 == target_seconds
    ), f"{distances[destination]//100=}, {target_seconds}"
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
    nodes = read_complete(
        "island_noder.txt",
        "island_kanter.txt",
        "island_interessepkt.txt",
        loading_bar=True,
    )
    _vars = vars().copy()
    for name, value in _vars.items():
        if name.startswith("test_"):
            print(name)
            try:
                value()
            except AssertionError as e:
                print("Exception!")
                print(str(e))
