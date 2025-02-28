import secrets


def random_number(low: int, high: int) -> int:
    return secrets.randbelow(high + 1 - low) + low
