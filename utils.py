from itertools import combinations, product
from typing import Iterator


def hamming_circle(string_input: str, k_distance: int, alphabet: str) -> Iterator:
    """Generate strings over alphabet whose Hamming distance from string_input is
    exactly k_distance.
    """

    string_input_length = len(string_input)

    for positions in combinations(range(string_input_length), k_distance):
        for replacements in product(range(len(alphabet) - 1), repeat=k_distance):
            cousin = list(string_input)
            for p, r in zip(positions, replacements):
                if cousin[p] == alphabet[r]:
                    cousin[p] = alphabet[-1]
                else:
                    cousin[p] = alphabet[r]
            yield ''.join(cousin)

    for index in range(string_input_length):
        sliced = string_input[:index] + string_input[index + 1:]
        yield ''.join(sliced)

    for char in alphabet:
        yield string_input + char
        yield char + string_input
