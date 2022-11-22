from dataclasses import dataclass


@dataclass
class Node:
    number: int
    edges: list[tuple[int, int]]  # node, cost
    pos: tuple[float, float]
    type: int = 0


def is_placename(node: Node) -> bool:
    return bool(node.type & 1)


def is_gas_station(node: Node) -> bool:
    return bool(node.type & 2)


def is_charging_station(node: Node) -> bool:
    return bool(node.type & 4)


def is_eating_place(node: Node) -> bool:
    return bool(node.type & 8)


def is_drinking_place(node: Node) -> bool:
    return bool(node.type & 16)


def is_sleeping_place(node: Node) -> bool:
    return bool(node.type & 32)


def write_path_to_file(previous_nodes: list[Node], filename: str):
    with open(filename, "w") as f:
        for node in previous_nodes[::-1]:
            f.write(f"{node.pos[0]},{node.pos[1]}\n")


def hour_min_sec_to_cs(hours: int, minutes: int, seconds: int):
    return hour_min_sec_to_sec(hours, minutes, seconds) * 100


def hour_min_sec_to_sec(hours: int, minutes: int, seconds: int):
    minutes += hours * 60
    seconds += minutes * 60
    return seconds


def cs_to_hour_min_sec(cs: int):
    seconds = cs // 100

    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return hours, minutes, seconds
