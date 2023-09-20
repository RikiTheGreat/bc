from backend.blockchain.block import Block

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
  
    def replace_chain(self, chain):
        """
        To replace local chain, incoming chain must follow these rules:
            - It must be longer than local chain
            - It must have correct format
        """

        if len(self.chain) >= len(chain):
            raise Exception("can't replace. chain must be longer!") from None
        
        try:
            Blockchain.is_valid_chain(chain)
        except Exception as e:
            print(f"can't replace. chain is not valid: {e}") 
        
        #two rules has been passed
        self.chain = chain


    @staticmethod
    def is_valid_chain(chain):
        """
        Validate the incoming chain.
        Enforce the following rules of the blockchain:
            - the chain must start with the genesis block
            - blocks must be formatted correctly
        """
        
        #check is the first block is the gensis block
        if chain[0] != Block.genesis():
            raise Exception('blockchain must start with the gensis block!')
        
        #validate each block of chain
        for i in range(1, len(chain)):
            block = chain[i]
            last_block = chain[i - 1]

            Block.is_valid_block(last_block, block)
def main():
    print(f'blockchain.py __name__: {__name__}')
    blockchain = Blockchain()
    blockchain.add_block('one')
    blockchain.add_block('two')

    print(blockchain)
if __name__ == '__main__':
    main()