from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet
import pytest


def test_transaction():
    sender = Wallet()
    recipient = "recipient"
    amount = 50
    tr = Transaction(sender, recipient, amount)

    assert tr.output[recipient] == amount
    assert tr.output[sender.address] == sender.balance - amount

    assert "timestamp" in tr.input
    assert tr.input["amount"] == sender.balance
    assert tr.input["address"] == sender.address

    assert Wallet.verify(tr.input["public_key"], tr.output, tr.input["signature"])


def test_trasaction_balance_check():
    with pytest.raises(Exception, match="Amount exceeds balance"):
        assert Transaction(Wallet(), "fake_address", 500000)


def test_update_transaction():
    sender_wallet = Wallet()
    first_recipient = "first_recipient"
    first_amount = 100
    transaction = Transaction(sender_wallet, first_recipient, first_amount)

    another_recipient = "another_recipient"
    second_amount = 300
    transaction.update(sender_wallet, another_recipient, second_amount)

    assert transaction.output[sender_wallet.address] == sender_wallet.balance - (
        first_amount + second_amount
    )

    assert sender_wallet.verify(
        transaction.input["public_key"],
        transaction.output,
        transaction.input["signature"],
    )


def test_validate_transaction():
    Transaction.validate_transaction(Transaction(Wallet(), "recipient", 100))


def test_bad_validation_transaction():
    sender_wallet = Wallet()
    tr = Transaction(sender_wallet, "recipient", 100)
    tr.output[sender_wallet.address] = 9002

    with pytest.raises(Exception, match="Invalid transaction output values"):
        Transaction.validate_transaction(tr)
