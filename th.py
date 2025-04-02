from collections.abc import Callable
from typing import Tuple

from common import save_checkpoint, load_checkpoint, delete_checkpoint

# For every `CHECKPOINT` iteration, save to pickle file.
CHECKPOINT = 10_000_000


def meeting_vertex(
    t: bytes,
    h: bytes,
    hash_function: Callable[[bytes], bytes],
    step1_pkl: str,
    step1_complete_pkl: str,
) -> Tuple[bytes, bytes]:
    print("STEP 1: find meeting vertex")

    try:
        t, h, _ = load_checkpoint(step1_complete_pkl)
        print(f"Step 1 Already Finished, t = {t.hex()}, h = {h.hex()}")
        return (t, h)
    except FileNotFoundError:
        pass

    count = 0

    try:
        t, h, count = load_checkpoint(step1_pkl)
        print(f"Resumed from checkpoint: count = {count}")
    except FileNotFoundError:
        pass

    while t != h:
        count += 1
        if count % CHECKPOINT == 0:
            print(f"current count: {count}, t = {t.hex()}, h = {h.hex()}")
            save_checkpoint(step1_pkl, t, h, count)

        t = hash_function(t)
        h = hash_function(hash_function(h))

    print(f"STEP 1: finished. t = {t.hex()}, h = {h.hex()}")

    delete_checkpoint(step1_pkl)
    save_checkpoint(step1_complete_pkl, t, h, count)
    return (t, h)


def initial_vertex(
    t: bytes,
    h: bytes,
    hash_function: Callable[[bytes], bytes],
    step2_pkl: str,
    step2_complete_pkl: str,
) -> Tuple[bytes, bytes, bytes, bytes]:
    print("STEP 2: find initial vertex of the cycle")

    try:
        if len(step2_complete_pkl) > 0:
            t, h, _ = load_checkpoint(step2_complete_pkl)
            print(f"Step 2 Already Finished, t = {t.hex()}, h = {h.hex()}")
            return (t, h)
    except FileNotFoundError:
        pass

    count = 0

    tail_preimage = t
    cycle_preimage = h

    try:
        t, h, count = load_checkpoint(step2_pkl)
        print(f"Resumed from checkpoint: count = {count}")
    except FileNotFoundError:
        pass

    while t != h:
        count += 1
        if count % CHECKPOINT == 0:
            print(f"current count: {count}, t = {t.hex()}, h = {h.hex()}")
            save_checkpoint(step2_pkl, t, h, count)

        tail_preimage = t
        t = hash_function(t)
        cycle_preimage = h
        h = hash_function(h)

    print(
        f"STEP 2: finished. t = {t.hex()} (preimage: {tail_preimage.hex()}), h = {h.hex()} (preimage: {cycle_preimage.hex()})"
    )

    delete_checkpoint(step2_pkl)
    if len(step2_complete_pkl) > 0:
        save_checkpoint(step2_complete_pkl, t, h, count)
    return (t, h, tail_preimage, cycle_preimage)


def calculate_cycle_length(
    t: bytes, h: bytes, hash_function: Callable[[bytes], bytes], step3_pkl: str
) -> Tuple[bytes, bytes, int]:
    print("STEP 3: calculate length of the cycle")

    cycle_length = 1

    try:
        t, h, cycle_length = load_checkpoint(step3_pkl)
        print(f"Resumed from checkpoint: cycle_length = {cycle_length}")
    except FileNotFoundError:
        pass

    while t != h:
        if cycle_length % CHECKPOINT == 0:
            print(f"cycle_length: {cycle_length}, t = {t.hex()}, h = {h.hex()}")
            save_checkpoint(step3_pkl, t, h, count=cycle_length)

        h = hash_function(h)
        cycle_length += 1

    print(f"STEP 3: finished. t = {t.hex()}, h = {h.hex()}, cycle_length = {cycle_length}")

    delete_checkpoint(step3_pkl)
    return (t, h, cycle_length)
