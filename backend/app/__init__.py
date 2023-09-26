from backend.blockchain.blockchain import Blockchain
from flask import Flask, jsonify, request
from backend.pubsub import PubSub
import os
import random
import requests
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet
from backend.wallet.transaction_pool import TransactionPool

app = Flask(__name__)

blockchain = Blockchain()
wallet = Wallet()
transaction = Transaction(wallet, "recipient", 100)
transaction_pool = TransactionPool()
pubsub = PubSub(blockchain, transaction, transaction_pool)


@app.route("/")
def route_default():
    return "Welcome to the bc (implimentation of blockchain and cryptocurrency)"


@app.route("/blockchain")
def route_blockchain():
    return jsonify(blockchain.to_json())


@app.route("/blockchain/mine")
def route_mine():
    transaction_data = "test_web"
    blockchain.add_block(transaction_data)

    block = blockchain.chain[-1]
    pubsub.broadcast_block(block)
    return jsonify(blockchain.chain[-1].to_json())


@app.route("/tr", methods=["POST"])
def route_wallet_transact():
    transaction_data = request.get_json()
    print(f"transaction_data: {transaction_data}")

    transaction = transaction_pool.transaction_already_exist(wallet.address)
    if transaction:
        transaction.update(
            wallet, transaction_data["recipient"], transaction_data["amount"]
        )

    else:
        transaction = Transaction(
            wallet, transaction_data["recipient"], transaction_data["amount"]
        )

    pubsub.broadcast_transaction(transaction)
    return jsonify(transaction.to_json())


# to run muliple instances of app we use env variables
ROOT_PORT = 5000
PORT = ROOT_PORT

if os.environ.get("PEER") == "True":
    PORT = random.randint(5001, 6000)
    result = requests.get(f"http://localhost:{ROOT_PORT}/blockchain")
    result_blockchain = Blockchain.from_json(result.json())

    try:
        blockchain.replace_chain(result_blockchain.chain)
        print("\n -- Successfully synchronized the local chain")
    except Exception as e:
        print(f"\n -- Can not synchronized the local chain. {e}")
app.run(port=PORT)
