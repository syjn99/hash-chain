from collections.abc import Callable
from collections import defaultdict
from typing import List, Dict


from common import make_hash_function


def run_analysis(k: int):
    print(f"Run analysis for k={k}")

    hash_function = make_hash_function(k)

    # Initialize data structures for tracking this algorithm
    visited: Dict[bytes, int] = defaultdict()  # value = depth
    edges_to_cycle: Dict[bytes, int] = (
        defaultdict()
    )  # After finding the cycle, update this dictionary for later search

    # Initialize data structures for printing the final analysis
    components_cnt = 0
    tail_length_list = []
    cycle_length_list = []

    for terminal_point in find_terminal_points(k, hash_function):
        path = []
        cur = terminal_point
        while cur not in visited:
            visited[cur] = len(path)
            path.append(cur)
            cur = hash_function(cur)

        # Cycle detected.
        if cur in path:
            # New component found. Increment the count
            components_cnt += 1

            # Tail length for this terminal point is the depth of the initial vertex of the cycle.
            tail_length = visited[cur]
            tail_length_list.append(tail_length)

            # Cycle length is trivial if tail length is given
            cycle_length = len(path) - tail_length
            cycle_length_list.append(cycle_length)

            # Update `edges_to_cycle`
            cur_idx = path.index(cur)
            for i in range(len(path)):
                # From `cur_idx`, this vertex is the member of this cycle.
                if i >= cur_idx:
                    edges_to_cycle[path[i]] = 0
                # The tail part
                else:
                    edges_to_cycle[path[i]] = tail_length - visited[path[i]]
        # This terminal_point is a part of the already found component.
        else:
            tail_length = len(path) + edges_to_cycle[cur]
            tail_length_list.append(tail_length)

            # Update `edges_to_cycle`
            for i in range(len(path)):
                edges_to_cycle[path[i]] = tail_length - i

    print("==== Result of analysis ====")
    print(f"Number of components: {components_cnt}")
    print(f"Average of tail length: {sum(tail_length_list) / len(tail_length_list)}")
    print(f"Max of tail length: {max(tail_length_list)}")
    print(f"Min of cycle length: {min(cycle_length_list)}")
    print(f"Average of cycle length: {sum(cycle_length_list) / len(cycle_length_list)}")
    print(f"Max of cycle length: {max(cycle_length_list)}")


def find_terminal_points(k: int, hash_function: Callable[[bytes], bytes]) -> List[bytes]:
    byte = k // 8
    inbound_dict: Dict[bytes, int] = defaultdict()  # Store the inbound edges for each bytes.

    for i in range(pow(2, k)):
        # Initialize dictionary if unset
        i_bytes = i.to_bytes(byte, byteorder="big")
        inbound_dict[i_bytes] = inbound_dict.get(i_bytes, 0)

        # Apply hash_function
        res = hash_function(i_bytes)
        inbound_dict[res] = inbound_dict.get(res, 0) + 1

    terminal_points = []

    for b, ref_cnt in inbound_dict.items():
        if ref_cnt > 0:
            continue
        terminal_points.append(b)

    return terminal_points
