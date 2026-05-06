#!/usr/bin/env python
"""Find words with QWERTY-Workman viability

That is, if you press the keys to type them in QWERTY,
those positions spell a valid word with Workman.

Within the main "puzzle-scripts" directory, run:
./employee_words.py --word-list ./all_words.txt > employee_words.txt
"""

import argparse # Command-line argument handling

MAPPING = {'a': 'a',
           'b': 'v',
           'c': 'm',
           'd': 'h',
           'e': 'r',
           'f': 't',
           'g': 'g',
           'h': 'y',
           'i': 'u',
           'j': 'n',
           'k': 'e',
           'l': 'o',
           'm': 'l',
           'n': 'k',
           'o': 'p',
           'p': ';',
           'q': 'q',
           'r': 'w',
           's': 's',
           't': 'b',
           'u': 'f',
           'v': 'c',
           'w': 'd',
           'x': 'x',
           'y': 'j',
           'z': 'z'}
"""QWERTY position : Workman position"""

def parse_args() -> argparse.Namespace:
    """Prepare a Namespace object with parsed command line arguments."""
    parser = argparse.ArgumentParser(
        description='Find words with QWERTY-Workman viability')
    parser.add_argument('--word-list', help='File with words, one per line')
    return parser.parse_args()

def read_wordlist(wordlist_file: str) -> set:
    """Read a wordlist into a set of strings."""
    all_words = set()
    with open(wordlist_file) as input_file:
        for line in input_file:
            all_words.add(line.strip())
    return all_words

def translate_to_workman(word: str) -> str:
    """Convert QWERTY keypresses to Workman output."""
    return ''.join([MAPPING[letter] if letter in MAPPING else '$'
                    for letter in word])
        
if __name__ == '__main__':
    args = parse_args()

    all_words = read_wordlist(args.word_list)
    employee_words = set()
    # I'm also interested in which is the longest
    max_len = 0

    for word in all_words:
        if translate_to_workman(word) in all_words:
            print(word, translate_to_workman(word))
            employee_words.add(word)
            if len(word) >= max_len:
                max_len = len(word)

    print('---')

    # All max length words
    print(max_len)
    for word in employee_words:
        if len(word) == max_len:
            print(word, translate_to_workman(word))