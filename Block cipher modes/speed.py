import time
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util import Counter
from Crypto.Util.Padding import pad, unpad


files = ["small.txt", "medium.txt", "large.txt"]

modes = {
    'ECB': AES.MODE_ECB,
    'CBC': AES.MODE_CBC,
    'CFB': AES.MODE_CFB,
    'OFB': AES.MODE_OFB,
    'CTR': AES.MODE_CTR
}

key = get_random_bytes(16)  # AES-128


def encrypt(data, mode_name):
    if mode_name == 'ECB':
        cipher = AES.new(key, modes[mode_name])
        return cipher.encrypt(pad(data, AES.block_size)), {'mode': mode_name}
    elif mode_name == 'CBC':
        iv = get_random_bytes(16)
        cipher = AES.new(key, modes[mode_name], iv=iv)
        return cipher.encrypt(pad(data, AES.block_size)), {'mode': mode_name, 'iv': iv}
    elif mode_name in ['CFB', 'OFB']:
        iv = get_random_bytes(16)
        cipher = AES.new(key, modes[mode_name], iv=iv)
        return cipher.encrypt(pad(data, AES.block_size)), {'mode': mode_name, 'iv': iv}
    elif mode_name == 'CTR':
        ctr = Counter.new(128)
        cipher = AES.new(key, modes[mode_name], counter=ctr)
        return cipher.encrypt(pad(data, AES.block_size)), {'mode': mode_name, 'counter': ctr}


def decrypt(ciphertext, mode_name, cipher_info):
    if mode_name == 'ECB':
        cipher = AES.new(key, AES.MODE_ECB)
    elif mode_name == 'CBC':
        cipher = AES.new(key, AES.MODE_CBC, iv=cipher_info['iv'])
    elif mode_name == 'CFB':
        cipher = AES.new(key, AES.MODE_CFB, iv=cipher_info['iv'])
    elif mode_name == 'OFB':
        cipher = AES.new(key, AES.MODE_OFB, iv=cipher_info['iv'])
    elif mode_name == 'CTR':
        cipher = AES.new(key, AES.MODE_CTR, counter=cipher_info['counter'])
    decrypted = cipher.decrypt(ciphertext)

    return unpad(decrypted, AES.block_size)


for file in files:
    with open(file, "rb") as f:
        data = f.read()
    print(f"Plik: {file}")

    for mode_name in modes:
        start = time.time()
        encrypted, cipher_info = encrypt(data, mode_name)
        enc_time = time.time() - start

        start = time.time()
        decrypted = decrypt(encrypted, mode_name, cipher_info)
        dec_time = time.time() - start

        print(f"{mode_name}: szyfrowanie = {round(enc_time, 4)} s, deszyfrowanie = {round(dec_time, 4)} s")
