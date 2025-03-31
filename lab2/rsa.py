import random
from sympy import isprime


def generate_prime(bits):
    while True:
        n = random.getrandbits(bits) | 1  # Liczba nieparzysta
        if isprime(n):
            return n
        

def are_consecutive_primes(a, b):
    if a > b:
        a, b = b, a

    for i in range(a + 1, b):
        if isprime(i):
            return False
    return True


def generate_keys():
    while True:
        p = generate_prime(1024)
        q = generate_prime(1024)
        if not are_consecutive_primes(p, q):
            break

    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randint(2, phi)
    while not isprime(e) or phi % e == 0:
        e = random.randint(2, phi)
    
    d = pow(e, -1, phi)

    return (e, n), (d, n)  # Klucz publiczny, klucz prywatny


def encrypt(message, public_key):
    e, n = public_key
    encrypted_message = [pow(ord(char), e, n) for char in message if ord(char) < n]
    return encrypted_message


def decrypt(encrypted_message, private_key):
    d, n = private_key
    decrypted_message = ''.join(chr(pow(char, d, n)) for char in encrypted_message)
    return decrypted_message


public_key, private_key = generate_keys()

message = 'This a test message for RSA algorithm. 0123456789!'
print("Pierwotna wiadomość: ", message)
if any(ord(char) >= public_key[1] for char in message):
    raise ValueError("Wiadomość zawiera znaki o wartości większej niż n. Zwiększ rozmiar klucza.")

# Szyfrowanie 
encrypted_message = encrypt(message, public_key)
#print("Zaszyfrowana wiadomość: ", encrypted_message)

# Deszyfrowanie
decrypted_message = decrypt(encrypted_message, private_key)
print("Odszyfrowana wiadomość: ", decrypted_message)

if message == decrypted_message:
    print("Odszyfrowana wiadomość jest identyczna z wiadomością pierwotną.")
else:
    print("Wiadomość nie została odszyfrowana poprawnie.")
