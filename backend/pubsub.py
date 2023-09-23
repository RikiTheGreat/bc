from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory, PNOperationType
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from backend.blockchain.block import Block

pnconfig = PNConfiguration()
pnconfig.publish_key = "pub-c-0a522040-9d41-4904-9b54-c8efc8331c4b"
pnconfig.subscribe_key = "sub-c-5e4907db-a7e8-40ca-b8c6-3b4a5cd7de5a"
pnconfig.user_id = "bc"


CHANNELS = {"TEST": "TEST", "BLOCK": "BLOCK"}


class Listener(SubscribeCallback):
    def __init__(self, blockchain):
        self.blockchain = blockchain

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            print("errror")

    def message(self, pubnub, message):
        print(f"\n-- Channel: {message.channel} | Message: {message.message}")
        # check if incoming message is from blockchain channel
        if message.channel == CHANNELS["BLOCK"]:
            block = Block.from_json(message.message)
            temp_chain = self.blockchain.chain[:]
            temp_chain.append(block)

            try:
                self.blockchain.replace_chain(temp_chain)
                print("\n-- Replacing the local chain")

            except Exception as e:
                print(f"\n-- Can not replcae the local chain {e}")


class PubSub:
    def __init__(self, blockchain):
        self.pubnub = PubNub(pnconfig)
        self.pubnub.add_listener(Listener(blockchain))
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()

    def publish(self, channel, message):
        """
        Publish the message object to the channel.
        """

        self.pubnub.publish().channel(channel).message(message).sync()

    def broadcast_block(self, block):
        """
        Broadcast a block object to all nodes.
        """
        self.publish(CHANNELS["BLOCK"], block.to_json())
