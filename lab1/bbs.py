import math
import random


def is_prime(n):
    for i in range(2, int(math.sqrt(n)) + 1):
        if (n % i) == 0:
            return False
    return True


# Generuje liczbę pierwszą Bluma (n ≡ 3 mod 4)
def generate_large_blum_prime():
    while True:
        n = random.randint(100000, 999999)
        if n % 4 == 3 and is_prime(n):
            return n


def bbs(num_of_bits):
    p = generate_large_blum_prime()
    q = generate_large_blum_prime()
    while p == q:
        q = generate_large_blum_prime()

    N = p * q

    # Wybranie liczby takiej liczby x, że x i N są względnie pierwsze
    x = random.randint(2, N - 1)
    while math.gcd(x, N) != 1:
        x = random.randint(2, N - 1)

    # Wartość pierwotna generatora
    seed = (x ** 2) % N

    output_bits = []
    val = seed
    for _ in range(num_of_bits):
        val = (val ** 2) % N
        output_bits.append(val & 1)  # Bit wyjścia - najmłodszy bit (LSB)

    return output_bits
