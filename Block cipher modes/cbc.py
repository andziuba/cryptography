from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64


def encrypt(text, key, iv):
    text = pad(text.encode('utf-8'), AES.block_size)
    cipher_ecb = AES.new(key, AES.MODE_ECB)
    blocks = [text[i:i + AES.block_size] for i in range(0, len(text), AES.block_size)]

    ciphertext = b''
    previous_block = iv
    for block in blocks:
        xored_block = bytes([x ^ y for x, y in zip(block, previous_block)])
        encrypted_block = cipher_ecb.encrypt(xored_block)
        ciphertext += encrypted_block
        previous_block = encrypted_block

    return base64.b64encode(ciphertext).decode('utf-8')


def decrypt(ciphertext, key, iv):
    ciphertext = base64.b64decode(ciphertext)
    cipher_ecb = AES.new(key, AES.MODE_ECB)
    blocks = [ciphertext[i:i + AES.block_size] for i in range(0, len(ciphertext), AES.block_size)]

    plaintext = b''
    previous_block = iv
    for block in blocks:
        decrypted_block = cipher_ecb.decrypt(block)
        xored_block = bytes([x ^ y for x, y in zip(decrypted_block, previous_block)])
        plaintext += xored_block
        previous_block = block

    return unpad(plaintext, AES.block_size).decode('utf-8')


key = get_random_bytes(16)
iv = get_random_bytes(16)

message = "To jest przykładowy tekst"
print("Oryginalna wiadomość:", message)

encrypted = encrypt(message, key, iv)
print("Zaszyfrowana wiadomość:", encrypted)

decrypted = decrypt(encrypted, key, iv)
print("Odszyfrowana wiadomość:", decrypted)
