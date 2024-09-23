from dataclasses import dataclass
import json
import asyncio
import base64 # encoding bytes to a string for JSON

# little helper function to simplify the conversion
def int_to_bytes(num: int) -> bytes:
    return num.to_bytes(32, 'big', signed=True) # 32 bit big-endian signed integer

def bytes_to_int(data: bytes) -> int:
    return int.from_bytes(data, 32, 'big', signed=True)

@dataclass
class Transaction:
    sender: str
    reciever: str
    amount: int
    # perhaps add a digital signature?

    def to_bytes(self) -> bytes:
        return bytes(self.sender, 'utf-8') + bytes(self.receiver + 'utf-8') + int_to_bytes(32)

    def to_dict(self) -> dict:
        d = { "sender": self.sender: "receiver": self.receiver, "amount": self.amount }
        return d

    def to_json(self) -> str:
        d = self.to_dict()
        return json.dumps(d)

    @staticmethod # class method that does not take self
    def from_dict(data: dict) -> 'Transaction': # The type checker does not have the current class in scope, so quotes have to be used
        return Transaction(d["sender"], d["receiver"], d["amount"])

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

    # add include_pow as a kwarg to enable/disable adding the proof of work for mining
    def to_bytes(self, include_pow=False) -> bytes:
        # bytes are immutable and create new bytes objects on every append which hogs memory.
        # byte arrays are mutable and can simply be converted back into a bytes class, basically
        # a more memory efficient buffer of bytes.
        res = bytearray()

        id = int_to_bytes(self.id)

        transactions = bytearray() 
        for idx, transaction in enumerate(self.transactions): # loop over pairs of the index and element
            transactions += transaction.to_bytes()
            if idx != len(self.transactions)-1:
                transactions += bytes(',', 'utf-8')

    def to_dict(self) -> dict:
        d = {
            "id": self.id,
            "transactions": [transaction.to_dict() for transaction in self.transactions],
            "prev_hash": base64.b64encode(self.prev_hash).decode('utf-8'), # encode it as a base64 object and immediately
                                                                          # chain the result to decode it into UTF-8
            "pow": base64.b64encode(self.prev_hash).decode('utf-8'),
            "timestamp": self.timestamp,
        }

    def to_json(self) -> str:
        d = self.to_dict()
        return json.dumps(d)

    @staticmethod # class method that does not take self
    def from_dict(data: dict) -> 'Transaction': # The type checker does not have the current class in scope, so quotes have to be used
        id = data["id"]
        transactions = [Transaction.from_dict(transaction) for transaction in data["transactions"]]
        prev_hash = base64.b64decode(data["prev_hash"])
        pow = base64.b64decode(data["pow"])
        timestamp = data["timestamp"]
        return Transaction(id, transactions, timestamp, prev_hash, pow)

    @staticmethod
    def from_json(data: str) -> 'Transaction':
        d = json.loads(data)
        return Block.from_dict(d)

@dataclass
class NodeInfo:
    id: intm
    ipaddr: str
    port: int

class BlockchainClient:
    node_info: NodeInfo # some unique data about each node
    blocks: list[Block] # every client should have its own blockchain 
    current_data: list[Transaction]
    other_nodes: set[NodeInfo] # IP addresses of other nodes

    # pass in the node_id as other logic might provide it
    def __init__(self, node_id: int, other_nodes: set[str]) -> None:
        self.blocks = list() # construct an empty list class
        self.current_data = list()
        self.node_id = node_id
        self.other_nodes = other_nodes

    async def listen_transaction(self):
        while True:
            new_data = await next_transaction() # represents an asynchronous task that grabs the next transaction from peers.
            transaction = Transaction.from_json(new_data)
            self.current_data.append(transaction)

    async def listen_new_blocks(self):
        while True:
            new_data = await next_block()
            
