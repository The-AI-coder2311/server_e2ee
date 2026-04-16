import json, os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

KEY = AESGCM.generate_key(bit_length=128)

def save(file, data):
    aes = AESGCM(KEY)
    nonce = os.urandom(12)
    ct = aes.encrypt(nonce, json.dumps(data).encode(), None)
    with open(file, "wb") as f:
        f.write(nonce + ct)

def load(file):
    if not os.path.exists(file):
        return {}
    raw = open(file, "rb").read()
    aes = AESGCM(KEY)
    return json.loads(aes.decrypt(raw[:12], raw[12:], None))
