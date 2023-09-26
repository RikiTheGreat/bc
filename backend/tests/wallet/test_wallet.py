from backend.wallet.wallet import Wallet
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
