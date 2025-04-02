from common import make_hash_function


def find_cycle(k: int, iv: str):
    print(f"Find cycle for k={k} with iv={iv}")

    hash_function = make_hash_function(k)

    # Here, we will going to use Tortoise-Hare Algorithm
    # to find the initial value and the cycle length.
    # `t` for Tortoise, `h` for Hare.
    # `t` jumps one edge per step while `f` jumps two edges per step.

    start = hash_function(iv.encode("utf-8"))
    t = hash_function(start)
    h = hash_function(hash_function(start))
    while t != h:
        t = hash_function(t)
        h = hash_function(hash_function(h))

    # Tortoise and Hare met at some point.
    # Let the tortoise to go back to the starting point.
    # And they will move one edge per step.
    # The vertex they met is the initial edge that this cycle begins.
    t = start
    while t != h:
        t = hash_function(t)
        h = hash_function(h)

    # Fix the tortoise at that point, and move the hare to calculate the cycle length.
    cycle_length = 1
    h = hash_function(t)
    while t != h:
        h = hash_function(h)
        cycle_length += 1

    print(f"Initial Value: {t.hex()}, and the cycle length: {cycle_length}")
