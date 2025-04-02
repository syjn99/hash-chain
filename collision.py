import time
import os

from common import (
    make_hash_function,
    save_starting_point,
    load_starting_point,
    delete_checkpoint,
    PICKLES,
)
from th import meeting_vertex, initial_vertex

RESULTS_FILE = "collisions-results.txt"


def find_collision(k: int, iv: str):
    print(f"Find collision for k={k} with iv={iv}")

    STARTING_POINT_PKL = f"{PICKLES}/collision-{k}-starting-point.pkl"
    STEP1_PKL = f"{PICKLES}/collision-{k}-step1.pkl"
    STEP1_COMPLETE_PKL = f"{PICKLES}/collision-{k}-step1-complete.pkl"
    STEP2_PKL = f"{PICKLES}/collision-{k}-step2.pkl"

    start_time = time.time()

    hash_function = make_hash_function(k)

    # We will use same Tortoise-Hare Algorithm like
    # finding a cycle.
    # This algorithm will eventually find out the cycle,
    # but in this collision case, we want to make sure that
    # the initial vertex is NOT the part of the cycle:
    # If there is no tail, it is impossible to find the two preimages.
    # Then, how can we decide whether it is IN the cycle?
    # We have to check whether the tortoise and hare
    # jumps or not at the `initial_vertex`.
    # That is, if the input value for function `initial_vertex`
    # is same, then we have to find a fresh new value.

    starting_point = bytes.fromhex(iv)
    try:
        starting_point = load_starting_point(STARTING_POINT_PKL)
        print(f"Starting point is loaded: {starting_point.hex()}")
    except FileNotFoundError:
        pass

    while True:
        start = hash_function(starting_point)
        t = hash_function(start)
        h = hash_function(hash_function(start))
        (t, h) = meeting_vertex(t, h, hash_function, STEP1_PKL, STEP1_COMPLETE_PKL)

        t = start
        if t == h:
            print(f"Tail length is 0, try another iv")
            starting_point = get_random_iv(k)
            save_starting_point(starting_point)
            delete_checkpoint(STEP1_PKL)
            delete_checkpoint(STEP1_COMPLETE_PKL)
            continue

        (t, h, tail_preimage, cycle_preimage) = initial_vertex(t, h, hash_function, STEP2_PKL, "")
        if t != h:
            raise Exception

        if hash_function(tail_preimage) != hash_function(cycle_preimage):
            raise Exception

        print(f"Collided hash: {t.hex()}")
        print(f"Preimage in the tail: {tail_preimage.hex()}")
        print(f"Preimage in the cycle: {cycle_preimage.hex()}")
        print(f"Total seconds: {time.time() - start_time}")
        delete_checkpoint(STEP1_COMPLETE_PKL)

        with open(RESULTS_FILE, "a") as f:
            f.write(
                f"k={k}, Collided hash={t.hex()}, Preimage(tail)={tail_preimage.hex()}, Preimage(cycle)={cycle_preimage.hex()}, time={time.time() - start_time:.2f}s\n"
            )
        break


def get_random_iv(k: int) -> bytes:
    byte_len = k // 8
    return os.urandom(byte_len)
