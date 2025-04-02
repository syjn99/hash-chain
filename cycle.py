import time
from collections.abc import Callable
from typing import Tuple

from common import make_hash_function, save_checkpoint, load_checkpoint, delete_checkpoint, PICKLES

# For every `CHECKPOINT` iteration, save to pickle file.
CHECKPOINT = 10_000_000


STEP1_PKL = f"{PICKLES}/cycle-step1.pkl"
STEP1_COMPLETE_PKL = f"{PICKLES}/cycle-step1-complete.pkl"
STEP2_PKL = f"{PICKLES}/cycle-step2.pkl"
STEP2_COMPLETE_PKL = f"{PICKLES}/cycle-step2-complete.pkl"
STEP3_PKL = f"{PICKLES}/cycle-step3.pkl"


def find_cycle(k: int, iv: str):
    print(f"Find cycle for k={k} with iv={iv}")

    start_time = time.time()

    hash_function = make_hash_function(k)

    # Here, we will going to use Tortoise-Hare Algorithm
    # to find the initial value and the cycle length.
    # `t` for Tortoise, `h` for Hare.
    # `t` jumps one edge per step while `f` jumps two edges per step.

    start = hash_function(bytes.fromhex(iv))
    t = hash_function(start)
    h = hash_function(hash_function(start))
    (t, h) = meeting_vertex(t, h, hash_function)

    # Tortoise and Hare met at some point.
    # Let the tortoise to go back to the starting point.
    # And they will move one edge per step.
    # The vertex they met is the initial edge that this cycle begins.
    t = start
    (t, h) = initial_vertex(t, h, hash_function)

    # Fix the tortoise at that point, and move the hare to calculate the cycle length.
    h = hash_function(t)
    (t, h, cycle_length) = calculate_cycle_length(t, h, hash_function)

    delete_checkpoint(STEP1_COMPLETE_PKL)
    delete_checkpoint(STEP2_COMPLETE_PKL)

    print(f"Initial Value: {t.hex()}, and the cycle length: {cycle_length}")
    print(f"Total seconds: {time.time() - start_time}")


def meeting_vertex(
    t: bytes, h: bytes, hash_function: Callable[[bytes], bytes]
) -> Tuple[bytes, bytes]:
    print("STEP 1: find meeting vertex")

    try:
        t, h, _ = load_checkpoint(STEP1_COMPLETE_PKL)
        print(f"Step 1 Already Finished, t = {t.hex()}, h = {h.hex()}")
        return (t, h)
    except FileNotFoundError:
        pass

    count = 0

    try:
        t, h, count = load_checkpoint(STEP1_PKL)
        print(f"Resumed from checkpoint: count = {count}")
    except FileNotFoundError:
        pass

    while t != h:
        count += 1
        if count % CHECKPOINT == 0:
            print(f"current count: {count}, t = {t.hex()}, h = {h.hex()}")
            save_checkpoint(STEP1_PKL, t, h, count)

        t = hash_function(t)
        h = hash_function(hash_function(h))

    print(f"STEP 1: finished. t = {t.hex()}, h = {h.hex()}")

    delete_checkpoint(STEP1_PKL)
    save_checkpoint(STEP1_COMPLETE_PKL, t, h, count)
    return (t, h)


def initial_vertex(
    t: bytes, h: bytes, hash_function: Callable[[bytes], bytes]
) -> Tuple[bytes, bytes]:
    print("STEP 2: find initial vertex of the cycle")

    try:
        t, h, _ = load_checkpoint(STEP2_COMPLETE_PKL)
        print(f"Step 2 Already Finished, t = {t.hex()}, h = {h.hex()}")
        return (t, h)
    except FileNotFoundError:
        pass

    count = 0

    try:
        t, h, count = load_checkpoint(STEP2_PKL)
        print(f"Resumed from checkpoint: count = {count}")
    except FileNotFoundError:
        pass

    while t != h:
        count += 1
        if count % CHECKPOINT == 0:
            print(f"current count: {count}, t = {t.hex()}, h = {h.hex()}")
            save_checkpoint(STEP2_PKL, t, h, count)

        t = hash_function(t)
        h = hash_function(h)

    print(f"STEP 2: finished. t = {t.hex()}, h = {h.hex()}")

    delete_checkpoint(STEP2_PKL)
    save_checkpoint(STEP2_COMPLETE_PKL, t, h, count)
    return (t, h)


def calculate_cycle_length(
    t: bytes, h: bytes, hash_function: Callable[[bytes], bytes]
) -> Tuple[bytes, bytes, int]:
    print("STEP 3: calculate length of the cycle")

    cycle_length = 1

    try:
        t, h, cycle_length = load_checkpoint(STEP3_PKL)
        print(f"Resumed from checkpoint: cycle_length = {cycle_length}")
    except FileNotFoundError:
        pass

    while t != h:
        if cycle_length % CHECKPOINT == 0:
            print(f"cycle_length: {cycle_length}, t = {t.hex()}, h = {h.hex()}")
            save_checkpoint(STEP3_PKL, t, h, count=cycle_length)

        h = hash_function(h)
        cycle_length += 1

    print(f"STEP 3: finished. t = {t.hex()}, h = {h.hex()}, cycle_length = {cycle_length}")

    delete_checkpoint(STEP3_PKL)
    return (t, h, cycle_length)
