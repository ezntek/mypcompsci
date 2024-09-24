from dataclasses import dataclass
import json
import asyncio
import hashlib
import sys
import random
import time
import base64 # encoding bytes to a string for JSON

# globalvalues to simulate all clients having a synchronized current transaction and block
curr_transaction_id = 0
curr_block_id = 0

# The block cap is set low for testing only.
BLOCK_CAP = 20

# print transactions
PRINT_TRANSACTIONS = False

# print "incoming" blocks
PRINT_NEW_BLOCKS = False

# print hashes
PRINT_HASHES = False

# how many nibbles must be 0 at the beginning of the hash
NIBBLES = 5

# defines if there should be a delay for asynchronous operations
DELAY = False

@dataclass
class Transaction:
    id: int 
    sender: str
    receiver: str
    amount: int
    # perhaps add a digital signature?

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
    id: int
    transactions: list[Transaction]
    timestamp: float # UNIX timestamp + decimal, from time.time()
    prev_hash: bytes
    pow: bytes # proof of work

    def mine(self):
        def int_to_bytes(num: int) -> bytes:
            return num.to_bytes(32, 'big')

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
        h = bytes(h, 'utf-8') # hashlib expects a ReadableBuffer which str does not implement (but bytes doens)
        h = hashlib.sha256(h).digest() # digest at the end to get a bytes
        return h

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
        
        transactions = "["
        for idx, transaction in enumerate(self.transactions):
            transactions += str(transaction)
            if idx != len(self.transactions)-1:
                transactions += ';'
        
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



@dataclass
class Node:
    id: int
    ipaddr: str
    port: int

    async def send(self, data: str):
        await asyncio.sleep(1) # represent a network task that sends the data to another node

        data = data[:10] # limit logging to 10 chars
        print(f"sent \"{data}...\" to node: {self.id} ({self.ipaddr}:{self.port})")

# utility function for inputting numbers
def input_int(*args, **kwargs) -> int:
    """
    using input without any inputs might lead to unwanted program crashes.
    with *args and **kwargs and recursion a safe function for inputting numbers
    that will not result in program crashes should be used.

    *args are all the unnamed parameters, and **kwargs are all keyword arguments.
    """

    val = input(*args, **kwargs) # expand out the args and keyword args

    try:
        return int(val)
    except ValueError:
        print("Invalid Input, try again!", file=sys.stderr)
        return input_int(*args, **kwargs)


# dummy functions to simulate things coming in from the network
async def next_transaction(wait=True) -> Transaction:
    global curr_transaction_id

    NAMES = ["John", "James", "Peter", "Harry", "Marcus", "James"]
    if wait or DELAY: 
        await asyncio.sleep(random.randint(1, 3))

    id = curr_transaction_id
    curr_transaction_id += 1
    res = Transaction(id, random.choice(NAMES), random.choice(NAMES), random.randint(0, 200))

    if PRINT_TRANSACTIONS:
        print(f"got transaction {res.id}: {res.sender} gives {res.receiver} {res.amount} Siyyats.")

    return res

async def next_block(prev_block: Block) -> Block:
    global curr_block_id

    if DELAY:
        await asyncio.sleep(random.randint(1, 10))

    transactions = []
    for _ in range(BLOCK_CAP+1):
        transactions.append(await next_transaction(wait=False))
    timestamp = time.time()
    
    # grab the hash of the previous block
    prev_hash = prev_block.hash()
    pow = bytes()
    id = curr_block_id
    curr_block_id += 1

    b = Block(id, transactions, timestamp, prev_hash, pow)

    if PRINT_NEW_BLOCKS:
        print(f"got block: {b.to_str(include_pow=True)}")
    return b

class BlockchainClient:
    username: str
    node_info: Node # some unique data about each node
    blocks: list[Block] # every client should have its own blockchain 
    current_data: list[Transaction]
    other_nodes: set[Node] # IP addresses of other nodes

    # pass in the node_id as other logic might provide it
    def __init__(self, username: str, node_id: int, other_nodes: set[Node]) -> None:
        self.username = username
        self.blocks = list() # construct an empty list class
        self.current_data = list()
        self.node_id = node_id
        self.other_nodes = other_nodes

    async def listen_transaction(self):
        while True:
            new_data = await next_transaction() # represents an asynchronous task that grabs the next transaction from peers.
            self.current_data.append(new_data)

    async def listen_new_blocks(self):
        while True:
            new_data = await next_block(self.blocks[len(self.blocks)-1])
            self.blocks.append(new_data)
    
    async def broadcast_transaction(self, transaction: Transaction):
        t = transaction.to_json()

        # spawn a task per node and send the data to each node
        async with asyncio.TaskGroup() as task_group:
            for node in self.other_nodes:
                task_group.create_task(node.send(t))

    async def run(self):
        listen_transaction_task = asyncio.create_task(self.listen_transaction())
        listen_new_blocks_task = asyncio.create_task(self.listen_new_blocks())

        while True:
            choice = input("(e)xit the program or (s)end a transaction? ").strip().lower()[0]
            
            match choice:
                case 's':
                    name = input("What is the receiver's name? ")
                    amt = input_int("What is the amount to send (Siyyats)? ")

                    global curr_transaction_id
                    id = curr_transaction_id
                    curr_transaction_id += 1
                    transaction = Transaction(id, self.username, name, amt)
                    await self.broadcast_transaction(transaction)
                case 'e':
                    break
                case _:
                    pass

        
        await asyncio.wait(listen_transaction_task)
        await asyncio.wait(listen_new_blocks_task)

        return

