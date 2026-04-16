import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def encrypt_file(path):
    key = AESGCM.generate_key(bit_length=128)
    aes = AESGCM(key)

    with open(path, "rb") as f:
        data = f.read()

    nonce = os.urandom(12)
    ct = aes.encrypt(nonce, data, None)

    with open(path + ".enc", "wb") as f:
        f.write(nonce + ct)

    return key.hex()

def decrypt_file(path, key):
    aes = AESGCM(bytes.fromhex(key))

    raw = open(path, "rb").read()
    data = aes.decrypt(raw[:12], raw[12:], None)

    with open(path + ".dec", "wb") as f:
        f.write(data)
