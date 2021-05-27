#!/usr/bin/env python

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
import os

def decrypt(data_str = None, data_file = None, private_key = None):
    if data_str == None and data_file is None:
        return 'data string or file needed'
    if data_file:
        with open(data_file, "rb") as f:
            data = f.read()
    else:
        data = data_str
    if private_key == None:
        private_key = os.environ['HOME'] + '/.ssh/id_rsa'
    with open(private_key, "rb") as k:
        key = RSA.importKey(k.read())

    decipher = Cipher_PKCS1_v1_5.new(key)
    return decipher.decrypt(data, None).decode()

