from backend.wallet.wallet import Wallet
from backend.blockchain.blockchain import Blockchain
from backend.wallet.transaction import Transaction
from backend.config import DEFAULT_BALANCE
from cryptography.exceptions import InvalidSignature
import pytest


def test_check_verify_is_successful():
    wallet = Wallet()
    data = "Hello"
    signature = wallet.sign(data)

    assert wallet.verify(wallet.public_key, data, signature)


def test_check_verify_is_not_successful():
    wallet = Wallet()
    data = "Hello"
    signature = wallet.sign(data)

    assert not wallet.verify(Wallet().public_key, data, signature)


def test_calculate_balance():
    blockchain = Blockchain()
    wallet = Wallet()

    assert Wallet.claulate_balance(blockchain, wallet.address) == DEFAULT_BALANCE

    amount = 50
    transaction = Transaction(wallet, "recipient", amount)
    blockchain.add_block([transaction.to_json()])

    assert (
        Wallet.claulate_balance(blockchain, wallet.address) == DEFAULT_BALANCE - amount
    )
