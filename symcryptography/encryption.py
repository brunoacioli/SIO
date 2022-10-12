import sys
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from more_itertools import padded

def main():
    fileIn = sys.argv[1]
    fileOut = sys.argv[2]
    encrypt = sys.argv[3]

    fIn = open(fileIn, "r")
    fOut = open(fileOut, "wb")
    keyFile = open("key.txt", "wb")
    fiv = open("iv.txt", "wb")

    s = fIn.read()
    print(s)
    print(len(s))
    
    key = os.urandom(32)
    keyFile.write(key)
    

    padder = padding.PKCS7(128).padder()
    unpadder = padding.PKCS7(128).unpadder()

    padded_data = padder.update(bytes(s, 'utf-8'))
    print("padded data " + str(padded_data))
    padded_data += padder.finalize()
    print("padded data with finalize " + str(padded_data))

    
    if encrypt == "AES":
        
        iv = os.urandom(16)

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        ct = encryptor.update(padded_data) + encryptor.finalize()

        fiv.write(iv)
        fOut.write(ct)

        decryptor = cipher.decryptor()
        
        decryptedData = decryptor.update(ct) + decryptor.finalize()
        data = unpadder.update(decryptedData) + unpadder.finalize()
        
        print(data)

    if encrypt == "CHACHA20":

        nonce = os.urandom(16)

        algorithm = algorithms.ChaCha20(key, nonce)
        cipher = Cipher(algorithm, mode=None)
        encryptor = cipher.encryptor()
        ct = encryptor.update(padded_data)

        fOut.write(ct)

        decryptor = cipher.decryptor()
        decryptedData = decryptor.update(ct)
        data = unpadder.update(decryptedData) + unpadder.finalize()
        print(data)


    fIn.close()
    fOut.close()
    keyFile.close()
    fiv.close()



if __name__ == '__main__':
    main()