import random
from math import gcd
from sympy import isprime, primefactors


def generate_large_prime():
    while True:
        n = random.randint(100000, 999999)
        if isprime(n):
            return n
        

def is_primitive_root(g, n):
    if gcd(g, n) != 1:
        return False
    
    phi = n - 1
    factors = primefactors(phi)

    for factor in factors:
        if pow(g, phi // factor, n) == 1:
            return False
    return True


def find_primitive_root(n):
    for g in range(2, n):
        if is_primitive_root(g, n):
            return g
    return None


def dh():
    n = generate_large_prime()
    
    g = find_primitive_root(n)

    x = random.randint(2, n - 1)  # prywatny klucz A
    X = pow(g, x, n)

    y = random.randint(2, n - 1)  # prywatny klucz B
    Y = pow(g, y, n)

    k_A = pow(Y, x, n)

    k_B = pow(X, y, n)

    if k_A == k_B:
        print("Klucz wspólny: ", k_A)
    else:
        print("Błąd: klucze nie są równe")


dh()
