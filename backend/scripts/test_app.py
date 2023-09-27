import requests
from backend.wallet.wallet import Wallet
import time

BASE_URL = "http://127.0.0.1:5000"


def get_blockchain():
    return requests.get(f"{BASE_URL}/blockchain").json()


def get_blockchain_mine():
    return requests.get(f"{BASE_URL}/blockchain/mine").json()


def post_wallet_transact(recipient, amount):
    return requests.post(
        f"{BASE_URL}/tr", json={"recipient": recipient, "amount": amount}
    ).json()


recipient = Wallet().address
post_wallet_transact_result = post_wallet_transact(recipient, 40)

time.sleep(1)
print(f"post_wallet_transact_result: {post_wallet_transact_result}\n\n")

time.sleep(1)
blockcahin_result = get_blockchain()
print(f"blockchain_result: {blockcahin_result}\n\n")

time.sleep(1)

get_blockchain_mine_result = get_blockchain_mine()
print(f"get_blockchain_mine_result: {get_blockchain_mine_result}\n\n")
