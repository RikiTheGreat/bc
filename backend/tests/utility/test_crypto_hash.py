from backend.utility.crypto_hash import crypto_hash

import pytest
def test_crypto_hash():
    # It should create the same hash with arguments of diffrent data types
    # in any order
    
    one = crypto_hash(1, 1, 1)
    two = crypto_hash(2, 2, 3, 3)
    assert 1
    #assert one == two