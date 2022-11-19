from dataclasses import dataclass

@dataclass
class Node:
    number: int
    edges: list[tuple[int, int]] # node, cost
    pos: tuple[float, float]

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