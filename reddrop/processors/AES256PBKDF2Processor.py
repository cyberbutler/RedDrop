import hashlib
from Crypto.Cipher import AES
from .BaseProcessor import BaseProcessor

class AES256PBKDF2Processor(BaseProcessor):
    """
    This Processor class implements the OpenSSL AES256 CBC PBKDF2 decryption standard. 

    An example of encrypting data using `openssl` given this standard is:
    ```bash
    openssl enc -aes-256-cbc -pbkdf2 -pass 'pass:EncryptMe' -md sha256 -pbkdf2 -e
    ```
    """

    name = 'openssl-aes256-pbkdf2'
    parameters = {
        "password": "EncryptMe",
        "iterations": 10000
    }
    
    def processData(self, encrypted:bytes, password:str, iterations:int=10000) -> bytes:
        """
        Decrypt the provided bytes using the OpenSSL AES256 PBKDF2 format.

        Shamelessly borrowed from @mti2935 here: https://crypto.stackexchange.com/a/79855
        It's highly recommended reviewing the entire thread on StackExchange, there is substantial information
        about the nuances of OpenSSL's methods for encryption when using the `enc` command. 

        """
        salt = encrypted[8:16]
        passwordBytes = password.encode('utf-8')
        derivedKey = hashlib.pbkdf2_hmac('sha256', passwordBytes, salt, iterations, 48)
        key = derivedKey[0:32]
        iv = derivedKey[32:48]
        ciphertext = encrypted[16:]
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        plaintext = decryptor.decrypt(ciphertext)

        return bytes(plaintext[:-plaintext[-1]])
    
    def validate(self, encrypted) -> bool:
        return b"Salted__" == encrypted[:8]