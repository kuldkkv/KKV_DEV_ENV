#!/usr/bin/env python

from cryptography.fernet import Fernet



class Decrypt:

    def __init__(self, key_file_name, encrypted_message):
        self.key_file_name = key_file_name
        self.encrypted_message = encrypted_message


    def __load_key(self):
        """
        Load the previously generated key
        """
        return open(self.key_file_name, "rb").read()


    def decrypt_message(self):
        """
        Decrypts an encrypted message
        """
        key = self.__load_key()
        f = Fernet(key)
        decrypted_message = f.decrypt(self.encrypted_message)

        return decrypted_message.decode()
