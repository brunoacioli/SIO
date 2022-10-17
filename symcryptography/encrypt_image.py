import sys
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from more_itertools import padded

def select_alg(alg_name, key, nonce = None):
    if alg_name == "AES":
        return algorithms.AES(key)
    if alg_name == "CHACHA20":
        return algorithms.ChaCha20(key, nonce)

def generate_cipher(algorithm, mode = None):
    return Cipher(algorithm, mode)

def update_bmp_header(original_image, enc_image):
    cmd_dd = "dd if=" + original_image + " of=" + enc_image +" ibs=1 count=54 conv=notrunc"
    print(cmd_dd)
    os.system(cmd_dd)
    


def main():
    fileIn = sys.argv[1]
    fileOut = sys.argv[2]
    alg_name = sys.argv[3]

    fIn = open(fileIn, "rb")
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

    padded_data = padder.update(s)
    print("padded data " + str(padded_data))
    padded_data += padder.finalize()
    print("padded data with finalize " + str(padded_data))

    
    if alg_name == "AES":
        
        iv = os.urandom(16)
        algorithm = select_alg(alg_name, key)
        cipher = generate_cipher(algorithm, modes.CBC(iv))
        #cipher = generate_cipher(algorithm, modes.ECB())

        encryptor = cipher.encryptor()
        ct = encryptor.update(padded_data) + encryptor.finalize()

        fiv.write(iv)
        fOut.write(ct)

        decryptor = cipher.decryptor()
        
        decryptedData = decryptor.update(ct) + decryptor.finalize()
        data = unpadder.update(decryptedData) + unpadder.finalize()
        
        print(data)

    if alg_name == "CHACHA20":

        nonce = os.urandom(16)

        algorithm = select_alg(alg_name, key, nonce)
        cipher = generate_cipher(algorithm, mode=None)
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
    update_bmp_header(fileIn, fileOut)



if __name__ == '__main__':
    main()