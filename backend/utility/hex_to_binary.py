from backend.utility.crypto_hash import crypto_hash

HEX_TO_BINARY_CONVERTION_TABLE = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'a': '1010',
    'b': '1011',
    'c': '1100',
    'd': '1101',
    'e': '1110',
    'f': '1111'
}

def hex_to_binary(hex_string):
    binray_string = ''

    for ch in hex_string:
        binray_string+= HEX_TO_BINARY_CONVERTION_TABLE[ch]

    return binray_string


def main():

    binary_res = hex_to_binary(crypto_hash('test-data'))
    print(binary_res)

if __name__ == '__main__':
    main()