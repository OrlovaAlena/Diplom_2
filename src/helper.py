import random
import string


def generate_random_string(n):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(n))
    return random_string
