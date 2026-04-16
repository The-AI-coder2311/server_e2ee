import os, hashlib
from cryptography.hazmat.primitives.asymmetric import x25519, ed25519
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def gen_identity():
    priv = ed25519.Ed25519PrivateKey.generate()
    return priv, priv.public_key()

def fingerprint(pub):
    return hashlib.sha256(pub.public_bytes_raw()).hexdigest()

def gen_dh():
    priv = x25519.X25519PrivateKey.generate()
    return priv, priv.public_key()

def kdf(data):
    return HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b"secure-chat"
    ).derive(data)

def x3dh(priv_a, eph_a, pub_b):
    return kdf(priv_a.exchange(pub_b) + eph_a.exchange(pub_b))

class Ratchet:
    def __init__(self, root):
        self.chain = root

    def next_key(self):
        self.chain = kdf(self.chain)
        return self.chain

    def encrypt(self, msg):
        key = self.next_key()
        aes = AESGCM(key)
        nonce = os.urandom(12)
        ct = aes.encrypt(nonce, msg.encode(), None)
        return nonce.hex(), ct.hex()

    def decrypt(self, nonce, ct):
        key = self.next_key()
        aes = AESGCM(key)
        return aes.decrypt(bytes.fromhex(nonce), bytes.fromhex(ct), None).decode()
