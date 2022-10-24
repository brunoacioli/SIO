import sys
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


def main():
    private_key_file = open(sys.argv[1], "wb")
    public_key_file = open(sys.argv[2], "wb")
    

    size = int(sys.argv[3])

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=size
    )


    
    print(type(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.OpenSSH,
        encryption_algorithm=serialization.NoEncryption()
    )))

    private_key_file.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.OpenSSH,
        encryption_algorithm=serialization.NoEncryption()
    ))
    
    public_key_file.write(private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))

    public_key_file.close()
    private_key_file.close()


if __name__ == '__main__':
    main()