from backend.blockchain.block import Block, GENESIS_DATA
from backend.utility.hex_to_binary import hex_to_binary
import pytest

def test_genesis_block():
    gen = Block.genesis()
    assert GENESIS_DATA['hash'] == gen.hash


def test_mine_block():
    last_block = Block.genesis()
    data= 'testing_with_pytest'
    block = Block.mine_block(last_block, data)

    assert isinstance(block, Block)
    assert block.data == data 
    assert hex_to_binary(block.hash)[0:block.difficulty] == '0' * block.difficulty

@pytest.fixture
def last_block():
    return Block.genesis()

@pytest.fixture
def block(last_block):
    return Block.mine_block(last_block, 'test_data')

def test_is_valid_block(last_block, block):

    Block.is_valid_block(last_block, block)


def test_is_valid_block_bad_last_hash(last_block, block):
    block.last_hash = 'evil_last_hash'

    with pytest.raises(Exception, match='last_hash must be correct'):
        Block.is_valid_block(last_block, block)