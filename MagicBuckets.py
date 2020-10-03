from typing import Callable, List, Optional
from sympy import *
import random


class Prime:
    def __init__(self, value: int):
        if isprime(value):
            self.value: int = value
        else:
            raise ValueError("You have fucked up, attempted to use non prime as p.")


class MagicBuckets:
    def __init__(self, p: int = None, bucket_functions: List[Callable[[int, int], int]] = None):

        self.bucket_functions: List[Callable[[int,int],int]]  \
            = bucket_functions if bucket_functions is not None else self.default_bucket_functions()

        self.p: Prime = prime(p) if p is not None else self.default_prime()
        self.r: int = random.randint(1, self.p.value - 1)

        self.magic_buckets: List[int] = [0 for _ in range(len(self.bucket_functions))]

    def add(self, value: int, position: int):
        for i, magic_bucket in enumerate(self.magic_buckets):
            magic_bucket += self.bucket_functions[i](value, position)
            magic_bucket %= self.p.value

    def subtract(self, value: int, position: int):
        for i, magic_bucket in enumerate(self.magic_buckets):
            magic_bucket -= self.bucket_functions[i](value, position)
            magic_bucket %= self.p.value

    def default_bucket_functions(self) -> List[Callable[[int, int], int]]:
        a = lambda value, position: value
        b = lambda value, position: value * position
        c = lambda value, position: (value * pow(self.r, position, self.p.value)) % self.p.value
        return [a, b, c]

    @staticmethod
    def default_prime() -> Prime:
        return Prime(2)

    def get_prime_in_range(self, start: int, finish: int) -> Prime:
        return Prime(randprime(start, finish))

    def get_bucket_value(self) -> Optional[int]:
        buckets_match = True
        for i, bucket_function in enumerate(self.bucket_functions[1:]):
            if bucket_function(self.magic_buckets[0]) != self.magic_buckets[i]:
                buckets_match = False
        return self.magic_buckets[0] if buckets_match else False
