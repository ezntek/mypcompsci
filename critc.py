from dataclasses import dataclass
import json
import logging
import asyncio
import hashlib
import random
import time
import base64 # encoding bytes to a string for JSON

# global values to simulate all clients having a synchronized current transaction and block
curr_transaction_id = 0
curr_block_id = 0

# This is the max number of transactions in a block.
# The block cap is set low for testing only.
BLOCK_CAP = 20

# log transactios
PRINT_TRANSACTIONS = False

# log "incoming" blocks
PRINT_NEW_BLOCKS = False

# log hashes
PRINT_HASHES = False

# how many nibbles must be 0 at the beginning of the hash
NIBBLES = 5

# defines if there should be a delay for asynchronous operations
DELAY = False

@dataclass
class Transaction:
    """
    Class to represent a transaction.
    """
    id: int 
    sender: str
    receiver: str
    amount: int

    def __str__(self) -> str: # allows str(Transaction)
        return f"({self.id},{self.sender},{self.receiver},{self.amount})"

    def to_dict(self) -> dict:
        d = { "id": self.id, "sender": self.sender, "receiver": self.receiver, "amount": self.amount }
        return d

    def to_json(self) -> str:
        d = self.to_dict()
        return json.dumps(d)

    @staticmethod # class method that does not take self
    def from_dict(d: dict) -> 'Transaction': # The type checker does not have the current class in scope, so quotes have to be used
        return Transaction(d["id"], d["sender"], d["receiver"], d["amount"])

    @staticmethod # class method that does not take self
    def from_json(data: str) -> 'Transaction': # The type checker does not have the current class in scope, so quotes have to be used
        d = json.loads(data)
        return Transaction.from_dict(d)

@dataclass
class Block:
    """
    Class to model a block.
    """

    id: int
    transactions: list[Transaction]
    timestamp: float # UNIX timestamp + decimal, from time.time()
    prev_hash: bytes
    pow: bytes # proof of work

    # brute force the hash
    def mine(self):
        # the function is only used inside this function,
        # so just declare it inside
        def int_to_bytes(num: int) -> bytes:
            return num.to_bytes(32, 'big') # specify big-endian encoding

        # if the proof of work is already mined and not empty, leave.
        if self.pow != bytes():
            return

        # base as in the base of the block without the POW
        base = self.to_str() + '+' # create a "{ <block contents> }+", ready to attatch the POW to
        base = base.encode()
        pow = 0
        matching = False

        while not matching:
            pow += 1 

            pow_bytes = int_to_bytes(pow)
            potential_base = base + pow_bytes
            guess_hash = hashlib.sha256(potential_base).hexdigest()
            
            if pow % 10000 == 0 and PRINT_HASHES:
                print(f"{pow}: {guess_hash}")

            zeros = '0' * NIBBLES
            if guess_hash[:NIBBLES] == zeros: # first 3 bytes (6 nibbles, 24 bits) are 0
                break

        self.pow = int_to_bytes(pow)
    
    def hash(self) -> bytes:
        h = self.to_str(include_pow=True)
        h = bytes(h, 'utf-8') # hashlib expects a ReadableBuffer which str does not implement (but bytes does)
        h = hashlib.sha256(h).digest() # digest at the end to get a bytes
        return h

    # Functions to encode/serialize/deserialize the block
    # add include_pow as a kwarg to enable/disable adding the proof of work for mining
    def to_str(self, include_pow=False) -> str:
        """
        Encodes a block to a string to calculate the proof of work.
        We can't use __str__ because we need a keyword argument, callers can choose between adding the proof of
        work to the end, like so:

        "{index;transactions;timestamp;previous hash}"

        or

        "{index;transactions;timestamp;previous hash}+proof of work"
        """
        
        # start building transaction string
        transactions = "["

        # loop over all transactions and keep an index
        for idx, transaction in enumerate(self.transactions):

            # stringify each transaction and add a semicolon if it is not
            # the last element
            transactions += str(transaction)
            if idx != len(self.transactions)-1:
                transactions += ';'

        transactions += "]"
        
        # build the string
        res = f"{{{self.id};{transactions};{self.timestamp};{self.prev_hash.hex()}}}"
        if include_pow:
            res += f"+{self.pow.hex()}}}"
        
        return res

    def to_dict(self) -> dict:
        d = {
            "id": self.id,
            "transactions": [transaction.to_dict() for transaction in self.transactions],
            "prev_hash": base64.b64encode(self.prev_hash).decode('utf-8'), # encode it as a base64 object and immediately
                                                                          # chain the result to decode it into UTF-8
            "pow": base64.b64encode(self.prev_hash).decode('utf-8'),
            "timestamp": self.timestamp,
        }
        return d

    def to_json(self) -> str:
        d = self.to_dict()
        return json.dumps(d)

    @staticmethod # class method that does not take self
    def from_dict(data: dict) -> 'Block': # The type checker does not have the current class in scope, so quotes have to be used
        id = data["id"]
        transactions = [Transaction.from_dict(transaction) for transaction in data["transactions"]]
        prev_hash = base64.b64decode(data["prev_hash"])
        pow = base64.b64decode(data["pow"])
        timestamp = data["timestamp"]
        return Block(id, transactions, timestamp, prev_hash, pow)

    @staticmethod
    def from_json(data: str) -> 'Block':
        d = json.loads(data)
        return Block.from_dict(d)

async def next_transaction(wait=True) -> Transaction:
    """
    Function to simulate getting a new transaction over
    the network.

    In reality, the transaction would not be randomly generated,
    instead it would be from real transactions.

    Edit the transactions.json file if you want to simulate real
    transactions being put into the system.
    """

    global curr_transaction_id 

    NAMES = ["John", "James", "Peter", "Harry", "Marcus", "Adrian", "Anna", "Beatrice", "Cindy", "Diana", "Eason", "Francis", "Gregory", "Hannna", "Ken", "Elizabeth", "Monty", "Thomas", "Samuel"]
    if wait or DELAY: 
        await asyncio.sleep(random.randint(1, 3))

    sender = random.choice(NAMES)
    receiver = random.choice(NAMES)

    # Makes sure that duplicates do not happen.
    #
    # The while loop makes it so that if a duplicate happens
    # twice or thrice or n times in a row, it will not register.
    while sender == receiver:
        receiver = random.choice(NAMES)

    id = curr_transaction_id
    curr_transaction_id += 1
    res = Transaction(id, sender, receiver, random.randint(0, 200))

    if PRINT_TRANSACTIONS:
        print(f"got transaction {res.id}: \"{res.sender} gives {res.receiver} {res.amount} Siyyats.\"")

    return res

async def next_block(prev_block: Block) -> Block:
    """
    Function to simulate creating a new block.
    In a real implementation, this would be a task run
    on another node over the network,
    """
    
    global curr_block_id

    if DELAY:
        await asyncio.sleep(random.randint(1, 10))

    transactions = []
    for _ in range(BLOCK_CAP+1):
        # simulate waiting for the next block to come over from the network.
        transactions.append(await next_transaction(wait=False))
    timestamp = time.time()
    
    # grab the hash of the previous block
    prev_hash = prev_block.hash()
    pow = bytes()
    id = curr_block_id
    curr_block_id += 1
    
    b = Block(id, transactions, timestamp, prev_hash, pow)

    if PRINT_NEW_BLOCKS:
        print(f"block: {b.to_str(include_pow=True)}")
    return b

async def main():
    logging.basicConfig(
        format="[{asctime} {levelname}] {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M",
        filename="blocks.log",
        filemode='a',
        encoding="utf-8",
    )

    #                    id, transactions,                          timestamp,   prev_hash, pow
    genesis_block = Block(0, [Transaction(0, "Jason", "James", 1)], time.time(), bytes(),   bytes())
    genesis_block.mine() # generate proof of work for the first block

    # start the blockchain
    blocks = [genesis_block]

    while True:
        # save the previous block for easy access
        prev_block = blocks[len(blocks)-1]

        # simulate waiting for a block to come over from the network.
        new_block = await next_block(prev_block)
        new_block.mine()

        # Crash if the hashes do not match.
        #
        # In a real blockchain, the blockchain would simply be abandoned.
        # However, this is just a simple demonstration project, meaning
        # that keeping many of them is not needed.
        if new_block.prev_hash != prev_block.hash():
            print("hashes do not match. exiting...")

        # add it to the blockchain
        blocks.append(new_block)

        # add it to the log.
        print(f"{new_block.id}: {new_block.to_str(include_pow=True)}")

if __name__ == "__main__":
    asyncio.run(main())
