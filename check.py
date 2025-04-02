from common import make_hash_function


def check_result(k: int, iv: str, cycle: int):
    print(f"Check result for k={k}, iv={iv}, cycle={cycle}")

    hash_function = make_hash_function(k)

    start = bytes.fromhex(iv)
    walk = hash_function(start)
    count = 1

    while start != walk:
        walk = hash_function(walk)
        count += 1

    if count == cycle:
        print("CHECK SUCCESS")
    else:
        print("CHECK FAIL")
