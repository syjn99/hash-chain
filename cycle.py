import time

from common import make_hash_function, delete_checkpoint, PICKLES
from th import meeting_vertex, initial_vertex, calculate_cycle_length

RESULTS_FILE = "cycles-results.txt"


def find_cycle(k: int, iv: str):
    print(f"Find cycle for k={k} with iv={iv}")

    STEP1_PKL = f"{PICKLES}/cycle-{k}-step1.pkl"
    STEP1_COMPLETE_PKL = f"{PICKLES}/cycle-{k}-step1-complete.pkl"
    STEP2_PKL = f"{PICKLES}/cycle-{k}-step2.pkl"
    STEP2_COMPLETE_PKL = f"{PICKLES}/cycle-{k}-step2-complete.pkl"
    STEP3_PKL = f"{PICKLES}/cycle-{k}-step3.pkl"

    start_time = time.time()

    hash_function = make_hash_function(k)

    # Here, we will going to use Tortoise-Hare Algorithm
    # to find the initial value and the cycle length.
    # `t` for Tortoise, `h` for Hare.
    # `t` jumps one edge per step while `f` jumps two edges per step.

    start = hash_function(bytes.fromhex(iv))
    t = hash_function(start)
    h = hash_function(hash_function(start))
    (t, h) = meeting_vertex(t, h, hash_function, STEP1_PKL, STEP1_COMPLETE_PKL)

    # Tortoise and Hare met at some point.
    # Let the tortoise to go back to the starting point.
    # And they will move one edge per step.
    # The vertex they met is the initial edge that this cycle begins.
    t = start
    (t, h, _, _) = initial_vertex(t, h, hash_function, STEP2_PKL, STEP2_COMPLETE_PKL)

    # Fix the tortoise at that point, and move the hare to calculate the cycle length.
    h = hash_function(t)
    (t, h, cycle_length) = calculate_cycle_length(t, h, hash_function, STEP3_PKL)

    delete_checkpoint(STEP1_COMPLETE_PKL)
    delete_checkpoint(STEP2_COMPLETE_PKL)

    print(f"Initial Value: {t.hex()}, and the cycle length: {cycle_length}")
    print(f"Total seconds: {time.time() - start_time}")

    with open(RESULTS_FILE, "a") as f:
        f.write(
            f"k={k}, iv={iv}, start={t.hex()}, cycle_length={cycle_length}, time={time.time() - start_time:.2f}s\n"
        )
