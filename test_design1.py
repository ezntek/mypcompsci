import design1 as d
import time
import asyncio

async def main():
    genesis_block = d.Block(0, [d.Transaction(0, "John", "James", 1)], time.time(), bytes(), bytes())
    genesis_block.mine()

    blocks = [genesis_block]

    while True:
        prev_block = blocks[len(blocks)-1]
        new_block = await d.next_block(prev_block)
        new_block.mine()

        if new_block.prev_hash != prev_block.hash():
            print("hashes do not match. exiting...")
            exit(1)

        blocks.append(new_block)
        print(f"{new_block.id}: {new_block.to_str(include_pow=True)}")

asyncio.run(main())
