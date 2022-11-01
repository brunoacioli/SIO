from operator import length_hint
import click

@click.command()
@click.option('--filename', required=True, help='File to be hashed')
@click.option('--hash_function', required=True, help='Hash function')
def main(filename, hash_function):

    text_file = open(filename, "rb")
    text = text_file.read()

    length = len(text)
    


def hash_compare(h1, h2):
    comp_hash = int.from_bytes(h1) ^ int.from_bytes(h2)
    bin_str = bin(comp_hash)[2:].ljust(len(h1*8), '0')
    return bin_str.count("0")


def flip_bit(data, bit_n):
    adata = bytearray(data)
    offset = int(bit_n/8)
    bit_offset = bit_n % 8
    if len(adata) <= offset:
        return adata
    
    adata[offset] = adata[offset] ^ (0x80 >> bit_offset)

    return adata    


if __name__ == '__main__':
    main()
