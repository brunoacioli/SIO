import sys
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from more_itertools import padded

def main():
    fileIn = sys.argv[1]
    fileOut = sys.argv[2]
    keyFile = sys.argv[3]

    key = open(keyFile, "rb").read()
    print(len(key))
    iv = open("iv.txt", "rb").read()
    print(len(iv))

    fin = open(fileIn, "rb")
    fout = open(fileOut, "w")
    s = fin.read()
    unpadder = padding.PKCS7(128).unpadder()


    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()

    encryptedData = decryptor.update(s) + decryptor.finalize()

    decryptedData = unpadder.update(encryptedData) + unpadder.finalize()
    
    print(str(decryptedData))
    fout.write(str(decryptedData))

    fin.close()
    fout.close()
    

if __name__ == '__main__':
    main()
