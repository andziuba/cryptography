from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


def modify_first_byte(ciphertext):
    modified = bytearray(ciphertext)
    modified[0] ^= 0x01
    return bytes(modified)

def test_mode(mode_name, mode_creator):
    print(f"\nTryb: {mode_name}")

    key = get_random_bytes(16)
    iv = get_random_bytes(16)
    plaintext = b"To jest zdanie testowe do analizy propagacji bledow."

    cipher = mode_creator(key, iv)
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

    corrupted_ciphertext = modify_first_byte(ciphertext)

    cipher = mode_creator(key, iv)
    decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)

    cipher = mode_creator(key, iv)
    try:
        corrupted_decrypted = cipher.decrypt(corrupted_ciphertext)
        corrupted_decrypted = unpad(corrupted_decrypted, AES.block_size)
    except ValueError:
        corrupted_decrypted = "[Błąd podczas odszyfrowywania / padding error]"

    print(f"Oryginał:  {plaintext.decode('utf-8')}")
    print(f"Po błędzie: {corrupted_decrypted.decode('utf-8', errors='ignore')}")


modes = {
    "ECB": lambda key, iv: AES.new(key, AES.MODE_ECB),
    "CBC": lambda key, iv: AES.new(key, AES.MODE_CBC, iv),
    "CFB": lambda key, iv: AES.new(key, AES.MODE_CFB, iv, segment_size=128),
    "OFB": lambda key, iv: AES.new(key, AES.MODE_OFB, iv),
    "CTR": lambda key, iv: AES.new(key, AES.MODE_CTR, nonce=iv[:8])
}

for mode_name, mode_creator in modes.items():
    test_mode(mode_name, mode_creator)
