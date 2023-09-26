from backend.blockchain.blockchain import Blockchain
from backend.blockchain.block import GENESIS_DATA

import pytest


def test_add_block():
    blockchain = Blockchain()
    blockchain.add_block("test_data")

    assert blockchain.chain[-1].data == "test_data"


def test_is_valid_chain():
    blockchain = Blockchain()

    for i in range(3):
        blockchain.add_block(i)

    Blockchain.is_valid_chain(blockchain.chain)


@pytest.fixture
def blockchain_with_three_block():
    blockchain = Blockchain()
    blockchain.add_block("block2")
    blockchain.add_block("block3")
    blockchain.add_block("block4")
    return blockchain


def test_replace_with_greater_chain(blockchain_with_three_block):
    blockchain1 = Blockchain()  # it only has genesis block in it
    blockchain1.replace_chain(blockchain_with_three_block.chain)

    assert blockchain1.chain == blockchain_with_three_block.chain


def test_replace_with_lower_chain(blockchain_with_three_block):
    blockchain1 = Blockchain()

    with pytest.raises(Exception, match="can't replace. chain must be longer!"):
        blockchain_with_three_block.replace_chain(blockchain1.chain)
