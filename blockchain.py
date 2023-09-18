from block import Block

class Blockchain:
    """
    Blockchain: a public ledger of transcations.
    Implemented as a list of blocks - data sets of transactions.
    """

    def __init__(self):
       #genesis block is always the first block of blockchain
       self.chain = [Block.genesis()]

    
    def add_block(self, data):
       last_block = self.chain[-1]
       self.chain.append(Block.mine_block(last_block, data))


    def __repr__(self) -> str:
        return f'Blockchain: {self.chain}'
  
    
def main():
    print(f'blockchain.py __name__: {__name__}')
    blockchain = Blockchain()
    blockchain.add_block('one')
    blockchain.add_block('two')

    print(blockchain)
if __name__ == '__main__':
    main()