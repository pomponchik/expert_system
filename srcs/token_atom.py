class TokenAtom:
    mark = None
    types = {
        '>': lambda x: x == '>',
        '=': lambda x: x == '=',
        '<': lambda x: x == '<',
        '^': lambda x: x == '^',
        '!': lambda x: x == '!',
        '|': lambda x: x == '|',
        '+': lambda x: x == '+',
        '(': lambda x: x == '(',
        ')': lambda x: x == ')',
        '_': lambda x: x.isalpha() and x.isupper(),
    }

    def __init__(self, letter):
        for mark, checker in self.types.items():
            if checker(letter):
                self.mark = mark
                self.source = letter
                break
        if self.mark is None:
            raise ValueError('An impossible symbol was detected.')

    def __eq__(self, other):
        if type(other) is type(self):
            if self.mark == other.mark:
                return True
        return False

    @classmethod
    def get_atoms_mask_from_string(cls, string):
        result = []
        for letter in string:
            if letter == '_':
                result.append(cls('A'))
            else:
                result.append(cls(letter))
        return result
