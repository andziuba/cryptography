import hashlib
import time
import string
import random
from statistics import mean


def generate_hash(hash_func, input_text, iterations):
    times = []
    output = None
    for _ in range(iterations):
        start_time = time.perf_counter_ns()
        output = hash_func(input_text.encode("utf-8")).hexdigest()
        end_time = time.perf_counter_ns()
        times.append((end_time - start_time) / 1000000)  # czas w ms

    return output, mean(times)


def generate_all_hashes(input_text, iterations):
    hash_funcs = {
        'MD5': hashlib.md5,
        'SHA-1': hashlib.sha1,
        'SHA-256': hashlib.sha256,
        'SHA-512': hashlib.sha512,
        'SHA3-256': hashlib.sha3_256,
        'SHA3-512': hashlib.sha3_512,
    }

    results = {}
    for name, func in hash_funcs.items():
        hash_value, avg_time = generate_hash(func, input_text, iterations)
        results[name] = (hash_value, avg_time)
    return results


def user_input_test():
    user_input = input("Wprowadź tekst: ")
    hashes = generate_all_hashes(user_input, iterations=1)
    for name, (val, t) in hashes.items():
        print(f"{name}:")
        print(f"Wartość skrótu: {val}")
        print(f"Długość: {len(val)} znaków ({len(val) * 4} bitów)")
        print(f"Czas wykonania: {t:.4f} ms\n")


def random_test():
    input_lengths = [500, 1000, 5000, 10000]

    for length in input_lengths:
        print(f"\nDługość wejścia: {length} znaków")
        generated_input = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

        hashes = generate_all_hashes(generated_input, iterations=100)
        for name, (val, t) in hashes.items():
            print(f"{name}:")
            print(f"Wartość skrótu: {val}")
            print(f"Długość: {len(val)} znaków ({len(val) * 4} bitów)")
            print(f"Czas wykonania: {t:.4f} ms\n")


while True:
    print("1. Funkcje skrótu dla tekstu wprowadzanego przez użytkownika")
    print("2. Wejście losowe o różnych długościach")
    choice = input("Wybierz opcję (1 lub 2): ")

    if choice == '1':
        user_input_test()
        break
    elif choice == '2':
        random_test()
        break
    else:
        print("Nieprawidłowy wybór")
