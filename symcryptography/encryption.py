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
    fOut = open(fileOut, "w")
    keyFile = open("key.txt", "wb")
    fiv = open("iv.txt", "wb")

    s = fIn.read()
    print(s)
    print(len(s))
    
    key = os.urandom(32)
    keyFile.write(key)
    

    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(bytes(s, 'utf-8'))
    print("padded data " + str(padded_data))
    padded_data += padder.finalize()
    print("padded data with finalize " + str(padded_data))

    
    if encrypt == "AES":
        
        iv = os.urandom(16)
        iv2 = str(iv)
        print(iv == bytes(iv2, 'utf-8'))
        print("len iv " + str(len(iv)))
        print("len str(iv) " + str(len(str(iv))))

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        ct = encryptor.update(padded_data) + encryptor.finalize()

        fiv.write(iv)
        fOut.write(str(ct))

        decryptor = cipher.decryptor()
        unpadder = padding.PKCS7(128).unpadder()
        decryptedData = decryptor.update(ct) + decryptor.finalize()
        data = unpadder.update(decryptedData) + unpadder.finalize()
        
        print(str(data))

    if encrypt == "CHACHA20":

        nonce = os.urandom(16)

        algorithm = algorithms.ChaCha20(key, nonce)
        cipher = Cipher(algorithm, mode=None)
        encryptor = cipher.encryptor()
        ct = encryptor.update(padded_data)

        fOut.write(str(ct))

        decryptor = cipher.decryptor()
        decryptor.update(ct)


    fIn.close()
    fOut.close()
    keyFile.close()
    fiv.close()





if __name__ == '__main__':
    main()