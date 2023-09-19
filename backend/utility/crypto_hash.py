import hashlib
import json

def stringfy(data):
    return json.dumps(data)


def crypto_hash(*args):
    """
    Return a sha-251 hash of the given arguments.
    """

    stringfied_args = map(stringfy, args)
   # print(f'stringfied_args: {stringfied_args}')

    joined_data = ''.join(stringfied_args)
    #print(f'joined_data: {joined_data}')
    return hashlib.sha256(joined_data.encode('utf-8')).hexdigest()


def main():
    print(f"crypto_hash('1', 'two', 3): {crypto_hash('1', 'two', 3)}")


if __name__ == '__main__':
    main()