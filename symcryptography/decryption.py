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

    fin = open(fileIn, "r")
    fout = open(fileOut, "w")
    s = fin.read()
    unpadder = padding.PKCS7(128).unpadder()


    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()

    #consertar erro    
    encryptedData = bytes(s, 'utf-8')
    encryptedData = unpadder.update(encryptedData) + unpadder.finalize()
    #decryptedData = decryptor.update(encryptedData) + decryptor.finalize()
    #data = unpadder.update(decryptedData)
    print(str(encryptedData))
    fout.write(str(encryptedData))
    

if __name__ == '__main__':
    main()
