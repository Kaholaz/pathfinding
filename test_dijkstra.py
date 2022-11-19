from pathfinding import run_dijkstra
from file_handling import read_complete
from utils import hour_min_sec_to_sec as seconds


def general_test(nodes, origin, destination, target_path_length, target_seconds):
    distances, prev = run_dijkstra(nodes, origin, destination, True)

    path_length, current = 2, destination
    while (current := prev[current]) != origin: path_length += 1
    assert distances[destination] // 100 == target_seconds, f"{distances[destination]//100=}, {target_seconds}"
    assert path_length == target_path_length, f"{path_length=}, {target_path_length=}"

def test_karvag_gjemmnes():
    general_test(nodes, 3292784, 7352330, 329, seconds(0,40,46))

def test_gjemmnes_karvag():
    general_test(nodes, 7352330, 3292784, 329, seconds(0,40,46))

def test_trondheim_oslo():
    general_test(nodes, 7425499, 3430400, 1963, seconds(5,53, 26))

def test_oslo_trondheim():
    general_test(nodes, 3430400, 7425499, 2013, seconds(5,53,19))

def test_jyva_karasjohk():
    general_test(nodes, 6748209, 2709967, 3283, seconds(11,4, 52))

def test_karasjohk_jyva():
    general_test(nodes, 2709967, 6748209, 3336, seconds(11,6, 7))

def test_stavanger_tampere():
    general_test(nodes, 4247796, 232073, 5316, seconds(19,51, 8))

def test_tampere_stavanger():
    general_test(nodes, 232073, 4247796, 5258, seconds(19, 50,33))

if __name__=="__main__":
    nodes = read_complete("noder.txt", "kanter.txt", True)
    _vars = vars().copy()
    for name, value in _vars.items():
        if name.startswith("test_"):
            print(name)
            try:
                value()
            except AssertionError as e:
                print("Exception!")
                print(str(e))