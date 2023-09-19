from backend.utility.hex_to_binary import hex_to_binary

def test_hex_to_binary():
    num = 234
    hex_num = hex(num)[2:]
    binary_num = hex_to_binary(hex_num)

    assert int(binary_num, 2) == num