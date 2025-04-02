import hashlib
import os
from collections.abc import Callable
import pickle
from typing import Tuple

PICKLES = "pickles"


def make_hash_function(k: int) -> Callable[[bytes], bytes]:
    def hash_function(input: bytes) -> bytes:
        hashed = hashlib.md5(input).digest()
        byte = k // 8
        return hashed[-byte:]

    return hash_function


def save_checkpoint(filename, t: bytes, h: bytes, count: int):
    with open(filename, "wb") as f:
        pickle.dump((t, h, count), f)


def load_checkpoint(filename) -> Tuple[bytes, bytes, int]:
    with open(filename, "rb") as f:
        return pickle.load(f)


def delete_checkpoint(filename: str):
    if os.path.exists(filename):
        os.remove(filename)
        print(f"Deleted checkpoint file: {filename}")
    else:
        print(f"No checkpoint file found at: {filename}")
