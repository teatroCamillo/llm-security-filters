import itertools
from typing import Dict, List

class WordMutator:
    def __init__(self, custom_map: Dict[str, List[str]] = None):
        self.char_map = {
            'a': ['a', '4', '@', '*'],
            'b': ['b', '8', 'd', '6', '*'],
            'c': ['c', '(', '<', '*'],
            'd': ['d', 'b', '*'],
            'e': ['e', '3', '€', '*'],
            'f': ['f', 'ph', 'fi', '*'],
            'g': ['g', '9', '*'],
            'h': ['h', '#', '*'],
            'i': ['i', '1', '!', 'l', '*'],
            'j': ['j', '*'],
            'k': ['k', '*'],
            'l': ['l', '1', '|', 'i', '*'],
            'm': ['m', 'nn', '*'],
            'n': ['n', '*'],
            'o': ['o', '0', '()', '*'],
            'p': ['p', '*'],
            'q': ['q', '9', '*'],
            'r': ['r', '*'],
            's': ['s', '5', '$', '*'],
            't': ['t', '7', '*'],
            'u': ['u', 'v', '*'],
            'v': ['v', 'u', '*'],
            'w': ['w', 'vv', '*'],
            'x': ['x', '*'],
            'y': ['y', '*'],
            'z': ['z', '2', 's', '*'],
        }

        if custom_map:
            for k, v in custom_map.items():
                if k in self.char_map:
                    self.char_map[k].extend(v)
                else:
                    self.char_map[k] = v

        self.phrase_dict: Dict[str, List[str]] = {}

    def _get_char_options(self, char: str) -> List[str]:
        return self.char_map.get(char.lower(), [char])

    def _get_all_word_variants(self, word: str) -> List[str]:
        char_options = [self._get_char_options(c) for c in word]
        return [''.join(p) for p in itertools.product(*char_options)]

    def _generate_case_variants(self, word: str) -> List[str]:
        lower = word.lower()
        upper = word.upper()
        title = word.capitalize()
        return list(set([lower, upper, title]))

    def generate_mutations(self, phrase: str):
        words = phrase.split()
        word_mutations = [self._get_all_word_variants(w) for w in words]
        phrase_mutations = [' '.join(p) for p in itertools.product(*word_mutations)]

        all_mutations = set()
        for p in phrase_mutations:
            for variant in self._generate_case_variants(p):
                all_mutations.add(variant)

        self.phrase_dict[phrase] = sorted(all_mutations)

    def get_mutations(self, phrase: str) -> List[str]:
        return self.phrase_dict.get(phrase, [])

    def list_all(self):
        return self.phrase_dict
