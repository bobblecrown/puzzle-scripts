#!/usr/bin/env python
"""Find Fibonacci values for numbers X-Y.

e.g. 5 can be made by starting with (2, 3) and taking the third value.
so 5 could be (2, 3, 3)

Also takes a file to check which is a three-column whitespace separated file
with three columns, for first num, second num, and sequence index.

Within the "fib_trees" directory, run:
./fib_nums.py --min 1 --max 90 --check-file ./check.txt 
"""

import argparse # Command-line argument handling
from dataclasses import dataclass # Basic struct

from typing import Tuple # Type hints

@dataclass
class FibNum:
    first_num: int
    """First number in the Fib. sequence."""
    second_num: int
    """Second number in the Fib. sequence."""
    index: int
    """Index in the Fib. sequence."""

def parse_args() -> argparse.Namespace:
    """Prepare a Namespace object with parsed command line arguments."""
    parser = argparse.ArgumentParser(
        description='Find Fibonacci possibilities for numbers')
    parser.add_argument('--min', '-m', type=int, help='Min number')
    parser.add_argument('--max', '-M', type=int, help='Max number')
    parser.add_argument('--check-file', '-c', type=str, help='File to check')
    return parser.parse_args()

def next_fib(previous: int, current: int, index: int) -> Tuple[int, int, int]:
    """Output the next pair of Fib. nums & index given the previous pair."""
    return current, previous + current, index + 1

def fill_in_fibs(fib_nums: dict, first_num: int, second_num: int) -> dict:
    """Add in Fib. possibilities when not yet existing."""
    # Handle the base cases
    if fib_nums[first_num] is None:
        fib_nums[first_num] = FibNum(first_num, second_num, 1)
    if fib_nums[second_num] is None:
        fib_nums[second_num] = FibNum(first_num, second_num, 2)
    
    # Try other values until we get too big
    previous, current, index = next_fib(first_num, second_num, 2)
    while current in fib_nums:
        # Only save if not saved yet
        if fib_nums[current] is None:
            fib_nums[current] = FibNum(first_num, second_num, index)
        previous, current, index = next_fib(previous, current, index)
    
    return fib_nums

def fib_not_done(fib_nums: dict) -> bool:
    """Check if there are any Nones left in fib_nums."""
    for val in fib_nums.values():
        if val is None:
            return True
    return False

def check_fib_num(first_num: int, second_num: int, index: int) -> int:
    """Calculate the number at an index in a Fibonacci sequence."""
    if index == 1:
        return first_num
    elif index == 2:
        return second_num
    previous, current, cur_index = next_fib(first_num, second_num, 2)
    while True:
        if cur_index == index:
            return current
        previous, current, cur_index = next_fib(previous, current, cur_index)
        
if __name__ == '__main__':
    args = parse_args()

    # At first none have been found
    fib_nums = dict()
    for i in range(args.min, args.max + 1):
        fib_nums[i] = None
    
    # Try all first/second num possibilities until done
    second_num = 1
    while fib_not_done(fib_nums):
        for first_num in range(1, second_num + 1):
            fill_in_fibs(fib_nums, first_num, second_num)
        second_num += 1

    # Print construction for each number
    for i in range(args.min, args.max):
        print(f'{i}:', fib_nums[i].first_num,
              fib_nums[i].second_num, fib_nums[i].index)
        
    # Check the encoded message from a file
    with open(args.check_file) as file:
        for line in file:
            if line.strip():
                # Only do this for lines with data
                first_num, second_num, index = line.split()
                cur_fib = check_fib_num(int(first_num),
                                        int(second_num),
                                        int(index))
                # Translate to ASCII if possible
                if cur_fib > 32:
                    print(f'{cur_fib} {chr(cur_fib)}')
                else:
                    print(cur_fib)
            else:
                # Maintain blank lines for readability
                print()