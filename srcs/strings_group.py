from srcs.goodbye import goodbye


class StringsGroup:
    """
    Обертка вокруг списка строк.

    Здесь происходят: проверка порядка подачи строк, группировка строк по типам и обращение к ним по индексам.
    """
    order = ['rules', 'initial_facts', 'queries']

    def __init__(self, strings, check_order=True):
        self.strings = strings
        if check_order:
            self.check_order(self.strings)

    def __iter__(self):
        return iter(self.strings)

    def __getitem__(self, key):
        if isinstance(key, int):
            return strings[key]
        elif isinstance(key, str):
            if key not in self.order:
                raise KeyError(key)
            result = []
            for string in self.strings:
                if string.type == key:
                    result.append(string)
            return type(self)(result, check_order=False)
        else:
            raise KeyError(key)

    def __len__(self):
        return len(self.strings)

    def check_order(self, strings):
        order_index = 0
        previous_string = None

        for string in strings:
            string_type = string.type
            order_unit = self.order[order_index]
            if string_type != order_unit:
                if order_index == len(self.order) - 1:
                    goodbye(f'Line {string.index + 1} breaks the order: {string.type.replace("_", " ")} comes after {self.order[-1].replace("_", " ")}.')
                order_index += 1
                order_unit = self.order[order_index]
            if string_type != order_unit:
                if previous_string is not None:
                    goodbye(f'Line {string.index + 1} breaks the order: {string.type.replace("_", " ")} comes after {previous_string.type.replace("_", " ")}.')
                else:
                    goodbye(f'Line {string.index + 1} breaks the order: {string.type.replace("_", " ")} before other types of strings.')
            previous_string = string
