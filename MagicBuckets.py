from typing import Callable, List, Optional
from sympy import *
import random
import Hasher


class Prime:
    def __init__(self, value: int):
        if isprime(value):
            self.value: int = value
        else:
            raise ValueError("You have fucked up, attempted to use non prime as p.")


class MagicBuckets:
    def __init__(self, n: int, log_mu: int, p: int = None, bucket_functions: List[Callable[[int, int], int]] = None):
        self.mu: int = 2 ** log_mu
        self.mu_inv = 1/self.mu

        self.p: Prime = Prime(p) if p is not None else self.default_prime(n)
        self.r: int = random.randint(1, self.p.value - 1)

        self.bucket_functions: List[Callable[[int,int],int]]  \
            = bucket_functions if bucket_functions is not None else self.default_bucket_functions()

        self.magic_buckets: List[int] = [0 for _ in range(len(self.bucket_functions))]

        self.hasher: Hasher = Hasher.Hasher()

    def add(self, value: int, position: int):
        if self.hasher.hashes_to_bucket(position, self.mu_inv):
            for i in range(len(self.magic_buckets)):
                self.magic_buckets[i] += self.bucket_functions[i](value, position)
                self.magic_buckets[i] %= self.p.value

    def default_bucket_functions(self) -> List[Callable[[int, int], int]]:
        a = lambda value, position: value
        b = lambda value, position: value * position
        c = lambda value, position: (value * pow(self.r, position, self.p.value))
        return [a, b, c]

    def default_prime(self, n) -> Prime:
        return self.get_prime_in_range(n**2, n**3)

    def get_prime_in_range(self, start: int, finish: int) -> Prime:
        return Prime(randprime(start, finish))

    def get_bucket_value(self) -> Optional[int]:
        buckets_match = True
        for i, bucket_function in enumerate(self.bucket_functions[2:]):
            if bucket_function(self.magic_buckets[0], self.magic_buckets[1] // self.magic_buckets[0]) != self.magic_buckets[i]:
                buckets_match = False
        return self.magic_buckets[0] if buckets_match else False
