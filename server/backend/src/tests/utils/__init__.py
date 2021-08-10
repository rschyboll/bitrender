import random
import string


def random_lower_string(length: int = random.randint(0, 32)) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=length))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"
