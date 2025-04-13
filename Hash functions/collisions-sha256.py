import hashlib
import string
import random

saved = {}
iterations = 500

for _ in range(iterations):
    generated_input = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
    sha256_prefix = hashlib.sha3_256(generated_input.encode('utf-8')).hexdigest()[:3]  # 3 znaki hex = 12 bitów

    if sha256_prefix in saved:
        saved[sha256_prefix].append(generated_input)
    else:
        saved[sha256_prefix] = [generated_input]

count = 0
for prefix, inputs in saved.items():
    if len(inputs) > 1:
        found = True
        count += 1
        print(f"Kolizja dla pierwszych 12 bitów ciągu wyjściowego '{prefix}' dla ciagow wejsciowych:")
        for i in inputs:
            print(f"{i}")

if count > 0:
    print(f"Znaleziono {count} kolizji.")
else:
    print(f"Nie znaleziono żadnych kolizji dla {iterations} prób.")
