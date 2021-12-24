from srcs.tokens_group import TokensGroup


class String:
    """
    Представление единичной строки исходного файла с правилами.
    Используется для парсинга.
    """
    def __init__(self, source, index):
        self.source = source
        self.index = index + 1
        sumbols = list(self.source)
        self.clean_source = self.get_clean_data(sumbols, lambda x: not x).replace(' ', '').replace('\t', '')
        self.comment = self.get_clean_data(sumbols, lambda x: x)
        self.is_empty = not bool(self.clean_source)
        self.type = self.get_type()
        self.tokens = TokensGroup(self)

    def __str__(self):
        return f'<source string representation, clean data = "{self.clean_source}", comment = "{self.comment}">'

    def get_clean_data(self, sumbols, flag_interpreter):
        result = []
        flag = False

        for sumbol in sumbols:
            if sumbol == '#':
                flag = True
            if flag_interpreter(flag):
                result.append(sumbol)

        result = ''.join(result)
        return result

    def get_type(self):
        if self.is_empty:
            return 'empty'
        elif self.clean_source[0] == '=':
            return 'initial_facts'
        elif self.clean_source[0] == '?':
            return 'queries'
        else:
            return 'rules'
