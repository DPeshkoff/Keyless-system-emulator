#!/usr/bin/python
# -*- coding: UTF-8 -*-
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from Cryptodome import Random
from Cryptodome.Cipher import AES


class RK:
    """Remote Key emulator"""
 

    def __init__(self):
        self.private_handshake_key = X25519PrivateKey.generate()
        self.public_handshake_key = self.private_handshake_key.public_key()

        self.private_key = Ed25519PrivateKey.generate()
        self.public_key = self.private_key.public_key()

        self.data = "data".encode('utf8')

    def handshake(self, peer_key):
        self.shared_handshake_key = self.private_handshake_key.exchange(peer_key)



    def encrypted_package(self, car_public_key):
        # encrypt session key
        iv = Random.new().read(16)
        self.session_key = Random.new().read(32)
        encrypted_session_key = AES.new(self.session_key, AES.MODE_CFB, iv)

        self.encrypted_data = iv + encrypted_session_key.encrypt(self.data)

        self.signed_encrypted_data = self.private_key.sign(self.encrypted_data)

        self.signed_session_key = self.private_key.sign(self.session_key)

        return [self.shared_handshake_key, self.encrypted_data, self.signed_encrypted_data, self.session_key, self.public_key]

    





class Car:
    """Car emulator"""

    def __init__(self):
        self.private_handshake_key = X25519PrivateKey.generate()
        self.public_handshake_key = self.private_handshake_key.public_key()

        self.private_key = Ed25519PrivateKey.generate()
        self.public_key = self.private_key.public_key()

    def handshake(self, peer_key):
        self.shared_handshake_key = self.private_handshake_key.exchange(peer_key)


    def verify_package(self, package):

        # [0] = shared_handshake_key, [1] = encrypted_data, [2] = signed_encrypted_data, [3] = session_key, [4] = public_key

        if package[0] == self.shared_handshake_key:
            print("     User is correct, shared handshake key from package is the same as local shared_handshake_key")
            try:
                package[4].verify(package[2], package[1])
            except:
                print("Invalid signature of data!")
                exit()
            else: 
                print("     Signature is verified")

            iv = package[1][:16]
            encrypted_session_key = AES.new(package[3], AES.MODE_CFB, iv)

            print("     Encrypted session key is restored")

            data = encrypted_session_key.decrypt(package[1])

            self.data = data[16:]

            print("     Data is decrypted")



        else:
                print("Invalid user!")
                exit()            


if __name__ == '__main__':
    Alice = RK()
    Bob = Car()

    print("Step 0: keys generation: \n RK Public Handshake Key:", Alice.public_handshake_key, "\n RK Public Key: ", Alice.public_key, "\n Car Public Handshake Key:", Bob.public_handshake_key, "\n Car Public Key: ", Bob.public_key)

    Alice.handshake(Bob.public_handshake_key)
    Bob.handshake(Alice.public_handshake_key)

    print("Step 1: exchange of public handshake keys.")

    package = Alice.encrypted_package(Bob.public_key)

    print("Step 2: package is sent:")
    print("     Shared handshake key: ", package[0])
    print("     Encrypted data:", package[1])
    print("     Signed encrypted data: ", package[2])
    print("     Session key: ", package[3])
    print("     Public key: ", package[4])

    print("Step 3: package is received:")
    Bob.verify_package(package)


    print("Original data is: ", Alice.data, "\n Decoded data is: ", Bob.data)

    if Bob.data == Alice.data:
        print("Success!")
    else:
        print("Fail!")