#!/usr/bin/env python
"""Extract an SE-site spacing ciphertext from a plaintext.

The cipher is to count the number of words between SE site names,
then convert that via A1Z26. Sentence start/end letters are hints.

Within the "site_rec" directory, run:
./site_rec.py --site-names ./site_names.txt --test-file ./siterec_part1.txt
./site_rec.py --site-names ./site_names.txt --test-file ./siterec_part2.txt
"""

import argparse # Command-line argument handling

def parse_args() -> argparse.Namespace:
    """Prepare a Namespace object with parsed command line arguments."""
    parser = argparse.ArgumentParser(
        description='Extract an SE-site spacing ciphertext from a plaintext.')
    parser.add_argument('--site-names',
                        help='File with site names, one per line')
    parser.add_argument('--test-file', help='File with text to test')
    return parser.parse_args()

def sanitize_words(spaceless: str) -> list:
    """Convert a string into its bare individual words.
    
    Split on emdashes. Remove commas, colons, fancy quote marks.
    Convert to lowercase.
    """
    spaceless = spaceless.lower()
    for punctuation in [',', ':', '“', '”']:
        spaceless = spaceless.replace(punctuation, "")
    return spaceless.split('—')

def read_test_file(filepath: str) -> list:
    """Read a file into a list of sentences, each with a list of words."""
    words = [[]]
    with open(filepath) as file:
        for line in file:
            if line.strip():
                for spaceless in line.strip().split():
                    # Add new words to active sentence
                    clean = sanitize_words(spaceless)
                    words[-1] += clean

                    if clean[-1][-1] in ['.', '!', '?']:
                        # Get rid of the punctuation at the end of this sentence
                        words[-1][-1] = words[-1][-1][:-1]
                        # Start a new sentence
                        words.append([])
    # Don't return an empty last sentence
    return words[:-1]

def read_sentence_ends(words: list) -> None:
    """Print out the first and last characters of each sentence."""
    print(''.join(sentence[0][0] for sentence in words))
    print(''.join(sentence[-1][-1] for sentence in words))

def read_site_names(site_name_file: str) -> dict:
    """Read site names into a {first word : [["ext", "ext"], ["ext"]]} dict."""
    site_names = dict()
    with open(site_name_file) as file:
        for line in file:
            words = line.lower().strip().split()
            first_word = words[0]
            if not first_word in site_names:
                site_names[first_word] = []
            site_names[first_word].append(words[1:])
    return site_names

def site_name_length(site_names: dict, sentence: list, i: int) -> int:
    """Returns the length of a site that starts here, or 0 if not."""
    word = sentence[i]
    if word in site_names:
        for other_words in site_names[word]:
            works = True
            for (j, next_word) in enumerate(other_words):
                if j + i + 1 < len(sentence) and sentence[j + i + 1] == next_word:
                    continue
                else:
                    works = False
                    break
            if works:
                return len(other_words) + 1
    return 0

def replace_site_names(site_names: dict, sentence: list) -> list:
    """Replace all site names by None in the list."""
    for i in range(len(sentence)):
        len_here = site_name_length(site_names, sentence, i)
        if len_here:
            new_start = sentence[:i] + [None]
            new_end = replace_site_names(site_names, sentence[i + len_here:])
            return new_start + new_end
    return sentence

def interpret_words(words: list) -> None:
    """Translate the count of words between Nones by A1Z26."""
    if not (words[0][0] is None and words[-1][-1] is None):
        raise ValueError('Must start and end with a None')
    count = 0
    for sentence in words:
        for w in sentence:
            if w is None:
                # Don't print out at the start
                if count != 0:
                    print(chr(count + 96))
                # Reset the count
                count = 0
            else:
                count += 1

if __name__ == '__main__':
    args = parse_args()

    site_names = read_site_names(args.site_names)
    words = read_test_file(args.test_file)
    # Check the hint
    read_sentence_ends(words)

    # Check the cipher
    words = [replace_site_names(site_names, sentence) for sentence in words]
    interpret_words(words)