from utils import Node
import gc


def read_nodes(file_name: str, loading_bar: bool = False) -> list[Node]:
    if loading_bar:
        from tqdm import tqdm  # type: ignore
    nodes: list[Node] = list()

    gc.disable()
    with open(file_name, "r") as f:
        number_of_nodes = int(f.readline().strip())
        i = 0
        if loading_bar:
            with tqdm(total=number_of_nodes, desc="Reading nodes...") as bar:
                while line := f.readline():
                    fields = line.split()
                    nodes.append(Node(i, list(), (float(fields[1]), float(fields[2]))))
                    i += 1
                    bar.update(1)
        else:
            print("Reading nodes...")
            while line := f.readline():
                fields = line.split()
                nodes.append(Node(i, list(), (float(fields[1]), float(fields[2]))))
                i += 1
    gc.enable()

    assert number_of_nodes == len(nodes)
    return nodes


def read_edges(
    file_name: str, nodes: list[Node], reverse: bool = False, loading_bar: bool = False
) -> list[Node]:
    if loading_bar:
        from tqdm import tqdm

    gc.disable()
    with open(file_name, "r") as f:
        entries = int(f.readline().strip())
        if loading_bar:
            with tqdm(total=entries, desc="Reading edges...") as bar:
                while line := f.readline():
                    fields = line.split()
                    values = tuple(map(int, fields[:3]))
                    if reverse:
                        nodes[values[1]].edges.append((values[0], values[2]))
                    else:
                        nodes[values[0]].edges.append((values[1], values[2]))
                    bar.update(1)

        else:
            print("Reading edges...")
            while line := f.readline():
                fields = line.split()
                values = tuple(map(int, fields[:3]))
                if reverse:
                    nodes[values[1]].edges.append((values[0], values[2]))
                else:
                    nodes[values[0]].edges.append((values[1], values[2]))
    gc.enable()

    return nodes


def read_place(
    file_name: str, nodes: list[Node], loading_bar: bool = False
) -> list[Node]:
    if loading_bar:
        from tqdm import tqdm

    gc.disable()
    with open(file_name, "r") as f:
        entries = int(f.readline().strip())
        if loading_bar:
            with tqdm(total=entries, desc="Reading place types...") as bar:
                while line := f.readline():
                    fields = line.split()
                    int_fields = tuple(map(int, fields[:2]))
                    name = fields[-1][1:-1]
                    nodes[int_fields[0]].type = int_fields[1]
                    nodes[int_fields[0]].name = name
                    bar.update(1)
        else:
            print("Reading place types...")
            while line := f.readline():
                fields = line.split()
                int_fields = tuple(map(int, fields[:2]))
                name = fields[-1][1:-1]
                nodes[int_fields[0]].type = int_fields[1]
                nodes[int_fields[0]].name = name
    gc.enable()

    return nodes


def read_complete(
    node_file: str,
    edges_file: str,
    place_file: str,
    reverse: bool = False,
    loading_bar: bool = False,
) -> list[Node]:
    nodes = read_nodes(node_file, loading_bar=loading_bar)
    nodes = read_edges(edges_file, nodes, reverse=reverse, loading_bar=loading_bar)
    return read_place(place_file, nodes, loading_bar=loading_bar)
