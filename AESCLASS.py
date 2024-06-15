


import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random
# import pyAesCrypt

BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

def encrypt(raw, password):
    #print ("okkkkkkkkkkkkkkkkkkkkkkk")  
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    raw = pad(raw).encode('utf-8')
    print ("okkkkkkkkkkkkkkkkkkkkkkk")
    iv = Random.new().read(AES.block_size)
    print ("okkkkkkkkkkkkkkkkkkkkkkk")
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    print ("okkkkkkkkkkkkkkkkkkkkkkk",type(raw))

    return base64.b64encode(iv + cipher.encrypt(raw))

def decrypt(enc, password):
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[16:]))
