import uuid
from backend.config import DEFAULT_BALANCE
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.utils import (
    encode_dss_signature,
    decode_dss_signature,
)

import json


class Wallet:
    """
    An individual wallet for a miner.
    Keeps track of the miner's balance.
    Allows a miner to authorize transactions.
    """

    def __init__(self, blockchain=None):
        self.blockchain = blockchain
        self.address = str(uuid.uuid4())[0:8]
        self.private_key = ec.generate_private_key(ec.SECP256K1(), default_backend)
        self.public_key = self.private_key.public_key()
        self.serilize_public_key()

    @property
    def balance(self):
        return Wallet.claulate_balance(self.blockchain, self.address)

    def sign(self, data):
        """
        Generate a signature based on the data using the local private key.
        """

        # to sign data must be encoded
        encoded_data = json.dumps(data).encode("utf-8")

        return decode_dss_signature(
            self.private_key.sign(encoded_data, ec.ECDSA(hashes.SHA256()))
        )

    def serilize_public_key(self):
        """
        Reset the public key to its serialized version.
        """
        self.public_key = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode("utf-8")

    @staticmethod
    def verify(public_key, data, signature):
        """
        Verify data based on wallet public_key and its signature.
        """

        (r, s) = signature

        deserialized_public_key = serialization.load_pem_public_key(
            public_key.encode("utf-8"), default_backend
        )

        encoded_data = json.dumps(data).encode("utf-8")

        try:
            deserialized_public_key.verify(
                encode_dss_signature(r, s), encoded_data, ec.ECDSA(hashes.SHA256())
            )
            return True
        except InvalidSignature:
            return False

    @staticmethod
    def claulate_balance(blockchain, address):
        """
        Calucalte the balance of the given address considering the transaction
        data within the blockchain.

        The balance is found by adding the output values that belong to the address since
        the most recent transaction by that address
        """
        balance = DEFAULT_BALANCE

        if not blockchain:
            return balance

        for block in blockchain.chain:
            for transaction in block.data:
                if transaction["input"]["address"] == address:
                    # Any time the address conducts a new transacion it resests
                    # its balance
                    balance = transaction["output"][address]
                elif address in transaction["output"]:
                    balance += transaction["output"][address]

        return balance


def main():
    wallet = Wallet()
    print(wallet.__dict__)


if __name__ == "__main__":
    main()
