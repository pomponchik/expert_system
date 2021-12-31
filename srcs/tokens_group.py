from srcs.goodbye import goodbye
from srcs.token import Token
from srcs.token_atom import TokenAtom


class TokensGroup:
    def __init__(self, string):
        self.string = string
        try:
            self.tokens = self.separate_tokens(string)
        except Exception as e:
            goodbye(f'An impossible character or a group of characters was detected in line {string.index}.')

    def __len__(self):
        return len(self.tokens)

    def __iter__(self):
        return iter(self.tokens)

    def __str__(self):
        tokens = (''.join([atom.source for atom in token.atoms]) for token in self.tokens)
        tokens = ', '.join([f'"{token}"' for token in tokens])
        return f'<tokens group with content: {tokens}>'

    def separate_tokens(self, string):
        string = TokenAtom.get_atoms_mask_from_string(string.clean_source)
        index = 0
        tokens = []

        while index < len(string):
            token = Token(string, index)
            tokens.append(token)
            index += token.size

        return tokens
