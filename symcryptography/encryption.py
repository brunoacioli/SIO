import sys
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def main():
    fileIn = sys.argv[1]
    fileOut = sys.argv[2]
    encrypt = sys.argv[3]

    fIn = open(fileIn, "r")
    fOut = open(fileOut, "a")

    s = fIn.read()
    print(s)
    print(len(s))
    
    key = os.urandom(32)
    

    # ESCREVER IV NO FICHEIRO
    
    if encrypt == "AES":
        
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        ct = encryptor.update(b"" + bytes(s, 'utf-8')) + encryptor.finalize()

        fOut.write(str(ct))
        decryptor = cipher.decryptor()
        print(decryptor.update(ct) + decryptor.finalize())

    if encrypt == "CHACHA20":

        nonce = os.urandom(16)
        algorithm = algorithms.ChaCha20(key, nonce)
        cipher = Cipher(algorithm, mode=None)
        encryptor = cipher.encryptor()
        ct = encryptor.update(b"" + bytes(s, 'utf-8'))

        fOut.write(str(ct) + "\n")
        decryptor = cipher.decryptor()
        decryptor.update(ct)


    fIn.close()
    fOut.close()





if __name__ == '__main__':
    main()