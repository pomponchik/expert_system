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
                break

        if not success:
            raise ValueError('The token is not recognized.')


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
