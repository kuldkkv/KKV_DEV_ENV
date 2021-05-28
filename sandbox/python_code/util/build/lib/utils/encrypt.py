#!/usr/bin/env python

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
import os

def encrypt(data, out_file = None, public_key=None):
    if public_key == None:
        public_key = os.environ['HOME'] + '/.ssh/id_rsa.pub'
    with open(public_key, "rb") as k:
        key = RSA.importKey(k.read())

    cipher = Cipher_PKCS1_v1_5.new(key)
    enc_str = cipher.encrypt(data.encode())
    if out_file:
        with open(out_file, "wb") as f:
            f.write(enc_str)
        print('written to file [%s].' % out_file)
            
    return enc_str
