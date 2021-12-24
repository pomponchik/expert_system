from srcs.token_atom import TokenAtom


class Token:
    marks = [
        TokenAtom.get_atoms_mask_from_string('<=>'),
        TokenAtom.get_atoms_mask_from_string('=>'),
        TokenAtom.get_atoms_mask_from_string('!'),
        TokenAtom.get_atoms_mask_from_string('_'),
        TokenAtom.get_atoms_mask_from_string('|'),
        TokenAtom.get_atoms_mask_from_string('+'),
        TokenAtom.get_atoms_mask_from_string('^'),
        TokenAtom.get_atoms_mask_from_string('('),
        TokenAtom.get_atoms_mask_from_string(')'),
        TokenAtom.get_atoms_mask_from_string('='),
        TokenAtom.get_atoms_mask_from_string('?'),
    ]

    def __init__(self, string, index):
        success = False

        for mark in self.marks:
            if self.check_overlay(string, index, mark):
                success = True
                self.size = len(mark)
                self.mark = mark
                self.atoms = string[index:index + self.size]
                self.type = self.get_type(self.mark)
                self.source = ''.join([x.source for x in self.atoms])
                break

        if not success:
            raise ValueError('The token is not recognized.')

    def get_type(self, mark):
        types = {
            '<=>': 'binary',
            '=>': 'binary',
            '!': 'unary',
            '_': 'named',
            '|': 'binary',
            '+': 'binary',
            '^': 'binary',
            '(': 'other',
            ')': 'other',
            '=': 'other',
            '?': 'other',
        }
        mark_string = ''.join([atom.mark for atom in mark])
        return types[mark_string]

    @staticmethod
    def check_overlay(string, index, string_to_compare):
        index_compared = 0

        while (index < len(string)) and (index < (index + len(string_to_compare))):
            try:
                if string[index] != string_to_compare[index_compared]:
                    return False
                index += 1
                index_compared += 1
            except IndexError:
                break

        if len(string_to_compare) != index_compared:
            return False

        return True
