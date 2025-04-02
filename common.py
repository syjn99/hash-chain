import hashlib
from collections.abc import Callable


def make_hash_function(k: int) -> Callable[[bytes], bytes]:
    def hash_function(input: bytes) -> bytes:
        hashed = hashlib.md5(input).digest()
        byte = k // 8
        return hashed[-byte:]

    return hash_function
