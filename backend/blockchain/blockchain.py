from backend.blockchain.block import Block
from backend.config import MINING_REWARD, MINING_REWARD_INPUT
from backend.wallet.transaction import Transaction


class Blockchain:
    """
    Blockchain: a public ledger of transcations.
    Implemented as a list of blocks - data sets of transactions.
    """

    def __init__(self):
        # genesis block is always the first block of blockchain
        self.chain = [Block.genesis()]

    def add_block(self, data):
        last_block = self.chain[-1]
        self.chain.append(Block.mine_block(last_block, data))

    def __repr__(self) -> str:
        return f"Blockchain: {self.chain}"

    def replace_chain(self, chain):
        """
        To replace local chain, incoming chain must follow these rules:
            - It must be longer than local chain
            - It must have correct format
        """

        if len(self.chain) >= len(chain):
            raise Exception("can't replace. chain must be longer!")

        try:
            Blockchain.is_valid_chain(chain)
        except Exception as e:
            print(f"can't replace. chain is not valid: {e}")

        # two rules has been passed
        self.chain = chain

    def to_json(self):
        """
        Make the chain serializable
        """
        serialized_chain = []
        for block in self.chain:
            serialized_chain.append(block.to_json())

        return serialized_chain

    @staticmethod
    def from_json(json_chain):
        """
        Deserialize a list of serialized blocks into a Blockchain instance.
        The result will contain a chain list of Block instances.
        """

        blockchain = Blockchain()
        blockchain.chain = list(
            map(lambda json_block: Block.from_json(json_block), json_chain)
        )
        return blockchain

    @staticmethod
    def is_valid_chain(chain):
        """
        Validate the incoming chain.
        Enforce the following rules of the blockchain:
            - the chain must start with the genesis block
            - blocks must be formatted correctly
        """

        # check is the first block is the gensis block
        if chain[0] != Block.genesis():
            raise Exception("blockchain must start with the gensis block!")

        # validate each block of chain
        for i in range(1, len(chain)):
            block = chain[i]
            last_block = chain[i - 1]

            Block.is_valid_block(last_block, block)

    @staticmethod
    def is_valid_transaction_chain(chain):
        """
        Enforce the rules of a chain composed of blocks of transactions.
        - Each transaction must only appear once in the chain.
        - There can only be one mining reward per block.
        - Each transaction must be valid.
        """

        transaction_ids = set()
        for block in chain:
            has_mining_reward = False
            for transaction_json in block.data:
                transaction = Transaction.from_json(transaction_json)

                if transaction.input == MINING_REWARD_INPUT:
                    if has_mining_reward:
                        raise Exception(
                            "Thre can only be one mining reward per block."
                            f"Check block with hash {block.hash}"
                        )

                if transaction.id in transaction_ids:
                    raise Exception(f"Transaction {transaction.id} is not uniqe")

                has_mining_reward = True
                transaction_ids.add(transaction.id)


def main():
    print(f"blockchain.py __name__: {__name__}")
    blockchain = Blockchain()
    blockchain.add_block("one")
    blockchain.add_block("two")

    print(blockchain)


if __name__ == "__main__":
    main()
