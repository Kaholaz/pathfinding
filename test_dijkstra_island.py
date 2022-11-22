from pathfinding import PathFinder
from file_handling import read_complete
from utils import hour_min_sec_to_sec as seconds


def general_test(
    pathfinder: PathFinder, origin, destination, target_path_length, target_seconds
):
    distance, path = pathfinder.run_dijkstra(origin, destination)
    path_length = len(path)

    assert distance // 100 == target_seconds, f"{distance//100=}, {target_seconds}"
    assert path_length == target_path_length, f"{path_length=}, {target_path_length=}"


def test_zero_ten_thousand():
    general_test(pathfinder, 0, 10000, 128, seconds(1, 53, 9))


def test_ten_thousand_zero():
    general_test(pathfinder, 10000, 0, 128, seconds(1, 53, 9))


def test_500_100000():
    general_test(pathfinder, 500, 100000, 64, seconds(0, 5, 32))


def test_100000_50():
    general_test(pathfinder, 100000, 500, 70, seconds(0, 5, 41))


if __name__ == "__main__":
    loading_bar = False

    nodes = read_complete(
        "island_noder.txt",
        "island_kanter.txt",
        "island_interessepkt.txt",
        loading_bar=loading_bar
    )
    pathfinder = PathFinder(nodes, loading_bar)
    test_500_100000()
    _vars = vars().copy()
    for name, value in _vars.items():
        if name.startswith("test_"):
            print(name)
            try:
                value()
            except AssertionError as e:
                print("Exception!")
                print(str(e))
