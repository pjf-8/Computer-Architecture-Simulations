import sys
import math
import time

# Global variables
blocks_per_set = 0
words_per_block = 0
dm_sets = 0
num_hits = 0
num_accesses = 0
cache = []

# Classes for a blocks, sets, and the cache


class Cache:
    def __init__(self, sets):
        self.sets = sets


class Set:
    def __init__(self, blocks):
        self.blocks = blocks


class Block:
    def __init__(self, tag, valid, dirty, lru):
        self.tag = tag
        self.valid = valid
        self.dirty = dirty
        self.lru = lru

# Function to setup cache system and sotre data given by trace file


def cache_setup():
    global cache
    global dm_sets
    global words_per_block
    # Initialize the blocks
    blocks = []
    for i in range(words_per_block):
        blocks.append(Block(0, 0, 0, 0))
    # Initialize the sets
    sets = []
    for i in range(dm_sets):
        sets.append(Set(blocks))
    cache = Cache(sets)

# Function to read trace file and


def read_trace_file(trace_file):
    global num_accesses
    global num_hits
    # Open the trace file
    trace = open(trace_file, "r")
    # Read the trace file
    for line in trace:
        try:
            format(int(line, 16), '0>48b')
            num_accesses += 1
            read(line[2:])
        except:
            print("Data error, line skipped")
    # Close the trace file
    trace.close()
# Function to read a memory address


def read(address):
    global num_hits
    # Convert the memory address to a binary string
    address = bin(int(address, 16))[2:].zfill(48)
    # Get the tag, set index, and block offset
    tag = address[0:48 - int(math.log(dm_sets, 2)) -
                  int(math.log(blocks_per_set, 2))]
    set_index = address[48 - int(math.log(dm_sets, 2)) - int(
        math.log(blocks_per_set, 2)):48 - int(math.log(blocks_per_set, 2))]
    block_offset = address[48 - int(math.log(blocks_per_set, 2)):]
    # Get the set
    set = cache.sets[int(set_index, 2)]
    # Check if the block is in the cache
    for block in set.blocks:
        if block.valid and block.tag == tag:
            num_hits += 1
            block.lru = num_accesses
            return
    # Find the least recently used block
    lru = set.blocks[0]
    for block in set.blocks:
        if block.lru < lru.lru:
            lru = block
    # Replace the least recently used block
    lru.tag = tag
    lru.valid = 1
    lru.dirty = 0
    lru.lru = num_accesses
# Function to write a memory address


def write(address):
    global num_hits
    # Convert the memory address to a binary string
    address = bin(int(address, 16))[2:].zfill(48)
    # Get the tag, set index, and block offset
    tag = address[0:48 - int(math.log(dm_sets, 2)) -
                  int(math.log(blocks_per_set, 2))]
    set_index = address[48 - int(math.log(dm_sets, 2)) - int(
        math.log(blocks_per_set, 2)):48 - int(math.log(blocks_per_set, 2))]
    block_offset = address[48 - int(math.log(blocks_per_set, 2)):]
    # Get the set
    set = cache.sets[int(set_index, 2)]
    # Check if the block is in the cache
    for block in set.blocks:
        if block.valid and block.tag == tag:
            num_hits += 1
            block.lru = num_accesses
            block.dirty = 1
            return
    # Find the least recently used block
    lru = set.blocks[0]
    for block in set.blocks:
        if block.lru < lru.lru:
            lru = block
    # Replace the least recently used block
    lru.tag = tag
    lru.valid = 1
    lru.dirty = 1
    lru.lru = num_accesses


def main():
    global dm_sets
    global blocks_per_set
    global words_per_block
    global num_accesses
    global num_hits

    # Check the number of arguments
    if len(sys.argv) != 5:
        print("Usage: python3 prog3_pf.py <trace file> <block size> <number of sets> <words_per_block>")
        print("Example: python3 prog3_pf.py trace.tra 3 2 4")
        sys.exit(1)

    # Get the arguments and assign the variables
    trace_file = sys.argv[1]
    dm_sets = 2**int(sys.argv[2])
    blocks_per_set = 2**int(sys.argv[3])
    words_per_block = 2**int(sys.argv[4])

    # Initialize the cache
    cache_setup()
    # Read the trace file
    read_trace_file(trace_file)
    # Output results
    print("Hits: " + str(num_hits), "/", str(num_accesses))


# Call the main function
if __name__ == "__main__":
    main()
