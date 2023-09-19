from backend.blockchain.block import Block, GENESIS_DATA
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