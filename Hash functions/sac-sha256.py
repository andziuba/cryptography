import hashlib
import random
import string

generated_input = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(100))
sha256 = hashlib.sha256(generated_input.encode('utf-8')).hexdigest()
print(f"Wartość funkcji skrótu: {sha256}")

# Wybór znaku do zmiany
generated_input_list = list(generated_input)
char_position = random.randint(0, len(generated_input_list) - 1)
selected_char = generated_input_list[char_position]

# Zmiana jednego bitu na wybranym znaku
bit_position = random.randint(0, 7)
new_char = chr(ord(selected_char) ^ (1 << bit_position))
generated_input_list[char_position] = new_char
modified_input = ''.join(generated_input_list)

new_sha256 = hashlib.sha256(modified_input.encode('utf-8')).hexdigest()
print(f"Wartość nowej funkcji skrótu: {new_sha256}")

# Powinna zmienić się połowa bitów
length = len(sha256) * 4
expected_diff = length / 2

# Obliczenie ile bitów różni się w dwóch ciągach binarnych
sha256_bin = ''.join(format(int(char, 16), '04b') for char in sha256)
new_sha256_bin = ''.join(format(int(char, 16), '04b') for char in new_sha256)
diff = sum(x != y for x, y in zip(sha256_bin, new_sha256_bin))

if abs(diff - expected_diff) < expected_diff * 0.1:
    print(f"Zmieniła się około połowa bitów: {diff}/{length} ({diff/length*100}%)")
else:
    print(f"Zmieniła się {diff}/{length} ({diff/length*100}%) bitów, co nie jest poprawne.")
