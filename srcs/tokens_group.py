from srcs.goodbye import goodbye
from srcs.token import Token


class TokensGroup:
    def __init__(self, string):
        self.string = string
        self.tokens = self.separate_tokens(string)

    def __len__(self):
        return len(self.tokens)

    def __iter__(self):
        return iter(self.tokens)

    def separate_tokens(self, string):
        string = string.clean_source
        index = 0
        tokens = []

        while index < len(string):
            token = Token.create_by_index(string, index)
            index += token.size

        return tokens
