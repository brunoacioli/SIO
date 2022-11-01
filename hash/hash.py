
from cryptography.hazmat.primitives import hashes
import click

@click.command()
@click.option('--filename', required=True, help='File to be hashed')
@click.option('--number', required=True, help='Number of messages')
def main(filename, number):
    print('Hello')
    print(filename)
    print(number)

    hash_file = open("digest2.txt", "w")
    text_file = open(filename, "rb")
    text = text_file.read()

    digest = hashes.Hash(hashes.SHA256())
    digest.update(text)
    hash_file.write(digest.finalize().hex())
    hash_file.close()
    text_file.close()
    


if __name__ == '__main__':
    main()
