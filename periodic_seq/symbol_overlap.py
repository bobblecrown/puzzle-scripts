#!/usr/bin/env python
"""Output a "symbol overlap" sequence for chemical elements.

For each element, count the number of other elements that
include its symbol within the other symbol.
(Yes, so two-letter elements must be 0).

Show both case-sensitive and case-insensitive versions.

Expects a three-column TSV with element name (ignored),
then element symbol, then element number (also ignored).
Ignores header row.

Within the "periodic_seq" directory, run:
./symbol_overlap.py --input-file elements.tsv
"""

import argparse # Command-line argument handling

def parse_args() -> argparse.Namespace:
    """Prepare a Namespace object with parsed command line arguments."""
    parser = argparse.ArgumentParser(
        description='Calculate elemental symbol overlap')
    parser.add_argument('--input-file', '-i', type=str, help='Input TSV')
    return parser.parse_args()

def read_symbols(filepath: str) -> list:
    """Read second column of TSV into a list of strings."""
    symbols = []
    with open(filepath) as file:
        file.readline() # Skip header
        for line in file:
            symbols.append(line.split()[1])
    return symbols

def find_overlap(symbols: list) -> list:
    """For each symbol in a list, find others it is within."""
    overlaps = []
    for sym in symbols:
        count = 0
        for other_sym in symbols:
            if sym != other_sym and sym in other_sym:
                count += 1
        overlaps.append(count)
    return overlaps

if __name__ == '__main__':
    args = parse_args()

    symbols = read_symbols(args.input_file)
    # Case-sensitive
    strict_overlap = find_overlap(symbols)
    # Case-insensitive
    lenient_overlap = find_overlap([sym.lower() for sym in symbols])

    for i in range(len(symbols)):
        print(symbols[i], strict_overlap[i], lenient_overlap[i])