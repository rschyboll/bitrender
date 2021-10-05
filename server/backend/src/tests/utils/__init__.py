import os
import random
import string


def random_lower_string(length: int = random.randint(0, 32)) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=length))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def random_byte_data(length: int = random.randint(16, 256)) -> bytes:
    return os.urandom(length)
