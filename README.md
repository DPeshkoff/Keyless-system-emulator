# Keyless system emulator

Keyless system emulator of Remote Control — Car system for cryptography studying.

List of dependencies:

* Ed25519PrivateKey from cryptography.hazmat.primitives.asymmetric.ed25519
* X25519PrivateKey from cryptography.hazmat.primitives.asymmetric.x25519
* Random from Cryptodome
* AES from Cryptodome.Cipher

# Build

* Install [Python3](https://www.python.org/downloads/)
* Run `pip install pycryptodomex`to install Cryptodome
* Run `pip install cryprography`to install Cryptography
* Navigate the terminal to the directory where the script is located using the `$ cd` command.
* Type `python kse.py` or `python3 kse.py` in the terminal to execute the script.

# How it works

Both Remote Key (RK) and Car generate two pairs of keys. The first (Handshake key) is x25519 and is used to generate shared handshake key to prove that the connection is secure and not modified. Ed25519 keys are used to sign and verify the signature of the data. The data itself is encrypted by AES.

# Test run

* Step 0: keys generation:
 RK Public Handshake Key: <cryptography.hazmat.backends.openssl.x25519._X25519PublicKey object at 0x0000024848AD8BE0>
 RK Public Key:  <cryptography.hazmat.backends.openssl.ed25519._Ed25519PublicKey object at 0x0000024849006400>24849006400>                                                                                       0x000002484984DE10>
 Car Public Handshake Key: <cryptography.hazmat.backends.openssl.x25519._X25519PublicKey object at02484984DE80> 0x000002484984DE10>
 Car Public Key:  <cryptography.hazmat.backends.openssl.ed25519._Ed25519PublicKey object at 0x000002484984DE80>                                                                                     \x80\xcbO\x9d\xa3E'
* Step 1: exchange of public handshake keys.
* Step 2: package is sent:
     Shared handshake key:  b'-\xc8Jt\x9e\x05^\x8a3\x1d\xc5\x0c\x0b/L)F\x16\xd1X\xb3v\x96?\xa7\xfe\x80\xcbO\x9d\xa3E'     Encrypted data: b'+\xf0\xea\xde\x97\x16P\x7f\xda\x97\xb0e\x16\x99\xc0r3\x8f\x92\xfd'
     Signed encrypted data:  b'\xb8:*\x80\x90r\xa8\x8aZz\xf2\x02U7\\\x16\xaaz\xa2\x8d\x02R\x80s\xe2\xa5I\x17\xe1[#\x998\x04\xd2\x01\xc6\xd18@@*:2\xf7\xfd&\xf5yp\xec\xe4\x15xP,E{\x07}k\x19p\x04'     Session key:  b'0s\xe93n#S\x18\xaeXW\xfc\xd3UYm\x9c\xc3\xa7$\x9e\xaf\x1e\xfe\x82\xc7B\t\xd6#\xae*'     Public key:  <cryptography.hazmat.backends.openssl.ed25519._Ed25519PublicKey object at 0x0000024849006400>
* Step 3: package is received:     User is correct, shared handshake key from package is the same as local shared_handshake_key
     Signature is verified     Encrypted session key is restored
     Data is decrypted
* Original data is:  b'data'
* Decoded data is:  b'data'
* Success!